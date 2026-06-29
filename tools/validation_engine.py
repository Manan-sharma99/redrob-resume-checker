#!/usr/bin/env python3
import pandas as pd
import numpy as np

DEFAULT_CONFIG = {
    "ALPHA": 0.30,
    "BETA": 0.20,
    "GAMMA": 0.50,
    "W_PROD": 0.35,
    "W_SPEC": 0.25,
    "W_EVID": 0.40,
    "PENALTY_CONSULTING_ONLY": 0.50,
    "PENALTY_CONSULTING_HEAVY": 0.80,
    "PENALTY_TITLE_CHASER": 0.90
}

def compute_scores(df: pd.DataFrame, config: dict = None) -> pd.DataFrame:
    """
    Computes ranking scores deterministically.
    Can accept a custom config dict for sensitivity analysis overrides.
    """
    cfg = DEFAULT_CONFIG.copy()
    if config:
        cfg.update(config)
        
    out = df.copy()
    
    # Scale 0-100 to 0-1
    ret = out["retrieval_score"] / 100.0
    rec = out["recommendation_score"] / 100.0
    evl = out["evaluation_score"] / 100.0
    
    primary = np.maximum(ret, rec)
    secondary = np.minimum(ret, rec)
    
    base_rel = primary + cfg["BETA"] * secondary
    rel = base_rel * (1.0 + cfg["GAMMA"] * evl)
    
    prod = out["production_score"] / 100.0
    spec = out["specificity_score"] / 100.0
    evid = out["evidence_support_score"] / 100.0
    
    cred_raw = prod * cfg["W_PROD"] + spec * cfg["W_SPEC"] + evid * cfg["W_EVID"]
    cred_mult = cfg["ALPHA"] + (1.0 - cfg["ALPHA"]) * cred_raw
    
    pen = pd.Series(1.0, index=out.index)
    pen = np.where(out["consulting_only_flag"], cfg["PENALTY_CONSULTING_ONLY"], pen)
    
    heavy_consulting = (~out["consulting_only_flag"]) & (out["consulting_ratio"] > 0.60)
    pen = np.where(heavy_consulting, pen * cfg["PENALTY_CONSULTING_HEAVY"], pen)
    
    title_chaser = (out["title_progression_score"] > 75) & (out["short_tenure_count"] >= 2) & (out["job_count"] >= 4)
    pen = np.where(title_chaser, pen * cfg["PENALTY_TITLE_CHASER"], pen)
    
    # Hard reject
    pen = np.where(out["contradiction_score"] >= 30, 0.0, pen)
    
    out["relevance_score"] = rel
    out["credibility_score"] = cred_mult
    out["penalty_multiplier"] = pen
    out["final_score"] = rel * cred_mult * pen
    
    # Re-rank
    out = out.sort_values(["final_score", "candidate_id"], ascending=[False, True]).reset_index(drop=True)
    out["rank"] = out.index + 1
    
    return out

if __name__ == "__main__":
    df = pd.read_parquet("../data/candidate_features.parquet")
    ranked = compute_scores(df)
    ranked.to_parquet("../outputs/ranked_candidates_final.parquet", index=False)
    print("Wrote ../outputs/ranked_candidates_final.parquet")
