# Stage 1 Rejection Diagnostics

> Generated from `candidate_features.parquet` + `candidates.jsonl`  

> As-of date: 2026-06-24  

> Hard-reject threshold: `contradiction_score >= 30.0`


---


## 1. Rejection Counts by Primary Reason

| Category | Count | % of pool |

|----------|------:|----------:|

| Total candidates | 100,000 | 100.00% |

| **Total hard rejected** | **5,600** | **5.60%** |

| → `contradiction_score >= 30` | 26 | 0.026% |

| → `consulting_only` + zero relevance | 5579 | 5.58% |

| → Both reasons | 5 | 0.005% |


---


## 2. Contradiction Sub-Reason Frequency

*Applies only to the 26 candidates rejected via `contradiction_score >= 30`.*

| Sub-reason | Candidates | % of contradiction-rejected |

|------------|:----------:|:---------------------------:|

| Experience mismatch (claimed YOE vs computed) | 26 | 100.0% |

| Future dates (start/end in future) | 0 | 0.0% |

| Impossible work timeline (end before start) | 0 | 0.0% |

| Impossible education timeline (end before start) | 0 | 0.0% |

| Multiple concurrent current jobs | 0 | 0.0% |

| Overlapping roles (>60-day overlap) | 0 | 0.0% |

| Missing dates (start or end absent) | 0 | 0.0% |

| Duration mismatch (stated vs computed > 4 months) | 16 | 61.5% |


---


## 3. Consulting-Only + Zero Relevance — Sub-breakdown

*These candidates were rejected because every role is at a consulting firm  

AND they have zero signal on retrieval, recommendation, and evaluation.*


| Metric | Value |
|--------|-------|

| Count | 5,574 |

| Mean `consulting_ratio` | 1.000 |

| Mean `total_months_experience` | 38.8 months |

| Mean `average_tenure_months` | 28.0 |

| Mean `behavior_score` | 45.8 |

| Retrieval > 0 in this group | 0 (by definition) |


---


## 4. Top 50 Rejected Candidates by Relevance Signal

*Sorted by combined relevance `retrieval_score + evaluation_score + recommendation_score` descending.*  

*This is the key table for identifying incorrect rejections.*


| # | candidate_id | current_title | current_company | primary_reason | retrieval | eval | rec | contra_score | consult_ratio |

|---|-------------|---------------|-----------------|----------------|:---------:|:----:|:---:|:------------:|:-------------:|

| 1 | CAND_0039754 | Senior Applied Scientist | Meta | contradiction_score >= 30 | 70 | 74 | 17 | 45.0 | 0.00 |

| 2 | CAND_0055992 | AI Engineer | CRED | contradiction_score >= 30 | 84 | 18 | 30 | 45.0 | 0.00 |

| 3 | CAND_0010770 | Recommendation Systems Engineer | Aganitha | contradiction_score >= 30 | 84 | 18 | 0 | 45.0 | 0.00 |

| 4 | CAND_0093331 | NLP Engineer | Genpact AI | contradiction_score >= 30 | 70 | 18 | 0 | 45.0 | 0.00 |

| 5 | CAND_0091534 | AI Engineer | Flipkart | contradiction_score >= 30 | 82 | 0 | 0 | 45.0 | 0.00 |

| 6 | CAND_0095619 | NLP Engineer | Nykaa | contradiction_score >= 30 | 44 | 0 | 0 | 45.0 | 0.00 |

| 7 | CAND_0013536 | Applied ML Engineer | Haptik | contradiction_score >= 30 | 18 | 20 | 0 | 45.0 | 0.00 |

| 8 | CAND_0019480 | NLP Engineer | Meesho | contradiction_score >= 30 | 16 | 22 | 0 | 37.9 | 0.00 |

| 9 | CAND_0090900 | Senior Data Engineer | PolicyBazaar | contradiction_score >= 30 | 0 | 36 | 0 | 50.0 | 0.00 |

| 10 | CAND_0071115 | Recommendation Systems Engineer | Meta | contradiction_score >= 30 | 4 | 20 | 0 | 45.0 | 0.00 |

| 11 | CAND_0066405 | Cloud Engineer | Initech | contradiction_score >= 30 | 2 | 0 | 0 | 50.0 | 0.00 |

| 12 | CAND_0000003 | Customer Support | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 13 | CAND_0000008 | Operations Manager | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 14 | CAND_0000028 | Operations Manager | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 15 | CAND_0000047 | Project Manager | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 16 | CAND_0000056 | Frontend Engineer | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 17 | CAND_0000059 | Frontend Engineer | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 18 | CAND_0000086 | Mechanical Engineer | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 19 | CAND_0000098 | Business Analyst | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 20 | CAND_0000164 | Content Writer | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 21 | CAND_0000174 | Marketing Manager | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 22 | CAND_0000175 | Project Manager | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 23 | CAND_0000234 | Frontend Engineer | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 24 | CAND_0000250 | Full Stack Developer | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 25 | CAND_0000257 | Full Stack Developer | Cognizant | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 26 | CAND_0000265 | HR Manager | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 27 | CAND_0000281 | Content Writer | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 28 | CAND_0000283 | Project Manager | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 29 | CAND_0000315 | DevOps Engineer | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 30 | CAND_0000326 | Full Stack Developer | Capgemini | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 31 | CAND_0000329 | Sales Executive | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 32 | CAND_0000335 | Mechanical Engineer | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 33 | CAND_0000362 | Project Manager | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 34 | CAND_0000369 | Business Analyst | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 35 | CAND_0000379 | Customer Support | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 36 | CAND_0000380 | Sales Executive | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 37 | CAND_0000407 | Mechanical Engineer | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 38 | CAND_0000416 | Customer Support | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 39 | CAND_0000427 | DevOps Engineer | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 40 | CAND_0000438 | Business Analyst | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 41 | CAND_0000463 | Accountant | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 42 | CAND_0000469 | Frontend Engineer | Accenture | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 43 | CAND_0000502 | HR Manager | Wipro | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 44 | CAND_0000531 | Customer Support | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 45 | CAND_0000546 | Marketing Manager | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 46 | CAND_0000567 | Operations Manager | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 47 | CAND_0000741 | Full Stack Developer | Capgemini | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 48 | CAND_0000758 | Customer Support | TCS | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 49 | CAND_0000763 | Customer Support | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |

| 50 | CAND_0000778 | Marketing Manager | Infosys | consulting_only + zero_relevance | 0 | 0 | 0 | 0.0 | 1.00 |


---


## 5. Detailed Contradiction Analysis — All 26 Rejected Candidates

*Full sub-reason breakdown for every candidate rejected via `contradiction_score >= 30`.*


### 1. CAND_0096150

- **Title**: Accountant

- **Company**: Wipro

- **YoE claimed**: 14.7

- **Rejection reason**: contradiction + consulting_zero_relevance

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 14.7 yrs vs computed 2.2 yrs (Δ 12.5 yrs, penalty 45.0pts)

  - Duration mismatch on 'Accountant': stated 10m vs computed 26m


### 2. CAND_0090900

- **Title**: Senior Data Engineer

- **Company**: PolicyBazaar

- **YoE claimed**: 11.7

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 36.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 11.7 yrs vs computed 3.2 yrs (Δ 8.5 yrs, penalty 45.0pts)

  - Duration mismatch on 'Senior Data Engineer': stated 9m vs computed 38m


### 3. CAND_0066405

- **Title**: Cloud Engineer

- **Company**: Initech

- **YoE claimed**: 12.3

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 2.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.3 yrs vs computed 2.6 yrs (Δ 9.7 yrs, penalty 45.0pts)

  - Duration mismatch on 'Cloud Engineer': stated 13m vs computed 31m


### 4. CAND_0025579

- **Title**: HR Manager

- **Company**: Acme Corp

- **YoE claimed**: 12.9

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.9 yrs vs computed 2.2 yrs (Δ 10.7 yrs, penalty 45.0pts)

  - Duration mismatch on 'HR Manager': stated 12m vs computed 27m


### 5. CAND_0036299

- **Title**: Mobile Developer

- **Company**: Cognizant

- **YoE claimed**: 12.2

- **Rejection reason**: contradiction + consulting_zero_relevance

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.2 yrs vs computed 3.7 yrs (Δ 8.5 yrs, penalty 45.0pts)

  - Duration mismatch on 'Mobile Developer': stated 8m vs computed 44m


### 6. CAND_0024752

- **Title**: Civil Engineer

- **Company**: Hooli

- **YoE claimed**: 14.9

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 14.9 yrs vs computed 4.0 yrs (Δ 10.9 yrs, penalty 45.0pts)

  - Duration mismatch on 'Civil Engineer': stated 8m vs computed 48m


### 7. CAND_0033131

- **Title**: Operations Manager

- **Company**: Pied Piper

- **YoE claimed**: 12.7

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.7 yrs vs computed 2.8 yrs (Δ 9.9 yrs, penalty 45.0pts)

  - Duration mismatch on 'Operations Manager': stated 16m vs computed 33m


### 8. CAND_0007413

- **Title**: Business Analyst

- **Company**: Globex Inc

- **YoE claimed**: 13.3

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 13.3 yrs vs computed 3.6 yrs (Δ 9.7 yrs, penalty 45.0pts)

  - Duration mismatch on 'Business Analyst': stated 16m vs computed 43m


### 9. CAND_0003430

- **Title**: Business Analyst

- **Company**: Infosys

- **YoE claimed**: 13.7

- **Rejection reason**: contradiction + consulting_zero_relevance

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 13.7 yrs vs computed 1.3 yrs (Δ 12.4 yrs, penalty 45.0pts)

  - Duration mismatch on 'Business Analyst': stated 11m vs computed 16m


### 10. CAND_0005291

- **Title**: Business Analyst

- **Company**: Hooli

- **YoE claimed**: 12.8

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.8 yrs vs computed 2.8 yrs (Δ 10.1 yrs, penalty 45.0pts)

  - Duration mismatch on 'Business Analyst': stated 11m vs computed 33m


### 11. CAND_0074119

- **Title**: Content Writer

- **Company**: Globex Inc

- **YoE claimed**: 11.4

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 11.4 yrs vs computed 2.2 yrs (Δ 9.2 yrs, penalty 45.0pts)

  - Duration mismatch on 'Content Writer': stated 13m vs computed 26m


### 12. CAND_0086808

- **Title**: Graphic Designer

- **Company**: TCS

- **YoE claimed**: 11.4

- **Rejection reason**: contradiction + consulting_zero_relevance

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 11.4 yrs vs computed 1.7 yrs (Δ 9.7 yrs, penalty 45.0pts)

  - Duration mismatch on 'Graphic Designer': stated 15m vs computed 20m


### 13. CAND_0065787

- **Title**: Java Developer

- **Company**: HCL

- **YoE claimed**: 10.9

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 10.9 yrs vs computed 2.7 yrs (Δ 8.2 yrs, penalty 45.0pts)

  - Duration mismatch on 'Java Developer': stated 14m vs computed 32m


### 14. CAND_0077250

- **Title**: Project Manager

- **Company**: Wayne Enterprises

- **YoE claimed**: 13.1

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 13.1 yrs vs computed 2.7 yrs (Δ 10.4 yrs, penalty 45.0pts)

  - Duration mismatch on 'Project Manager': stated 18m vs computed 32m


### 15. CAND_0091068

- **Title**: HR Manager

- **Company**: TCS

- **YoE claimed**: 12.7

- **Rejection reason**: contradiction + consulting_zero_relevance

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.7 yrs vs computed 2.3 yrs (Δ 10.4 yrs, penalty 45.0pts)

  - Duration mismatch on 'HR Manager': stated 12m vs computed 28m


### 16. CAND_0038431

- **Title**: Mobile Developer

- **Company**: Razorpay

- **YoE claimed**: 15.0

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 50.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 15.0 yrs vs computed 3.7 yrs (Δ 11.3 yrs, penalty 45.0pts)

  - Duration mismatch on 'Mobile Developer': stated 16m vs computed 44m


### 17. CAND_0093331

- **Title**: NLP Engineer

- **Company**: Genpact AI

- **YoE claimed**: 16.1

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 70.0

- **evaluation_score**: 18.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 16.1 yrs vs computed 7.2 yrs (Δ 8.9 yrs, penalty 45.0pts)


### 18. CAND_0039754

- **Title**: Senior Applied Scientist

- **Company**: Meta

- **YoE claimed**: 16.2

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 70.0

- **evaluation_score**: 74.0

- **recommendation_score**: 17.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 16.2 yrs vs computed 8.2 yrs (Δ 8.0 yrs, penalty 45.0pts)


### 19. CAND_0091534

- **Title**: AI Engineer

- **Company**: Flipkart

- **YoE claimed**: 16.6

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 82.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 16.6 yrs vs computed 7.1 yrs (Δ 9.5 yrs, penalty 45.0pts)


### 20. CAND_0052478

- **Title**: Marketing Manager

- **Company**: Dunder Mifflin

- **YoE claimed**: 12.4

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 0.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 12.4 yrs vs computed 1.4 yrs (Δ 11.0 yrs, penalty 45.0pts)


### 21. CAND_0055992

- **Title**: AI Engineer

- **Company**: CRED

- **YoE claimed**: 16.9

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 84.0

- **evaluation_score**: 18.0

- **recommendation_score**: 30.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 16.9 yrs vs computed 6.7 yrs (Δ 10.2 yrs, penalty 45.0pts)


### 22. CAND_0095619

- **Title**: NLP Engineer

- **Company**: Nykaa

- **YoE claimed**: 15.6

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 44.0

- **evaluation_score**: 0.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 15.6 yrs vs computed 4.2 yrs (Δ 11.4 yrs, penalty 45.0pts)


### 23. CAND_0071115

- **Title**: Recommendation Systems Engineer

- **Company**: Meta

- **YoE claimed**: 16.5

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 4.0

- **evaluation_score**: 20.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 16.5 yrs vs computed 5.8 yrs (Δ 10.8 yrs, penalty 45.0pts)


### 24. CAND_0010770

- **Title**: Recommendation Systems Engineer

- **Company**: Aganitha

- **YoE claimed**: 15.2

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 84.0

- **evaluation_score**: 18.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 15.2 yrs vs computed 7.2 yrs (Δ 8.0 yrs, penalty 45.0pts)


### 25. CAND_0013536

- **Title**: Applied ML Engineer

- **Company**: Haptik

- **YoE claimed**: 14.1

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 45.00

- **retrieval_score**: 18.0

- **evaluation_score**: 20.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 14.1 yrs vs computed 4.7 yrs (Δ 9.4 yrs, penalty 45.0pts)


### 26. CAND_0019480

- **Title**: NLP Engineer

- **Company**: Meesho

- **YoE claimed**: 2.8

- **Rejection reason**: contradiction_score >= 30

- **contradiction_score**: 37.88

- **retrieval_score**: 16.0

- **evaluation_score**: 22.0

- **recommendation_score**: 0.0

- **Detected sub-reasons**:

  - Experience mismatch: claimed 2.8 yrs vs computed 7.2 yrs (Δ 4.4 yrs, penalty 37.9pts)


---


## 6. Incorrect Rejection Risk Assessment

| Metric | Value |
|--------|-------|

| Rejected candidates with any retrieval signal | 10 |

| Rejected candidates with any evaluation signal | 8 |

| Rejected candidates with any recommendation signal | 2 |

| Rejected candidates with combined relevance >= 30 | 9 |

| Rejected candidates with combined relevance >= 50 | 5 |

| Rejected candidates with combined relevance >= 100 | 3 |



> [!CAUTION]

> **3 candidate(s) with combined relevance ≥ 100 were rejected.**  

> These are the highest-risk incorrect rejections. Review Section 5 for details.


**Consulting-zero rejections**: All 5,574 pure consulting-zero rejections have  

`retrieval_score = 0`, `recommendation_score = 0`, `evaluation_score = 0`.  

These are definitionally irrelevant to the JD and present zero incorrect-rejection risk.


---


## 7. Contradiction Score Distribution (Rejected Candidates Only)

| Score | Count |
|-------|-------|

| 37.88 | 1 |

| 45.00 | 9 |

| 50.00 | 16 |


---


## 8. Summary Verdict

- **5,600 candidates** were removed by Stage 1.

- **5,579** (99.6%) were consulting-only with zero domain signal — these are definitionally irrelevant and correctly rejected.

- **26** were rejected for severe timeline contradictions (`contradiction_score >= 30.0`).

- Of those, **10** had any retrieval signal > 0.

- The **highest-retrieval rejected candidate** is `CAND_0010770` (retrieval=84, eval=18, rec=0, title='Recommendation Systems Engineer').

  Their `contradiction_score` is **45.00** — see Section 5 for the specific violations.


**Bottom line**: The contradiction threshold of 30.0 is calibrated to catch only the most severe violations.  

The 26 contradiction-rejected candidates all have scores of 37.88 or higher,  

indicating genuinely broken profiles (not edge cases). The few with retrieval signal  

should be reviewed manually before any threshold adjustment.
