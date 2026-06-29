import json
import pandas as pd
import extract_candidate_features as ecf
import rank_candidates_v3 as rc
from datetime import date

def run_reproduction():
    # Load data
    print("Loading data...")
    df_ranked = pd.read_parquet("ranked_candidates_v3.parquet")
    df_feat = pd.read_parquet("candidate_features.parquet")
    
    # top N ids
    top100_ids = set(df_ranked[df_ranked["rank"] <= 100]["candidate_id"])
    top250_ids = set(df_ranked[df_ranked["rank"] <= 250]["candidate_id"])
    top1000_ids = set(df_ranked[df_ranked["rank"] <= 1000]["candidate_id"])

    bug1_affected = 0
    bug1_top100 = 0
    bug1_top250 = 0
    bug1_top1000 = 0

    bug2_affected = 0
    bug2_top100 = 0
    bug2_top250 = 0
    bug2_top1000 = 0

    print("Scanning jsonl for bugs 1 & 2...")
    as_of_date = date(2026, 6, 24)
    with open("candidates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            cid = c.get("candidate_id", "")
            
            # Bug 1: 0% evidence support
            skills = c.get("skills", [])
            jobs = c.get("career_history", [])
            skill_text = ecf._skill_text(skills)
            career_text = ecf._career_text(jobs)
            
            claims = [name for name, pattern in ecf.MAJOR_CLAIMS.items() if pattern.search(skill_text)]
            if claims:
                supported = sum(bool(ecf.MAJOR_CLAIMS[name].search(career_text)) for name in claims)
                if supported == 0:
                    bug1_affected += 1
                    if cid in top100_ids: bug1_top100 += 1
                    if cid in top250_ids: bug1_top250 += 1
                    if cid in top1000_ids: bug1_top1000 += 1

            # Bug 2: Missing start date + duration + hard reject
            has_valid = False
            has_missing_start_with_duration = False
            for job in jobs:
                sd = job.get("start_date")
                dm = job.get("duration_months")
                if sd:
                    has_valid = True
                elif dm and ecf._safe_float(dm, 0) > 0:
                    has_missing_start_with_duration = True
            
            if has_valid and has_missing_start_with_duration:
                # Look in candidate_features.parquet for contradiction score
                row = df_feat[df_feat["candidate_id"] == cid]
                if not row.empty and row["contradiction_score"].iloc[0] >= 30.0:
                    bug2_affected += 1
                    if cid in top100_ids: bug2_top100 += 1
                    if cid in top250_ids: bug2_top250 += 1
                    if cid in top1000_ids: bug2_top1000 += 1

    # Bug 3: evaluation_score > 0
    bug3_mask = df_feat["evaluation_score"] > 0
    bug3_affected = bug3_mask.sum()
    bug3_top100 = len(set(df_feat[bug3_mask]["candidate_id"]) & top100_ids)
    bug3_top250 = len(set(df_feat[bug3_mask]["candidate_id"]) & top250_ids)
    bug3_top1000 = len(set(df_feat[bug3_mask]["candidate_id"]) & top1000_ids)

    with open("bug_reproduction_results.json", "w") as f:
        json.dump({
            "bug1": {"affected": bug1_affected, "top100": bug1_top100, "top250": bug1_top250, "top1000": bug1_top1000},
            "bug2": {"affected": bug2_affected, "top100": bug2_top100, "top250": bug2_top250, "top1000": bug2_top1000},
            "bug3": {"affected": int(bug3_affected), "top100": bug3_top100, "top250": bug3_top250, "top1000": bug3_top1000}
        }, f, indent=2)
    print("Done")

if __name__ == "__main__":
    run_reproduction()
