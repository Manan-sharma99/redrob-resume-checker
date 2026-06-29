# Pre-Submission Bug Reproduction Audit

This audit evaluates the three architectural issues discovered during the adversarial design review. Every issue was subjected to strict reproduction criteria against the 100k candidate dataset.

## Issue 1: Stage 3 Credibility Penalty Bypassed by 0-Evidence Stuffers

**1. Exact Code Path:**
- `extract_candidate_features.py:416`: `return round(100.0 * supported / len(claims), 2)` returns `0.0` when zero claims are supported.
- `rank_candidates_v3.py:187`: `unsupported_mask = (df["evidence_support_score"] > 0) & (df["evidence_support_score"] < 50)`

**2. Reproducible Example:**
Candidate claims "BM25, FAISS" in skills, but neither term appears in their career history.

**3. Incorrect Output:**
`evidence_support_score = 0.0`. The ranker's `> 0` mask evaluates to `False`, so the `0.05` penalty is NOT applied.

**4. Expected Output:**
The penalty should apply to candidates with 0% supported claims, resulting in `0.05` penalty.

**5. Candidates Affected:**
18,334 candidates in the dataset have an `evidence_support_score` of `0.0` despite claiming skills.

**6. Top N Impact:**
- Top 100: 0
- Top 250: 0
- Top 1000: 0

**7. Hidden Dataset Risk:**
Negligible. Because `evidence_support_score` carries a 25% weight in the base credibility score, an `evidence_support_score` of `0.0` natively crushes the candidate's base score. The lack of an additional `0.05` penalty is mathematically moot because these candidates never score high enough to enter the Top 1000 anyway.

**Classification:** INSUFFICIENT EVIDENCE (Does not reduce leaderboard performance)

---

## Issue 2: Stage 1 Hard-Reject Bug for Missing Job Start Dates

**1. Exact Code Path:**
`extract_candidate_features.py:480`: `total_months = _union_months(valid_intervals) if valid_intervals else sum(durations)`

**2. Reproducible Example:**
Job 1: `start_date="2024-01-01"`, `end_date="2024-03-01"` (Valid Interval)
Job 2: `start_date=null`, `duration_months=60` (Fallback Duration)

**3. Incorrect Output:**
`total_months` evaluates to 2 months. The 60-month duration is discarded because `valid_intervals` is truthy.

**4. Expected Output:**
`total_months` should equal 62 months.

**5. Candidates Affected:**
0 candidates in the dataset.

**6. Top N Impact:**
0.

**7. Hidden Dataset Risk:**
Severe. While the current 100k public dataset is perfectly sanitized and every job possesses a valid `start_date`, real-world unseen datasets frequently contain jobs with omitted exact dates. Any unseen candidate with mixed date formats will suffer massive `contradiction_score` penalties (>30) and be unfairly Hard-Rejected.

**Classification:** NOT REPRODUCIBLE (on current dataset, despite massive hidden data risk)

---

## Issue 3: Stage 2 Evaluation Bonus Hardcoded to 0.0

**1. Exact Code Path:**
`rank_candidates_v3.py:148`: `eval_bonus = 0.0`

**2. Reproducible Example:**
Candidate achieves `evaluation_score = 100.0`.

**3. Incorrect Output:**
`eval_bonus` remains `0.0`. Base relevance score receives no multiplicative/additive lift.

**4. Expected Output:**
`eval_bonus` should provide a non-zero lift to break ties for candidates with offline/online evaluation experience.

**5. Candidates Affected:**
2,062 candidates in the dataset have genuine evaluation experience (`evaluation_score > 0`).

**6. Top N Impact:**
- Top 100: 77
- Top 250: 154
- Top 1000: 208

**7. Hidden Dataset Risk:**
High. 77 out of the Top 100 candidates are actively being deprived of an intended tie-breaking bonus. This causes generic keyword matchers to unfairly tie or outrank highly specialized senior candidates who possess rare evaluation metrics experience.

**Classification:** VERIFIED BUG

---

# Mandatory Double Check

• **What was originally believed?** All three issues were believed to be critical bugs threatening the leaderboard submission.
• **What was actually verified?** Only Issue 3 (Evaluation Bonus) actively damages the Top 100 on the current dataset. Issue 1 mathematically resolves itself. Issue 2 is an architectural time-bomb that doesn't trigger on the sanitized public data.
• **What assumptions were wrong?** I incorrectly assumed that 0-evidence keyword stuffers could achieve high enough base relevance scores to enter the Top 1000. I also assumed the dataset contained messy date fields, which it does not.
• **Was this bug actually reproducible?** Issue 3 was successfully reproduced and verified. Issue 1 was reproduced but lacks leaderboard impact. Issue 2 failed to reproduce due to clean data.
• **How many real candidates are affected?** Issue 3 affects 2,062 real candidates, including 77 in the Top 100.
• **Would fixing this introduce regression risk?** Fixing `eval_bonus` introduces low regression risk, as it merely restores intended tie-breaking logic.
• **Should this fix be implemented?** Yes, Issue 3 must be fixed. (Issue 2 should also be patched preemptively before hidden evaluation, despite classification).
• **Confidence:** High.
