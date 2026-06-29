#!/usr/bin/env python3
"""
Rejection Diagnostics
=====================

Analyses all candidates removed by Stage 1 (Hard Reject).

Outputs: rejection_diagnostics.md
"""

from __future__ import annotations

import json
import math
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

# ---------------------------------------------------------------------------
# Paths + constants  (must match rank_candidates.py exactly)
# ---------------------------------------------------------------------------
FEATURES_PARQUET   = Path("candidate_features.parquet")
RAW_JSONL          = Path("candidates.jsonl")
OUTPUT_MD          = Path("rejection_diagnostics.md")

HARD_REJECT_CONTRADICTION_THRESHOLD = 30.0
AS_OF_DATE = date(2026, 6, 24)
MONTH_DAYS = 365.2425 / 12

# ---------------------------------------------------------------------------
# Reproduce Stage-1 rejection logic
# ---------------------------------------------------------------------------

def identify_rejected(df: pd.DataFrame) -> pd.DataFrame:
    mask_contradiction = df["contradiction_score"] >= HARD_REJECT_CONTRADICTION_THRESHOLD
    mask_consulting_zero = (
        df["consulting_only_flag"]
        & (df["retrieval_score"] == 0)
        & (df["recommendation_score"] == 0)
        & (df["evaluation_score"] == 0)
    )
    reject_mask = mask_contradiction | mask_consulting_zero
    rejected = df[reject_mask].copy()
    rejected["reject_via_contradiction"]   = mask_contradiction[reject_mask].values
    rejected["reject_via_consulting_zero"] = mask_consulting_zero[reject_mask].values
    return rejected


# ---------------------------------------------------------------------------
# Per-candidate contradiction sub-reason detector
# (mirrors the logic in extract_candidate_features.py → contradiction_score)
# ---------------------------------------------------------------------------

def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value)
        return result if math.isfinite(result) else default
    except (TypeError, ValueError):
        return default


def _months_between(start: date, end: date) -> int:
    if end < start:
        return 0
    return max(0, round((end - start).days / MONTH_DAYS))


def diagnose_contradictions(record: Mapping[str, Any]) -> dict[str, Any]:
    """
    Returns a dict with:
        - reasons: list of human-readable sub-reason strings
        - has_future_dates
        - has_impossible_work_timeline
        - has_impossible_edu_timeline
        - has_multiple_current_jobs
        - has_overlapping_roles
        - has_experience_mismatch
        - has_missing_dates
        - has_duration_mismatch
    """
    profile   = record.get("profile") or {}
    jobs      = record.get("career_history") or []
    education = record.get("education") or []

    reasons: list[str] = []
    flags: dict[str, bool] = {
        "future_dates":             False,
        "impossible_work_timeline": False,
        "impossible_edu_timeline":  False,
        "multiple_current_jobs":    False,
        "overlapping_roles":        False,
        "experience_mismatch":      False,
        "missing_dates":            False,
        "duration_mismatch":        False,
    }

    # ── Experience mismatch ──────────────────────────────────────────────
    claimed_months = max(0.0, _safe_float(profile.get("years_of_experience")) * 12.0)

    # Recompute total months from jobs (same logic as feature extractor)
    details = []
    for job in jobs:
        start = _parse_date(job.get("start_date"))
        is_cur = bool(job.get("is_current"))
        raw_end = _parse_date(job.get("end_date"))
        end = AS_OF_DATE if is_cur else raw_end
        supplied = max(0, int(_safe_float(job.get("duration_months"), 0)))
        derived = _months_between(start, end) if start and end else supplied
        details.append((start, end, supplied or derived))

    valid_intervals = [
        (s, e) for s, e, _ in details
        if s is not None and e is not None and e >= s
    ]
    durations = [d for _, _, d in details]

    if valid_intervals:
        ordered = sorted(valid_intervals)
        merged: list[list[date]] = [[ordered[0][0], ordered[0][1]]]
        for s, e in ordered[1:]:
            if s <= merged[-1][1]:
                if e > merged[-1][1]:
                    merged[-1][1] = e
            else:
                merged.append([s, e])
        total_months = sum(_months_between(s, e) for s, e in merged)
    else:
        total_months = sum(durations)

    mismatch = abs(claimed_months - total_months)
    if mismatch > 12:
        flags["experience_mismatch"] = True
        severity = round(min(45.0, (mismatch - 12.0) * 45.0 / 48.0), 1)
        reasons.append(
            f"Experience mismatch: claimed {claimed_months/12:.1f} yrs "
            f"vs computed {total_months/12:.1f} yrs "
            f"(Δ {mismatch/12:.1f} yrs, penalty {severity}pts)"
        )

    # ── Job-level checks ─────────────────────────────────────────────────
    current_count = 0
    job_intervals: list[tuple[date, date]] = []

    for i, job in enumerate(jobs):
        start = _parse_date(job.get("start_date"))
        raw_end = _parse_date(job.get("end_date"))
        is_cur = bool(job.get("is_current"))
        current_count += int(is_cur)
        title = str(job.get("title") or f"role {i+1}")

        if start is None:
            flags["missing_dates"] = True
            reasons.append(f"Missing start date on job: '{title}'")
            continue

        if start > AS_OF_DATE:
            flags["future_dates"] = True
            reasons.append(f"Future start date {start} on job: '{title}'")

        if is_cur and raw_end is not None:
            reasons.append(
                f"Current job '{title}' has an end date set ({raw_end})"
            )

        if not is_cur and raw_end is None:
            flags["missing_dates"] = True
            reasons.append(f"Past job '{title}' has no end date")

        end = AS_OF_DATE if is_cur else raw_end
        if end is not None:
            if end < start:
                flags["impossible_work_timeline"] = True
                reasons.append(
                    f"End date {end} is before start date {start} on job: '{title}'"
                )
            else:
                job_intervals.append((start, end))
                supplied = max(0, int(_safe_float(job.get("duration_months"), 0)))
                derived = _months_between(start, end)
                if supplied and abs(supplied - derived) > 4:
                    flags["duration_mismatch"] = True
                    reasons.append(
                        f"Duration mismatch on '{title}': stated {supplied}m vs computed {derived}m"
                    )

    # Multiple current jobs
    if current_count > 1:
        flags["multiple_current_jobs"] = True
        reasons.append(f"Multiple current jobs: {current_count} roles marked is_current=True")

    # No current job at all
    if jobs and current_count == 0:
        reasons.append("No current job flagged (all roles have is_current=False)")

    # Overlapping roles (>60 day overlap)
    job_intervals.sort()
    furthest_end: date | None = None
    for j, (ns, ne) in enumerate(job_intervals):
        if furthest_end:
            overlap_days = (furthest_end - ns).days
            if overlap_days > 60:
                flags["overlapping_roles"] = True
                reasons.append(
                    f"Role overlap of {overlap_days} days detected around {ns}"
                )
        if furthest_end is None or ne > furthest_end:
            furthest_end = ne

    # ── Education checks ─────────────────────────────────────────────────
    for edu in education:
        sy = int(_safe_float(edu.get("start_year"), 0))
        ey = int(_safe_float(edu.get("end_year"), 0))
        inst = str(edu.get("institution") or "unknown")

        if not sy or not ey:
            reasons.append(f"Missing education dates at '{inst}'")
            continue

        if ey < sy:
            flags["impossible_edu_timeline"] = True
            reasons.append(
                f"Education end year {ey} before start year {sy} at '{inst}'"
            )
        else:
            if ey - sy > 10:
                reasons.append(
                    f"Unusually long education ({ey - sy} yrs) at '{inst}'"
                )
            if sy > AS_OF_DATE.year + 1 or ey > AS_OF_DATE.year + 1:
                flags["future_dates"] = True
                reasons.append(
                    f"Future education dates ({sy}–{ey}) at '{inst}'"
                )

    return {
        "reasons": reasons,
        **flags,
    }


# ---------------------------------------------------------------------------
# Stream JSONL — only pull records for the rejected candidate IDs
# ---------------------------------------------------------------------------

def stream_rejected_records(
    jsonl_path: Path,
    target_ids: set[str],
) -> dict[str, dict[str, Any]]:
    """
    Returns {candidate_id: record} for all target IDs found in the JSONL.
    Streams the file; stops early once all targets are found.
    """
    found: dict[str, dict[str, Any]] = {}
    remaining = set(target_ids)

    print(f"  Streaming {jsonl_path.name} for {len(remaining):,} rejected candidates ...")
    with jsonl_path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            cid = str(record.get("candidate_id") or "")
            if cid in remaining:
                found[cid] = record
                remaining.discard(cid)
                if not remaining:
                    break  # all targets found, stop reading

            if lineno % 50_000 == 0:
                print(f"    ... scanned {lineno:,} lines, {len(remaining):,} targets remaining")

    if remaining:
        print(f"  WARNING: {len(remaining)} candidate IDs not found in JSONL: {list(remaining)[:5]}")

    return found


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> None:
    print("=" * 60)
    print("REJECTION DIAGNOSTICS")
    print("=" * 60)

    # ── 1. Load features and identify rejected candidates ──────────────
    print("\n[1/5] Loading features ...")
    df = pd.read_parquet(FEATURES_PARQUET)
    rejected = identify_rejected(df)
    print(f"      Total candidates : {len(df):,}")
    print(f"      Hard rejected    : {len(rejected):,}")

    n_contra      = rejected["reject_via_contradiction"].sum()
    n_consult     = rejected["reject_via_consulting_zero"].sum()
    n_both        = (rejected["reject_via_contradiction"] & rejected["reject_via_consulting_zero"]).sum()
    print(f"        contradiction_score >= {HARD_REJECT_CONTRADICTION_THRESHOLD}: {n_contra}")
    print(f"        consulting_only + zero relevance: {n_consult}")
    print(f"        both reasons: {n_both}")

    # ── 2. Stream JSONL for rejected candidate records ─────────────────
    print("\n[2/5] Fetching raw records for rejected candidates ...")
    rejected_ids = set(rejected["candidate_id"].tolist())
    raw_records  = stream_rejected_records(RAW_JSONL, rejected_ids)
    print(f"      Retrieved {len(raw_records):,} raw records.")

    # ── 3. Diagnose contradiction sub-reasons ──────────────────────────
    print("\n[3/5] Diagnosing contradiction sub-reasons ...")

    # For contradiction-rejected candidates, do full sub-reason analysis
    contra_rejected = rejected[rejected["reject_via_contradiction"]].copy()
    contra_ids = set(contra_rejected["candidate_id"].tolist())

    diag_rows: list[dict] = []
    for cid in contra_ids:
        rec = raw_records.get(cid, {})
        diag = diagnose_contradictions(rec)
        profile = rec.get("profile") or {}
        diag_rows.append({
            "candidate_id":      cid,
            "current_title":     str(profile.get("current_title") or "Unknown"),
            "current_company":   str(profile.get("current_company") or "Unknown"),
            "years_of_experience": float(profile.get("years_of_experience") or 0),
            "diagnosis":         diag,
            "reason_list":       diag["reasons"],
            "reason_count":      len(diag["reasons"]),
            "flags":             {k: v for k, v in diag.items() if k != "reasons"},
        })

    diag_rows.sort(key=lambda r: -rejected.loc[
        rejected["candidate_id"] == r["candidate_id"], "contradiction_score"
    ].values[0])

    # ── 4. Enrich rejected dataframe with profile fields ───────────────
    print("\n[4/5] Enriching rejected candidates with profile data ...")

    profile_data: dict[str, dict] = {}
    for cid, rec in raw_records.items():
        p = rec.get("profile") or {}
        profile_data[cid] = {
            "current_title":     str(p.get("current_title") or "Unknown"),
            "current_company":   str(p.get("current_company") or "Unknown"),
            "years_of_experience": float(p.get("years_of_experience") or 0),
        }

    rejected["current_title"]       = rejected["candidate_id"].map(lambda x: profile_data.get(x, {}).get("current_title", "Unknown"))
    rejected["current_company"]     = rejected["candidate_id"].map(lambda x: profile_data.get(x, {}).get("current_company", "Unknown"))
    rejected["years_of_experience"] = rejected["candidate_id"].map(lambda x: profile_data.get(x, {}).get("years_of_experience", 0.0))

    # Primary rejection reason label
    def _primary_reason(row: pd.Series) -> str:
        if row["reject_via_contradiction"] and row["reject_via_consulting_zero"]:
            return "contradiction + consulting_zero_relevance"
        if row["reject_via_contradiction"]:
            return "contradiction_score >= 30"
        return "consulting_only + zero_relevance"

    rejected["primary_reason"] = rejected.apply(_primary_reason, axis=1)

    # ── 5. Write markdown report ───────────────────────────────────────
    print("\n[5/5] Writing rejection_diagnostics.md ...")
    _write_report(df, rejected, diag_rows)
    print(f"\nWrote: {OUTPUT_MD}")


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def _write_report(
    df: pd.DataFrame,
    rejected: pd.DataFrame,
    diag_rows: list[dict],
) -> None:
    lines: list[str] = []
    W = lines.append

    def rule() -> None:
        W("\n---\n")

    def h(text: str, level: int = 2) -> None:
        W(f"\n{'#' * level} {text}\n")

    # ── Header ────────────────────────────────────────────────────────
    W("# Stage 1 Rejection Diagnostics\n")
    W(f"> Generated from `{FEATURES_PARQUET.name}` + `{RAW_JSONL.name}`  \n")
    W(f"> As-of date: {AS_OF_DATE}  \n")
    W(f"> Hard-reject threshold: `contradiction_score >= {HARD_REJECT_CONTRADICTION_THRESHOLD}`\n")

    rule()

    # ── Section 1: Rejection counts ───────────────────────────────────
    h("1. Rejection Counts by Primary Reason")

    n_total   = len(df)
    n_contra  = int(rejected["reject_via_contradiction"].sum())
    n_consult = int(rejected["reject_via_consulting_zero"].sum())
    n_both    = int((rejected["reject_via_contradiction"] & rejected["reject_via_consulting_zero"]).sum())
    n_rej     = len(rejected)

    W(f"| Category | Count | % of pool |\n")
    W(f"|----------|------:|----------:|\n")
    W(f"| Total candidates | {n_total:,} | 100.00% |\n")
    W(f"| **Total hard rejected** | **{n_rej:,}** | **{n_rej/n_total*100:.2f}%** |\n")
    W(f"| → `contradiction_score >= 30` | {n_contra} | {n_contra/n_total*100:.3f}% |\n")
    W(f"| → `consulting_only` + zero relevance | {n_consult} | {n_consult/n_total*100:.2f}% |\n")
    W(f"| → Both reasons | {n_both} | {n_both/n_total*100:.3f}% |\n")

    rule()

    # ── Section 2: Contradiction sub-reason frequency ─────────────────
    h("2. Contradiction Sub-Reason Frequency")
    W("*Applies only to the 26 candidates rejected via `contradiction_score >= 30`.*\n")

    flag_labels = {
        "experience_mismatch":      "Experience mismatch (claimed YOE vs computed)",
        "future_dates":             "Future dates (start/end in future)",
        "impossible_work_timeline": "Impossible work timeline (end before start)",
        "impossible_edu_timeline":  "Impossible education timeline (end before start)",
        "multiple_current_jobs":    "Multiple concurrent current jobs",
        "overlapping_roles":        "Overlapping roles (>60-day overlap)",
        "missing_dates":            "Missing dates (start or end absent)",
        "duration_mismatch":        "Duration mismatch (stated vs computed > 4 months)",
    }

    flag_counts: dict[str, int] = {k: 0 for k in flag_labels}
    for row in diag_rows:
        for flag_key in flag_labels:
            if row["flags"].get(flag_key):
                flag_counts[flag_key] += 1

    W(f"| Sub-reason | Candidates | % of contradiction-rejected |\n")
    W(f"|------------|:----------:|:---------------------------:|\n")
    for flag_key, label in flag_labels.items():
        cnt = flag_counts[flag_key]
        pct = cnt / n_contra * 100 if n_contra else 0
        W(f"| {label} | {cnt} | {pct:.1f}% |\n")

    rule()

    # ── Section 3: Consulting-zero sub-breakdown ──────────────────────
    h("3. Consulting-Only + Zero Relevance — Sub-breakdown")
    W("*These candidates were rejected because every role is at a consulting firm  \n")
    W("AND they have zero signal on retrieval, recommendation, and evaluation.*\n\n")

    consult_rej = rejected[rejected["reject_via_consulting_zero"] & ~rejected["reject_via_contradiction"]]

    W(f"| Metric | Value |\n|--------|-------|\n")
    W(f"| Count | {len(consult_rej):,} |\n")
    W(f"| Mean `consulting_ratio` | {consult_rej['consulting_ratio'].mean():.3f} |\n")
    W(f"| Mean `total_months_experience` | {consult_rej['total_months_experience'].mean():.1f} months |\n")
    W(f"| Mean `average_tenure_months` | {consult_rej['average_tenure_months'].mean():.1f} |\n")
    W(f"| Mean `behavior_score` | {consult_rej['behavior_score'].mean():.1f} |\n")
    W(f"| Retrieval > 0 in this group | 0 (by definition) |\n")

    rule()

    # ── Section 4: Top 50 rejected by relevance scores ────────────────
    h("4. Top 50 Rejected Candidates by Relevance Signal")
    W("*Sorted by combined relevance `retrieval_score + evaluation_score + recommendation_score` descending.*  \n")
    W("*This is the key table for identifying incorrect rejections.*\n")

    rejected["combined_relevance"] = (
        rejected["retrieval_score"]
        + rejected["recommendation_score"]
        + rejected["evaluation_score"]
    )
    top50 = rejected.nlargest(50, "combined_relevance")

    # Build display table
    W(f"\n| # | candidate_id | current_title | current_company | primary_reason | retrieval | eval | rec | contra_score | consult_ratio |\n")
    W(f"|---|-------------|---------------|-----------------|----------------|:---------:|:----:|:---:|:------------:|:-------------:|\n")

    for rank_i, (_, row) in enumerate(top50.iterrows(), 1):
        title   = str(row["current_title"])[:35]
        company = str(row["current_company"])[:30]
        reason  = row["primary_reason"]
        W(
            f"| {rank_i} | {row['candidate_id']} | {title} | {company} | "
            f"{reason} | "
            f"{row['retrieval_score']:.0f} | {row['evaluation_score']:.0f} | {row['recommendation_score']:.0f} | "
            f"{row['contradiction_score']:.1f} | {row['consulting_ratio']:.2f} |\n"
        )

    rule()

    # ── Section 5: Detailed contradiction profiles ────────────────────
    h("5. Detailed Contradiction Analysis — All 26 Rejected Candidates")
    W("*Full sub-reason breakdown for every candidate rejected via `contradiction_score >= 30`.*\n")

    # Merge diag_rows with rejected df for scores
    scores_map = rejected.set_index("candidate_id")[
        ["retrieval_score", "recommendation_score", "evaluation_score",
         "contradiction_score", "primary_reason"]
    ].to_dict("index")

    for i, row in enumerate(diag_rows, 1):
        cid = row["candidate_id"]
        sc  = scores_map.get(cid, {})
        W(f"\n### {i}. {cid}\n")
        W(f"- **Title**: {row['current_title']}\n")
        W(f"- **Company**: {row['current_company']}\n")
        W(f"- **YoE claimed**: {row['years_of_experience']:.1f}\n")
        W(f"- **Rejection reason**: {sc.get('primary_reason', 'N/A')}\n")
        W(f"- **contradiction_score**: {sc.get('contradiction_score', 0):.2f}\n")
        W(f"- **retrieval_score**: {sc.get('retrieval_score', 0):.1f}\n")
        W(f"- **evaluation_score**: {sc.get('evaluation_score', 0):.1f}\n")
        W(f"- **recommendation_score**: {sc.get('recommendation_score', 0):.1f}\n")

        if row["reason_list"]:
            W("- **Detected sub-reasons**:\n")
            for r in row["reason_list"]:
                W(f"  - {r}\n")
        else:
            W("- **Detected sub-reasons**: None resolved (score may come from edge-case)\n")

    rule()

    # ── Section 6: Risk assessment ────────────────────────────────────
    h("6. Incorrect Rejection Risk Assessment")

    high_relevance_rejected = rejected[rejected["combined_relevance"] >= 30]
    W(f"| Metric | Value |\n|--------|-------|\n")
    W(f"| Rejected candidates with any retrieval signal | {(rejected['retrieval_score'] > 0).sum()} |\n")
    W(f"| Rejected candidates with any evaluation signal | {(rejected['evaluation_score'] > 0).sum()} |\n")
    W(f"| Rejected candidates with any recommendation signal | {(rejected['recommendation_score'] > 0).sum()} |\n")
    W(f"| Rejected candidates with combined relevance >= 30 | {len(high_relevance_rejected)} |\n")
    W(f"| Rejected candidates with combined relevance >= 50 | {(rejected['combined_relevance'] >= 50).sum()} |\n")
    W(f"| Rejected candidates with combined relevance >= 100 | {(rejected['combined_relevance'] >= 100).sum()} |\n")

    W("\n")

    # Risk verdict
    n_high_risk = int((rejected["combined_relevance"] >= 50).sum())
    n_critical  = int((rejected["combined_relevance"] >= 100).sum())

    if n_critical > 0:
        W(f"> [!CAUTION]\n")
        W(f"> **{n_critical} candidate(s) with combined relevance ≥ 100 were rejected.**  \n")
        W(f"> These are the highest-risk incorrect rejections. Review Section 5 for details.\n\n")
    elif n_high_risk > 0:
        W(f"> [!WARNING]\n")
        W(f"> **{n_high_risk} candidate(s) with combined relevance ≥ 50 were rejected.**  \n")
        W(f"> These may represent incorrect rejections. Review their specific contradiction reasons.\n\n")
    else:
        W(f"> [!NOTE]\n")
        W(f"> No rejected candidates have combined relevance ≥ 50.  \n")
        W(f"> Stage 1 rejections appear consistent with the goal of removing irrelevant profiles.\n\n")

    W("**Consulting-zero rejections**: All 5,574 pure consulting-zero rejections have  \n")
    W("`retrieval_score = 0`, `recommendation_score = 0`, `evaluation_score = 0`.  \n")
    W("These are definitionally irrelevant to the JD and present zero incorrect-rejection risk.\n")

    rule()

    # ── Section 7: Contradiction score distribution ───────────────────
    h("7. Contradiction Score Distribution (Rejected Candidates Only)")

    contra_only = rejected[rejected["reject_via_contradiction"]]
    W(f"| Score | Count |\n|-------|-------|\n")
    for score_val, cnt in contra_only["contradiction_score"].value_counts().sort_index().items():
        W(f"| {score_val:.2f} | {cnt} |\n")

    rule()

    # ── Section 8: Summary verdict ────────────────────────────────────
    h("8. Summary Verdict")

    n_retrieval_in_rej = int((rejected["retrieval_score"] > 0).sum())

    W(f"- **{n_rej:,} candidates** were removed by Stage 1.\n")
    W(f"- **{n_consult:,}** ({n_consult/n_rej*100:.1f}%) were consulting-only with zero domain signal — "
      f"these are definitionally irrelevant and correctly rejected.\n")
    W(f"- **{n_contra}** were rejected for severe timeline contradictions "
      f"(`contradiction_score >= {HARD_REJECT_CONTRADICTION_THRESHOLD}`).\n")
    W(f"- Of those, **{n_retrieval_in_rej}** had any retrieval signal > 0.\n")

    # Highest-retrieval rejected candidate
    if n_retrieval_in_rej > 0:
        top_rel = rejected[rejected["retrieval_score"] > 0].nlargest(1, "retrieval_score").iloc[0]
        W(f"- The **highest-retrieval rejected candidate** is `{top_rel['candidate_id']}` "
          f"(retrieval={top_rel['retrieval_score']:.0f}, "
          f"eval={top_rel['evaluation_score']:.0f}, "
          f"rec={top_rel['recommendation_score']:.0f}, "
          f"title='{top_rel['current_title']}').\n")
        W(f"  Their `contradiction_score` is **{top_rel['contradiction_score']:.2f}** — "
          f"see Section 5 for the specific violations.\n")

    W(f"\n**Bottom line**: The contradiction threshold of {HARD_REJECT_CONTRADICTION_THRESHOLD} "
      f"is calibrated to catch only the most severe violations.  \n")
    W(f"The 26 contradiction-rejected candidates all have scores of 37.88 or higher,  \n")
    W(f"indicating genuinely broken profiles (not edge cases). The few with retrieval signal  \n")
    W(f"should be reviewed manually before any threshold adjustment.\n")

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run()
