# Redrob Ranking System

## Project Overview
This repository contains the production code for the Redrob candidate ranking system. It is designed to reliably evaluate, score, and rank large volumes of candidates (up to 100,000 per run) against complex job descriptions without relying on superficial keyword matching. 

## Problem Statement
Traditional candidate ranking systems are easily fooled by keyword stuffing, "consulting-only" experience that lacks technical depth, and timeline inconsistencies. Our objective is to distinguish genuine production experience from superficial mentions by analyzing chronological evidence, recommendation system signals, and job stability.

## Architecture
The system operates as a deterministic, three-stage pipeline:
1. **Feature Extraction (`extract_candidate_features.py`)**: Streams raw JSONL candidates, applies regex-based extraction grouped by concept families, parses employment dates robustly, and outputs an interpretable Parquet feature table.
2. **Ranking Engine (`rank_candidates.py`)**: Applies mathematically stable weights and a multiplicative scoring approach. It computes `relevance_score`, `credibility_score`, and applies hard contradictions and penalties to generate a deterministic ranking.
3. **Validation Suite (`validate_ranking_system.py`)**: Evaluates the ranking against verified gold pairs, measures feature entropy, checks for drift, and generates a comprehensive HTML-style markdown report.

## Reviewer Quick-Start

**What does this repository do?**
This is the production ranking system for evaluating candidates. It extracts features from `candidates.jsonl`, scores them for domain relevance and credibility, and penalizes contradictory signals.

**How do I install dependencies?**
```bash
pip install -r requirements.txt
```

**What single command reproduces the submission?**
```bash
python run_pipeline.py
```

**Where is the submission CSV written?**
The pipeline writes the final submission strictly to `outputs/final_submission.csv`.

**How is the ranking pipeline organized?**
1. `extract_candidate_features.py` -> Streams `data/candidates.jsonl` to `outputs/candidate_features.parquet`
2. `rank_candidates.py` -> Ranks features and generates `outputs/final_submission.csv`
3. `validate_ranking_system.py` -> Validates results against human baselines in `data/gold_pairs.yaml`

---

## Folder Structure
- **`data/`**: Input candidate datasets and gold pairs.
- **`outputs/`**: Generated features, ranked parquets, and the final CSV.
- **`docs/`**: Deep-dives into architecture, validation reports, and historic methodology.
- **`tools/`**: Core utilities, including `validation_engine.py` required by the test suite.
- **`tests/`**: Unit, integration, and synthetic data stress tests.
- **`archive/`**: Safely preserved legacy scripts and old drafts.

## Installation
1. Ensure Python 3.11+ is installed.
2. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Usage
The system is fully reproducible and requires zero manual intervention once the dataset is placed in the `data/` directory.

### One-Command Execution
You can run the complete end-to-end pipeline (Extraction -> Ranking -> Validation) with a single command:
```bash
python run_pipeline.py
```

Other available flags:
- `python run_pipeline.py --skip-validation`
- `python run_pipeline.py --validate-only`

### Manual Execution
1. Extract features:
```bash
python extract_candidate_features.py --input data/candidates.jsonl --output outputs/candidate_features.parquet
```
2. Rank candidates:
```bash
python rank_candidates.py
```
3. Validate ranking:
```bash
python validate_ranking_system.py
```

## Methodology & Design Decisions
- **Domain Relevance is Core**: We evaluate based on Retrieval, Recommendation, Evaluation metrics, and Machine Learning depth.
- **Evaluation Amplifies**: The presence of offline evaluation experience (like NDCG or MAP) acts as a multiplicative bonus, breaking ties between otherwise identical candidates.
- **Credibility Realization**: Features such as production scale markers (QPS, Millions of Users) and explicit specificity metrics establish credibility.
- **Multiplicative Penalties**: We apply severe, non-linear dampening for title-chasers and short-tenure hopping, rather than simple additive deductions.

## Streamlit Demo

A lightweight Streamlit application (`app.py`) wraps the existing pipeline for interactive use.

### Local Execution

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser. You can either:
- **Use the bundled sample dataset** (`data/sample_candidates.json`), or
- **Upload your own** JSON/JSONL file (≤100 candidates).

Click **Run Ranking Pipeline** and the results appear as a sortable table with a CSV download button.

### Streamlit Community Cloud Deployment

1. Push this repository to GitHub (ensure `data/sample_candidates.json` is included).
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
3. Select the repository and set:
   - **Main file path:** `app.py`
   - **Python version:** 3.11+
4. Deploy. Dependencies are installed automatically from `requirements.txt`.

> **Note:** The full `data/candidates.jsonl` (487 MB) is git-ignored and not required for the demo — the app uses `sample_candidates.json` by default.

## Limitations
- The system evaluates resumes based on text extraction constraints; heavily obfuscated PDF-to-text anomalies may bypass some chronological validation.
- Network calls and Large Language Models are intentionally disabled during inference to maintain strict latency limits and deterministic reproducibility.

## Reproducibility
This system uses no external APIs during the ranking stage and contains zero stochastic elements. Running the pipeline multiple times on the same input data will yield the exact same `final_submission.csv`.
