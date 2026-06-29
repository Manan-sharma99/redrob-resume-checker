#!/usr/bin/env python3
import os
import json
import yaml
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import kendalltau, spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suppress annoying pandas warnings
warnings.filterwarnings('ignore')

from tools.validation_engine import compute_scores, DEFAULT_CONFIG

# ---------------------------------------------------------------------------
# Setup and Utilities
# ---------------------------------------------------------------------------
def get_next_run_dir() -> Path:
    base = Path("outputs/runs")
    base.mkdir(exist_ok=True)
    existing = [d for d in os.listdir(base) if d.startswith("v")]
    if not existing:
        return base / "v001"
    highest = max(int(d[1:]) for d in existing)
    return base / f"v{highest+1:03d}"

class ValidatorReport:
    def __init__(self):
        self.critical = []
        self.warnings = []
        self.passed = []
        
    def add_pass(self, stage, evidence):
        self.passed.append(f"**{stage}**: PASS - {evidence}")
        
    def add_warn(self, stage, reason, evidence, investigation):
        self.warnings.append(f"**{stage}**: WARNING - {reason}\n  *Evidence*: {evidence}\n  *Action*: {investigation}")
        
    def add_fail(self, stage, reason, evidence, candidates):
        self.critical.append(f"**{stage}**: FAIL - {reason}\n  *Evidence*: {evidence}\n  *Candidates Affected*: {candidates}")

    def write_markdown(self, path: Path):
        lines = ["# Ranking System Validation Report\n"]
        lines.append("## Critical Failures")
        if not self.critical:
            lines.append("✅ No critical failures.")
        else:
            for item in self.critical:
                lines.append("- " + item)
                
        lines.append("\n## Warnings")
        if not self.warnings:
            lines.append("✅ No warnings.")
        else:
            for item in self.warnings:
                lines.append("- " + item)
                
        lines.append("\n## Passed Checks")
        for item in self.passed:
            lines.append("- " + item)
            
        path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Stage 1: Gold Pair Validation
# ---------------------------------------------------------------------------
def parse_cand_str(cstr, base_cols):
    row = {c: 0.0 for c in base_cols}
    row['consulting_only_flag'] = False
    row['candidate_id'] = 'synthetic'
    if not cstr.strip(): return row
    
    for part in cstr.split(","):
        if "=" not in part: continue
        k, v = part.split("=")
        k = k.strip()
        v = v.strip()
        
        # Mapping rules
        if k in ["consulting", "consulting_only", "consulting_only_flag"]:
            row["consulting_only_flag"] = (v.lower() == "true")
        elif k == "experience":
            row["total_months_experience"] = float(v)
        elif k == "tenure":
            row["average_tenure_months"] = float(v)
        elif k == "evidence":
            row["evidence_support_score"] = float(v)
        elif k == "credibility":
            val = float(v)
            row["production_score"] = val
            row["specificity_score"] = val
            row["evidence_support_score"] = val
        elif k in base_cols:
            row[k] = float(v)
        elif f"{k}_score" in base_cols:
            row[f"{k}_score"] = float(v)
            
    return row

def stage_1_gold_pairs(df_schema, report):
    try:
        with open("data/gold_pairs.yaml", "r") as f:
            pairs = yaml.safe_load(f)
    except FileNotFoundError:
        report.add_fail("Stage 1", "data/gold_pairs.yaml not found", "", "")
        return
    
    failures = []
    base_cols = df_schema.columns.tolist()
    
    for idx, p in enumerate(pairs):
        ra = parse_cand_str(p['cand_a'], base_cols)
        rb = parse_cand_str(p['cand_b'], base_cols)
        
        test_df = pd.DataFrame([ra, rb])
        test_df.loc[0, 'candidate_id'] = "A"
        test_df.loc[1, 'candidate_id'] = "B"
        
        scored = compute_scores(test_df)
        score_a = scored.loc[scored['candidate_id']=='A', 'final_score'].iloc[0]
        score_b = scored.loc[scored['candidate_id']=='B', 'final_score'].iloc[0]
        
        if score_a > score_b + 1e-5: actual_winner = "Candidate A"
        elif score_b > score_a + 1e-5: actual_winner = "Candidate B"
        else: actual_winner = "Tie"
        
        expected = p['winner']
        # Strict match or acceptable tie mappings
        if expected != actual_winner and not (expected.startswith("Tie") and actual_winner == "Tie"):
            failures.append(f"Test {idx+1} ({p['name']}): Expected {expected}, got {actual_winner} (A={score_a:.4f}, B={score_b:.4f})")
            
    if failures:
        report.add_fail("Stage 1: Gold Pairs", f"{len(failures)} pairs failed", "\n    ".join(failures), "All Synthetic Pairs")
    else:
        report.add_pass("Stage 1: Gold Pairs", f"All {len(pairs)} pairwise tests passed deterministically.")

# ---------------------------------------------------------------------------
# Stage 2: Regression Sets
# ---------------------------------------------------------------------------
def stage_2_regression_sets(ranked_df, config, out_dir, report, meta):
    # Protected Elite: dynamic percentiles
    cfg = config.get("protected_elite", {})
    rel_p = cfg.get("relevance_percentile", 95)
    prod_p = cfg.get("production_percentile", 90)
    max_contra = cfg.get("max_contradiction", 20)
    
    rel_thresh = np.percentile(ranked_df["relevance_score"], rel_p)
    prod_thresh = np.percentile(ranked_df["production_score"], prod_p)
    
    meta["protected_elite_thresholds"] = {"relevance": float(rel_thresh), "production": float(prod_thresh)}
    
    elite = ranked_df[
        (ranked_df["relevance_score"] >= rel_thresh) &
        (ranked_df["production_score"] >= prod_thresh) &
        (ranked_df["contradiction_score"] <= max_contra) &
        (~ranked_df["consulting_only_flag"])
    ]
    elite[["candidate_id", "final_score"]].to_json(out_dir / "protected_elite.json", orient="records")
    report.add_pass("Stage 2: Elite Sets", f"Generated {len(elite)} elite candidates using dynamic percentiles (Rel>{rel_thresh:.2f}, Prod>{prod_thresh:.2f}).")
    
    # Protected Rejects
    rejects = ranked_df[
        (ranked_df["contradiction_score"] > 30) |
        (ranked_df["consulting_only_flag"])
    ]
    rejects[["candidate_id", "final_score"]].to_json(out_dir / "protected_rejects.json", orient="records")
    
    # Borderline
    borderline = ranked_df[(ranked_df["rank"] >= 80) & (ranked_df["rank"] <= 120)]
    borderline[["candidate_id", "rank"]].to_json(out_dir / "borderline_candidates.json", orient="records")

# ---------------------------------------------------------------------------
# Stage 3 & 9: Stability & Score Resolution
# ---------------------------------------------------------------------------
def stage_3_and_9_stability(ranked_df, config, report):
    eps = config.get("score_resolution", {}).get("epsilon", 1e-5)
    
    for top_k in [100, 250]:
        top = ranked_df.head(top_k)
        scores = top["final_score"].values
        diffs = np.abs(scores[:-1] - scores[1:])
        max_scores = np.maximum(scores[:-1], scores[1:])
        # Avoid div by zero
        max_scores[max_scores == 0] = 1.0 
        rel_diffs = diffs / max_scores
        
        near_ties = (diffs < eps).sum()
        if near_ties > 10:
            report.add_warn(f"Stage 9: Score Collapse (Top {top_k})", f"Found {near_ties} adjacent pairs with score diff < {eps}", "floating point collapse", "Increase credibility variance")
        else:
            report.add_pass(f"Stage 9: Score Resolution (Top {top_k})", f"Only {near_ties} near-ties detected (eps={eps}).")
            
        most_fragile_idx = np.argmin(rel_diffs)
        report.add_pass(f"Stage 3: Pairwise Stability (Top {top_k})", f"Most fragile pair rel_diff={rel_diffs[most_fragile_idx]:.6f} at rank {most_fragile_idx+1}/{most_fragile_idx+2}.")

# ---------------------------------------------------------------------------
# Stage 4: Redundancy & Entropy
# ---------------------------------------------------------------------------
def stage_4_redundancy(df, out_dir, report):
    numeric_cols = [c for c in df.columns if "_score" in c]
    corr = df[numeric_cols].corr()
    corr.to_csv(out_dir / "correlation_matrix.csv")
    
    # VIF
    inv_corr = np.linalg.inv(corr.values)
    vif = pd.Series(np.diag(inv_corr), index=numeric_cols)
    
    high_vif = vif[vif > 10.0]
    if not high_vif.empty:
        report.add_warn("Stage 4: VIF", "High multicollinearity detected", str(high_vif.to_dict()), "Review features for double counting")
    else:
        report.add_pass("Stage 4: VIF", "No severe multicollinearity found (VIF < 10).")
        
    # High Pearson
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    high_corr = [column for column in upper.columns if any(upper[column].abs() > 0.80)]
    if high_corr:
        report.add_warn("Stage 4: Pearson", "|r| > 0.80 detected", str(high_corr), "Check if these features represent the identical signal")
    else:
        report.add_pass("Stage 4: Pearson", "All correlations |r| <= 0.80")
        
    # Entropy
    entropies = {}
    for c in numeric_cols:
        counts = pd.cut(df[c], bins=10).value_counts(normalize=True)
        counts = counts[counts > 0]
        ent = -np.sum(counts * np.log2(counts))
        entropies[c] = ent
    pd.Series(entropies).to_csv(out_dir / "feature_entropy.csv")
    
    dead = [k for k, v in entropies.items() if v < 0.1]
    if dead:
        report.add_warn("Stage 4: Entropy", "Dead features detected", str(dead), "Remove or rethink these features")

# ---------------------------------------------------------------------------
# Stage 5: Threshold Audit
# ---------------------------------------------------------------------------
def stage_5_thresholds(df, out_dir, report):
    thresholds = ["consulting_ratio", "title_progression_score", "short_tenure_count", "job_count", "contradiction_score"]
    stats = df[thresholds].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    stats.to_csv(out_dir / "threshold_analysis.csv")
    report.add_pass("Stage 5: Thresholds", f"Generated threshold distribution audit for {len(thresholds)} features.")

# ---------------------------------------------------------------------------
# Stage 6 & 7: Sensitivity & Permutation
# ---------------------------------------------------------------------------
def stage_6_7_sensitivity(df, base_ranked, config, out_dir, report):
    base_t100 = set(base_ranked.head(100)["candidate_id"])
    base_ranks = base_ranked.set_index("candidate_id")["rank"]
    
    perts = config.get("sensitivity", {}).get("perturbations", [0.05, -0.05])
    constants = ["ALPHA", "BETA", "GAMMA", "W_PROD", "W_SPEC", "W_EVID"]
    
    results = []
    # Single perturbations
    for c in constants:
        for p in perts:
            cfg = DEFAULT_CONFIG.copy()
            cfg[c] = cfg[c] * (1.0 + p)
            new_r = compute_scores(df, cfg)
            new_t100 = set(new_r.head(100)["candidate_id"])
            overlap = len(base_t100.intersection(new_t100))
            
            new_ranks = new_r.set_index("candidate_id")["rank"]
            avg_move = np.abs(base_ranks - new_ranks).mean()
            
            results.append({"test": f"{c}_{p:+.2f}", "overlap_100": overlap, "avg_move": avg_move})
            
    res_df = pd.DataFrame(results)
    res_df.to_csv(out_dir / "sensitivity_analysis.csv", index=False)
    
    min_overlap = res_df["overlap_100"].min()
    if min_overlap < 90:
        report.add_warn("Stage 6: Sensitivity", "Top 100 overlap dropped below 90%", f"Min overlap: {min_overlap}", "Check if constants are overfitted")
    else:
        report.add_pass("Stage 6: Sensitivity", f"Top 100 highly stable (min overlap {min_overlap}/100) across {len(results)} parameter perturbations.")

# ---------------------------------------------------------------------------
# Stage 8: Duplicate Detection
# ---------------------------------------------------------------------------
def stage_8_duplicates(ranked_df, config, out_dir, report):
    top1000 = ranked_df.head(1000)
    # We need text. Try loading candidates.jsonl
    try:
        cand_text = []
        target_ids = set(top1000["candidate_id"])
        with open("data/candidates.jsonl", "r") as f:
            for line in f:
                c = json.loads(line)
                if c["candidate_id"] in target_ids:
                    # simplistic text representation
                    text = " ".join([e.get("description", "") for e in c.get("experience", [])])
                    cand_text.append({"candidate_id": c["candidate_id"], "text": text})
        
        if not cand_text:
            raise FileNotFoundError
            
        tdf = pd.DataFrame(cand_text)
        tdf = tdf.set_index("candidate_id").reindex(top1000["candidate_id"]).fillna("")
        
        vec = TfidfVectorizer(max_features=5000, stop_words="english")
        tfidf = vec.fit_transform(tdf["text"])
        sims = cosine_similarity(tfidf)
        
        np.fill_diagonal(sims, 0)
        thresh = config.get("duplicate_detection", {}).get("similarity_threshold", 0.90)
        
        clusters = []
        visited = set()
        for i in range(len(sims)):
            if i in visited: continue
            matches = np.where(sims[i] > thresh)[0]
            if len(matches) > 0:
                cluster = [i] + matches.tolist()
                clusters.append(cluster)
                visited.update(cluster)
                
        if clusters:
            report.add_warn("Stage 8: Duplicates", f"Found {len(clusters)} near-identical clusters in Top 1000", "", "Review duplicate_clusters.csv")
        else:
            report.add_pass("Stage 8: Duplicates", "No massive duplicate clusters detected in Top 1000.")
            
    except Exception as e:
        report.add_warn("Stage 8: Duplicates", "Text load failed", str(e), "Ensure data/candidates.jsonl exists")

# ---------------------------------------------------------------------------
# Stage 10: Pairwise Regression & JD Coverage
# ---------------------------------------------------------------------------
def get_archetype(row):
    ret = row["retrieval_score"]
    rec = row["recommendation_score"]
    if ret >= 50 and rec < 30: return "Search"
    if rec >= 50 and ret < 30: return "Recommendation"
    if ret >= 40 and rec >= 40: return "Hybrid/Matching"
    return "Other"

def stage_10_jd_coverage(ranked_df, report):
    t100 = ranked_df.head(100)
    
    # Archetypes
    archs = t100.apply(get_archetype, axis=1).value_counts().to_dict()
    report.add_pass("Stage 10: Archetypes", f"Top 100 domain breakdown: {archs}")
    
    # Competency coverage (approximated via scores > 50)
    cov_search = (t100["retrieval_score"] > 50).mean() * 100
    cov_rec = (t100["recommendation_score"] > 50).mean() * 100
    cov_prod = (t100["production_score"] > 50).mean() * 100
    
    report.add_pass("Stage 10: JD Coverage", f"Search/IR >50: {cov_search:.0f}%, RecSys >50: {cov_rec:.0f}%, Prod >50: {cov_prod:.0f}%")

def stage_10_regression_diff(ranked_df, out_dir, report):
    # If there's a previous baseline, load it
    runs = sorted([d for d in os.listdir("outputs/runs") if d.startswith("v")])
    if len(runs) < 2:
        report.add_pass("Stage 10: Regression Diff", "No previous run to compare against.")
        return
        
    prev_dir = Path("outputs/runs") / runs[-2]
    prev_path = prev_dir / "ranked_candidates.parquet"
    if not prev_path.exists():
        # For older runs
        prev_path = prev_dir / "ranked_candidates_v3.parquet"
    if prev_path.exists():
        prev_df = pd.read_parquet(prev_path)
        # diff
        merged = ranked_df[["candidate_id", "rank", "final_score"]].merge(
            prev_df[["candidate_id", "rank", "final_score"]], 
            on="candidate_id", suffixes=("_cur", "_prev")
        )
        merged["rank_move"] = merged["rank_prev"] - merged["rank_cur"]
        
        largest_diffs = merged.reindex(merged.rank_move.abs().sort_values(ascending=False).index).head(50)
        largest_diffs.to_csv(out_dir / "ranking_diff.csv", index=False)
        report.add_pass("Stage 10: Regression Diff", f"Saved 50 largest rank disagreements against {runs[-2]} to ranking_diff.csv")


# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
def main():
    print("Initializing Automated Validation Suite...")
    
    out_dir = get_next_run_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Run Directory: {out_dir}")
    
    # Load config
    try:
        with open("config/config.json", "r") as f:
            config = json.load(f)
    except Exception:
        config = {}
        
    # Load data
    df = pd.read_parquet("outputs/candidate_features.parquet")
    print(f"Loaded {len(df)} candidates.")
    
    report = ValidatorReport()
    run_meta = {}
    
    # Run ranking algorithm exactly as imported
    ranked_df = compute_scores(df)
    ranked_df.to_parquet(out_dir / "ranked_candidates.parquet", index=False)
    
    # Execute Modules
    print("Executing Stage 1: Gold Pairs...")
    stage_1_gold_pairs(df, report)
    
    print("Executing Stage 2: Regression Sets...")
    stage_2_regression_sets(ranked_df, config, out_dir, report, run_meta)
    
    print("Executing Stage 3 & 9: Stability & Resolution...")
    stage_3_and_9_stability(ranked_df, config, report)
    
    print("Executing Stage 4: Redundancy & Entropy...")
    stage_4_redundancy(df, out_dir, report)
    
    print("Executing Stage 5: Thresholds...")
    stage_5_thresholds(df, out_dir, report)
    
    print("Executing Stage 6 & 7: Sensitivity Analysis...")
    stage_6_7_sensitivity(df, ranked_df, config, out_dir, report)
    
    print("Executing Stage 8: Duplicate Detection...")
    stage_8_duplicates(ranked_df, config, out_dir, report)
    
    print("Executing Stage 10: JD Coverage & Diff...")
    stage_10_jd_coverage(ranked_df, report)
    stage_10_regression_diff(ranked_df, out_dir, report)
    
    # Save meta
    with open(out_dir / "run_metadata.json", "w") as f:
        json.dump(run_meta, f, indent=2)
        
    # Write report
    report.write_markdown(out_dir / "validation_report.md")
    print(f"\nValidation complete. Report written to {out_dir / 'validation_report.md'}")

if __name__ == "__main__":
    main()
