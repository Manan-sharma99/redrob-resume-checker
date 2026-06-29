import pandas as pd

df = pd.read_parquet("candidate_features.parquet")

print("Columns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

print("\nSample:")
print(df.head())