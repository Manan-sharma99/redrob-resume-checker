#!/usr/bin/env python3
import os
import subprocess
import pandas as pd
from pathlib import Path

# 1. Create the variant scripts
baseline = Path("rank_candidates.py").read_text(encoding="utf-8")

v1 = baseline.replace('OUTPUT_PARQUET = Path("ranked_candidates.parquet")', 'OUTPUT_PARQUET = Path("ranked_candidates_v1.parquet")')
Path("rank_candidates_v1.py").write_text(v1, encoding="utf-8")

v2 = baseline.replace('OUTPUT_PARQUET = Path("ranked_candidates.parquet")', 'OUTPUT_PARQUET = Path("ranked_candidates_v2.parquet")')
v2 = v2.replace('raw = RETRIEVAL_W * r + EVALUATION_W * e + RECOMMENDATION_W * rec', 'raw = np.maximum(r, rec) * 0.75 + e * 0.25')
v2 = v2.replace('eval_bonus = np.where(df["evaluation_score"] >= 18, 0.03, 0.0)', 'eval_bonus = 0.0')
v2 = v2.replace('eval_bonus = np.where(df["evaluation_score"] >= 36, 0.06, eval_bonus)', '')
v2 = v2.replace('eval_bonus = np.where(df["evaluation_score"] >= 36, 0.06, eval_bonus)', '')
Path("rank_candidates_v2.py").write_text(v2, encoding="utf-8")

v3 = v2.replace('OUTPUT_PARQUET = Path("ranked_candidates_v2.parquet")', 'OUTPUT_PARQUET = Path("ranked_candidates_v3.parquet")')
v3 = v3.replace('RELEVANCE_WEIGHT = 0.65', 'RELEVANCE_WEIGHT = 0.55')
v3 = v3.replace('CREDIBILITY_WEIGHT = 0.35', 'CREDIBILITY_WEIGHT = 0.45')
Path("rank_candidates_v3.py").write_text(v3, encoding="utf-8")

# 2. Run the variants
print("Running v1...")
subprocess.run(["python", "rank_candidates_v1.py"], check=True)
print("Running v2...")
subprocess.run(["python", "rank_candidates_v2.py"], check=True)
print("Running v3...")
subprocess.run(["python", "rank_candidates_v3.py"], check=True)

# 3. Evaluate the results
df1 = pd.read_parquet("ranked_candidates_v1.parquet")
df2 = pd.read_parquet("ranked_candidates_v2.parquet")
df3 = pd.read_parquet("ranked_candidates_v3.parquet")

feats = pd.read_parquet("candidate_features.parquet")
feats = feats[['candidate_id', 'retrieval_score', 'recommendation_score', 'evaluation_score', 'production_score']]

def analyze_variant(df, name):
    t100 = df.nsmallest(100, "rank").merge(feats, on="candidate_id", how="left")
    t20 = df.nsmallest(20, "rank").merge(feats, on="candidate_id", how="left")
    
    avg_ret = t100["retrieval_score"].mean()
    avg_rec = t100["recommendation_score"].mean()
    avg_eval = t100["evaluation_score"].mean()
    avg_cred = t100["credibility_score"].mean()
    
    # Archetype detection
    def get_archetype(row):
        ret = row["retrieval_score"]
        rec = row["recommendation_score"]
        ev = row["evaluation_score"]
        
        if ret >= 50 and rec < 30: return "Search"
        if rec >= 50 and ret < 30: return "Recommendation"
        if ret >= 40 and rec >= 40: return "Hybrid/Matching"
        if ev >= 40 and ret < 40 and rec < 40: return "ML Eval"
        if ret >= rec and ret >= 30: return "Search-Leaning"
        if rec > ret and rec >= 30: return "Recommendation-Leaning"
        return "Data Science / Other"
        
    archs = t100.apply(get_archetype, axis=1).value_counts()
    
    return {
        "name": name,
        "t100_ids": set(t100["candidate_id"]),
        "avg_ret": avg_ret,
        "avg_rec": avg_rec,
        "avg_eval": avg_eval,
        "avg_cred": avg_cred,
        "archs": archs.to_dict()
    }

a1 = analyze_variant(df1, "Variant A (Baseline)")
a2 = analyze_variant(df2, "Variant B (Balanced Domains)")
a3 = analyze_variant(df3, "Variant C (Cred Emphasis)")

lines = []
def W(t): lines.append(t)

W("# Calibration Report\n")

W("## 1. Variant Comparison\n")
W("| Metric | Variant A (Baseline) | Variant B (Balanced) | Variant C (Cred Emphasis) |\n")
W("|---|---|---|---|\n")

# Averages
W(f"| Avg Retrieval | {a1['avg_ret']:.1f} | {a2['avg_ret']:.1f} | {a3['avg_ret']:.1f} |\n")
W(f"| Avg Recommendation | {a1['avg_rec']:.1f} | {a2['avg_rec']:.1f} | {a3['avg_rec']:.1f} |\n")
W(f"| Avg Evaluation | {a1['avg_eval']:.1f} | {a2['avg_eval']:.1f} | {a3['avg_eval']:.1f} |\n")
W(f"| Avg Credibility | {a1['avg_cred']:.3f} | {a2['avg_cred']:.3f} | {a3['avg_cred']:.3f} |\n")
W(f"| Top100 Overlap w/ Baseline | - | {len(a1['t100_ids'].intersection(a2['t100_ids']))}% | {len(a1['t100_ids'].intersection(a3['t100_ids']))}% |\n")

# Archetypes
arch_keys = set(list(a1["archs"].keys()) + list(a2["archs"].keys()) + list(a3["archs"].keys()))
W("\n### Archetype Distribution\n")
W("| Archetype | Variant A | Variant B | Variant C |\n")
W("|---|---|---|---|\n")
for k in sorted(arch_keys):
    W(f"| {k} | {a1['archs'].get(k, 0)} | {a2['archs'].get(k, 0)} | {a3['archs'].get(k, 0)} |\n")

W("\n## 2. Top100 Differences\n")
entered_b = a2["t100_ids"] - a1["t100_ids"]
left_b = a1["t100_ids"] - a2["t100_ids"]
W(f"- Candidates entering Top100 in Variant B: {len(entered_b)}\n")
W(f"- Candidates leaving Top100 in Variant B: {len(left_b)}\n")

W("\n## 3. Why the Chosen Variant is Better\n")
W("*(To be written in final report after viewing this output)*\n")

W("\n## 4. Exact Code Changes Made\n")
W("*(To be written in final report)*\n")

W("\n## 5. Expected Impact on Leaderboard Performance\n")
W("*(To be written in final report)*\n")

Path("CALIBRATION_OUTPUT_TEMP.md").write_text("".join(lines), encoding="utf-8")
print("Evaluation complete. Results in CALIBRATION_OUTPUT_TEMP.md")
