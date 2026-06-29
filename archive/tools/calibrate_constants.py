#!/usr/bin/env python3
import pandas as pd
import numpy as np
from scipy.stats import kendalltau

FEATURES = "candidate_features.parquet"

def load_data():
    df = pd.read_parquet(FEATURES)
    # Scale features
    for c in ['retrieval_score', 'recommendation_score', 'evaluation_score',
              'production_score', 'specificity_score', 'evidence_support_score']:
        df[c] = df[c] / 100.0
    return df

def get_archetype(row):
    ret = row["retrieval_score"]
    rec = row["recommendation_score"]
    if ret >= 0.5 and rec < 0.3: return "Search"
    if rec >= 0.5 and ret < 0.3: return "Recommendation"
    if ret >= 0.4 and rec >= 0.4: return "Hybrid/Matching"
    if ret >= rec and ret >= 0.3: return "Search-Leaning"
    if rec > ret and rec >= 0.3: return "Recommendation-Leaning"
    return "Other"

def compute_score(df, cred_alpha, cred_w, sec_beta, eval_gamma, cap=False):
    ret = df['retrieval_score']
    rec = df['recommendation_score']
    evl = df['evaluation_score']
    
    primary = np.maximum(ret, rec)
    secondary = np.minimum(ret, rec)
    
    base_rel = primary + sec_beta * secondary
    rel = base_rel * (1.0 + eval_gamma * evl)
    
    if cap:
        rel = np.clip(rel, 0, 1.0)
        
    prod = df['production_score']
    spec = df['specificity_score']
    evid = df['evidence_support_score']
    
    cred = prod * cred_w[0] + spec * cred_w[1] + evid * cred_w[2]
    cred_multiplier = cred_alpha + (1 - cred_alpha) * cred
    
    # Negative penalties
    pen = pd.Series(1.0, index=df.index)
    pen = np.where(df["consulting_only_flag"], 0.0, pen)
    pen = np.where((~df["consulting_only_flag"]) & (df["consulting_ratio"] > 0.60), pen * 0.8, pen)
    
    tc = (df["title_progression_score"] > 75) & (df["short_tenure_count"] >= 2) & (df["job_count"] >= 4)
    pen = np.where(tc, pen * 0.9, pen)
    
    final = rel * cred_multiplier * pen
    return final

def main():
    df = load_data()
    
    print("=== 2. Credibility Weights ===")
    for c in ['production_score', 'specificity_score', 'evidence_support_score']:
        print(f"{c}: Mean={df[c].mean():.3f}, Std={df[c].std():.3f}, Max={df[c].max():.3f}")
        
    print("\n=== 5. Cap Capping ===")
    s_cap = compute_score(df, 0.0, [0.4, 0.4, 0.2], 0.2, 0.5, cap=True)
    s_uncap = compute_score(df, 0.0, [0.4, 0.4, 0.2], 0.2, 0.5, cap=False)
    capped_count = (s_uncap > 1.0).sum()
    print(f"Candidates exceeding 1.0 before cred multiplier: {capped_count}")
    
    print("\n=== 1. Credibility Alpha Sweep ===")
    for alpha in [0.0, 0.3, 0.5, 0.7]:
        scores = compute_score(df, alpha, [0.4, 0.4, 0.2], 0.2, 0.5)
        top100 = df.iloc[scores.nlargest(100).index]
        min_cred = top100['production_score'].min() # approximate
        print(f"Alpha {alpha:.1f} -> Min Credibility in Top 100 approx: {min_cred:.3f}")
        
    print("\n=== 3. Secondary Beta Sweep ===")
    for beta in [0.1, 0.15, 0.2, 0.25, 0.3]:
        scores = compute_score(df, 0.3, [0.4, 0.4, 0.2], beta, 0.5)
        top100 = df.iloc[scores.nlargest(100).index].copy()
        archs = top100.apply(get_archetype, axis=1).value_counts().to_dict()
        print(f"Beta {beta:.2f} -> Archs: {archs}")
        
    print("\n=== 4. Eval Gamma Sweep ===")
    for gamma in [0.2, 0.3, 0.5, 0.7]:
        scores = compute_score(df, 0.3, [0.4, 0.4, 0.2], 0.2, gamma)
        top100 = df.iloc[scores.nlargest(100).index]
        avg_eval = top100['evaluation_score'].mean()
        max_score = scores.max()
        print(f"Gamma {gamma:.1f} -> Avg Eval in Top100: {avg_eval:.3f}, Max Score: {max_score:.3f}")
        
    print("\n=== 6. Sensitivity Analysis (Baseline: alpha=0.3, w=[0.35,0.45,0.2], beta=0.2, gamma=0.3) ===")
    base_scores = compute_score(df, 0.3, [0.35, 0.45, 0.2], 0.2, 0.3)
    base_ranks = pd.Series(base_scores).rank(ascending=False, method='first')
    base_t100 = set(base_ranks.nsmallest(100).index)
    base_t20 = set(base_ranks.nsmallest(20).index)
    
    def test_sens(name, p_alpha, p_w, p_beta, p_gamma):
        s = compute_score(df, p_alpha, p_w, p_beta, p_gamma)
        r = pd.Series(s).rank(ascending=False, method='first')
        t100 = set(r.nsmallest(100).index)
        t20 = set(r.nsmallest(20).index)
        o100 = len(base_t100.intersection(t100))
        o20 = len(base_t20.intersection(t20))
        tau, _ = kendalltau(base_ranks, r)
        avg_mov = np.abs(base_ranks - r).mean()
        print(f"{name:20s}: T100 Overlap={o100:3d}, T20 Overlap={o20:2d}, Tau={tau:.4f}, Avg Move={avg_mov:.1f}")

    test_sens("Alpha +10%", 0.33, [0.35, 0.45, 0.2], 0.2, 0.3)
    test_sens("Alpha -10%", 0.27, [0.35, 0.45, 0.2], 0.2, 0.3)
    test_sens("Beta +10%", 0.3, [0.35, 0.45, 0.2], 0.22, 0.3)
    test_sens("Beta -10%", 0.3, [0.35, 0.45, 0.2], 0.18, 0.3)
    test_sens("Gamma +10%", 0.3, [0.35, 0.45, 0.2], 0.2, 0.33)
    test_sens("Gamma -10%", 0.3, [0.35, 0.45, 0.2], 0.2, 0.27)

if __name__ == "__main__":
    main()
