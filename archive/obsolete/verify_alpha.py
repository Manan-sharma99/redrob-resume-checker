import json
import pandas as pd
from rank_candidates_final import compute_scores, DEFAULT_CONFIG

def run():
    df = pd.read_parquet("candidate_features.parquet")
    cfg_new = DEFAULT_CONFIG.copy()
    cfg_new["ALPHA"] = 0.10
    
    base_ranked = compute_scores(df, DEFAULT_CONFIG)
    new_ranked = compute_scores(df, cfg_new)
    
    df_base = base_ranked[["candidate_id", "rank", "final_score", "credibility_score"]].rename(columns={
        "rank": "rank_base", "final_score": "score_base", "credibility_score": "cred_base"
    })
    
    df_new = new_ranked[["candidate_id", "rank", "final_score", "credibility_score"]].rename(columns={
        "rank": "rank_new", "final_score": "score_new", "credibility_score": "cred_new"
    })
    
    merged = df_base.merge(df_new, on="candidate_id")
    merged["rank_move"] = merged["rank_base"] - merged["rank_new"]
    
    # Also merge features
    feats = df[["candidate_id", "retrieval_score", "recommendation_score", "production_score", "specificity_score", "evidence_support_score"]]
    merged = merged.merge(feats, on="candidate_id")
    
    # Top 50 upward
    up = merged.sort_values("rank_move", ascending=False).head(50)
    
    # Top 50 downward
    down = merged.sort_values("rank_move", ascending=True).head(50)
    
    out = {
        "upward": up.to_dict(orient="records"),
        "downward": down.to_dict(orient="records")
    }
    
    with open("alpha_movers.json", "w") as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    run()
