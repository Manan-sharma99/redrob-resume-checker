import pandas as pd
import json
import re
from collections import Counter

def main():
    df = pd.read_parquet('candidate_features.parquet')
    
    # 3. Coverage across dataset
    coverage = {}
    for col in df.columns:
        if col == 'candidate_id': continue
        non_zero = (df[col] > 0).mean() * 100
        coverage[col] = non_zero
        
    print("=== Coverage ===")
    for col, cov in coverage.items():
        print(f"{col}: {cov:.2f}%")

if __name__ == '__main__':
    main()
