import subprocess
import argparse
import sys

def run_command(cmd):
    print(f"\n=======================================================")
    print(f"Running: {' '.join(cmd)}")
    print(f"=======================================================\n")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed at command: {' '.join(cmd)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="End-to-End Ranking Pipeline")
    parser.add_argument("--skip-validation", action="store_true", help="Skip the validation suite")
    parser.add_argument("--validate-only", action="store_true", help="Only run the validation suite")
    args = parser.parse_args()

    if not args.validate_only:
        run_command([sys.executable, "extract_candidate_features.py"])
        run_command([sys.executable, "rank_candidates.py"])
        
    if not args.skip_validation:
        run_command([sys.executable, "validate_ranking_system.py"])
        
    print("\nPipeline complete.")

if __name__ == "__main__":
    main()
