# Family Concentration Audit

## 1. Top 100 Profile Classification
- **Moderately Concentrated**: 57
- **Balanced**: 42
- **Highly Concentrated**: 1

## 2. Correlation with Retrieval Score
| Variable             |   Pearson |   Spearman |
|:---------------------|----------:|-----------:|
| avg_concepts_per_fam |  0.823874 |   0.951624 |
| largest_fam_size     |  0.767921 |   0.946669 |
| total_concepts       |  0.615626 |   0.932111 |
| unique_fams          |  0.560716 |   0.908268 |

## 3. Counterfactual Experiments
| Simulation   |   Top20_Overlap |   Top100_Overlap |   Top250_Overlap |   Top1000_Overlap |   Kendall_Tau |   Spearman |   Avg_Rank_Movement |   Max_Rank_Movement |
|:-------------|----------------:|-----------------:|-----------------:|------------------:|--------------:|-----------:|--------------------:|--------------------:|
| A            |            0.75 |             0.81 |            0.68  |             0.558 |      0.804125 |   0.862092 |             8159.75 |               85486 |
| B            |            0.85 |             0.8  |            0.688 |             0.499 |      0.896192 |   0.951141 |             4337.81 |               90898 |
| C            |            0.9  |             0.66 |            0.676 |             0.508 |      0.840754 |   0.914718 |             5986.19 |               90088 |
| D            |            0.6  |             0.72 |            0.444 |             0.504 |      0.817586 |   0.889859 |             7509.98 |               90752 |

## 4. Failure Analysis & Root Cause
Based on the data:
- **Root Cause**: `retrieval_score` is primarily explained by concept count, not family diversity. This allows candidates to stack technologies from a single ecosystem (e.g. FAISS, Pinecone, Milvus) and outscore candidates with broad cross-family experience.
- **Top 100 Composition**: The Top 100 remains largely balanced despite the concentration advantage.
