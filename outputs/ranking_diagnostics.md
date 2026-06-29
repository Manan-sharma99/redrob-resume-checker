# Ranking Diagnostics

**Total candidates**: 100,000  
**Hard rejected**: 4,971  
**Ranked**: 95,029  


## Score Distributions (full dataset before hard reject)

| feature                 |   mean |   std |   min |   p25 |   p50 |    p75 |    p95 |   max |   nonzero |
|:------------------------|-------:|------:|------:|------:|------:|-------:|-------:|------:|----------:|
| retrieval_score         |   6.42 | 10.86 |  0    |  0    |  0    |   8    |  28    | 100   |    38,651 |
| recommendation_score    |   0.28 |  1.55 |  0    |  0    |  0    |   0    |   4    |  64   |     5,420 |
| evaluation_score        |   0.68 |  4.83 |  0    |  0    |  0    |   0    |   0    |  90   |     2,062 |
| production_score        |  24.01 | 12.44 |  0    | 16    | 22    |  28    |  49    | 100   |    99,996 |
| specificity_score       |  10.57 | 13.63 |  0    |  0    |  7    |  20    |  40    |  94   |    50,019 |
| evidence_support_score  |   1.96 | 12.31 |  0    |  0    |  0    |   0    |   0    | 100   |     2,782 |
| contradiction_score     |   0.01 |  0.79 |  0    |  0    |  0    |   0    |   0    |  50   |        49 |
| behavior_score          |  45.43 | 11.53 | 10.67 | 37.25 | 45.33 |  53.42 |  64.51 |  91.5 |   100,000 |
| consulting_ratio        |   0.26 |  0.31 |  0    |  0    |  0.16 |   0.45 |   1    |   1   |    55,575 |
| title_progression_score |  50    | 14.87 |  0    | 50    | 50    |  50    |  75    | 100   |    97,019 |
| average_tenure_months   |  28.36 |  7.82 |  8    | 23.25 | 28    |  33    |  42    |  98   |   100,000 |
| total_months_experience |  84.51 | 44.64 | 13    | 47    | 81    | 117    | 164    | 178   |   100,000 |


## Penalty Distributions (post hard-reject)

| metric                      |      value |
|:----------------------------|-----------:|
| candidates with any penalty | 31377      |
| consulting_only_flag=True   |  2084      |
| consulting_ratio > 0.60     |  8226      |
| title_chaser detected       |     0      |
| behavior_score below p25    | 23652      |
| mean penalty                |     0.0202 |
| max penalty                 |     0.32   |


## Hard Rejected Candidates

**Count**: 4,971

| candidate_id   | reject_reason              |   contradiction_score | consulting_only_flag   |
|:---------------|:---------------------------|----------------------:|:-----------------------|
| CAND_0000003   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000008   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000028   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000047   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000059   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000086   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000098   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000164   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000174   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000175   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000250   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000257   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000265   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000281   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000283   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000315   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000329   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000335   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000362   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000369   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000379   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000380   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000407   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000416   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000427   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000438   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000463   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000469   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000502   | consulting_zero_relevance; |                     0 | True                   |
| CAND_0000531   | consulting_zero_relevance; |                     0 | True                   |


## Top 20 Candidates by Relevance Score

| candidate_id   |   relevance_score |   credibility_score |   negative_signal_score |   final_score |   rank |   retrieval_score |   evaluation_score |   recommendation_score |
|:---------------|------------------:|--------------------:|------------------------:|--------------:|-------:|------------------:|-------------------:|-----------------------:|
| CAND_0092278   |             0.975 |              0.498  |                    0.02 |        0.7347 |      9 |               100 |                 90 |                     51 |
| CAND_0094759   |             0.935 |              0.699  |                    0    |        0.8084 |      1 |               100 |                 74 |                      0 |
| CAND_0046064   |             0.93  |              0.538  |                    0    |        0.7367 |      7 |               100 |                 72 |                     32 |
| CAND_0086022   |             0.93  |              0.4183 |                    0    |        0.6866 |     16 |               100 |                 72 |                      4 |
| CAND_0041611   |             0.92  |              0.666  |                    0.02 |        0.7617 |      4 |                98 |                 74 |                      0 |
| CAND_0046525   |             0.9   |              0.502  |                    0    |        0.6983 |     13 |                96 |                 72 |                      0 |
| CAND_0018499   |             0.9   |              0.4377 |                    0    |        0.6723 |     18 |               100 |                 60 |                     19 |
| CAND_0077337   |             0.895 |              0.751  |                    0    |        0.7947 |      3 |               100 |                 58 |                     49 |
| CAND_0055905   |             0.89  |              0.774  |                    0    |        0.7995 |      2 |               100 |                 56 |                     15 |
| CAND_0081846   |             0.89  |              0.5023 |                    0    |        0.6907 |     15 |               100 |                 56 |                      4 |
| CAND_0033861   |             0.885 |              0.625  |                    0    |        0.7357 |      8 |               100 |                 54 |                     60 |
| CAND_0080766   |             0.885 |              0.566  |                    0    |        0.7122 |     12 |               100 |                 54 |                     15 |
| CAND_0005260   |             0.885 |              0.333  |                    0    |        0.6194 |     41 |               100 |                 54 |                     15 |
| CAND_0079387   |             0.84  |              0.742  |                    0    |        0.7425 |      5 |               100 |                 36 |                     34 |
| CAND_0008425   |             0.84  |              0.734  |                    0    |        0.7395 |      6 |               100 |                 36 |                     36 |
| CAND_0068811   |             0.84  |              0.718  |                    0    |        0.7334 |     10 |               100 |                 36 |                     30 |
| CAND_0005649   |             0.84  |              0.5812 |                    0    |        0.6817 |     17 |               100 |                 36 |                      4 |
| CAND_0044883   |             0.825 |              0.6485 |                    0    |        0.6945 |     14 |                98 |                 36 |                      0 |
| CAND_0010685   |             0.81  |              0.5965 |                    0    |        0.6629 |     20 |                96 |                 36 |                      0 |
| CAND_0030953   |             0.805 |              0.746  |                    0    |        0.713  |     11 |               100 |                 22 |                     30 |


## Top 20 Candidates by Final Score

| candidate_id   |   final_score |   relevance_score |   credibility_score |   negative_signal_score |   rank |   retrieval_score |   evaluation_score |   recommendation_score |   production_score |   specificity_score |   evidence_support_score |
|:---------------|--------------:|------------------:|--------------------:|------------------------:|-------:|------------------:|-------------------:|-----------------------:|-------------------:|--------------------:|-------------------------:|
| CAND_0094759   |        0.8084 |             0.935 |              0.699  |                    0    |      1 |               100 |                 74 |                      0 |                 37 |                  86 |                   100    |
| CAND_0055905   |        0.7995 |             0.89  |              0.774  |                    0    |      2 |               100 |                 56 |                     15 |                 61 |                  80 |                   100    |
| CAND_0077337   |        0.7947 |             0.895 |              0.751  |                    0    |      3 |               100 |                 58 |                     49 |                 43 |                  94 |                   100    |
| CAND_0041611   |        0.7617 |             0.92  |              0.666  |                    0.02 |      4 |                98 |                 74 |                      0 |                 53 |                  94 |                    50    |
| CAND_0079387   |        0.7425 |             0.84  |              0.742  |                    0    |      5 |               100 |                 36 |                     34 |                 60 |                  72 |                   100    |
| CAND_0008425   |        0.7395 |             0.84  |              0.734  |                    0    |      6 |               100 |                 36 |                     36 |                 58 |                  72 |                   100    |
| CAND_0046064   |        0.7367 |             0.93  |              0.538  |                    0    |      7 |               100 |                 72 |                     32 |                 58 |                  16 |                   100    |
| CAND_0033861   |        0.7357 |             0.885 |              0.625  |                    0    |      8 |               100 |                 54 |                     60 |                 55 |                  80 |                    50    |
| CAND_0092278   |        0.7347 |             0.975 |              0.498  |                    0.02 |      9 |               100 |                 90 |                     51 |                 32 |                  70 |                    50    |
| CAND_0068811   |        0.7334 |             0.84  |              0.718  |                    0    |     10 |               100 |                 36 |                     30 |                 54 |                  72 |                   100    |
| CAND_0030953   |        0.713  |             0.805 |              0.746  |                    0    |     11 |               100 |                 22 |                     30 |                 54 |                  80 |                   100    |
| CAND_0080766   |        0.7122 |             0.885 |              0.566  |                    0    |     12 |               100 |                 54 |                     15 |                 49 |                  70 |                    50    |
| CAND_0046525   |        0.6983 |             0.9   |              0.502  |                    0    |     13 |                96 |                 72 |                      0 |                 33 |                  70 |                    50    |
| CAND_0044883   |        0.6945 |             0.825 |              0.6485 |                    0    |     14 |                98 |                 36 |                      0 |                 62 |                  43 |                   100    |
| CAND_0081846   |        0.6907 |             0.89  |              0.5023 |                    0    |     15 |               100 |                 56 |                      4 |                 49 |                  78 |                    33.33 |
| CAND_0086022   |        0.6866 |             0.93  |              0.4183 |                    0    |     16 |               100 |                 72 |                      4 |                 35 |                  70 |                    33.33 |
| CAND_0005649   |        0.6817 |             0.84  |              0.5812 |                    0    |     17 |               100 |                 36 |                      4 |                 66 |                  43 |                    66.67 |
| CAND_0018499   |        0.6723 |             0.9   |              0.4377 |                    0    |     18 |               100 |                 60 |                     19 |                 52 |                  18 |                    66.67 |
| CAND_0086151   |        0.6698 |             0.795 |              0.65   |                    0    |     19 |               100 |                 18 |                     34 |                 37 |                  72 |                   100    |
| CAND_0010685   |        0.6629 |             0.81  |              0.5965 |                    0    |     20 |                96 |                 36 |                      0 |                 49 |                  43 |                   100    |


## Top 100 Candidates — Score Summary

| score                 |    min |   mean |    max |
|:----------------------|-------:|-------:|-------:|
| relevance_score       | 0.54   | 0.7537 | 0.975  |
| credibility_score     | 0.2673 | 0.5131 | 0.774  |
| negative_signal_score | 0      | 0.0004 | 0.02   |
| final_score           | 0.4371 | 0.589  | 0.8084 |

**consulting_only_flag=True in Top 100**: 0

**Candidates with evaluation_score > 0 in Top 100**: 77


## Scoring Formula Documentation

```

relevance_score  = 0.60 * retrieval_score/100

                 + 0.25 * evaluation_score/100   [+ 0.03-0.06 eval bonus]

                 + 0.15 * recommendation_score/100


credibility_score = 0.40 * production_score/100

                  + 0.35 * specificity_score/100

                  + 0.25 * evidence_support_score/100

                  [- 0.05 unsupported-claims penalty if evidence_support 0<x<50]


base_score = relevance * 0.65 + (relevance * credibility) * 0.35


penalty    = consulting_only          * 0.30  [if consulting_only_flag]

           + heavy_consulting         * 0.10  [if consulting_ratio > 0.60 and not only]

           + title_chaser             * 0.06  [if progression>75 + short>=2 + jobs>=4]

           + low_behavior             * 0.02  [if behavior_score < p25]

           [capped at 0.35]


final_score = (base_score - penalty).clip(0, 1)

```
