# Candidate feature extraction

Run:

```powershell
python -m pip install -r requirements.txt
python extract_candidate_features.py
```

This streams `candidates.jsonl` and writes `candidate_features.parquet` in
5,000-row batches with bounded memory. The default as-of date is `2026-06-24`; override it with
`--as-of-date YYYY-MM-DD` when processing a later snapshot.
Use `--limit 1000` for a quick representative test run.

## Scoring rules

All score features are deterministic and bounded to 0–100.

- `production_score`: action verbs, named infrastructure technologies,
  production signals, and per-role co-occurrence. Career descriptions can
  contribute 90 points; skill names can contribute at most 10.
- `retrieval_score`, `recommendation_score`, `evaluation_score`: exact
  case-insensitive phrase families. Career descriptions contribute up to 90
  points and skills up to 10. Evaluation terms have the largest per-term
  weight because the specification marks them high-confidence.
- `specificity_score`: quantities with units or scale suffixes, named metrics,
  and quantified improvement language. It uses descriptions only.
- `evidence_support_score`: percentage of claimed major skill families
  (`retrieval`, `ranking`, `recommendation`, `ml`, `search`) also found in
  career descriptions. No relevant skill claim produces 0.
- `total_months_experience`: union of valid career intervals, avoiding double
  counting overlapping roles. Supplied durations are the fallback.
- `average_tenure_months`: mean supplied/derived role duration.
- `short_tenure_count`: roles shorter than 12 months.
- `title_progression_score`: 50 is flat/unknown; promotions raise it and
  regressions lower it using an explicit title-seniority dictionary.
- `consulting_ratio`: share of role months at the six specified consulting
  firms. `consulting_only_flag` requires every role to be at one.
- `behavior_score`: weighted recruiter response (25%), GitHub activity (20%),
  recruiter saves (20%), interview completion (25%), open-to-work (5%), and
  shorter notice period (5%). Missing/unlinked GitHub contributes zero.
- `contradiction_score`: experience mismatch after a 12-month tolerance,
  invalid/future/inconsistent job dates, duration disagreement, overlapping
  roles, multiple current roles, and invalid/future education dates. Higher
  means more contradictions.

No ranking formula, embeddings, transformers, semantic similarity, or model
calls are used.
