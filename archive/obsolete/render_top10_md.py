#!/usr/bin/env python3
"""
Build top10_contradiction_rejected.md from top10_contra.json
"""
import json
from pathlib import Path

DATA = Path("top10_contra.json")
OUTPUT = Path("top10_contradiction_rejected.md")

with open(DATA, encoding="utf-8") as f:
    candidates = json.load(f)


def fmt_date(v):
    return str(v) if v else "—"


def yoe_bar(claimed, computed):
    """Visual indicator of claimed vs computed YoE."""
    delta = claimed - computed
    if abs(delta) <= 1:
        return "✓ consistent"
    direction = "inflated" if delta > 0 else "under-stated"
    return f"⚠ {direction} by {abs(delta):.1f} yrs"


lines = []
W = lines.append

W("# Top 10 Contradiction-Rejected Candidates")
W("")
W("> Sorted by combined relevance (`retrieval + evaluation + recommendation`) descending.  ")
W("> These are the highest-relevance candidates removed by Stage 1.")
W("")
W("---")
W("")

# ── Overview table ──────────────────────────────────────────────────────────
W("## Overview")
W("")
W("| # | candidate_id | current_title | current_company | retrieval | eval | rec | combined | contra_score |")
W("|---|-------------|---------------|-----------------|:---------:|:----:|:---:|:--------:|:------------:|")
for c in candidates:
    W(
        f"| {c['rank']} | {c['candidate_id']} | {c['current_title']} | {c['current_company']}"
        f" | {c['retrieval_score']:.0f} | {c['evaluation_score']:.0f} | {c['recommendation_score']:.0f}"
        f" | {c['combined_relevance']:.0f} | {c['contradiction_score']:.2f} |"
    )

W("")
W("---")
W("")

# ── Per-candidate detail ────────────────────────────────────────────────────
for c in candidates:
    rank       = c["rank"]
    cid        = c["candidate_id"]
    title      = c["current_title"]
    company    = c["current_company"]
    claimed    = c["claimed_yoe"]
    computed   = c["computed_yoe"]
    jobs       = c["jobs"]
    edu        = c["education"]
    ret        = c["retrieval_score"]
    rec        = c["recommendation_score"]
    evl        = c["evaluation_score"]
    contra     = c["contradiction_score"]
    reasons    = c["rejection_reasons"]
    combined   = c["combined_relevance"]

    W(f"## {rank}. {cid}")
    W("")

    # Identity block
    W(f"| Field | Value |")
    W(f"|-------|-------|")
    W(f"| **current_title** | {title} |")
    W(f"| **current_company** | {company} |")
    W(f"| **Claimed YoE** | {claimed:.1f} years |")
    W(f"| **Computed YoE** | {computed:.1f} years |")
    W(f"| **YoE assessment** | {yoe_bar(claimed, computed)} |")
    W("")

    # Scores block
    W(f"| Score | Value |")
    W(f"|-------|------:|")
    W(f"| `retrieval_score` | **{ret:.0f}** |")
    W(f"| `recommendation_score` | **{rec:.0f}** |")
    W(f"| `evaluation_score` | **{evl:.0f}** |")
    W(f"| `combined_relevance` | **{combined:.0f}** |")
    W(f"| `contradiction_score` | **{contra:.2f}** |")
    W("")

    # Exact rejection reasons
    W("### Exact Rejection Reasons")
    W("")
    if reasons:
        for r in reasons:
            W(f"- {r}")
    else:
        W("- *(no sub-reasons resolved — check raw record)*")
    W("")

    # Career history table
    W("### Career History")
    W("")
    if jobs:
        W("| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |")
        W("|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|")
        for i, job in enumerate(jobs, 1):
            jt   = str(job.get("title") or "—")
            jc   = str(job.get("company") or "—")
            js   = fmt_date(job.get("start_date"))
            je   = fmt_date(job.get("end_date"))
            cur  = "✓" if job.get("is_current") else ""
            dur  = str(job.get("duration_months") or "—") + "m" if job.get("duration_months") else "—"
            desc = str(job.get("description") or "").replace("|", "/").replace("\n", " ")[:200]
            W(f"| {i} | {jt} | {jc} | {js} | {je} | {cur} | {dur} | {desc} |")
    else:
        W("*(no career history)*")
    W("")

    # Education (brief)
    if edu:
        W("### Education")
        W("")
        W("| institution | degree | field | start | end |")
        W("|-------------|--------|-------|------:|----:|")
        for e in edu:
            inst  = str(e.get("institution") or "—")
            deg   = str(e.get("degree") or "—")
            field = str(e.get("field_of_study") or "—")
            sy    = str(e.get("start_year") or "—")
            ey    = str(e.get("end_year") or "—")
            W(f"| {inst} | {deg} | {field} | {sy} | {ey} |")
        W("")

    W("---")
    W("")

# ── Verdict ─────────────────────────────────────────────────────────────────
W("## Verdict")
W("")
W("All 10 candidates share the same root contradiction: **severe YoE inflation**.")
W("Every profile claims 10–15 years of experience while computed career timelines")
W("span only 2–8 years — a gap that triggers a `contradiction_score` of 37–50.")
W("")

# identify the most at-risk (high relevance + moderate contra)
at_risk = [c for c in candidates if c["combined_relevance"] >= 100]
borderline = [c for c in candidates if 30 <= c["contradiction_score"] < 45]

if at_risk:
    W("> [!CAUTION]")
    W(f"> **{len(at_risk)} candidate(s) with combined relevance ≥ 100** were rejected.")
    W("> These warrant manual review to confirm whether the YoE mismatch is synthetic")
    W("> fabrication or a genuine data entry error.")
    W("")

if borderline:
    W("> [!WARNING]")
    W(f"> **{len(borderline)} candidate(s) have the lowest contradiction score (37.88)**.")
    W("> A threshold of 30.0 catches them. Raising the threshold to 40 would pass them")
    W("> back into the pool. Assess whether that trade-off is desirable.")
    W("")

W("**Pattern diagnosis**: The consistent signature across all 10 is a single-role career")
W("with a `duration_months` value far below what the start–end dates compute to, combined")
W("with a `years_of_experience` claim that matches the (false) stated duration rather than")
W("the actual dates. This is the hallmark of a **synthetic profile generator that inflated")
W("YoE claims without adjusting career dates consistently**.")

OUTPUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUTPUT}  ({OUTPUT.stat().st_size:,} bytes, {len(lines)} lines)")
