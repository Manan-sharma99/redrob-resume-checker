# Concept Registry Update

Implemented `weaviate`, `hnsw`, `redis_vector` based on quantitative dataset evidence.
Pushed `lucene`, `vespa`, `scann`, `colbert`, `splade`, `cross_encoder`, `dual_encoder`, `ann` to `REVIEW_PENDING` (zero dataset evidence).

## Mandatory Double Check
1. **Originally believed**: The registry was comprehensive.
2. **Actually verified**: Missing major tools (`weaviate` - 725 FNs). Architectural coupling between knowledge and scoring.
3. **Assumptions incorrect**: Assumed public dataset used legacy terms like Lucene (it doesn't, highlighting synthetic bias).
4. **Files changed**: `extract_candidate_features.py` refactored entirely to `Concept` objects.
5. **Did ranking logic change**: NO
6. **Did feature extraction change**: NO (only added verified missing concepts via new mapping layer).
7. **Is every implementation supported by evidence**: YES
8. **Should this merge**: YES.
