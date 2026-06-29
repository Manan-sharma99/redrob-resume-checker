import yaml
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from rank_candidates_final import compute_scores, DEFAULT_CONFIG
from run_rca import parse_cand_str, decompose

def run_pass_fail():
    df = pd.read_parquet("candidate_features.parquet")
    base_cols = df.columns.tolist()
    
    cfg_base = DEFAULT_CONFIG.copy()
    cfg_new = DEFAULT_CONFIG.copy()
    cfg_new["ALPHA"] = 0.10
    
    base_ranked = compute_scores(df, cfg_base)
    new_ranked = compute_scores(df, cfg_new)
    
    with open("gold_pairs.yaml") as f:
        pairs = yaml.safe_load(f)
        
    pass_to_fail = []
    fail_to_pass = []
    
    for idx, p in enumerate(pairs):
        ra = parse_cand_str(p['cand_a'], base_cols)
        rb = parse_cand_str(p['cand_b'], base_cols)
        
        ca_base = decompose(ra, cfg_base)
        cb_base = decompose(rb, cfg_base)
        
        ca_new = decompose(ra, cfg_new)
        cb_new = decompose(rb, cfg_new)
        
        sa_base = ca_base["final_score"]
        sb_base = cb_base["final_score"]
        if sa_base > sb_base + 1e-5: actual_base = "Candidate A"
        elif sb_base > sa_base + 1e-5: actual_base = "Candidate B"
        else: actual_base = "Tie"
        
        sa_new = ca_new["final_score"]
        sb_new = cb_new["final_score"]
        if sa_new > sb_new + 1e-5: actual_new = "Candidate A"
        elif sb_new > sa_new + 1e-5: actual_new = "Candidate B"
        else: actual_new = "Tie"
        
        expected = p['winner']
        
        base_correct = actual_base == expected or (expected.startswith("Tie") and actual_base == "Tie")
        new_correct = actual_new == expected or (expected.startswith("Tie") and actual_new == "Tie")
        
        if base_correct and not new_correct:
            pass_to_fail.append(idx + 1)
        elif not base_correct and new_correct:
            fail_to_pass.append(idx + 1)
            
    # Overlaps
    b20 = set(base_ranked.head(20)["candidate_id"])
    b100 = set(base_ranked.head(100)["candidate_id"])
    b250 = set(base_ranked.head(250)["candidate_id"])
    
    n20 = set(new_ranked.head(20)["candidate_id"])
    n100 = set(new_ranked.head(100)["candidate_id"])
    n250 = set(new_ranked.head(250)["candidate_id"])
    
    ov20 = len(b20.intersection(n20))
    ov100 = len(b100.intersection(n100))
    ov250 = len(b250.intersection(n250))
    
    ranks_base = base_ranked.set_index("candidate_id")["rank"]
    ranks_new = new_ranked.set_index("candidate_id")["rank"]
    
    diffs = np.abs(ranks_base - ranks_new)
    avg_move = diffs.mean()
    max_move = diffs.max()
    
    tau, _ = kendalltau(base_ranked["rank"].values, new_ranked.set_index("candidate_id").loc[base_ranked["candidate_id"]]["rank"].values)
    
    out = {
        "pass_to_fail": pass_to_fail,
        "fail_to_pass": fail_to_pass,
        "overlap_20": ov20,
        "overlap_100": ov100,
        "overlap_250": ov250,
        "avg_move": float(avg_move),
        "max_move": int(max_move),
        "tau": float(tau)
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    run_pass_fail()
