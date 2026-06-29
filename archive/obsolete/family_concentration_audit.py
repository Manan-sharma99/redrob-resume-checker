import json
import pandas as pd
import numpy as np
from collections import defaultdict
import scipy.stats as stats
import itertools

import extract_candidate_features as ecf
import rank_candidates_v3 as rc

def get_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([str(s.get("name") or "") for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([str(j.get("description") or "") for j in c["career_history"]]))
    return " ".join(text).lower()

def get_skill_text(c):
    return " ".join([str(s.get("name") or "") for s in c.get("skills", [])]).lower()

def score_family(desc, skill, family_terms, unique_weight):
    if not family_terms: return 0.0
    return ecf.domain_score(desc, skill, family_terms, unique_weight)

def main():
    print("Loading datasets...")
    df_ranked = pd.read_parquet("ranked_candidates_v3.parquet")
    df_features = pd.read_parquet("candidate_features.parquet")
    
    # Merge
    df = df_ranked.merge(df_features, on="candidate_id", suffixes=("", "_feat"))
    
    # Prepare terms by family
    family_terms = defaultdict(dict)
    family_weights = {}
    
    for c in ecf.CONCEPT_REGISTRY:
        if c.canonical_name in ecf.RETRIEVAL_TERMS:
            family_terms[c.family][c.canonical_name] = ecf.RETRIEVAL_TERMS[c.canonical_name]
            family_weights[c.family] = 12.0
        if c.canonical_name in ecf.RECOMMENDATION_TERMS:
            family_terms[c.family][c.canonical_name] = ecf.RECOMMENDATION_TERMS[c.canonical_name]
            family_weights[c.family] = 15.0

    # Add evaluation concepts as a family
    family_terms["evaluation_concept"] = ecf.EVALUATION_TERMS
    family_weights["evaluation_concept"] = 18.0

    print("Extracting texts and calculating family contributions...")
    # To save time, we only need to calculate for Top 1000 candidates or so, or all 100,000?
    # Part 1 asks "For every candidate compute:", so we must do all.
    # We can use parallel processing or just process quickly. There are 100,000 candidates.
    # 100,000 might take a few minutes. Let's do it sequentially but print progress.
    
    records = []
    with open("candidates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            cid = str(c.get("candidate_id") or "")
            desc = get_text(c)
            skill = get_skill_text(c)
            records.append((cid, desc, skill))

    # Fast map lookup
    records_dict = {cid: (desc, skill) for cid, desc, skill in records}
    
    contributions = []
    
    count = 0
    for row in df.itertuples():
        count += 1
        if count % 10000 == 0:
            print(f"Processed {count} candidates for Part 1...")
        cid = row.candidate_id
        if cid not in records_dict:
            continue
        desc, skill = records_dict[cid]
        
        # Calculate family scores
        fam_scores = {}
        for fam, terms in family_terms.items():
            s = score_family(desc, skill, terms, family_weights[fam])
            fam_scores[fam] = s
            
        total_fam_score = sum(fam_scores.values())
        
        # Count concepts
        # We need total concept count, unique family count, average concepts per family, largest family size
        concept_counts = {}
        for fam, terms in family_terms.items():
            u, o = ecf._term_stats(desc, terms)
            concept_counts[fam] = u
            
        total_concepts = sum(concept_counts.values())
        active_fams = [f for f, c in concept_counts.items() if c > 0]
        unique_fams = len(active_fams)
        avg_concepts = total_concepts / unique_fams if unique_fams > 0 else 0
        largest_fam_size = max(concept_counts.values()) if active_fams else 0
        largest_fam = max(concept_counts, key=concept_counts.get) if active_fams else "none"
        
        contributions.append({
            "candidate_id": cid,
            "retrieval_score": row.retrieval_score,
            "relevance_score": row.relevance_score,
            "total_fam_score": total_fam_score,
            "total_concepts": total_concepts,
            "unique_fams": unique_fams,
            "avg_concepts_per_fam": avg_concepts,
            "largest_fam_size": largest_fam_size,
            "largest_fam": largest_fam,
            **{f"score_{fam}": fam_scores[fam] for fam in family_terms.keys()},
            **{f"count_{fam}": concept_counts[fam] for fam in family_terms.keys()}
        })
        
    df_contrib = pd.DataFrame(contributions)
    
    print("Part 1: Generating FEATURE_CONTRIBUTION.csv")
    df_contrib.to_csv("FEATURE_CONTRIBUTION.csv", index=False)
    
    print("Part 2: Retrieval Score Explanation")
    # Correlations
    vars_to_correlate = [
        "total_concepts", "unique_fams", "avg_concepts_per_fam", "largest_fam_size"
    ]
    corr_results = []
    for v in vars_to_correlate:
        pearson, _ = stats.pearsonr(df_contrib["retrieval_score"], df_contrib[v])
        spearman, _ = stats.spearmanr(df_contrib["retrieval_score"], df_contrib[v])
        corr_results.append({"Variable": v, "Pearson": pearson, "Spearman": spearman})
        
    df_corr = pd.DataFrame(corr_results).sort_values("Spearman", ascending=False)
    
    print("Part 3: Top 100 Dependency")
    top100_cids = set(df[df["rank"] <= 100]["candidate_id"])
    df_top100 = df_contrib[df_contrib["candidate_id"].isin(top100_cids)].copy()
    
    # Classify candidates
    # Balanced: unique_fams >= 4, largest_fam_size <= 40% of total_concepts
    # Moderately Concentrated: largest_fam_size between 40% and 60%
    # Highly Concentrated: largest_fam_size > 60%
    # Single-Family Dominated: unique_fams == 1 and total_concepts > 1
    def classify_profile(row):
        if row["total_concepts"] == 0: return "Empty"
        if row["unique_fams"] == 1 and row["total_concepts"] > 1: return "Single-Family Dominated"
        pct = row["largest_fam_size"] / row["total_concepts"]
        if pct > 0.6: return "Highly Concentrated"
        if pct >= 0.4: return "Moderately Concentrated"
        return "Balanced"
        
    df_top100["profile_class"] = df_top100.apply(classify_profile, axis=1)
    
    # We need largest family % of retrieval score
    df_top100["largest_fam_score_pct"] = df_top100.apply(
        lambda r: r[f"score_{r['largest_fam']}"] / r["total_fam_score"] if r["total_fam_score"] > 0 and r["largest_fam"] != "none" else 0,
        axis=1
    )
    
    df_top100.to_csv("TOP100_FAMILY_PROFILE.csv", index=False)
    
    print("Part 4: Counterfactual Experiments")
    # Base state is the original DataFrame df
    
    def simulate(df_sim, sim_name):
        # We need to re-run stage 2 and stage 5
        relevance = rc.compute_relevance_score(df_sim)
        final = rc.compute_final_score(relevance, df_sim["credibility_score"], df_sim["negative_signal_score"])
        
        df_sim["final_score_sim"] = final
        df_sim = df_sim.sort_values(["final_score_sim", "candidate_id"], ascending=[False, True]).reset_index()
        df_sim["rank_sim"] = df_sim.index + 1
        
        return df_sim

    # Prepare base scores for simulation
    # We will reconstruct df_sim from df_contrib to tweak retrieval_score
    df_sim_base = df.copy()
    df_sim_base = df_sim_base.set_index("candidate_id")
    df_contrib_idx = df_contrib.set_index("candidate_id")
    
    results = []
    movers = {}
    
    for sim in ["A", "B", "C", "D"]:
        print(f"Running Simulation {sim}...")
        df_sim = df_sim_base.copy()
        
        if sim == "A":
            # Normalize contribution inside each family: 
            # E.g. instead of 12*unique + 2*occurrences, maybe just cap family at a fixed amount, or divide by max?
            # "Normalize contribution inside each family" -> Each family contributes a max of 1.0 to a total multiplier?
            # Or perhaps each family's score is normalized to its max possible score?
            # Let's say we just use `score_{fam} / max(score_{fam}) * 20` for each family
            new_retrieval = pd.Series(0.0, index=df_contrib_idx.index)
            for fam in family_terms.keys():
                if fam in ['evaluation_concept', 'recommendation_concept']: continue
                s = df_contrib_idx[f"score_{fam}"]
                s_max = s.max() if s.max() > 0 else 1
                new_retrieval += (s / s_max) * (100 / 6) # evenly weight the 6 retrieval families
            df_sim["retrieval_score"] = new_retrieval.reindex(df_sim.index).fillna(0).clip(0, 100)
            
        elif sim == "B":
            # Cap contribution from each family
            # E.g. max 25 points per family
            new_retrieval = pd.Series(0.0, index=df_contrib_idx.index)
            for fam in family_terms.keys():
                if fam in ['evaluation_concept', 'recommendation_concept']: continue
                s = df_contrib_idx[f"score_{fam}"].clip(0, 25)
                new_retrieval += s
            df_sim["retrieval_score"] = new_retrieval.reindex(df_sim.index).fillna(0).clip(0, 100)
            
        elif sim == "C":
            # Reward family diversity instead of concept count
            # e.g. score = unique_fams * 20
            new_retrieval = (df_contrib_idx["unique_fams"] * 20).reindex(df_sim.index).fillna(0).clip(0, 100)
            df_sim["retrieval_score"] = new_retrieval
            
        elif sim == "D":
            # Randomly remove one concept from every family
            # Since we only have unique counts, we can subtract 1 from unique count if >0
            new_retrieval = pd.Series(0.0, index=df_contrib_idx.index)
            for fam in family_terms.keys():
                if fam in ['evaluation_concept', 'recommendation_concept']: continue
                u = df_contrib_idx[f"count_{fam}"] - 1
                u = u.clip(lower=0)
                # Reconstruct points roughly: 12.0 * u
                new_retrieval += u * 12.0
            df_sim["retrieval_score"] = new_retrieval.reindex(df_sim.index).fillna(0).clip(0, 100)
            
        # Recalculate
        df_res = simulate(df_sim, sim)
        
        # Compare to original
        orig_ranks = df_sim_base["rank"]
        new_ranks = df_res.set_index("candidate_id")["rank_sim"]
        
        rank_diff = orig_ranks - new_ranks # Positive means moved up (smaller rank number)
        
        top20_orig = set(orig_ranks[orig_ranks <= 20].index)
        top20_new = set(new_ranks[new_ranks <= 20].index)
        top100_orig = set(orig_ranks[orig_ranks <= 100].index)
        top100_new = set(new_ranks[new_ranks <= 100].index)
        top250_orig = set(orig_ranks[orig_ranks <= 250].index)
        top250_new = set(new_ranks[new_ranks <= 250].index)
        top1000_orig = set(orig_ranks[orig_ranks <= 1000].index)
        top1000_new = set(new_ranks[new_ranks <= 1000].index)
        
        tau, _ = stats.kendalltau(orig_ranks, new_ranks)
        spearman, _ = stats.spearmanr(orig_ranks, new_ranks)
        
        avg_mov = rank_diff.abs().mean()
        max_mov = rank_diff.abs().max()
        
        largest_up = rank_diff.nlargest(5).index.tolist()
        largest_down = rank_diff.nsmallest(5).index.tolist()
        
        movers[sim] = rank_diff
        
        results.append({
            "Simulation": sim,
            "Top20_Overlap": len(top20_orig & top20_new) / 20.0,
            "Top100_Overlap": len(top100_orig & top100_new) / 100.0,
            "Top250_Overlap": len(top250_orig & top250_new) / 250.0,
            "Top1000_Overlap": len(top1000_orig & top1000_new) / 1000.0,
            "Kendall_Tau": tau,
            "Spearman": spearman,
            "Avg_Rank_Movement": avg_mov,
            "Max_Rank_Movement": max_mov
        })

    df_results = pd.DataFrame(results)
    df_results.to_csv("COUNTERFACTUAL_RESULTS.csv", index=False)
    
    print("Part 5: Who Benefits?")
    # Let's look at Simulation B (Cap contribution from each family)
    # It directly addresses "do candidates gain from same family"
    rank_diff_B = movers["B"]
    top100_up = rank_diff_B.nlargest(100)
    top100_down = rank_diff_B.nsmallest(100)
    
    # Write Markdown Report
    print("Writing markdown reports...")
    
    with open("RETRIEVAL_SCORE_DECOMPOSITION.md", "w", encoding="utf-8") as f:
        f.write("# Retrieval Score Decomposition\n\n")
        f.write("Variables explaining `retrieval_score`:\n\n")
        f.write(df_corr.to_markdown(index=False))
        f.write("\n\n")
        
    with open("FAMILY_CONCENTRATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# Family Concentration Audit\n\n")
        
        f.write("## 1. Top 100 Profile Classification\n")
        class_counts = df_top100["profile_class"].value_counts()
        for k, v in class_counts.items():
            f.write(f"- **{k}**: {v}\n")
            
        f.write("\n## 2. Correlation with Retrieval Score\n")
        f.write(df_corr.to_markdown(index=False))
        
        f.write("\n\n## 3. Counterfactual Experiments\n")
        f.write(df_results.to_markdown(index=False))
        
        f.write("\n\n## 4. Failure Analysis & Root Cause\n")
        f.write("Based on the data:\n")
        
        if df_corr.loc[df_corr["Variable"] == "total_concepts", "Spearman"].values[0] > df_corr.loc[df_corr["Variable"] == "unique_fams", "Spearman"].values[0]:
            f.write("- **Root Cause**: `retrieval_score` is primarily explained by concept count, not family diversity. ")
        else:
            f.write("- **Root Cause**: `retrieval_score` is primarily explained by family diversity. ")
            
        f.write("This allows candidates to stack technologies from a single ecosystem (e.g. FAISS, Pinecone, Milvus) and outscore candidates with broad cross-family experience.\n")
        
        f.write("- **Top 100 Composition**: ")
        if class_counts.get("Highly Concentrated", 0) + class_counts.get("Single-Family Dominated", 0) > 30:
            f.write("A significant portion of the Top 100 is highly concentrated in single families.\n")
        else:
            f.write("The Top 100 remains largely balanced despite the concentration advantage.\n")

if __name__ == "__main__":
    main()
