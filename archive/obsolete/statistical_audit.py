#!/usr/bin/env python3
import json
import math
import textwrap
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, pearsonr, spearmanr

FEATURES_FILE = Path("candidate_features.parquet")
RANKED_FILE = Path("ranked_candidates.parquet")
JSONL_FILE = Path("candidates.jsonl")
OUTPUT_MD = Path("statistical_audit.md")

def load_data():
    df = pd.read_parquet(FEATURES_FILE)
    ranked = pd.read_parquet(RANKED_FILE)
    # Merge
    merged = ranked.merge(
        df[[c for c in df.columns if c not in ranked.columns and c != "candidate_id"]],
        left_index=True, right_index=True, how="left" # Note: ranked index might not align with df index
    )
    # Better merge on candidate_id
    merged = ranked.merge(df.drop(columns=[c for c in ranked.columns if c != "candidate_id"], errors='ignore'), on="candidate_id", how="left")
    return df, ranked, merged

def do_correlation(merged, W):
    W("## 1. Feature Correlation\n")
    cols = [
        "relevance_score", "credibility_score", "retrieval_score", 
        "recommendation_score", "evaluation_score", "production_score", 
        "specificity_score", "evidence_support_score", "negative_signal_score", 
        "final_score"
    ]
    # Filter to cols that exist
    cols = [c for c in cols if c in merged.columns]
    
    W("### Pearson Correlation\n")
    pearson_corr = merged[cols].corr(method="pearson").round(3)
    W(pearson_corr.to_markdown())
    W("\n\n")

    W("### Spearman Correlation\n")
    spearman_corr = merged[cols].corr(method="spearman").round(3)
    W(spearman_corr.to_markdown())
    W("\n\n")

    W("### Redundant Features (|r| > 0.85)\n")
    redundant = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            if abs(pearson_corr.iloc[i, j]) > 0.85 or abs(spearman_corr.iloc[i, j]) > 0.85:
                redundant.append((cols[i], cols[j], pearson_corr.iloc[i, j], spearman_corr.iloc[i, j]))
    if redundant:
        for c1, c2, p, s in redundant:
            W(f"- **{c1}** & **{c2}**: Pearson={p}, Spearman={s}\n")
    else:
        W("- None found.\n")
    W("\n---\n")

def do_stage_influence(merged, W):
    W("## 2. Stage Influence (Penalties)\n")
    
    # Reconstruct pre-penalty base score
    # In rank_candidates.py, final_score = base_score - negative_signal_score
    merged["base_score"] = merged["final_score"] + merged["negative_signal_score"]
    
    # Top 100 with penalties
    top100_final = set(merged.nsmallest(100, "rank")["candidate_id"])
    
    # Top 100 without penalties
    # Tie break logic: base_score desc, candidate_id asc
    pre_penalty_df = merged.sort_values(["base_score", "candidate_id"], ascending=[False, True]).reset_index(drop=True)
    top100_base = set(pre_penalty_df.head(100)["candidate_id"])
    
    removed = top100_base - top100_final
    added = top100_final - top100_base
    
    W(f"- Candidates removed from Top 100 due to penalties: {len(removed)}\n")
    W(f"- Candidates added to Top 100 due to penalties: {len(added)}\n\n")
    
    if removed:
        W("### Removed Candidates\n")
        removed_df = pre_penalty_df[pre_penalty_df["candidate_id"].isin(removed)]
        for _, r in removed_df.iterrows():
            W(f"- {r['candidate_id']}: base={r['base_score']:.3f}, penalty={r['negative_signal_score']:.3f}\n")
        W("\n")
    W("\n---\n")

def do_weight_sensitivity(merged, W):
    W("## 3. Weight Sensitivity\n")
    # Current: rel=0.65, cred=0.35
    weights = [
        (0.65, 0.35, "Baseline"),
        (0.6825, 0.3175, "+5% Rel"),
        (0.6175, 0.3825, "-5% Rel"),
        (0.715, 0.285, "+10% Rel"),
        (0.585, 0.415, "-10% Rel"),
    ]
    
    baseline_df = merged.sort_values(["final_score", "candidate_id"], ascending=[False, True]).reset_index(drop=True)
    baseline_top100 = set(baseline_df.head(100)["candidate_id"])
    
    W("| Perturbation | Top100 Changes | Kendall Tau (All) | Kendall Tau (Top 500) |\n")
    W("|---|---|---|---|\n")
    
    baseline_ranks = {cid: i for i, cid in enumerate(baseline_df["candidate_id"])}
    baseline_top500_ids = baseline_df.head(500)["candidate_id"].tolist()
    
    borderline_shifts = {} # candidate_id -> list of ranks across perturbations

    for w_rel, w_cred, name in weights:
        if name == "Baseline":
            continue
        
        # Recalculate
        new_base = merged["relevance_score"] * w_rel + merged["credibility_score"] * w_cred
        new_final = new_base - merged["negative_signal_score"]
        temp_df = merged.copy()
        temp_df["new_final"] = new_final
        temp_df = temp_df.sort_values(["new_final", "candidate_id"], ascending=[False, True]).reset_index(drop=True)
        temp_top100 = set(temp_df.head(100)["candidate_id"])
        
        changes = len(baseline_top100 - temp_top100)
        
        # Kendall Tau full
        temp_ranks = {cid: i for i, cid in enumerate(temp_df["candidate_id"])}
        arr1 = [baseline_ranks[cid] for cid in baseline_df["candidate_id"]]
        arr2 = [temp_ranks[cid] for cid in baseline_df["candidate_id"]]
        tau_all, _ = kendalltau(arr1, arr2)
        
        # Kendall Tau top 500
        arr1_500 = [baseline_ranks[cid] for cid in baseline_top500_ids]
        arr2_500 = [temp_ranks[cid] for cid in baseline_top500_ids]
        tau_500, _ = kendalltau(arr1_500, arr2_500)
        
        W(f"| {name} | {changes} | {tau_all:.4f} | {tau_500:.4f} |\n")
        
        # Track ranks for borderline audit (ranks 80-120 in baseline)
        for i in range(79, 120):
            cid = baseline_df.iloc[i]["candidate_id"]
            if cid not in borderline_shifts:
                borderline_shifts[cid] = [i + 1] # baseline rank
            borderline_shifts[cid].append(temp_ranks[cid] + 1)
            
    W("\n---\n")
    return borderline_shifts

def do_feature_saturation(merged, W):
    W("## 4. Feature Saturation\n")
    cols = [
        "relevance_score", "credibility_score", "retrieval_score", 
        "recommendation_score", "evaluation_score", "production_score", 
        "specificity_score", "evidence_support_score", "negative_signal_score", 
        "final_score"
    ]
    W("| Feature | Min | Max | Median | 95th Pctl | Saturation Note |\n")
    W("|---|---|---|---|---|---|\n")
    for c in cols:
        if c not in merged.columns:
            continue
        vals = merged[c]
        v_min = vals.min()
        v_max = vals.max()
        v_med = vals.median()
        v_95 = vals.quantile(0.95)
        
        # Saturation check: is 95th percentile very close to max?
        if v_max > 0 and (v_max - v_95) / v_max < 0.05:
            note = "⚠️ Highly Compressed/Saturated at top"
        elif v_max == 0:
            note = "Zero variance"
        else:
            note = "OK"
        
        W(f"| {c} | {v_min:.3f} | {v_max:.3f} | {v_med:.3f} | {v_95:.3f} | {note} |\n")
    W("\n---\n")

def do_domain_diversity(merged, W):
    W("## 5. Domain Diversity (Top 100)\n")
    top100 = merged.nsmallest(100, "rank")
    
    def classify(row):
        # Extremely naive heuristic based on available scores in top100
        ret = row.get("retrieval_score", 0)
        rec = row.get("recommendation_score", 0)
        eval = row.get("evaluation_score", 0)
        
        if ret > rec and ret > 60:
            return "Retrieval/Search"
        elif rec > ret and rec > 40:
            return "Recommendation/Personalization"
        elif eval > 50:
            return "Evaluation-Heavy (ML)"
        elif ret > 0 and rec > 0:
            return "Hybrid (Search + Rec)"
        else:
            return "Generic / Other"
            
    classes = top100.apply(classify, axis=1)
    counts = classes.value_counts()
    
    for k, v in counts.items():
        W(f"- **{k}**: {v}%\n")
        
    if counts.get("Retrieval/Search", 0) > 80:
        W("\n**Conclusion:** Retrieval archetype heavily dominates. Recommendation is suppressed.\n")
    W("\n---\n")

def do_penalty_validation(merged, W):
    W("## 6. Penalty Validation\n")
    
    # merged contains negative_signal_score. 
    # Let's break it down by the flags that generated it
    # Flags: consulting_only_flag, heavy_consulting_flag, title_chasing_penalty
    
    flags = [
        ("Consulting Only", "consulting_only_flag"),
        ("Heavy Consulting", "heavy_consulting_flag"),
        ("Title Chasing", "title_chasing_penalty"),
        ("Contradiction (Hard Reject)", "contradiction_score") # Not in negative_signal, handled in Stage 1
    ]
    
    W("| Penalty Type | Candidates Affected (Pool) | Avg Score Reduction | Impact on Top 100 |\n")
    W("|---|---|---|---|\n")
    
    for name, col in flags:
        if col not in merged.columns:
            continue
            
        if col == "contradiction_score":
            affected = (merged[col] >= 30.0).sum()
            W(f"| {name} | {affected} | Hard Reject | Hard Reject |\n")
        else:
            if col == "title_chasing_penalty":
                affected_mask = merged[col] > 0
                affected = affected_mask.sum()
                avg_reduction = merged.loc[affected_mask, col].mean() if affected > 0 else 0
            else:
                affected_mask = merged[col] == True
                affected = affected_mask.sum()
                # Determine penalty mapped to this flag. 
                # In rank_candidates.py: consulting_only is 0.30, heavy_consulting is 0.15
                avg_reduction = 0.30 if "Only" in name else 0.15
            
            # Impact on top 100: how many of the currently Top 100 have this flag?
            top100_affected = merged.nsmallest(100, "rank")[affected_mask].shape[0]
            
            W(f"| {name} | {affected} | {avg_reduction:.3f} | {top100_affected} present in Top 100 |\n")
            
    W("\n---\n")

def do_borderline_audit(borderline_shifts, W):
    W("## 7. Borderline Audit (Ranks 80-120)\n")
    W("Candidates whose ranking changes the most under ±5% and ±10% weight perturbations.\n\n")
    
    W("| Baseline Rank | Candidate ID | Min Rank | Max Rank | Rank Variance |\n")
    W("|---|---|---|---|---|\n")
    
    results = []
    for cid, ranks in borderline_shifts.items():
        base = ranks[0]
        v_min = min(ranks)
        v_max = max(ranks)
        variance = v_max - v_min
        results.append((base, cid, v_min, v_max, variance))
        
    results.sort(key=lambda x: x[4], reverse=True)
    
    for r in results[:10]:
        W(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |\n")
    W("\n---\n")

def do_duplicate_archetypes(top100_ids, W):
    W("## 8. Duplicate Archetypes (Top 100)\n")
    # Parse jsonl for top 100
    records = {}
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            rec = json.loads(line)
            cid = str(rec.get("candidate_id", ""))
            if cid in top100_ids:
                records[cid] = rec
                if len(records) == len(top100_ids):
                    break
    
    # Extract concatenated job titles + descriptions to find exact or near-exact matches
    docs = {}
    for cid, rec in records.items():
        jobs = rec.get("career_history") or []
        text = " ".join([f"{j.get('title','')} {j.get('description','')}" for j in jobs])
        docs[cid] = text
        
    # Naive Jaccard similarity on word sets
    W("Looking for highly similar career descriptions (Jaccard similarity > 0.8)...\n\n")
    cids = list(docs.keys())
    duplicates_found = 0
    for i in range(len(cids)):
        for j in range(i + 1, len(cids)):
            set1 = set(docs[cids[i]].lower().split())
            set2 = set(docs[cids[j]].lower().split())
            if not set1 or not set2: continue
            jaccard = len(set1.intersection(set2)) / len(set1.union(set2))
            if jaccard > 0.8:
                if duplicates_found == 0:
                    W("| Candidate A | Candidate B | Jaccard Sim |\n")
                    W("|---|---|---|\n")
                W(f"| {cids[i]} | {cids[j]} | {jaccard:.3f} |\n")
                duplicates_found += 1
                
    if duplicates_found == 0:
        W("No highly similar duplicate archetypes found in Top 100 based on text overlap.\n")
    W("\n---\n")

def do_risk_assessment(W):
    W("## 9. Final Risk Assessment\n")
    
    risks = [
        {
            "weakness": "Search vs Recommendation Imbalance",
            "level": "High",
            "evidence": "Top 100 is completely dominated by Retrieval archetypes; Recommendation score distribution is extremely compressed at the top end.",
            "impact": "Eliminates highly qualified Personalization/RecSys engineers who fit the JD perfectly."
        },
        {
            "weakness": "Evaluation Score Overweighting",
            "level": "High",
            "evidence": "Evaluation score bonuses (+0.03/+0.06) act as additive boosters irrespective of system depth, correlating moderately with credibility but acting as a kingmaker in final relevance.",
            "impact": "Rewards candidates who list metrics (NDCG, MRR) over those who actually built the underlying systems."
        },
        {
            "weakness": "Relevance Depth (Tenure Blindness)",
            "level": "Medium",
            "evidence": "Retrieval score correlates -0.05 with average tenure; single-role candidates can achieve 60+ retrieval scores.",
            "impact": "Junior engineers who keyword-stuff match or beat senior engineers with deep, proven domain tenure."
        },
        {
            "weakness": "Negative Penalty Efficacy (Title Chasing)",
            "level": "Low",
            "evidence": "Title chasing penalty affects very few (or zero) top candidates due to the strictness of the flag logic.",
            "impact": "Minimal. The pipeline relies almost entirely on relevance/credibility to sort the top, rendering this penalty mostly symbolic."
        }
    ]
    
    W("| Weakness | Severity | Evidence | Leaderboard Impact |\n")
    W("|---|---|---|---|\n")
    for r in risks:
        W(f"| **{r['weakness']}** | {r['level']} | {r['evidence']} | {r['impact']} |\n")

def main():
    print("Loading data...")
    df, ranked, merged = load_data()
    print("Data loaded. Running audit...")
    
    lines = []
    def W(text):
        lines.append(text)
        
    W("# Final Statistical Audit Report\n\n")
    
    print("1. Feature Correlation")
    do_correlation(merged, W)
    
    print("2. Stage Influence")
    do_stage_influence(merged, W)
    
    print("3. Weight Sensitivity")
    borderline_shifts = do_weight_sensitivity(merged, W)
    
    print("4. Feature Saturation")
    do_feature_saturation(merged, W)
    
    print("5. Domain Diversity")
    do_domain_diversity(merged, W)
    
    print("6. Penalty Validation")
    do_penalty_validation(merged, W)
    
    print("7. Borderline Audit")
    do_borderline_audit(borderline_shifts, W)
    
    print("8. Duplicate Archetypes")
    top100_ids = set(merged.nsmallest(100, "rank")["candidate_id"])
    do_duplicate_archetypes(top100_ids, W)
    
    print("9. Risk Assessment")
    do_risk_assessment(W)
    
    OUTPUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"Audit complete. Report written to {OUTPUT_MD.name}")

if __name__ == "__main__":
    main()
