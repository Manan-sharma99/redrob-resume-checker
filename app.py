"""
Streamlit Demo — Redrob Resume Ranking System
================================================
Thin UI wrapper around the existing ranking pipeline.
Does NOT duplicate any ranking, feature-extraction, or scoring logic.

All demo files are written to a temporary directory that is automatically
deleted after each run.  No production files in data/ or outputs/ are
ever modified.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA = DATA_DIR / "sample_candidates.json"

MAX_CANDIDATES = 100

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Redrob Resume Ranking System",
    page_icon="📄",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("Redrob Resume Ranking System Demo")
st.markdown(
    "Upload a candidate JSON/JSONL file (≤100 candidates) or use the bundled "
    "sample dataset, then run the ranking pipeline."
)
st.divider()

# ---------------------------------------------------------------------------
# Data source selection
# ---------------------------------------------------------------------------
source = st.radio(
    "Choose data source",
    options=["Use sample dataset", "Upload candidate file"],
    horizontal=True,
)

uploaded_file = None
if source == "Upload candidate file":
    uploaded_file = st.file_uploader(
        "Upload a JSON or JSONL file",
        type=["json", "jsonl"],
        help="A JSON array or newline-delimited JSONL file with ≤100 candidate records.",
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_candidates(uploaded_file) -> list[dict]:
    """
    Parse candidate records from the uploaded file or the bundled sample.

    Returns a list of candidate dicts (≤MAX_CANDIDATES).
    """
    if uploaded_file is not None:
        raw = uploaded_file.read().decode("utf-8")
        # Try JSON array first, fall back to JSONL.
        try:
            records = json.loads(raw)
            if not isinstance(records, list):
                raise ValueError("Uploaded JSON is not an array of candidate records.")
        except json.JSONDecodeError:
            records = []
            for i, line in enumerate(raw.splitlines(), start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON on line {i}: {exc}") from exc

        if len(records) == 0:
            raise ValueError("Uploaded file contains no candidate records.")
        if len(records) > MAX_CANDIDATES:
            raise ValueError(
                f"Uploaded file contains {len(records)} candidates. "
                f"Maximum allowed is {MAX_CANDIDATES}."
            )
        return records

    # --- Use bundled sample dataset (data/sample_candidates.json) ---
    if not SAMPLE_DATA.is_file():
        raise FileNotFoundError(
            f"Sample dataset not found at {SAMPLE_DATA}. "
            "Please place sample_candidates.json in the data/ directory."
        )

    raw = SAMPLE_DATA.read_text(encoding="utf-8")

    # Try JSON array first, fall back to JSONL.
    try:
        records = json.loads(raw)
        if not isinstance(records, list):
            raise ValueError(
                "sample_candidates.json is not a JSON array of candidate records."
            )
    except json.JSONDecodeError:
        # Attempt JSONL (one JSON object per line).
        records = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if len(records) == 0:
        raise ValueError(
            "sample_candidates.json contains no valid candidate records. "
            "The file may be corrupted."
        )

    records = records[:MAX_CANDIDATES]
    return records


def _write_jsonl(records: list[dict], path: Path) -> None:
    """Write candidate records as JSONL."""
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _run_pipeline(
    tmp_dir: Path,
    status_placeholder,
) -> Path:
    """
    Execute the existing pipeline inside *tmp_dir* so that no production
    files are touched.  Returns the path to the generated submission CSV.
    """
    input_jsonl = tmp_dir / "demo_candidates.jsonl"
    features_pq = tmp_dir / "candidate_features.parquet"
    ranked_pq = tmp_dir / "ranked_candidates.parquet"
    submission_csv = tmp_dir / "final_submission.csv"
    diagnostics_md = tmp_dir / "ranking_diagnostics.md"

    # Step 1: extract features
    status_placeholder.text("Step 1/2 — Extracting candidate features …")
    result = subprocess.run(
        [
            sys.executable,
            str(BASE_DIR / "extract_candidate_features.py"),
            "--input", str(input_jsonl),
            "--output", str(features_pq),
        ],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Feature extraction failed:\n{result.stderr or result.stdout}"
        )

    # Step 2: rank candidates
    status_placeholder.text("Step 2/2 — Ranking candidates …")
    result = subprocess.run(
        [
            sys.executable,
            str(BASE_DIR / "rank_candidates.py"),
            "--input", str(features_pq),
            "--output", str(ranked_pq),
            "--submission", str(submission_csv),
            "--diagnostics", str(diagnostics_md),
        ],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Ranking failed:\n{result.stderr or result.stdout}"
        )

    return submission_csv


# ---------------------------------------------------------------------------
# Run button
# ---------------------------------------------------------------------------
run_disabled = source == "Upload candidate file" and uploaded_file is None
run_button = st.button(
    "🚀 Run Ranking Pipeline",
    disabled=run_disabled,
    use_container_width=True,
)

if run_button:
    try:
        # Parse input records (in memory — nothing written to disk yet)
        with st.spinner("Preparing input data …"):
            records = _parse_candidates(uploaded_file)
            n_candidates = len(records)

        st.info(f"**{n_candidates}** candidates loaded.")

        # Run inside a temporary directory — auto-cleaned on exit
        with tempfile.TemporaryDirectory(prefix="redrob_demo_") as tmp_str:
            tmp_dir = Path(tmp_str)

            # Write demo JSONL to temp
            _write_jsonl(records, tmp_dir / "demo_candidates.jsonl")

            # Execute pipeline
            status_area = st.empty()
            submission_csv = _run_pipeline(tmp_dir, status_area)
            status_area.empty()

            st.success("✅ Ranking complete!")

            # Read results before temp dir is deleted
            if submission_csv.is_file():
                df = pd.read_csv(submission_csv)
                csv_bytes = df.to_csv(index=False).encode("utf-8")
            else:
                df = None
                csv_bytes = None

        # Display results (temp dir already cleaned up)
        if df is not None:
            st.subheader("Ranked Results")
            st.caption(f"Showing top {len(df)} candidates")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                label="📥 Download Ranked CSV",
                data=csv_bytes,
                file_name="ranked_candidates.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.warning("Ranking completed but no output CSV was generated.")

    except (ValueError, FileNotFoundError) as exc:
        st.error(f"**Input error:** {exc}")
    except RuntimeError as exc:
        st.error(f"**Pipeline error:** {exc}")
    except Exception as exc:
        st.error(f"**Unexpected error:** {type(exc).__name__}: {exc}")
