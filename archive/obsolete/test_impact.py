import pandas as pd
import numpy as np

def test_impact():
    df = pd.read_parquet('candidate_features.parquet')
    
    # Baseline V3 logic
    r = df["retrieval_score"] / 100.0
    e = df["evaluation_score"] / 100.0
    rec = df["recommendation_score"] / 100.0

    raw = np.maximum(r, rec) * 0.75 + e * 0.25
    relevance_base = raw.clip(0, 1)
    
    p = df["production_score"] / 100.0
    s = df["specificity_score"] / 100.0
    ev = df["evidence_support_score"] / 100.0
    cred = 0.40 * p + 0.35 * s + 0.25 * ev
    unsupported_mask = (df["evidence_support_score"] > 0) & (df["evidence_support_score"] < 50)
    unsupported_penalty = np.where(unsupported_mask, 0.05, 0.0)
    credibility_base = (cred - unsupported_penalty).clip(0, 1)
    
    base_score = relevance_base * 0.55 + (relevance_base * credibility_base) * 0.45
    
    # We ignore penalties and hard rejects for this quick simulation as they affect both equally
    
    # New Logic: Multiplicative eval bonus as per FINAL_RANKING_DESIGN.md
    # "Base_Domain = Primary + 0.2 * Secondary"
    # "Relevance = min(1.0, Base_Domain * (1 + 0.5 * eval))"
    # Wait, the final design says:
    # Base_Domain = max(r, rec) + 0.2 * min(r, rec)
    # Rel = Base_Domain * (1 + 0.5 * e)
    
    primary = np.maximum(r, rec)
    secondary = np.minimum(r, rec)
    base_domain = primary + 0.2 * secondary
    # Cap at 1.0
    base_domain = np.minimum(1.0, base_domain)
    relevance_new = np.minimum(1.0, base_domain * (1.0 + 0.5 * e))
    
    base_score_new = relevance_new * 0.55 + (relevance_new * credibility_base) * 0.45
    
    # Compare rankings
    df['score_old'] = base_score
    df['score_new'] = base_score_new
    
    # Sort
    df_old = df.sort_values('score_old', ascending=False).head(100)
    df_new = df.sort_values('score_new', ascending=False).head(100)
    
    overlap = len(set(df_old['candidate_id']).intersection(set(df_new['candidate_id'])))
    print(f"Top 100 Overlap between Baseline and Multiplicative: {overlap}/100")
    
    # How many of the new entrants have evaluation > 0?
    new_entrants = set(df_new['candidate_id']) - set(df_old['candidate_id'])
    new_entrants_df = df[df['candidate_id'].isin(new_entrants)]
    eval_gt_0 = (new_entrants_df['evaluation_score'] > 0).sum()
    print(f"Number of new entrants with evaluation_score > 0: {eval_gt_0}")

if __name__ == "__main__":
    test_impact()
