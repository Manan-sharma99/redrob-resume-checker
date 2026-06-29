# Repository Map

A complete guide to navigating the submission structure.

```text
Root
│
├── rank_candidates.py                 - Canonical production ranking script
├── extract_candidate_features.py      - Canonical production extraction script
├── validate_ranking_system.py         - Canonical validation suite
├── validate_submission.py             - Competition submission validator
├── run_pipeline.py                    - E2E pipeline runner
│
├── data/                              - Static Input Data
│   ├── candidates.jsonl               - Raw candidate json data
│   ├── sample_candidates.json         - Smaller debugging set
│   └── gold_pairs.yaml                - Human-verified test assertions
│
├── outputs/                           - Generated pipeline outputs
│   ├── candidate_features.parquet     - Extracted feature matrix
│   ├── ranked_candidates.parquet      - Ranked database
│   ├── final_submission.csv           - Top 100 CSV for portal upload
│   └── ranking_diagnostics.md         - Breakdown of algorithm decisions
│
├── reference/                         - Unmodified Competition Materials
│   ├── job_description.docx           - Target role specs
│   ├── submission_spec.docx           - Official constraints
│   └── redrob_signals_doc.docx        - Additional scoring context
│
├── docs/                              - Structured Documentation
│   ├── Architecture/                  - Design docs for the ranking framework
│   ├── Validation/                    - Results from the validation suite and calibration tests
│   ├── Audits/                        - Extensive testing reports resolving bugs and assessing risk
│   └── Methodology/                   - Concept registry mapping
│
├── tools/                             - Active Engineering Utilities
│   ├── compare_runs.py                - Tau coefficient diff utility
│   ├── generate_gold_pairs.py         - Synthetic candidate generator
│   ├── calibrate_constants.py         - Hyperparameter sweep runner
│   ├── analyze_dependencies.py        - Dependency mapping script
│   ├── generate_health_report.py      - Project health generator
│   └── validation_engine.py           - Core scoring functions parameterized for grid sweeps
│
├── tests/                             - Verification tests
│   ├── unit/                          - e.g., Date Parsing functions
│   ├── integration/                   - e.g., Output schema and extraction targets
│   └── synthetic/                     - Synthetic stress-testing
│
├── runs/                              - Validation Checkpoints
│   └── v008/                          - Snapshot of the latest validated architecture
│
├── archive/                           - Safe cold storage
│   ├── old_versions/                  - Previously active implementations (v1, v2, v3)
│   ├── obsolete/                      - Scripts unreferenced by the current pipeline
│   ├── legacy/                        - Old checkpoints and historic parquets
│   └── drafts/                        - Temporary `.json` and `.csv` dumps
│
├── config/                            - Centralized configuration files
│   ├── config.json                    - Configuration toggles
│   └── submission_metadata_template.yaml
│
├── README.md
├── LICENSE
├── VERSION.md
├── CHANGELOG.md
├── REPOSITORY_HEALTH.md               - Dynamic health tracking
├── REPOSITORY_RESTRUCTURE.md          - Log of reorganization activities
├── FINAL_SUBMISSION_CHECKLIST.md      - Pre-flight delivery checklist
├── requirements.txt
└── .gitignore
```
