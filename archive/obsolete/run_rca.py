import yaml
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from rank_candidates_final import compute_scores, DEFAULT_CONFIG

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

def decompose(row, config):
    ret = row["retrieval_score"] / 100.0
    rec = row["recommendation_score"] / 100.0
    evl = row["evaluation_score"] / 100.0
    
    primary = max(ret, rec)
    secondary = min(ret, rec)
    base_rel = primary + config["BETA"] * secondary
    rel = base_rel * (1.0 + config["GAMMA"] * evl)
    
    prod = row["production_score"] / 100.0
    spec = row["specificity_score"] / 100.0
    evid = row["evidence_support_score"] / 100.0
    
    cred_raw = prod * config["W_PROD"] + spec * config["W_SPEC"] + evid * config["W_EVID"]
    cred_mult = config["ALPHA"] + (1.0 - config["ALPHA"]) * cred_raw
    
    pen = 1.0
    if row["consulting_only_flag"]: pen = 0.0
    elif row["consulting_ratio"] > 0.6: pen *= config["PENALTY_CONSULTING_HEAVY"]
    if row["contradiction_score"] >= 30: pen = 0.0
    
    return {
        "retrieval": ret,
        "recommendation": rec,
        "evaluation": evl,
        "primary": primary,
        "secondary_bonus": config["BETA"] * secondary,
        "base_relevance": base_rel,
        "relevance_final": rel,
        "production": prod,
        "specificity": spec,
        "evidence": evid,
        "cred_raw": cred_raw,
        "cred_multiplier": cred_mult,
        "penalty": pen,
        "final_score": rel * cred_mult * pen
    }

def run():
    df = pd.read_parquet("candidate_features.parquet")
    base_cols = df.columns.tolist()
    base_ranked = compute_scores(df)
    base_t100 = set(base_ranked.head(100)["candidate_id"])
    
    with open("gold_pairs.yaml") as f:
        pairs = yaml.safe_load(f)
        
    failed_pairs = []
    
    for idx, p in enumerate(pairs):
        ra = parse_cand_str(p['cand_a'], base_cols)
        rb = parse_cand_str(p['cand_b'], base_cols)
        
        ca_dec = decompose(ra, DEFAULT_CONFIG)
        cb_dec = decompose(rb, DEFAULT_CONFIG)
        
        sa = ca_dec["final_score"]
        sb = cb_dec["final_score"]
        
        if sa > sb + 1e-5: actual = "Candidate A"
        elif sb > sa + 1e-5: actual = "Candidate B"
        else: actual = "Tie"
        
        expected = p['winner']
        if expected != actual and not (expected.startswith("Tie") and actual == "Tie"):
            failed_pairs.append({
                "test_id": idx + 1,
                "name": p['name'],
                "expected": expected,
                "actual": actual,
                "score_a": sa,
                "score_b": sb,
                "cand_a_dec": ca_dec,
                "cand_b_dec": cb_dec,
                "reasoning": p['reasoning']
            })
            
    # Counterfactuals
    counterfactuals = [
        {"name": "ALPHA_0.10", "config": {"ALPHA": 0.10}},
        {"name": "ALPHA_0.0", "config": {"ALPHA": 0.0}},
        {"name": "BETA_0.0", "config": {"BETA": 0.0}},
        {"name": "GAMMA_0.2", "config": {"GAMMA": 0.2}},
        {"name": "W_EVID_0.6", "config": {"W_EVID": 0.6, "W_PROD": 0.2, "W_SPEC": 0.2}},
        {"name": "W_PROD_0.6", "config": {"W_PROD": 0.6, "W_EVID": 0.2, "W_SPEC": 0.2}},
        {"name": "W_SPEC_0.6", "config": {"W_SPEC": 0.6, "W_EVID": 0.2, "W_PROD": 0.2}},
    ]
    
    cf_results = {}
    
    for cf in counterfactuals:
        fixed_count = 0
        fixed_tests = []
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(cf["config"])
        
        for fp in failed_pairs:
            idx = fp["test_id"] - 1
            p = pairs[idx]
            ra = parse_cand_str(p['cand_a'], base_cols)
            rb = parse_cand_str(p['cand_b'], base_cols)
            ca_dec = decompose(ra, cfg)
            cb_dec = decompose(rb, cfg)
            sa = ca_dec["final_score"]
            sb = cb_dec["final_score"]
            
            if sa > sb + 1e-5: actual = "Candidate A"
            elif sb > sa + 1e-5: actual = "Candidate B"
            else: actual = "Tie"
            
            expected = p['winner']
            if expected == actual or (expected.startswith("Tie") and actual == "Tie"):
                fixed_count += 1
                fixed_tests.append(fp["test_id"])
                
        # If it fixes anything, run full simulation
        overlap = 0
        tau = 0.0
        avg_move = 0.0
        if fixed_count > 0:
            new_r = compute_scores(df, cfg)
            new_t100 = set(new_r.head(100)["candidate_id"])
            overlap = len(base_t100.intersection(new_t100))
            
            base_ranks = base_ranked.set_index("candidate_id")["rank"]
            new_ranks = new_r.set_index("candidate_id")["rank"]
            avg_move = np.abs(base_ranks - new_ranks).mean()
            
            # Subsample for Tau to speed up
            t_samp = base_ranked.head(1000)
            t_ranks1 = t_samp["rank"]
            t_ranks2 = new_r.set_index("candidate_id").loc[t_samp["candidate_id"]]["rank"]
            tau, _ = kendalltau(t_ranks1, t_ranks2)
            
        cf_results[cf["name"]] = {
            "fixed_count": fixed_count,
            "fixed_tests": fixed_tests,
            "top100_overlap": overlap,
            "avg_move": avg_move,
            "tau_top1000": tau
        }
        
    out = {
        "failed_pairs": failed_pairs,
        "counterfactuals": cf_results
    }
    
    with open("rca_data.json", "w") as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    run()
