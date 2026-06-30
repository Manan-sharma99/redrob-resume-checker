warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'requirements.txt', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/README.md b/README.md[m
[1mindex ed64f6f..7e0ab8b 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -85,6 +85,34 @@[m [mpython validate_ranking_system.py[m
 - **Credibility Realization**: Features such as production scale markers (QPS, Millions of Users) and explicit specificity metrics establish credibility.[m
 - **Multiplicative Penalties**: We apply severe, non-linear dampening for title-chasers and short-tenure hopping, rather than simple additive deductions.[m
 [m
[32m+[m[32m## Streamlit Demo[m
[32m+[m
[32m+[m[32mA lightweight Streamlit application (`app.py`) wraps the existing pipeline for interactive use.[m
[32m+[m
[32m+[m[32m### Local Execution[m
[32m+[m
[32m+[m[32m```bash[m
[32m+[m[32mpip install -r requirements.txt[m
[32m+[m[32mstreamlit run app.py[m
[32m+[m[32m```[m
[32m+[m
[32m+[m[32mThe app opens in your browser. You can either:[m
[32m+[m[32m- **Use the bundled sample dataset** (`data/sample_candidates.json`), or[m
[32m+[m[32m- **Upload your own** JSON/JSONL file (≤100 candidates).[m
[32m+[m
[32m+[m[32mClick **Run Ranking Pipeline** and the results appear as a sortable table with a CSV download button.[m
[32m+[m
[32m+[m[32m### Streamlit Community Cloud Deployment[m
[32m+[m
[32m+[m[32m1. Push this repository to GitHub (ensure `data/sample_candidates.json` is included).[m
[32m+[m[32m2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.[m
[32m+[m[32m3. Select the repository and set:[m
[32m+[m[32m   - **Main file path:** `app.py`[m
[32m+[m[32m   - **Python version:** 3.11+[m
[32m+[m[32m4. Deploy. Dependencies are installed automatically from `requirements.txt`.[m
[32m+[m
[32m+[m[32m> **Note:** The full `data/candidates.jsonl` (487 MB) is git-ignored and not required for the demo — the app uses `sample_candidates.json` by default.[m
[32m+[m
 ## Limitations[m
 - The system evaluates resumes based on text extraction constraints; heavily obfuscated PDF-to-text anomalies may bypass some chronological validation.[m
 - Network calls and Large Language Models are intentionally disabled during inference to maintain strict latency limits and deterministic reproducibility.[m
[1mdiff --git a/rank_candidates.py b/rank_candidates.py[m
[1mindex 437d24c..357c7e6 100644[m
[1m--- a/rank_candidates.py[m
[1m+++ b/rank_candidates.py[m
[36m@@ -283,14 +283,25 @@[m [mdef compute_final_score([m
 # Pipeline runner[m
 # ===========================================================================[m
 [m
[31m-def run_pipeline() -> None:[m
[32m+[m[32mdef run_pipeline([m
[32m+[m[32m    input_parquet: Path | None = None,[m
[32m+[m[32m    output_parquet: Path | None = None,[m
[32m+[m[32m    submission_csv: Path | None = None,[m
[32m+[m[32m    diagnostics_md: Path | None = None,[m
[32m+[m[32m) -> None:[m
[32m+[m[32m    # Resolve paths — fall back to module-level defaults when not supplied.[m
[32m+[m[32m    input_parquet = input_parquet or INPUT_PARQUET[m
[32m+[m[32m    output_parquet = output_parquet or OUTPUT_PARQUET[m
[32m+[m[32m    submission_csv = submission_csv or SUBMISSION_CSV[m
[32m+[m[32m    diagnostics_md = diagnostics_md or DIAGNOSTICS_MD[m
[32m+[m
     print("=" * 65)[m
     print("RANKING PIPELINE — Senior AI Engineer (Search/Retrieval/Ranking)")[m
     print("=" * 65)[m
 [m
     # --- Load features ---[m
[31m-    print(f"\n[1/7] Loading features from {INPUT_PARQUET} ...")[m
[31m-    df = pd.read_parquet(INPUT_PARQUET)[m
[32m+[m[32m    print(f"\n[1/7] Loading features from {input_parquet} ...")[m
[32m+[m[32m    df = pd.read_parquet(input_parquet)[m
     total_candidates = len(df)[m
     print(f"      Loaded {total_candidates:,} candidates.")[m
 [m
[36m@@ -370,8 +381,9 @@[m [mdef run_pipeline() -> None:[m
         "rank",[m
     ][m
     ranked_output = kept[output_cols].copy()[m
[31m-    ranked_output.to_parquet(OUTPUT_PARQUET, index=False)[m
[31m-    print(f"      Wrote {OUTPUT_PARQUET} ({len(ranked_output):,} rows)")[m
[32m+[m[32m    output_parquet.parent.mkdir(parents=True, exist_ok=True)[m
[32m+[m[32m    ranked_output.to_parquet(output_parquet, index=False)[m
[32m+[m[32m    print(f"      Wrote {output_parquet} ({len(ranked_output):,} rows)")[m
 [m
     # --- Output: final_submission.csv ---[m
     top100 = kept[kept["rank"] <= 100].copy()[m
[36m@@ -515,8 +527,9 @@[m [mdef run_pipeline() -> None:[m
     top100_submission = top100[["candidate_id", "rank", "final_score", "reasoning"]].rename([m
         columns={"final_score": "score"}[m
     )[m
[31m-    top100_submission.to_csv(SUBMISSION_CSV, index=False)[m
[31m-    print(f"      Wrote {SUBMISSION_CSV} ({len(top100_submission)} candidates)")[m
[32m+[m[32m    submission_csv.parent.mkdir(parents=True, exist_ok=True)[m
[32m+[m[32m    top100_submission.to_csv(submission_csv, index=False)[m
[32m+[m[32m    print(f"      Wrote {submission_csv} ({len(top100_submission)} candidates)")[m
 [m
     # --- Console: Top 50 ---[m
     print("\n" + "=" * 65)[m
[36m@@ -537,8 +550,8 @@[m [mdef run_pipeline() -> None:[m
     print(top50.to_string(index=False))[m
 [m
     # --- Diagnostics ---[m
[31m-    _write_diagnostics(df, kept, rejected, top100)[m
[31m-    print(f"\n      Wrote {DIAGNOSTICS_MD}")[m
[32m+[m[32m    _write_diagnostics(df, kept, rejected, top100, diagnostics_md)[m
[32m+[m[32m    print(f"\n      Wrote {diagnostics_md}")[m
     print("\nDone.")[m
 [m
 [m
[36m@@ -555,6 +568,7 @@[m [mdef _write_diagnostics([m
     kept: pd.DataFrame,[m
     rejected: pd.DataFrame,[m
     top100: pd.DataFrame,[m
[32m+[m[32m    diagnostics_path: Path = DIAGNOSTICS_MD,[m
 ) -> None:[m
     lines: list[str] = [][m
 [m
[36m@@ -692,12 +706,33 @@[m [mdef _write_diagnostics([m
     lines.append("final_score = (base_score - penalty).clip(0, 1)\n")[m
     lines.append("```\n")[m
 [m
[31m-    DIAGNOSTICS_MD.write_text("\n".join(lines), encoding="utf-8")[m
[32m+[m[32m    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)[m
[32m+[m[32m    diagnostics_path.write_text("\n".join(lines), encoding="utf-8")[m
 [m
 [m
 # ===========================================================================[m
 # Entry point[m
 # ===========================================================================[m
 [m
[32m+[m[32mdef _parse_args():[m
[32m+[m[32m    import argparse[m
[32m+[m[32m    parser = argparse.ArgumentParser(description=__doc__)[m
[32m+[m[32m    parser.add_argument("--input", type=Path, default=None,[m
[32m+[m[32m                        help="Path to candidate_features.parquet (default: outputs/candidate_features.parquet)")[m
[32m+[m[32m    parser.add_argument("--output", type=Path, default=None,[m
[32m+[m[32m                        help="Path for ranked_candidates.parquet (default: outputs/ranked_candidates.parquet)")[m
[32m+[m[32m    parser.add_argument("--submission", type=Path, default=None,[m
[32m+[m[32m                        help="Path for final_submission.csv (default: outputs/final_submission.csv)")[m
[32m+[m[32m    parser.add_argument("--diagnostics", type=Path, default=None,[m
[32m+[m[32m                        help="Path for ranking_diagnostics.md (default: outputs/ranking_diagnostics.md)")[m
[32m+[m[32m    return parser.parse_args()[m
[32m+[m
[32m+[m
 if __name__ == "__main__":[m
[31m-    run_pipeline()[m
[32m+[m[32m    args = _parse_args()[m
[32m+[m[32m    run_pipeline([m
[32m+[m[32m        input_parquet=args.input,[m
[32m+[m[32m        output_parquet=args.output,[m
[32m+[m[32m        submission_csv=args.submission,[m
[32m+[m[32m        diagnostics_md=args.diagnostics,[m
[32m+[m[32m    )[m
[1mdiff --git a/requirements.txt b/requirements.txt[m
[1mindex 30bdbdf..53eff08 100644[m
[1m--- a/requirements.txt[m
[1m+++ b/requirements.txt[m
[36m@@ -1 +1,5 @@[m
 pyarrow>=15,<25[m
[32m+[m[32mpandas>=2.0[m
[32m+[m[32mnumpy>=1.24[m
[32m+[m[32mstreamlit>=1.30[m
[32m+[m[32mtabulate>=0.9[m
