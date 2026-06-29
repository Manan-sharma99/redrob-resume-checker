import pandas as pd
import subprocess
import json
from scipy.stats import spearmanr

def main():
    # Load before
    print("Loading before...")
    df_before = pd.read_parquet('candidate_features.parquet')
    
    # Rebuild
    print("Rebuilding features...")
    subprocess.run(['python', 'extract_candidate_features.py'], check=True)
    
    # Load after
    print("Loading after...")
    df_after = pd.read_parquet('candidate_features.parquet')
    
    # Calculate before/after stats
    cols = ['production_score', 'retrieval_score', 'recommendation_score', 'evaluation_score', 'evidence_support_score']
    
    stats = []
    for col in cols:
        before_match = (df_before[col] > 0).sum()
        after_match = (df_after[col] > 0).sum()
        stats.append({
            'Feature': col,
            'Before': before_match,
            'After': after_match,
            'Delta': after_match - before_match
        })
        
    print("\n=== MATCH STATS ===")
    for s in stats:
        print(f"{s['Feature']}: {s['Before']} -> {s['After']} (+{s['Delta']})")
        
    print("\n=== CORRELATION AUDIT ===")
    # Pearson
    corr_pearson = df_after[cols].corr(method='pearson')
    print("Pearson:\n", corr_pearson)
    
    # Spearman
    corr_spearman = df_after[cols].corr(method='spearman')
    print("\nSpearman:\n", corr_spearman)
    
    # Output to CSV
    corr_pearson.to_csv("FEATURE_OVERLAP_REPORT.csv")
    print("Wrote FEATURE_OVERLAP_REPORT.csv")

if __name__ == "__main__":
    main()
