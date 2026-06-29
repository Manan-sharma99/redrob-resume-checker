import os
import shutil
import glob
from pathlib import Path

def setup_dirs():
    dirs = [
        "data",
        "outputs",
        "reference",
        "docs/Architecture",
        "docs/Validation",
        "docs/Audits",
        "docs/Methodology",
        "tools",
        "tests/unit",
        "tests/integration",
        "tests/synthetic",
        "archive/old_versions",
        "archive/obsolete",
        "archive/legacy",
        "archive/drafts",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def move_file(src, dst):
    if os.path.exists(src):
        # Handle if dst is a dir
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        if os.path.exists(dst):
            try:
                os.remove(dst)
            except PermissionError:
                pass
        try:
            shutil.move(src, dst)
            print(f"Moved {src} -> {dst}")
        except PermissionError:
            try:
                shutil.copy2(src, dst)
                print(f"Copied {src} -> {dst} (could not move)")
            except Exception as e:
                print(f"Failed to copy {src}: {e}")
    else:
        print(f"Warning: {src} not found")

def main():
    setup_dirs()
    
    # Data inputs
    move_file("candidates.jsonl", "data/candidates.jsonl")
    move_file("sample_candidates.json", "data/sample_candidates.json")
    move_file("gold_pairs.yaml", "data/gold_pairs.yaml")
    move_file("candidate_schema.json", "data/candidate_schema.json")
    
    # Outputs
    move_file("candidate_features.parquet", "outputs/candidate_features.parquet")
    move_file("ranked_candidates_v3.parquet", "outputs/ranked_candidates.parquet")
    move_file("final_submission.csv", "outputs/final_submission.csv")
    move_file("ranking_diagnostics.md", "outputs/ranking_diagnostics.md")
    move_file("validation_output.txt", "outputs/validation_output.txt")
    
    # Reference
    move_file("job_description.docx", "reference/job_description.docx")
    move_file("submission_spec.docx", "reference/submission_spec.docx")
    move_file("redrob_signals_doc.docx", "reference/redrob_signals_doc.docx")
    move_file("README.docx", "reference/README.docx")
    
    # Docs - Architecture
    move_file("FINAL_RANKING_DESIGN.md", "docs/Architecture/FINAL_RANKING_DESIGN.md")
    move_file("FEATURE_PIPELINE.md", "docs/Architecture/FEATURE_PIPELINE.md")
    move_file("RETRIEVAL_SCORE_DECOMPOSITION.md", "docs/Architecture/RETRIEVAL_SCORE_DECOMPOSITION.md")
    move_file("EVALUATION_BONUS_ROOT_CAUSE.md", "docs/Architecture/EVALUATION_BONUS_ROOT_CAUSE.md")
    
    # Docs - Validation
    move_file("GOLD_PAIR_VALIDATION.md", "docs/Validation/GOLD_PAIR_VALIDATION.md")
    move_file("CALIBRATION_REPORT.md", "docs/Validation/CALIBRATION_REPORT.md")
    move_file("ALPHA_IMPACT_VERIFICATION.md", "docs/Validation/ALPHA_IMPACT_VERIFICATION.md")
    move_file("REGRESSION_REPORT.md", "docs/Validation/REGRESSION_REPORT.md")
    move_file("FINAL_ROBUSTNESS_AUDIT.md", "docs/Validation/FINAL_ROBUSTNESS_AUDIT.md")
    
    # Docs - Audits
    move_file("FEATURE_EXTRACTION_AUDIT.md", "docs/Audits/FEATURE_EXTRACTION_AUDIT.md")
    move_file("FEATURE_EXTRACTION_EVIDENCE.md", "docs/Audits/FEATURE_EXTRACTION_EVIDENCE.md")
    move_file("FEATURE_EXTRACTION_IMPLEMENTATION.md", "docs/Audits/FEATURE_EXTRACTION_IMPLEMENTATION.md")
    move_file("FEATURE_PRECISION_AUDIT.md", "docs/Audits/FEATURE_PRECISION_AUDIT.md")
    move_file("EDUCATION_CHRONOLOGY_AUDIT.md", "docs/Audits/EDUCATION_CHRONOLOGY_AUDIT.md")
    move_file("FAMILY_CONCENTRATION_REPORT.md", "docs/Audits/FAMILY_CONCENTRATION_REPORT.md")
    move_file("FAMILY_DIVERSITY_AUDIT.md", "docs/Audits/FAMILY_DIVERSITY_AUDIT.md")
    move_file("REGEX_SHADOWING_REPORT.md", "docs/Audits/REGEX_SHADOWING_REPORT.md")
    move_file("SPECIFICATION_CONFORMANCE_AUDIT.md", "docs/Audits/SPECIFICATION_CONFORMANCE_AUDIT.md")
    move_file("TOP100_QUALITY_AUDIT.md", "docs/Audits/TOP100_QUALITY_AUDIT.md")
    move_file("VERIFIED_BUG_REPORT.md", "docs/Audits/VERIFIED_BUG_REPORT.md")
    move_file("HONEYPOT_ANALYSIS.md", "docs/Audits/HONEYPOT_ANALYSIS.md")
    move_file("statistical_audit.md", "docs/Audits/statistical_audit.md")
    move_file("rejection_diagnostics.md", "docs/Audits/rejection_diagnostics.md")
    move_file("final_validation_report.md", "docs/Validation/final_validation_report.md")
    
    # Docs - Methodology
    move_file("CONCEPT_REGISTRY.md", "docs/Methodology/CONCEPT_REGISTRY.md")
    move_file("CONCEPT_REGISTRY_SCHEMA.md", "docs/Methodology/CONCEPT_REGISTRY_SCHEMA.md")
    move_file("CONCEPT_REGISTRY_UPDATE.md", "docs/Methodology/CONCEPT_REGISTRY_UPDATE.md")
    move_file("JD_ANALYSIS.md", "docs/Methodology/JD_ANALYSIS.md")
    
    # Data dumps from audits -> archive/drafts
    csvs = glob.glob("*.csv")
    for csv in csvs:
        if csv not in ["final_submission.csv", "sample_submission.csv"]:
            move_file(csv, "archive/drafts/")
            
    # Tools
    tools = ["compare_runs.py", "generate_gold_pairs.py", "calibrate_constants.py", "run_audits.py", "analyze_dependencies.py"]
    for t in tools:
        move_file(t, "tools/")
        
    # Tests
    move_file("test_date_parser.py", "tests/unit/")
    move_file("test_feature_extraction.py", "tests/integration/")
    move_file("audit_synthetic.py", "tests/synthetic/")
    move_file("synthetic.jsonl", "tests/synthetic/")
    move_file("synthetic_features.parquet", "tests/synthetic/")
    move_file("synthetic_ranked.parquet", "tests/synthetic/")
    
    # Old versions
    for v in ["rank_candidates.py", "rank_candidates_v1.py", "rank_candidates_v2.py", "rank_candidates_v3.bak"]:
        if os.path.exists(v):
            move_file(v, "archive/old_versions/")
            
    # Ranking scripts renaming and archiving
    # The production script is rank_candidates_v3.py.
    # The validation engine is rank_candidates_final.py.
    move_file("rank_candidates_v3.py", "rank_candidates.py")
    move_file("rank_candidates_final.py", "tools/validation_engine.py")
            
    # Other obsolete python files
    unreferenced = [
        "audit_analysis.py", "audit_contribution.py", "audit_correlation.py",
        "audit_coverage.py", "audit_duplicates.py", "audit_education.py",
        "audit_evidence.py", "audit_fp.py", "audit_precision.py", "audit_recall.py",
        "audit_top100.py", "bug_reproduction.py", "extract_top10_contra.py",
        "family_concentration_audit.py", "final_validation.py", "fix.py",
        "fix_audit.py", "gen_alpha_report.py", "generate_and_run_variants.py",
        "inspect_features.py", "inspect_schema.py", "inspect_top20.py",
        "refactor.py", "refactor_extractor.py", "rejection_diagnostics.py",
        "render_top10_md.py", "run_rca.py", "spec_audit.py", "statistical_audit.py",
        "test_alpha.py", "test_impact.py", "verify_alpha.py"
    ]
    for u in unreferenced:
        move_file(u, "archive/obsolete/")
        
    # JSON drafts
    jsons = glob.glob("*.json")
    for j in jsons:
        if j not in ["config.json", "package.json"]:
            move_file(j, "archive/drafts/")
            
    # Runs directory cleanup
    if os.path.exists("runs"):
        runs = sorted(os.listdir("runs"))
        if runs:
            latest = runs[-1]
            for r in runs:
                if r != latest:
                    move_file(f"runs/{r}", "archive/legacy/")
                    
    # Old ranked parquet
    if os.path.exists("ranked_candidates.parquet"):
        move_file("ranked_candidates.parquet", "archive/legacy/")
    if os.path.exists("ranked_candidates_v1.parquet"):
        move_file("ranked_candidates_v1.parquet", "archive/legacy/")
    if os.path.exists("ranked_candidates_v2.parquet"):
        move_file("ranked_candidates_v2.parquet", "archive/legacy/")
        
    print("Reorganization complete.")

if __name__ == "__main__":
    main()
