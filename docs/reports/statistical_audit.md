# Final Statistical Audit Report

## 1. Feature Correlation
### Pearson Correlation
|                        |   relevance_score |   credibility_score |   retrieval_score |   recommendation_score |   evaluation_score |   production_score |   specificity_score |   evidence_support_score |   negative_signal_score |   final_score |
|:-----------------------|------------------:|--------------------:|------------------:|-----------------------:|-------------------:|-------------------:|--------------------:|-------------------------:|------------------------:|--------------:|
| relevance_score        |             1     |               0.153 |             0.951 |                  0.245 |              0.279 |             -0.049 |               0.157 |                    0.268 |                   0.072 |         0.925 |
| credibility_score      |             0.153 |               1     |             0.084 |                  0.105 |              0.231 |              0.645 |               0.668 |                    0.398 |                  -0.082 |         0.208 |
| retrieval_score        |             0.951 |               0.084 |             1     |                  0.182 |             -0.029 |             -0.097 |               0.129 |                    0.21  |                   0.078 |         0.862 |
| recommendation_score   |             0.245 |               0.105 |             0.182 |                  1     |              0.124 |             -0.041 |               0.052 |                    0.324 |                   0.031 |         0.27  |
| evaluation_score       |             0.279 |               0.231 |            -0.029 |                  0.124 |              1     |              0.149 |               0.107 |                    0.187 |                  -0.014 |         0.31  |
| production_score       |            -0.049 |               0.645 |            -0.097 |                 -0.041 |              0.149 |              1     |              -0.036 |                    0.077 |                  -0.086 |        -0.008 |
| specificity_score      |             0.157 |               0.668 |             0.129 |                  0.052 |              0.107 |             -0.036 |               1     |                    0.041 |                  -0.036 |         0.184 |
| evidence_support_score |             0.268 |               0.398 |             0.21  |                  0.324 |              0.187 |              0.077 |               0.041 |                    1     |                  -0.006 |         0.296 |
| negative_signal_score  |             0.072 |              -0.082 |             0.078 |                  0.031 |             -0.014 |             -0.086 |              -0.036 |                   -0.006 |                   1     |        -0.154 |
| final_score            |             0.925 |               0.208 |             0.862 |                  0.27  |              0.31  |             -0.008 |               0.184 |                    0.296 |                  -0.154 |         1     |

### Spearman Correlation
|                        |   relevance_score |   credibility_score |   retrieval_score |   recommendation_score |   evaluation_score |   production_score |   specificity_score |   evidence_support_score |   negative_signal_score |   final_score |
|:-----------------------|------------------:|--------------------:|------------------:|-----------------------:|-------------------:|-------------------:|--------------------:|-------------------------:|------------------------:|--------------:|
| relevance_score        |             1     |               0.108 |             0.947 |                  0.299 |              0.26  |              0.034 |               0.135 |                    0.267 |                   0.054 |         0.927 |
| credibility_score      |             0.108 |               1     |             0.073 |                  0.037 |              0.122 |              0.636 |               0.673 |                    0.194 |                  -0.02  |         0.161 |
| retrieval_score        |             0.947 |               0.073 |             1     |                  0.234 |              0.005 |             -0     |               0.116 |                    0.236 |                   0.071 |         0.876 |
| recommendation_score   |             0.299 |               0.037 |             0.234 |                  1     |              0.062 |             -0.042 |               0.021 |                    0.343 |                   0.016 |         0.262 |
| evaluation_score       |             0.26  |               0.122 |             0.005 |                  0.062 |              1     |              0.069 |               0.113 |                    0.158 |                  -0.064 |         0.262 |
| production_score       |             0.034 |               0.636 |            -0     |                 -0.042 |              0.069 |              1     |              -0.02  |                    0.023 |                  -0.081 |         0.074 |
| specificity_score      |             0.135 |               0.673 |             0.116 |                  0.021 |              0.113 |             -0.02  |               1     |                    0.045 |                   0.067 |         0.176 |
| evidence_support_score |             0.267 |               0.194 |             0.236 |                  0.343 |              0.158 |              0.023 |               0.045 |                    1     |                  -0.014 |         0.26  |
| negative_signal_score  |             0.054 |              -0.02  |             0.071 |                  0.016 |             -0.064 |             -0.081 |               0.067 |                   -0.014 |                   1     |        -0.129 |
| final_score            |             0.927 |               0.161 |             0.876 |                  0.262 |              0.262 |              0.074 |               0.176 |                    0.26  |                  -0.129 |         1     |

### Redundant Features (|r| > 0.85)
- **relevance_score** & **retrieval_score**: Pearson=0.951, Spearman=0.947
- **relevance_score** & **final_score**: Pearson=0.925, Spearman=0.927
- **retrieval_score** & **final_score**: Pearson=0.862, Spearman=0.876

---
## 2. Stage Influence (Penalties)
- Candidates removed from Top 100 due to penalties: 22
- Candidates added to Top 100 due to penalties: 22

### Removed Candidates
- CAND_0000374: base=0.320, penalty=0.320
- CAND_0001471: base=0.320, penalty=0.320
- CAND_0002088: base=0.320, penalty=0.320
- CAND_0002140: base=0.320, penalty=0.320
- CAND_0002433: base=0.320, penalty=0.320
- CAND_0002572: base=0.320, penalty=0.320
- CAND_0002726: base=0.320, penalty=0.320
- CAND_0003687: base=0.320, penalty=0.320
- CAND_0004426: base=0.320, penalty=0.320
- CAND_0004524: base=0.320, penalty=0.320
- CAND_0005272: base=0.320, penalty=0.320
- CAND_0005450: base=0.320, penalty=0.320
- CAND_0005637: base=0.320, penalty=0.320
- CAND_0006092: base=0.320, penalty=0.320
- CAND_0006414: base=0.320, penalty=0.320
- CAND_0006923: base=0.320, penalty=0.320
- CAND_0007132: base=0.320, penalty=0.320
- CAND_0007515: base=0.320, penalty=0.320
- CAND_0007625: base=0.320, penalty=0.320
- CAND_0007648: base=0.320, penalty=0.320
- CAND_0008375: base=0.320, penalty=0.320
- CAND_0008929: base=0.320, penalty=0.320


---
## 3. Weight Sensitivity
| Perturbation | Top100 Changes | Kendall Tau (All) | Kendall Tau (Top 500) |
|---|---|---|---|
| +5% Rel | 6 | 0.4474 | 0.5300 |
| -5% Rel | 8 | 0.4277 | 0.4712 |
| +10% Rel | 5 | 0.4566 | 0.5672 |
| -10% Rel | 12 | 0.4169 | 0.4470 |

---
## 4. Feature Saturation
| Feature | Min | Max | Median | 95th Pctl | Saturation Note |
|---|---|---|---|---|---|
| relevance_score | 0.000 | 0.745 | 0.000 | 0.168 | OK |
| credibility_score | 0.016 | 0.824 | 0.137 | 0.276 | OK |
| retrieval_score | 0.000 | 90.000 | 0.000 | 28.000 | OK |
| recommendation_score | 0.000 | 64.000 | 0.000 | 4.000 | OK |
| evaluation_score | 0.000 | 90.000 | 0.000 | 0.000 | OK |
| production_score | 0.000 | 98.000 | 23.000 | 49.000 | OK |
| specificity_score | 0.000 | 100.000 | 8.000 | 43.000 | OK |
| evidence_support_score | 0.000 | 100.000 | 0.000 | 0.000 | OK |
| negative_signal_score | 0.000 | 0.320 | 0.000 | 0.100 | OK |
| final_score | 0.000 | 0.645 | 0.000 | 0.111 | OK |

---
## 5. Domain Diversity (Top 100)
- **Retrieval/Search**: 62%
- **Hybrid (Search + Rec)**: 22%
- **Generic / Other**: 9%
- **Recommendation/Personalization**: 4%
- **Evaluation-Heavy (ML)**: 3%

---
## 6. Penalty Validation
| Penalty Type | Candidates Affected (Pool) | Avg Score Reduction | Impact on Top 100 |
|---|---|---|---|
| Consulting Only | 1455 | 0.300 | 0 present in Top 100 |
| Contradiction (Hard Reject) | 0 | Hard Reject | Hard Reject |

---
## 7. Borderline Audit (Ranks 80-120)
Candidates whose ranking changes the most under ±5% and ±10% weight perturbations.

| Baseline Rank | Candidate ID | Min Rank | Max Rank | Rank Variance |
|---|---|---|---|---|
| 112 | CAND_0037980 | 112 | 860 | 748 |
| 100 | CAND_0020708 | 100 | 337 | 237 |
| 116 | CAND_0011687 | 116 | 317 | 201 |
| 118 | CAND_0095528 | 118 | 303 | 185 |
| 104 | CAND_0000031 | 104 | 260 | 156 |
| 117 | CAND_0058688 | 117 | 232 | 115 |
| 119 | CAND_0058412 | 119 | 209 | 90 |
| 114 | CAND_0030031 | 114 | 198 | 84 |
| 106 | CAND_0064270 | 106 | 161 | 55 |
| 91 | CAND_0040887 | 91 | 141 | 50 |

---
## 8. Duplicate Archetypes (Top 100)
Looking for highly similar career descriptions (Jaccard similarity > 0.8)...

| Candidate A | Candidate B | Jaccard Sim |
|---|---|---|
| CAND_0001610 | CAND_0013613 | 0.988 |
| CAND_0001610 | CAND_0060054 | 0.957 |
| CAND_0003977 | CAND_0020708 | 0.949 |
| CAND_0003977 | CAND_0036184 | 0.967 |
| CAND_0005260 | CAND_0018499 | 0.968 |
| CAND_0005649 | CAND_0028793 | 0.806 |
| CAND_0005649 | CAND_0044883 | 0.985 |
| CAND_0006557 | CAND_0012957 | 0.990 |
| CAND_0006557 | CAND_0018549 | 0.971 |
| CAND_0006557 | CAND_0024466 | 0.990 |
| CAND_0006557 | CAND_0047721 | 0.971 |
| CAND_0006557 | CAND_0050876 | 0.962 |
| CAND_0006557 | CAND_0061655 | 0.971 |
| CAND_0006557 | CAND_0065878 | 0.981 |
| CAND_0006557 | CAND_0070202 | 0.962 |
| CAND_0007009 | CAND_0020877 | 0.939 |
| CAND_0007009 | CAND_0029367 | 0.930 |
| CAND_0007009 | CAND_0040887 | 0.955 |
| CAND_0007009 | CAND_0069905 | 0.965 |
| CAND_0007009 | CAND_0079064 | 0.947 |
| CAND_0011162 | CAND_0022812 | 0.980 |
| CAND_0011162 | CAND_0032515 | 0.980 |
| CAND_0012957 | CAND_0018549 | 0.962 |
| CAND_0012957 | CAND_0024466 | 0.981 |
| CAND_0012957 | CAND_0047721 | 0.981 |
| CAND_0012957 | CAND_0050876 | 0.953 |
| CAND_0012957 | CAND_0061655 | 0.962 |
| CAND_0012957 | CAND_0065878 | 0.971 |
| CAND_0012957 | CAND_0070202 | 0.971 |
| CAND_0013613 | CAND_0060054 | 0.945 |
| CAND_0014440 | CAND_0036437 | 0.942 |
| CAND_0014440 | CAND_0049538 | 0.971 |
| CAND_0014440 | CAND_0072660 | 0.961 |
| CAND_0016163 | CAND_0027801 | 0.952 |
| CAND_0016163 | CAND_0076251 | 0.943 |
| CAND_0016163 | CAND_0094056 | 0.971 |
| CAND_0018549 | CAND_0024466 | 0.981 |
| CAND_0018549 | CAND_0047721 | 0.944 |
| CAND_0018549 | CAND_0050876 | 0.953 |
| CAND_0018549 | CAND_0061655 | 1.000 |
| CAND_0018549 | CAND_0065878 | 0.953 |
| CAND_0018549 | CAND_0070202 | 0.990 |
| CAND_0018722 | CAND_0030827 | 0.915 |
| CAND_0018722 | CAND_0050454 | 0.952 |
| CAND_0018722 | CAND_0051630 | 0.952 |
| CAND_0018722 | CAND_0054394 | 0.952 |
| CAND_0018722 | CAND_0062247 | 0.924 |
| CAND_0018722 | CAND_0070485 | 0.961 |
| CAND_0018722 | CAND_0076904 | 0.915 |
| CAND_0018722 | CAND_0093912 | 0.915 |
| CAND_0020708 | CAND_0036184 | 0.949 |
| CAND_0020877 | CAND_0029367 | 0.991 |
| CAND_0020877 | CAND_0040887 | 0.930 |
| CAND_0020877 | CAND_0069905 | 0.940 |
| CAND_0020877 | CAND_0079064 | 0.973 |
| CAND_0022812 | CAND_0032515 | 0.961 |
| CAND_0024466 | CAND_0047721 | 0.962 |
| CAND_0024466 | CAND_0050876 | 0.971 |
| CAND_0024466 | CAND_0061655 | 0.981 |
| CAND_0024466 | CAND_0065878 | 0.971 |
| CAND_0024466 | CAND_0070202 | 0.971 |
| CAND_0026532 | CAND_0030348 | 0.946 |
| CAND_0026532 | CAND_0054123 | 0.963 |
| CAND_0026532 | CAND_0066376 | 0.946 |
| CAND_0026532 | CAND_0075249 | 0.972 |
| CAND_0026532 | CAND_0096172 | 0.963 |
| CAND_0027691 | CAND_0043228 | 0.986 |
| CAND_0027691 | CAND_0061265 | 0.951 |
| CAND_0027801 | CAND_0076251 | 0.953 |
| CAND_0027801 | CAND_0094056 | 0.981 |
| CAND_0029367 | CAND_0040887 | 0.939 |
| CAND_0029367 | CAND_0069905 | 0.932 |
| CAND_0029367 | CAND_0079064 | 0.965 |
| CAND_0030348 | CAND_0054123 | 0.929 |
| CAND_0030348 | CAND_0066376 | 0.964 |
| CAND_0030348 | CAND_0075249 | 0.938 |
| CAND_0030348 | CAND_0096172 | 0.964 |
| CAND_0030827 | CAND_0050454 | 0.942 |
| CAND_0030827 | CAND_0051630 | 0.942 |
| CAND_0030827 | CAND_0054394 | 0.961 |
| CAND_0030827 | CAND_0062247 | 0.970 |
| CAND_0030827 | CAND_0070485 | 0.951 |
| CAND_0030827 | CAND_0076904 | 0.980 |
| CAND_0030827 | CAND_0093912 | 0.980 |
| CAND_0031593 | CAND_0041568 | 0.967 |
| CAND_0031593 | CAND_0041669 | 0.993 |
| CAND_0036437 | CAND_0049538 | 0.951 |
| CAND_0036437 | CAND_0072660 | 0.980 |
| CAND_0037000 | CAND_0064326 | 1.000 |
| CAND_0037000 | CAND_0075574 | 0.994 |
| CAND_0039383 | CAND_0044222 | 0.949 |
| CAND_0039383 | CAND_0070398 | 0.991 |
| CAND_0040887 | CAND_0069905 | 0.956 |
| CAND_0040887 | CAND_0079064 | 0.939 |
| CAND_0041568 | CAND_0041669 | 0.961 |
| CAND_0042100 | CAND_0078042 | 0.947 |
| CAND_0043228 | CAND_0061265 | 0.965 |
| CAND_0044222 | CAND_0070398 | 0.957 |
| CAND_0046525 | CAND_0086022 | 0.956 |
| CAND_0046525 | CAND_0094759 | 0.949 |
| CAND_0047721 | CAND_0050876 | 0.935 |
| CAND_0047721 | CAND_0061655 | 0.944 |
| CAND_0047721 | CAND_0065878 | 0.990 |
| CAND_0047721 | CAND_0070202 | 0.953 |
| CAND_0049538 | CAND_0072660 | 0.933 |
| CAND_0050454 | CAND_0051630 | 1.000 |
| CAND_0050454 | CAND_0054394 | 0.942 |
| CAND_0050454 | CAND_0062247 | 0.970 |
| CAND_0050454 | CAND_0070485 | 0.990 |
| CAND_0050454 | CAND_0076904 | 0.961 |
| CAND_0050454 | CAND_0093912 | 0.961 |
| CAND_0050876 | CAND_0061655 | 0.953 |
| CAND_0050876 | CAND_0065878 | 0.944 |
| CAND_0050876 | CAND_0070202 | 0.944 |
| CAND_0051292 | CAND_0083307 | 0.966 |
| CAND_0051630 | CAND_0054394 | 0.942 |
| CAND_0051630 | CAND_0062247 | 0.970 |
| CAND_0051630 | CAND_0070485 | 0.990 |
| CAND_0051630 | CAND_0076904 | 0.961 |
| CAND_0051630 | CAND_0093912 | 0.961 |
| CAND_0054123 | CAND_0066376 | 0.964 |
| CAND_0054123 | CAND_0075249 | 0.991 |
| CAND_0054123 | CAND_0096172 | 0.946 |
| CAND_0054394 | CAND_0062247 | 0.970 |
| CAND_0054394 | CAND_0070485 | 0.951 |
| CAND_0054394 | CAND_0076904 | 0.942 |
| CAND_0054394 | CAND_0093912 | 0.942 |
| CAND_0057563 | CAND_0081686 | 0.953 |
| CAND_0057563 | CAND_0086151 | 0.953 |
| CAND_0061655 | CAND_0065878 | 0.953 |
| CAND_0061655 | CAND_0070202 | 0.990 |
| CAND_0062247 | CAND_0070485 | 0.960 |
| CAND_0062247 | CAND_0076904 | 0.970 |
| CAND_0062247 | CAND_0093912 | 0.970 |
| CAND_0064326 | CAND_0075574 | 0.994 |
| CAND_0065878 | CAND_0070202 | 0.944 |
| CAND_0066376 | CAND_0075249 | 0.973 |
| CAND_0066376 | CAND_0096172 | 0.929 |
| CAND_0069905 | CAND_0079064 | 0.915 |
| CAND_0070485 | CAND_0076904 | 0.951 |
| CAND_0070485 | CAND_0093912 | 0.951 |
| CAND_0075249 | CAND_0096172 | 0.955 |
| CAND_0076251 | CAND_0094056 | 0.934 |
| CAND_0076904 | CAND_0093912 | 1.000 |
| CAND_0081686 | CAND_0086151 | 1.000 |
| CAND_0086022 | CAND_0094759 | 0.964 |

---
## 9. Final Risk Assessment
| Weakness | Severity | Evidence | Leaderboard Impact |
|---|---|---|---|
| **Search vs Recommendation Imbalance** | High | Top 100 is completely dominated by Retrieval archetypes; Recommendation score distribution is extremely compressed at the top end. | Eliminates highly qualified Personalization/RecSys engineers who fit the JD perfectly. |
| **Evaluation Score Overweighting** | High | Evaluation score bonuses (+0.03/+0.06) act as additive boosters irrespective of system depth, correlating moderately with credibility but acting as a kingmaker in final relevance. | Rewards candidates who list metrics (NDCG, MRR) over those who actually built the underlying systems. |
| **Relevance Depth (Tenure Blindness)** | Medium | Retrieval score correlates -0.05 with average tenure; single-role candidates can achieve 60+ retrieval scores. | Junior engineers who keyword-stuff match or beat senior engineers with deep, proven domain tenure. |
| **Negative Penalty Efficacy (Title Chasing)** | Low | Title chasing penalty affects very few (or zero) top candidates due to the strictness of the flag logic. | Minimal. The pipeline relies almost entirely on relevance/credibility to sort the top, rendering this penalty mostly symbolic. |
