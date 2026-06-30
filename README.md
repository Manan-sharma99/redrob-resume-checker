# 🚀 Redrob Resume Ranking System

> AI-powered deterministic resume ranking system built for the **Redrob India Runs Data & AI Challenge**.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-success)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

---

# 🌐 Live Demo

### Streamlit Sandbox

**https://redrob-resume-checker.streamlit.app/**

The sandbox runs the complete ranking pipeline on a bundled sample dataset (≤100 candidates) and produces a ranked CSV in a few seconds.

---

# ⚡ Quick Start

## Install

```bash
git clone https://github.com/Manan-sharma99/redrob-resume-checker.git

cd redrob-resume-checker

pip install -r requirements.txt
```

## Run Complete Pipeline

```bash
python run_pipeline.py
```

## Launch Streamlit Demo

```bash
streamlit run app.py
```

---

# 📂 Important Files

| File | Purpose |
|------|----------|
| `app.py` | Streamlit sandbox demo |
| `run_pipeline.py` | Runs the complete ranking pipeline |
| `extract_candidate_features.py` | Resume feature extraction |
| `rank_candidates.py` | Core ranking algorithm |
| `validate_submission.py` | Submission validator |
| `validate_ranking_system.py` | Ranking validation |
| `requirements.txt` | Dependencies |

---

# ✨ Key Features

- ✅ Multi-stage resume ranking pipeline
- ✅ Deterministic and reproducible scoring
- ✅ Hard reject filtering
- ✅ Resume feature extraction
- ✅ Technical relevance scoring
- ✅ Credibility scoring
- ✅ Negative hiring signal detection
- ✅ Explainable final ranking
- ✅ Validation utilities
- ✅ CPU-only execution
- ✅ Streamlit sandbox
- ✅ Downloadable ranked CSV

---

# 🏗️ System Architecture

```text
Candidate Dataset
        │
        ▼
Feature Extraction
        │
        ▼
Hard Reject Stage
        │
        ▼
Relevance Scoring
        │
        ▼
Credibility Scoring
        │
        ▼
Negative Signal Analysis
        │
        ▼
Final Score Calculation
        │
        ▼
Ranked Candidate List
```

---

# 🧠 Ranking Methodology

The ranking engine evaluates candidates through multiple independent stages.

## 1. Feature Extraction

Structured candidate features are extracted from resume data.

Examples include:

- Skills
- Experience
- Projects
- Education
- Career history
- Technical evidence

---

## 2. Hard Reject Filtering

Candidates that clearly fail mandatory hiring requirements are removed before ranking.

This reduces noise and prevents unsuitable candidates from influencing the ranking.

---

## 3. Relevance Score

Measures how well a candidate matches the target AI Search / Retrieval / Ranking role.

Examples considered include:

- Elasticsearch
- BM25
- Retrieval Systems
- Ranking Systems
- Vector Databases
- Recommendation Systems
- Search Infrastructure
- Information Retrieval

---

## 4. Credibility Score

Measures the quality and strength of evidence supporting the candidate.

Examples include:

- Technical depth
- Project quality
- Consistency
- Demonstrated experience
- Engineering maturity

---

## 5. Negative Signal Analysis

Applies explainable penalties for undesirable hiring patterns while preserving transparency.

---

## 6. Final Ranking

All signals are combined into a deterministic final score.

Candidates are ranked by descending Final Score.

---

# 📊 Outputs

Running the pipeline generates:

```
outputs/
│
├── candidate_features.parquet
├── ranked_candidates.parquet
├── final_submission.csv
└── ranking_diagnostics.md
```

The final submission file is:

```
outputs/final_submission.csv
```

---

# 🖥️ Streamlit Sandbox

Launch locally:

```bash
streamlit run app.py
```

The sandbox supports:

- Bundled sample dataset
- Upload custom JSON files
- Upload JSONL files
- End-to-end ranking
- CSV download

The sandbox is completely isolated.

It uses temporary files and **never modifies** production datasets or outputs.

---

# 🔁 Reproducibility

This repository is fully reproducible.

The Streamlit sandbox:

- Uses temporary working directories
- Leaves production files unchanged
- Produces deterministic rankings
- Runs entirely on CPU
- Completes in under 5 minutes for demo datasets

---

# 📁 Repository Structure

```text
.
├── app.py
├── run_pipeline.py
├── extract_candidate_features.py
├── rank_candidates.py
├── validate_submission.py
├── validate_ranking_system.py
├── data/
├── docs/
├── outputs/
├── tests/
└── requirements.txt
```

---

# 📋 Requirements

- Python 3.11+
- Streamlit
- Pandas
- PyArrow

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# ✅ Validation

The repository includes utilities for:

- Submission validation
- Ranking validation
- Feature extraction validation
- Regression testing
- Robustness checks
- Diagnostic reporting

---

# 📜 License

MIT License

---

# 🙏 Acknowledgements

Developed for the **Redrob India Runs Data & AI Challenge**.

The goal of this project is to build a transparent, explainable, deterministic, and reproducible resume ranking system for evaluating AI engineering candidates.
