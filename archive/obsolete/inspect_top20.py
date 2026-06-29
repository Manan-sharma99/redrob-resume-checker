import pandas as pd
import json

ranked = pd.read_parquet("ranked_candidates.parquet")

top20_ids = set(
    ranked.sort_values("rank")
          .head(20)["candidate_id"]
)

rows = []

with open("candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        cid = candidate["candidate_id"]

        if cid in top20_ids:

            profile = candidate["profile"]

            rows.append({
                "candidate_id": cid,
                "current_title": profile.get("current_title"),
                "current_company": profile.get("current_company"),
                "headline": profile.get("headline")
            })

top20_meta = pd.DataFrame(rows)

merged = (
    ranked.merge(top20_meta, on="candidate_id")
          .sort_values("rank")
)

cols = [
    "rank",
    "candidate_id",
    "final_score",
    "relevance_score",
    "credibility_score",
    "negative_signal_score",
    "current_title",
    "current_company"
]

cols = [c for c in cols if c in merged.columns]

print(merged[cols].to_string(index=False))