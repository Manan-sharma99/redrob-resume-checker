#!/usr/bin/env python3
"""Extract top 10 contradiction-rejected candidates with full career detail."""
import json, math
from datetime import date, datetime
from pathlib import Path
import pandas as pd

AS_OF_DATE = date(2026, 6, 24)
MONTH_DAYS = 365.2425 / 12


def parse_date(v):
    if not v:
        return None
    try:
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def safe_float(v, d=0.0):
    try:
        r = float(v)
        return r if math.isfinite(r) else d
    except Exception:
        return d


def months_between(s, e):
    if e < s:
        return 0
    return max(0, round((e - s).days / MONTH_DAYS))


def compute_yoe(jobs):
    details = []
    for job in jobs:
        start = parse_date(job.get("start_date"))
        is_cur = bool(job.get("is_current"))
        raw_end = parse_date(job.get("end_date"))
        end = AS_OF_DATE if is_cur else raw_end
        supplied = max(0, int(safe_float(job.get("duration_months"), 0)))
        derived = months_between(start, end) if start and end else supplied
        if start and end and end >= start:
            details.append((start, end, supplied or derived))
        else:
            details.append((None, None, supplied or derived))
    valid = [(s, e) for s, e, _ in details if s and e]
    if valid:
        ordered = sorted(valid)
        merged = [[ordered[0][0], ordered[0][1]]]
        for s, e in ordered[1:]:
            if s <= merged[-1][1]:
                if e > merged[-1][1]:
                    merged[-1][1] = e
            else:
                merged.append([s, e])
        return sum(months_between(s, e) for s, e in merged) / 12.0
    return sum(d for _, _, d in details) / 12.0


def diagnose(rec):
    profile = rec.get("profile") or {}
    jobs = rec.get("career_history") or []
    edu = rec.get("education") or []
    claimed = safe_float(profile.get("years_of_experience"))
    computed = compute_yoe(jobs)
    reasons = []

    delta_months = abs(claimed - computed) * 12
    if delta_months > 12:
        delta_yrs = abs(claimed - computed)
        reasons.append(
            f"Experience mismatch: claimed {claimed:.1f} yrs vs computed {computed:.1f} yrs"
            f" (delta {delta_yrs:.1f} yrs = {delta_months:.0f} months)"
        )

    cur_count = 0
    for job in jobs:
        start = parse_date(job.get("start_date"))
        raw_end = parse_date(job.get("end_date"))
        is_cur = bool(job.get("is_current"))
        title = str(job.get("title") or "unknown role")
        cur_count += int(is_cur)

        if not start:
            reasons.append(f"Missing start date on job: [{title}]")
            continue

        if start > AS_OF_DATE:
            reasons.append(f"Future start date {start} on job: [{title}]")

        if is_cur and raw_end is not None:
            reasons.append(f"Current job [{title}] has an end date ({raw_end})")

        if not is_cur and raw_end is None:
            reasons.append(f"Past job [{title}] missing end date")

        end = AS_OF_DATE if is_cur else raw_end
        if end is not None:
            if end < start:
                reasons.append(
                    f"End before start on [{title}]: {start} -> {end}"
                )
            else:
                supplied = max(0, int(safe_float(job.get("duration_months"), 0)))
                derived = months_between(start, end)
                if supplied and abs(supplied - derived) > 4:
                    reasons.append(
                        f"Duration mismatch on [{title}]: stated {supplied}m vs computed {derived}m"
                    )

    if cur_count > 1:
        reasons.append(f"Multiple current jobs: {cur_count} roles marked is_current=True")

    for item in edu:
        inst = str(item.get("institution") or "unknown institution")
        sy = int(safe_float(item.get("start_year"), 0))
        ey = int(safe_float(item.get("end_year"), 0))
        if sy and ey and ey < sy:
            reasons.append(f"Education end year before start at [{inst}]: {sy}-{ey}")
        if sy > AS_OF_DATE.year + 1 or ey > AS_OF_DATE.year + 1:
            reasons.append(f"Future education dates at [{inst}]: {sy}-{ey}")

    return reasons, computed


# ── Load parquet and identify top-10 by combined relevance ────────────────
df = pd.read_parquet("candidate_features.parquet")
mask = df["contradiction_score"] >= 30.0
rejected = df[mask].copy()
rejected["combined"] = (
    rejected["retrieval_score"]
    + rejected["evaluation_score"]
    + rejected["recommendation_score"]
)
top10 = rejected.nlargest(10, "combined")
top10_ids = set(top10["candidate_id"].tolist())

# ── Stream JSONL ───────────────────────────────────────────────────────────
records = {}
print(f"Streaming candidates.jsonl for {len(top10_ids)} candidates ...")
with open("candidates.jsonl", encoding="utf-8") as f:
    for lineno, line in enumerate(f, 1):
        if not line.strip():
            continue
        rec = json.loads(line)
        cid = str(rec.get("candidate_id", ""))
        if cid in top10_ids:
            records[cid] = rec
            if len(records) == len(top10_ids):
                break
        if lineno % 50_000 == 0:
            print(f"  scanned {lineno:,} lines, {len(top10_ids) - len(records)} remaining")

print(f"Retrieved {len(records)} records.\n")

# ── Build output ───────────────────────────────────────────────────────────
scores_map = top10.set_index("candidate_id")[
    ["retrieval_score", "recommendation_score", "evaluation_score", "contradiction_score", "combined"]
].to_dict("index")

output = []
for rank_i, (_, row) in enumerate(top10.iterrows(), 1):
    cid = row["candidate_id"]
    rec = records.get(cid, {})
    profile = rec.get("profile") or {}
    jobs = rec.get("career_history") or []
    edu = rec.get("education") or []
    reasons, computed_yoe = diagnose(rec)
    sc = scores_map[cid]

    output.append({
        "rank": rank_i,
        "candidate_id": cid,
        "current_title": str(profile.get("current_title") or "Unknown"),
        "current_company": str(profile.get("current_company") or "Unknown"),
        "claimed_yoe": safe_float(profile.get("years_of_experience")),
        "computed_yoe": round(computed_yoe, 1),
        "jobs": jobs,
        "education": edu,
        "retrieval_score": sc["retrieval_score"],
        "recommendation_score": sc["recommendation_score"],
        "evaluation_score": sc["evaluation_score"],
        "contradiction_score": sc["contradiction_score"],
        "combined_relevance": sc["combined"],
        "rejection_reasons": reasons,
    })

# Save for the markdown writer
with open("top10_contra.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, default=str, indent=2)

print("Saved top10_contra.json")
for r in output:
    print(
        f"  {r['rank']}. {r['candidate_id']} | {r['current_title']} @ {r['current_company']}"
        f" | ret={r['retrieval_score']} eval={r['evaluation_score']} rec={r['recommendation_score']}"
        f" | contra={r['contradiction_score']}"
    )
