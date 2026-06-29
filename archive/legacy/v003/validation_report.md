# Ranking System Validation Report

## Critical Failures
- **Stage 1: Gold Pairs**: FAIL - 24 pairs failed
  *Evidence*: Test 2 (Moderate Prod Search vs Max Keyword Prototype): Expected Candidate A, got Candidate B (A=0.2829, B=0.2966)
    Test 11 (High Keyword Density vs Moderate Balanced): Expected Candidate B, got Candidate A (A=0.2850, B=0.1800)
    Test 12 (Metrics Operator vs Skill Lister): Expected Candidate A, got Candidate B (A=0.2288, B=0.2699)
    Test 14 (Avg Rel + Elite Metrics vs Elite Rel + Zero Metrics): Expected Candidate A, got Candidate B (A=0.2331, B=0.2933)
    Test 15 (Production Metric Heavy vs BM25 Keyword Lister): Expected Candidate A, got Candidate B (A=0.1830, B=0.2222)
    Test 21 (Weak Product vs Elite Consulting): Expected Candidate B, got Candidate A (A=0.1120, B=0.0000)
    Test 32 (High Eval/Low Cred vs Low Eval/High Cred): Expected Candidate B, got Tie (A=0.0000, B=0.0000)
    Test 34 (Solid Backend Search vs Search Keyword Spammer): Expected Candidate A, got Candidate B (A=0.1650, B=0.3000)
    Test 35 (RecSys Operator vs RecSys Spammer): Expected Candidate A, got Candidate B (A=0.1800, B=0.2850)
    Test 39 (High Total/High Prod vs High Total/Low Prod): Expected Candidate A, got Tie (A=0.0000, B=0.0000)
    Test 40 (Moderate Tenure/High Spec vs Long Tenure/Low Spec): Expected Candidate A, got Tie (A=0.0000, B=0.0000)
    Test 47 (Authentic Hybrid vs Synthetic Hybrid): Expected Candidate A, got Tie (A=0.2160, B=0.2160)
    Test 48 (Boundary Test 1): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 49 (Boundary Test 2): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 50 (Boundary Test 3): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 51 (Boundary Test 4): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 52 (Boundary Test 5): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 53 (Boundary Test 6): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 54 (Boundary Test 7): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 55 (Boundary Test 8): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 56 (Boundary Test 9): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 57 (Boundary Test 10): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 58 (Boundary Test 11): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
    Test 59 (Boundary Test 12): Expected Candidate A, got Candidate B (A=0.2550, B=0.2850)
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
- **Stage 2: Elite Sets**: PASS - Generated 26 elite candidates using dynamic percentiles (Rel>0.28, Prod>38.00).
- **Stage 9: Score Resolution (Top 100)**: PASS - Only 2 near-ties detected (eps=1e-05).
- **Stage 3: Pairwise Stability (Top 100)**: PASS - Most fragile pair rel_diff=0.000000 at rank 17/18.
- **Stage 3: Pairwise Stability (Top 250)**: PASS - Most fragile pair rel_diff=0.000000 at rank 17/18.
- **Stage 4: VIF**: PASS - No severe multicollinearity found (VIF < 10).
- **Stage 4: Pearson**: PASS - All correlations |r| <= 0.80
- **Stage 5: Thresholds**: PASS - Generated threshold distribution audit for 5 features.
- **Stage 6: Sensitivity**: PASS - Top 100 highly stable (min overlap 99/100) across 24 parameter perturbations.
- **Stage 10: Archetypes**: PASS - Top 100 domain breakdown: {'Search': 47, 'Other': 46, 'Hybrid/Matching': 5, 'Recommendation': 2}
- **Stage 10: JD Coverage**: PASS - Search/IR >50: 63%, RecSys >50: 6%, Prod >50: 1%
- **Stage 10: Regression Diff**: PASS - Saved 50 largest rank disagreements against v002 to ranking_diff.csv