import pandas as pd
import extract_candidate_features as ecf

def main():
    # Contribution Matrix
    # We want to map each concept dict to the downstream features it contributes to
    registry = {
        "SEARCH_ENGINES": ecf.SEARCH_ENGINES,
        "VECTOR_DATABASES": ecf.VECTOR_DATABASES,
        "RETRIEVAL_ALGORITHMS": ecf.RETRIEVAL_ALGORITHMS,
        "RANKING_TECHNIQUES": ecf.RANKING_TECHNIQUES,
        "REPRESENTATION_TECHNIQUES": ecf.REPRESENTATION_TECHNIQUES,
        "RETRIEVAL_CONCEPTS": ecf.RETRIEVAL_CONCEPTS,
        "RECOMMENDATION_SYSTEMS": ecf.RECOMMENDATION_SYSTEMS,
        "EVALUATION_TERMS": ecf.EVALUATION_TERMS,
        "PRODUCTION_TECH": ecf.PRODUCTION_TECH,
        "PRODUCTION_SIGNALS": ecf.PRODUCTION_SIGNALS,
        "SPECIFICITY_METRICS": ecf.SPECIFICITY_METRICS
    }
    
    downstream = {
        "production_score": [ecf.PRODUCTION_TECH, ecf.PRODUCTION_SIGNALS],
        "retrieval_score": [ecf.RETRIEVAL_TERMS],
        "recommendation_score": [ecf.RECOMMENDATION_TERMS],
        "evaluation_score": [ecf.EVALUATION_TERMS],
        "specificity_score": [ecf.SPECIFICITY_METRICS],
        "evidence_support_score": [ecf.MAJOR_CLAIMS["retrieval"], ecf.MAJOR_CLAIMS["recommendation"]]
    }
    
    records = []
    for reg_name, reg_dict in registry.items():
        row = {"Concept Group": reg_name}
        for score_name, score_deps in downstream.items():
            contributes = "No"
            # check if reg_dict elements are inside score_deps
            # Since ecf uses dict merging, if a key from reg_dict is in the merged dict, it contributes
            # For evidence_support_score, it's a regex union
            if score_name == "evidence_support_score":
                if reg_name in ["SEARCH_ENGINES", "VECTOR_DATABASES", "RETRIEVAL_ALGORITHMS", "RANKING_TECHNIQUES", "REPRESENTATION_TECHNIQUES", "RETRIEVAL_CONCEPTS"]:
                    contributes = "Yes"
                elif reg_name == "RECOMMENDATION_SYSTEMS":
                    contributes = "Yes"
            else:
                for dep in score_deps:
                    if isinstance(dep, dict) and any(k in dep for k in reg_dict):
                        contributes = "Yes"
            row[score_name] = contributes
        records.append(row)
        
    df = pd.DataFrame(records)
    df.to_csv("CONTRIBUTION_MATRIX.csv", index=False)
    print("Wrote CONTRIBUTION_MATRIX.csv")

if __name__ == "__main__":
    main()
