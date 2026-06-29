# Education Chronology Audit

## Objective
To determine whether education chronology inconsistencies are common enough in the `candidates.jsonl` dataset to justify adding a new contradiction rule, focusing on sequences that violate the normal academic hierarchy.

## Methodology
The dataset was scanned to identify candidates whose education history appears chronologically inconsistent. The following checks were performed:
- Master's completed before Bachelor's.
- PhD completed before Master's.
- PhD completed before Bachelor's.
- Degree end year earlier than start year.

*Integrated and combined degrees were handled conservatively to avoid false flags.*

## Summary Statistics
- **Total Candidates Scanned**: 100,000
- **Affected Candidates**: 11,294
- **Percentage of Dataset**: 11.29%

### Breakdown by Inconsistency Type
- **Master's completed before Bachelor's**: 7,159
- **PhD completed before Master's**: 2,383
- **PhD completed before Bachelor's**: 1,752
- **Degree end year earlier than start year**: 0
*(Note: Some candidates may have multiple inconsistencies.)*

## Cross-Reference Analysis
The affected candidates were cross-referenced against the final ranking features and `contradiction_score` from `ranked_candidates_v3.parquet` and `candidate_features.parquet`:
- **Affected in Top 100**: 9 (9.00% of the Top 100)
- **Affected in Top 1000**: 108 (10.80% of the Top 1000)
- **Affected candidates with existing contradiction penalty**: 2

**Finding**: The current contradiction logic only catches an extremely negligible fraction (2 out of 11,294) of these candidates.

## Impact Estimation
If this education chronology rule were implemented:
- **New Penalties**: 11,292 candidates would receive a new contradiction penalty.
- **Top Candidates Impact**: 9 candidates in the current Top 100 and 108 in the Top 1000 would be directly penalized, resulting in significant shifts to the top of the leaderboard.

## Recommendation
- Add this contradiction rule.

The statistics show a massive blind spot in the current pipeline (11.29% of the dataset exhibits impossible educational chronologies, but only 2 of these candidates are currently penalized). Introducing this rule will address a prevalent issue and improve the integrity of the top-ranked candidates.
