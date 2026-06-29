# Changelog

## v1.0 Submission (Current)
- Completed exhaustive repository restructuring.
- Frozen all feature extraction and ranking algorithms.
- Validated absolute 100/100 overlap on previous baseline targets.
- Separated input data, output assets, reference documents, and architectural methodology into modular subdirectories.
- Established strict `tools/` and `tests/` directories for engineering utilities and continuous integration checks.

## v0.4
- Conducted the final robustness audit.
- Implemented a Date Robustness patch covering missing strings, ambiguous inputs ("Present", "Current"), and non-ISO strings.
- Fixed a bug penalizing un-dated jobs, preventing arbitrary reduction of credibility.
- Stabilized `contradiction_score` generation.

## v0.3
- Replaced isolated keyword extraction dictionaries with a unified `CONCEPT_REGISTRY`.
- Conducted adversarial analysis evaluating family caps, feature overlap, and penalty weights.
- Diagnosed validation discrepancies related to evaluation metrics being disabled during production implementation.

## v0.2
- Implemented core mathematical penalty constraints targeting title-chasers and consulting-heavy resumes.
- Developed the `validate_ranking_system.py` suite mapping synthetic Gold Pairs and tracking parameter grid drift.

## v0.1
- Initialized core repository.
- Built regex mapping and extraction mechanisms over the candidate `jsonl` structure.
- Assembled the baseline `rank_candidates.py` iterative execution cycle.
