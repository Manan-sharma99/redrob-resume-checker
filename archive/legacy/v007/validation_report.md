# Ranking System Validation Report

## Critical Failures
- **Stage 1: Gold Pairs**: FAIL - 7 pairs failed
  *Evidence*: Test 2 (Moderate Prod Search vs Max Keyword Prototype): Expected Candidate A, got Candidate B (A=0.2829, B=0.2966)
    Test 12 (Metrics Operator vs Skill Lister): Expected Candidate A, got Candidate B (A=0.2288, B=0.2699)
    Test 14 (Avg Rel + Elite Metrics vs Elite Rel + Zero Metrics): Expected Candidate A, got Candidate B (A=0.2331, B=0.2933)
    Test 15 (Production Metric Heavy vs BM25 Keyword Lister): Expected Candidate A, got Candidate B (A=0.1830, B=0.2222)
    Test 32 (High Eval/Low Cred vs Low Eval/High Cred): Expected Candidate B, got Tie (A=0.0000, B=0.0000)
    Test 39 (High Total/High Prod vs High Total/Low Prod): Expected Candidate A, got Tie (A=0.0000, B=0.0000)
    Test 40 (Moderate Tenure/High Spec vs Long Tenure/Low Spec): Expected Candidate A, got Tie (A=0.0000, B=0.0000)
  *Candidates Affected*: All Synthetic Pairs

## Warnings
- **Stage 9: Score Collapse (Top 250)**: WARNING - Found 18 adjacent pairs with score diff < 1e-05
  *Evidence*: floating point collapse
  *Action*: Increase credibility variance
- **Stage 4: Entropy**: WARNING - Dead features detected
  *Evidence*: ['recommendation_score', 'contradiction_score']
  *Action*: Remove or rethink these features
- **Stage 8: Duplicates**: WARNING - Text load failed
  *Evidence*: empty vocabulary; perhaps the documents only contain stop words
  *Action*: Ensure candidates.jsonl exists

## Passed Checks
- **Stage 2: Elite Sets**: PASS - Generated 52 elite candidates using dynamic percentiles (Rel>0.28, Prod>39.00).
- **Stage 9: Score Resolution (Top 100)**: PASS - Only 5 near-ties detected (eps=1e-05).
- **Stage 3: Pairwise Stability (Top 100)**: PASS - Most fragile pair rel_diff=0.000000 at rank 21/22.
- **Stage 3: Pairwise Stability (Top 250)**: PASS - Most fragile pair rel_diff=0.000000 at rank 21/22.
- **Stage 4: VIF**: PASS - No severe multicollinearity found (VIF < 10).
- **Stage 4: Pearson**: PASS - All correlations |r| <= 0.80
- **Stage 5: Thresholds**: PASS - Generated threshold distribution audit for 5 features.
- **Stage 6: Sensitivity**: PASS - Top 100 highly stable (min overlap 99/100) across 24 parameter perturbations.
- **Stage 10: Archetypes**: PASS - Top 100 domain breakdown: {'Search': 58, 'Other': 36, 'Hybrid/Matching': 6}
- **Stage 10: JD Coverage**: PASS - Search/IR >50: 99%, RecSys >50: 5%, Prod >50: 24%
- **Stage 10: Regression Diff**: PASS - Saved 50 largest rank disagreements against v006 to ranking_diff.csv