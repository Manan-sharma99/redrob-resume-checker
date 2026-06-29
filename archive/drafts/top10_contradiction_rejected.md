# Top 10 Contradiction-Rejected Candidates

> Sorted by combined relevance (`retrieval + evaluation + recommendation`) descending.  
> These are the highest-relevance candidates removed by Stage 1.

---

## Overview

| # | candidate_id | current_title | current_company | retrieval | eval | rec | combined | contra_score |
|---|-------------|---------------|-----------------|:---------:|:----:|:---:|:--------:|:------------:|
| 1 | CAND_0039754 | Senior Applied Scientist | Meta | 70 | 74 | 17 | 161 | 45.00 |
| 2 | CAND_0055992 | AI Engineer | CRED | 84 | 18 | 30 | 132 | 45.00 |
| 3 | CAND_0010770 | Recommendation Systems Engineer | Aganitha | 84 | 18 | 0 | 102 | 45.00 |
| 4 | CAND_0093331 | NLP Engineer | Genpact AI | 70 | 18 | 0 | 88 | 45.00 |
| 5 | CAND_0091534 | AI Engineer | Flipkart | 82 | 0 | 0 | 82 | 45.00 |
| 6 | CAND_0095619 | NLP Engineer | Nykaa | 44 | 0 | 0 | 44 | 45.00 |
| 7 | CAND_0013536 | Applied ML Engineer | Haptik | 18 | 20 | 0 | 38 | 45.00 |
| 8 | CAND_0019480 | NLP Engineer | Meesho | 16 | 22 | 0 | 38 | 37.88 |
| 9 | CAND_0090900 | Senior Data Engineer | PolicyBazaar | 0 | 36 | 0 | 36 | 50.00 |
| 10 | CAND_0071115 | Recommendation Systems Engineer | Meta | 4 | 20 | 0 | 24 | 45.00 |

---

## 1. CAND_0039754

| Field | Value |
|-------|-------|
| **current_title** | Senior Applied Scientist |
| **current_company** | Meta |
| **Claimed YoE** | 16.2 years |
| **Computed YoE** | 8.2 years |
| **YoE assessment** | ⚠ inflated by 8.0 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **70** |
| `recommendation_score` | **17** |
| `evaluation_score` | **74** |
| `combined_relevance` | **161** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 16.2 yrs vs computed 8.2 yrs (delta 8.0 yrs = 96 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | Senior Applied Scientist | Meta | 2023-05-13 | — | ✓ | 37m | Owned the end-to-end ranking pipeline at a recommendations-heavy consumer product: candidate sourcing → embedding generation (using a fine-tuned BGE-large) → Pinecone retrieval → learning-to-rank re-s |
| 2 | Senior ML Engineer — Search & Ranking | Apple | 2020-01-29 | 2023-05-13 |  | 40m | Owned the design and rollout of a large-scale semantic search system serving an internal corpus of 35M+ items. Migrated the existing BM25-only retrieval to a hybrid setup combining sparse and dense ve |
| 3 | Senior Applied Scientist | Observe.AI | 2018-05-09 | 2020-01-29 |  | 21m | Built a RAG-based ranking pipeline serving 50M+ queries per month for an internal recruiter-facing search product. The architecture combined BM25 + dense retrieval (BGE embeddings, FAISS HNSW) with an |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| IIT Hyderabad | M.Sc | Data Science | 2017 | 2020 |

---

## 2. CAND_0055992

| Field | Value |
|-------|-------|
| **current_title** | AI Engineer |
| **current_company** | CRED |
| **Claimed YoE** | 16.9 years |
| **Computed YoE** | 6.7 years |
| **YoE assessment** | ⚠ inflated by 10.2 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **84** |
| `recommendation_score` | **30** |
| `evaluation_score` | **18** |
| `combined_relevance` | **132** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 16.9 yrs vs computed 6.7 yrs (delta 10.2 yrs = 123 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | AI Engineer | CRED | 2025-02-01 | — | ✓ | 16m | Implemented a RAG-based customer support chatbot integrated with our existing ticketing system. Built the document ingestion pipeline (chunking, embedding via OpenAI embeddings, storing in Pinecone) a |
| 2 | Senior Data Scientist | Aganitha | 2023-10-26 | 2025-01-18 |  | 15m | Developed a semantic search feature for an internal knowledge base of ~500K documents. Used sentence-transformers (all-MiniLM-L6-v2 initially, later upgraded to bge-base) with FAISS for fast nearest-n |
| 3 | AI Engineer | Observe.AI | 2020-10-11 | 2023-10-26 |  | 37m | Built a content recommendation system serving 10M+ users that combined collaborative filtering with content-based ranking. The system uses item-item similarity (via sentence-transformer embeddings) fo |
| 4 | Machine Learning Engineer | Ola | 2019-10-17 | 2020-10-11 |  | 12m | Owned the ranking layer for an e-commerce search product, evolving it from a hand-tuned scoring function to a learning-to-rank model over 9 months. Designed the relevance labeling pipeline (mix of cli |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| NIT Surathkal | M.E. | Computer Engineering | 2010 | 2013 |
| Delhi College of Engineering | B.Tech | Information Technology | 2018 | 2021 |

---

## 3. CAND_0010770

| Field | Value |
|-------|-------|
| **current_title** | Recommendation Systems Engineer |
| **current_company** | Aganitha |
| **Claimed YoE** | 15.2 years |
| **Computed YoE** | 7.2 years |
| **YoE assessment** | ⚠ inflated by 8.0 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **84** |
| `recommendation_score` | **0** |
| `evaluation_score` | **18** |
| `combined_relevance` | **102** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 15.2 yrs vs computed 7.2 yrs (delta 8.0 yrs = 96 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | Recommendation Systems Engineer | Aganitha | 2022-06-17 | — | ✓ | 48m | Trained and shipped multiple ranking models for our product's discovery feed using XGBoost and LightGBM. Designed features across three families: content metadata, user behavior signals, and item enga |
| 2 | AI Engineer | Verloop.io | 2020-10-25 | 2022-06-17 |  | 20m | Developed a semantic search feature for an internal knowledge base of ~500K documents. Used sentence-transformers (all-MiniLM-L6-v2 initially, later upgraded to bge-base) with FAISS for fast nearest-n |
| 3 | Senior Data Scientist | Observe.AI | 2019-10-31 | 2020-10-25 |  | 12m | Owned the ranking layer for an e-commerce search product, evolving it from a hand-tuned scoring function to a learning-to-rank model over 9 months. Designed the relevance labeling pipeline (mix of cli |
| 4 | Applied ML Engineer | Locobuzz | 2019-04-04 | 2019-10-01 |  | 6m | Developed a semantic search feature for an internal knowledge base of ~500K documents. Used sentence-transformers (all-MiniLM-L6-v2 initially, later upgraded to bge-base) with FAISS for fast nearest-n |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| IIT Delhi | M.Tech | Data Science | 2007 | 2012 |

---

## 4. CAND_0093331

| Field | Value |
|-------|-------|
| **current_title** | NLP Engineer |
| **current_company** | Genpact AI |
| **Claimed YoE** | 16.1 years |
| **Computed YoE** | 7.2 years |
| **YoE assessment** | ⚠ inflated by 8.9 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **70** |
| `recommendation_score` | **0** |
| `evaluation_score` | **18** |
| `combined_relevance` | **88** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 16.1 yrs vs computed 7.2 yrs (delta 8.9 yrs = 107 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | NLP Engineer | Genpact AI | 2022-05-18 | — | ✓ | 49m | Built and operated production ML pipelines using MLflow for experiment tracking, Kubeflow for orchestration, and our internal feature store. My main project was a churn prediction model that's now use |
| 2 | NLP Engineer | InMobi | 2021-04-09 | 2022-05-04 |  | 13m | Developed a semantic search feature for an internal knowledge base of ~500K documents. Used sentence-transformers (all-MiniLM-L6-v2 initially, later upgraded to bge-base) with FAISS for fast nearest-n |
| 3 | Recommendation Systems Engineer | Observe.AI | 2019-04-06 | 2021-03-26 |  | 24m | Developed a semantic search feature for an internal knowledge base of ~500K documents. Used sentence-transformers (all-MiniLM-L6-v2 initially, later upgraded to bge-base) with FAISS for fast nearest-n |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| Christ University | Ph.D | Computer Engineering | 2009 | 2013 |
| Anna University | M.S. | Artificial Intelligence | 2014 | 2019 |

---

## 5. CAND_0091534

| Field | Value |
|-------|-------|
| **current_title** | AI Engineer |
| **current_company** | Flipkart |
| **Claimed YoE** | 16.6 years |
| **Computed YoE** | 7.1 years |
| **YoE assessment** | ⚠ inflated by 9.5 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **82** |
| `recommendation_score` | **0** |
| `evaluation_score` | **0** |
| `combined_relevance` | **82** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 16.6 yrs vs computed 7.1 yrs (delta 9.5 yrs = 114 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | AI Engineer | Flipkart | 2022-02-17 | — | ✓ | 52m | Owned the ranking layer for an e-commerce search product, evolving it from a hand-tuned scoring function to a learning-to-rank model over 9 months. Designed the relevance labeling pipeline (mix of cli |
| 2 | Machine Learning Engineer | Adobe | 2020-11-24 | 2021-12-19 |  | 13m | Developed a semantic search feature for an internal knowledge base of ~500K documents. Used sentence-transformers (all-MiniLM-L6-v2 initially, later upgraded to bge-base) with FAISS for fast nearest-n |
| 3 | NLP Engineer | Glance | 2019-03-05 | 2020-10-25 |  | 20m | Implemented a RAG-based customer support chatbot integrated with our existing ticketing system. Built the document ingestion pipeline (chunking, embedding via OpenAI embeddings, storing in Pinecone) a |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| IIT Delhi | M.Tech | Computer Engineering | 2014 | 2018 |

---

## 6. CAND_0095619

| Field | Value |
|-------|-------|
| **current_title** | NLP Engineer |
| **current_company** | Nykaa |
| **Claimed YoE** | 15.6 years |
| **Computed YoE** | 4.2 years |
| **YoE assessment** | ⚠ inflated by 11.4 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **44** |
| `recommendation_score` | **0** |
| `evaluation_score` | **0** |
| `combined_relevance` | **44** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 15.6 yrs vs computed 4.2 yrs (delta 11.4 yrs = 137 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | NLP Engineer | Nykaa | 2022-04-18 | — | ✓ | 50m | Owned the ranking layer for an e-commerce search product, evolving it from a hand-tuned scoring function to a learning-to-rank model over 9 months. Designed the relevance labeling pipeline (mix of cli |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| NIT Warangal | M.Sc | Machine Learning | 2017 | 2022 |

---

## 7. CAND_0013536

| Field | Value |
|-------|-------|
| **current_title** | Applied ML Engineer |
| **current_company** | Haptik |
| **Claimed YoE** | 14.1 years |
| **Computed YoE** | 4.7 years |
| **YoE assessment** | ⚠ inflated by 9.4 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **18** |
| `recommendation_score` | **0** |
| `evaluation_score` | **20** |
| `combined_relevance` | **38** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 14.1 yrs vs computed 4.7 yrs (delta 9.4 yrs = 113 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | Applied ML Engineer | Haptik | 2023-08-11 | — | ✓ | 34m | Trained and shipped multiple ranking models for our product's discovery feed using XGBoost and LightGBM. Designed features across three families: content metadata, user behavior signals, and item enga |
| 2 | Recommendation Systems Engineer | Rephrase.ai | 2021-10-13 | 2023-08-04 |  | 22m | Trained and shipped multiple ranking models for our product's discovery feed using XGBoost and LightGBM. Designed features across three families: content metadata, user behavior signals, and item enga |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| Chandigarh University | M.Tech | Artificial Intelligence | 2002 | 2007 |

---

## 8. CAND_0019480

| Field | Value |
|-------|-------|
| **current_title** | NLP Engineer |
| **current_company** | Meesho |
| **Claimed YoE** | 2.8 years |
| **Computed YoE** | 7.2 years |
| **YoE assessment** | ⚠ under-stated by 4.4 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **16** |
| `recommendation_score` | **0** |
| `evaluation_score` | **22** |
| `combined_relevance` | **38** |
| `contradiction_score` | **37.88** |

### Exact Rejection Reasons

- Experience mismatch: claimed 2.8 yrs vs computed 7.2 yrs (delta 4.4 yrs = 52 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | NLP Engineer | Meesho | 2024-11-03 | — | ✓ | 19m | Trained and shipped multiple ranking models for our product's discovery feed using XGBoost and LightGBM. Designed features across three families: content metadata, user behavior signals, and item enga |
| 2 | Senior Data Scientist | InMobi | 2022-09-15 | 2024-11-03 |  | 26m | Implemented a RAG-based customer support chatbot integrated with our existing ticketing system. Built the document ingestion pipeline (chunking, embedding via OpenAI embeddings, storing in Pinecone) a |
| 3 | Senior Data Scientist | Vedantu | 2020-04-28 | 2022-07-17 |  | 27m | Trained and shipped multiple ranking models for our product's discovery feed using XGBoost and LightGBM. Designed features across three families: content metadata, user behavior signals, and item enga |
| 4 | Search Engineer | Freshworks | 2019-02-03 | 2020-04-28 |  | 15m | Trained and shipped multiple ranking models for our product's discovery feed using XGBoost and LightGBM. Designed features across three families: content metadata, user behavior signals, and item enga |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| Thapar University | B.Tech | Machine Learning | 2004 | 2007 |

---

## 9. CAND_0090900

| Field | Value |
|-------|-------|
| **current_title** | Senior Data Engineer |
| **current_company** | PolicyBazaar |
| **Claimed YoE** | 11.7 years |
| **Computed YoE** | 3.2 years |
| **YoE assessment** | ⚠ inflated by 8.5 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **0** |
| `recommendation_score` | **0** |
| `evaluation_score` | **36** |
| `combined_relevance` | **36** |
| `contradiction_score` | **50.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 11.7 yrs vs computed 3.2 yrs (delta 8.5 yrs = 102 months)
- Duration mismatch on [Senior Data Engineer]: stated 9m vs computed 38m

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | Senior Data Engineer | PolicyBazaar | 2023-04-13 | — | ✓ | 9m | Mixed data science and analytics-engineering role at a marketing-analytics startup. Spent maybe 30% of my time on lightweight ML (clustering, classification, churn prediction in sklearn/XGBoost) and 7 |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| Local Engineering College | B.E. | MBA | 2015 | 2020 |
| Chandigarh University | M.Sc | Mathematics | 2013 | 2017 |

---

## 10. CAND_0071115

| Field | Value |
|-------|-------|
| **current_title** | Recommendation Systems Engineer |
| **current_company** | Meta |
| **Claimed YoE** | 16.5 years |
| **Computed YoE** | 5.8 years |
| **YoE assessment** | ⚠ inflated by 10.7 yrs |

| Score | Value |
|-------|------:|
| `retrieval_score` | **4** |
| `recommendation_score` | **0** |
| `evaluation_score` | **20** |
| `combined_relevance` | **24** |
| `contradiction_score` | **45.00** |

### Exact Rejection Reasons

- Experience mismatch: claimed 16.5 yrs vs computed 5.8 yrs (delta 10.8 yrs = 129 months)

### Career History

| # | title | company | start | end | is_current | stated duration | description (first 200 chars) |
|---|-------|---------|-------|-----|:----------:|:---------------:|-------------------------------|
| 1 | Recommendation Systems Engineer | Meta | 2022-09-15 | — | ✓ | 45m | Built and operated production ML pipelines using MLflow for experiment tracking, Kubeflow for orchestration, and our internal feature store. My main project was a churn prediction model that's now use |
| 2 | AI Engineer | Krutrim | 2020-09-25 | 2022-09-15 |  | 24m | Built and operated production ML pipelines using MLflow for experiment tracking, Kubeflow for orchestration, and our internal feature store. My main project was a churn prediction model that's now use |

### Education

| institution | degree | field | start | end |
|-------------|--------|-------|------:|----:|
| IIT Madras | B.Tech | Information Technology | 2003 | 2007 |

---

## Verdict

All 10 candidates share the same root contradiction: **severe YoE inflation**.
Every profile claims 10–15 years of experience while computed career timelines
span only 2–8 years — a gap that triggers a `contradiction_score` of 37–50.

> [!CAUTION]
> **3 candidate(s) with combined relevance ≥ 100** were rejected.
> These warrant manual review to confirm whether the YoE mismatch is synthetic
> fabrication or a genuine data entry error.

> [!WARNING]
> **1 candidate(s) have the lowest contradiction score (37.88)**.
> A threshold of 30.0 catches them. Raising the threshold to 40 would pass them
> back into the pool. Assess whether that trade-off is desirable.

**Pattern diagnosis**: The consistent signature across all 10 is a single-role career
with a `duration_months` value far below what the start–end dates compute to, combined
with a `years_of_experience` claim that matches the (false) stated duration rather than
the actual dates. This is the hallmark of a **synthetic profile generator that inflated
YoE claims without adjusting career dates consistently**.