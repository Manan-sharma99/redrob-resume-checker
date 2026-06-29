# Repository Restructure Log

## Objective
To transform the codebase into a clean, professional, submission-ready repository while preserving 100% identical functionality and output, with NO modifications to the underlying mathematical scoring logic or ranking parameters.

## Architectural Changes (Zero Math Changes)
- **Consolidation**: Identified `rank_candidates_v3.py` as the canonical production pipeline runner and `rank_candidates_final.py` as the algorithmic core used during automated `validate_ranking_system.py` validation. 
- **Renames**: 
  - `rank_candidates_v3.py` -> `rank_candidates.py`
  - `rank_candidates_final.py` -> `tools/validation_engine.py`
- **Output Paths**: Extracted inputs (e.g., `candidates.jsonl`) now source from `data/` and all pipelines write to `outputs/` without any abstraction-heavy modifications (e.g. no overarching configuration classes were used, raw paths were string-updated locally).

## Move Log

### Production Core
- Kept strictly in Root: `extract_candidate_features.py`, `rank_candidates.py`, `validate_ranking_system.py`, `validate_submission.py`, `run_pipeline.py`

### Data to `data/`
- Moved `candidates.jsonl`
- Moved `sample_candidates.json`
- Moved `gold_pairs.yaml`
- Moved `candidate_schema.json`

### Outputs to `outputs/`
- Moved `candidate_features.parquet`
- Moved `ranked_candidates.parquet` (formerly `ranked_candidates_v3.parquet`)
- Moved `final_submission.csv`
- Moved `ranking_diagnostics.md`
- Moved `validation_output.txt`

### Documentation to `docs/`
- Architecture: `FINAL_RANKING_DESIGN.md`, `FEATURE_PIPELINE.md`, `RETRIEVAL_SCORE_DECOMPOSITION.md`, `EVALUATION_BONUS_ROOT_CAUSE.md`
- Validation: `GOLD_PAIR_VALIDATION.md`, `CALIBRATION_REPORT.md`, `ALPHA_IMPACT_VERIFICATION.md`, `REGRESSION_REPORT.md`, `FINAL_ROBUSTNESS_AUDIT.md`
- Audits: `FEATURE_EXTRACTION_AUDIT.md`, `FEATURE_PRECISION_AUDIT.md`, `VERIFIED_BUG_REPORT.md`, `HONEYPOT_ANALYSIS.md`, and ~10 others.
- Methodology: `CONCEPT_REGISTRY.md`, `JD_ANALYSIS.md`

### Engineering Scripts to `tools/`
- Moved `compare_runs.py`
- Moved `generate_gold_pairs.py`
- Moved `calibrate_constants.py`
- Moved `run_audits.py`
- Moved `analyze_dependencies.py`
- Moved `generate_health_report.py`

### Testing to `tests/`
- Moved `test_date_parser.py` (Unit)
- Moved `test_feature_extraction.py` (Integration)
- Moved `audit_synthetic.py` and `synthetic.jsonl` (Synthetic)

### Archive Hierarchy
- **Old Versions**: `rank_candidates.py` (legacy), `rank_candidates_v1.py`, `v2`, `v3.bak`
- **Legacy Runs**: `runs/v001` through `runs/v007`. `v008` preserved dynamically.
- **Obsolete**: 30+ python scripts validated as fully unused via `ast` dependency analysis (e.g. `audit_precision.py`, `bug_reproduction.py`, `fix_audit.py`).
- **Drafts**: Extraneous JSON and CSV analysis dumps.

## Pipeline Verification
The pipeline `python run_pipeline.py` was executed after all paths were updated. The process yielded:
- **0 errors** during Feature Extraction
- **0 errors** during Ranking Iteration
- **0 errors** during Score Validation

Output perfectly matches the frozen production baseline.
