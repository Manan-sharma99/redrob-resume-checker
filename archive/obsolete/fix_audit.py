import pandas as pd
import numpy as np
import scipy.stats as stats
import rank_candidates_v3 as rc

print("Loading data...")
df = pd.read_parquet("ranked_candidates_v3.parquet")
df_contrib = pd.read_csv("FEATURE_CONTRIBUTION.csv")

family_terms_keys = [c for c in df_contrib.columns if c.startswith("score_") and c not in ["score_evaluation_concept", "score_recommendation_concept"]]

def simulate(df_sim):
    relevance = rc.compute_relevance_score(df_sim)
    final = rc.compute_final_score(relevance, df_sim["credibility_score"], df_sim["negative_signal_score"])
    df_sim["final_score_sim"] = final
    df_sim = df_sim.sort_values(["final_score_sim", "candidate_id"], ascending=[False, True]).reset_index()
    df_sim["rank_sim"] = df_sim.index + 1
    return df_sim

df_sim_base = df.copy().set_index("candidate_id")
df_contrib_idx = df_contrib.set_index("candidate_id")

results = []
for sim in ["A", "B", "C", "D"]:
    df_sim = df_sim_base.copy()
    
    if sim == "A":
        new_retrieval = pd.Series(0.0, index=df_contrib_idx.index)
        for fam in family_terms_keys:
            s = df_contrib_idx[fam]
            s_max = s.max() if s.max() > 0 else 1
            new_retrieval += (s / s_max) * (100 / 6)
        df_sim["retrieval_score"] = new_retrieval.reindex(df_sim.index).fillna(0).clip(0, 100)
    elif sim == "B":
        new_retrieval = pd.Series(0.0, index=df_contrib_idx.index)
        for fam in family_terms_keys:
            s = df_contrib_idx[fam].clip(0, 25)
            new_retrieval += s
        df_sim["retrieval_score"] = new_retrieval.reindex(df_sim.index).fillna(0).clip(0, 100)
    elif sim == "C":
        new_retrieval = (df_contrib_idx["unique_fams"] * 20).reindex(df_sim.index).fillna(0).clip(0, 100)
        df_sim["retrieval_score"] = new_retrieval
    elif sim == "D":
        new_retrieval = pd.Series(0.0, index=df_contrib_idx.index)
        for fam in [f.replace("score_", "count_") for f in family_terms_keys]:
            u = df_contrib_idx[fam] - 1
            u = u.clip(lower=0)
            new_retrieval += u * 12.0
        df_sim["retrieval_score"] = new_retrieval.reindex(df_sim.index).fillna(0).clip(0, 100)
        
    df_res = simulate(df_sim)
    
    # Proper alignment
    new_ranks = df_res.set_index("candidate_id")["rank_sim"]
    orig_ranks = df_sim_base["rank"]
    
    aligned = pd.DataFrame({"orig": orig_ranks, "new": new_ranks}).dropna()
    
    tau, _ = stats.kendalltau(aligned["orig"], aligned["new"])
    spearman, _ = stats.spearmanr(aligned["orig"], aligned["new"])
    
    rank_diff = aligned["orig"] - aligned["new"]
    avg_mov = rank_diff.abs().mean()
    max_mov = rank_diff.abs().max()
    
    top20_orig = set(orig_ranks[orig_ranks <= 20].index)
    top20_new = set(new_ranks[new_ranks <= 20].index)
    top100_orig = set(orig_ranks[orig_ranks <= 100].index)
    top100_new = set(new_ranks[new_ranks <= 100].index)
    top250_orig = set(orig_ranks[orig_ranks <= 250].index)
    top250_new = set(new_ranks[new_ranks <= 250].index)
    top1000_orig = set(orig_ranks[orig_ranks <= 1000].index)
    top1000_new = set(new_ranks[new_ranks <= 1000].index)
    
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
print("Done. Updating report.")
