import pyarrow.parquet as pq
import pandas as pd
from scipy.stats import kendalltau

def main():
    df1 = pq.read_table("runs/v007/ranked_candidates.parquet").to_pandas()
    df2 = pq.read_table("runs/v008/ranked_candidates.parquet").to_pandas()

    # Get rankings
    # Assuming df is sorted by rank or score. Parquet is usually written sorted by final_score desc.
    df1 = df1.sort_values(by="final_score", ascending=False).reset_index(drop=True)
    df2 = df2.sort_values(by="final_score", ascending=False).reset_index(drop=True)
    
    top20_1 = set(df1.head(20)["candidate_id"])
    top20_2 = set(df2.head(20)["candidate_id"])
    top100_1 = set(df1.head(100)["candidate_id"])
    top100_2 = set(df2.head(100)["candidate_id"])
    top250_1 = set(df1.head(250)["candidate_id"])
    top250_2 = set(df2.head(250)["candidate_id"])
    top1000_1 = set(df1.head(1000)["candidate_id"])
    top1000_2 = set(df2.head(1000)["candidate_id"])
    
    print(f"Top 20 Overlap: {len(top20_1.intersection(top20_2))}/20")
    print(f"Top 100 Overlap: {len(top100_1.intersection(top100_2))}/100")
    print(f"Top 250 Overlap: {len(top250_1.intersection(top250_2))}/250")
    print(f"Top 1000 Overlap: {len(top1000_1.intersection(top1000_2))}/1000")
    
    # Kendall Tau on common candidates
    # To compute kendall tau properly on full rankings:
    merged = pd.merge(df1[["candidate_id", "final_score"]], df2[["candidate_id", "final_score"]], on="candidate_id", suffixes=("_1", "_2"))
    tau, p = kendalltau(merged["final_score_1"], merged["final_score_2"])
    print(f"Kendall Tau: {tau:.4f}")
    
    # Score distribution drift
    print(f"v007 Score Stats: Mean={df1['final_score'].mean():.4f}, Max={df1['final_score'].max():.4f}")
    print(f"v008 Score Stats: Mean={df2['final_score'].mean():.4f}, Max={df2['final_score'].max():.4f}")

    # Did the Top 100 change?
    diff_100 = top100_1.symmetric_difference(top100_2)
    if diff_100:
        print("Top 100 changed! Candidates affected:")
        print(diff_100)
    else:
        print("Top 100 remains exactly the same.")
        
    diff_count = (merged["final_score_1"] != merged["final_score_2"]).sum()
    print(f"Candidate scores changed: {diff_count}")

if __name__ == "__main__":
    main()
