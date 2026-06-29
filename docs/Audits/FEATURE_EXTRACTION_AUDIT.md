# Feature Extraction Audit Report

## Objective
To audit the feature extraction pipeline (`extract_candidate_features.py`) for correctness, completeness, and consistency, with a specific focus on modern Search, Retrieval, ML, and Recommendation Systems engineering signals. 

This is an evidence-only audit. No extraction logic, ranking formulas, or weights were modified.

---

## 1. Feature Coverage Overview (Extracted from Dataset)
- `production_score`: 99.99%
- `retrieval_score`: 30.05%
- `recommendation_score`: 5.42%
- `evaluation_score`: 2.06%
- `specificity_score`: 58.55%
- `evidence_support_score`: 2.42%
- `consulting_ratio`: 55.57%
- `consulting_only_flag`: 7.03%

---

## 2. Signal Analysis by Category

### A. Search & Retrieval Signals
**Where Extracted:** `RETRIEVAL_TERMS`  
**Current Logic:** `\binformation\s+retrieval\b`, `\bretrieval\b`, `\bsearch\b`, `\brank(?:ing|ed|s)?\b`, `\bre[\s-]?rank(?:ing|ed|s)?\b`, `\brelevance\b`, `\bquery\s+understanding\b`, `\bquery\s+expansion\b`, `\bsemantic\s+search\b`, `\bvector\s+search\b`.

**Audit Findings:**
- **Severe False Negatives (Missing Modern AI/Search Tech):** 
  - **BM25**, **Solr**, **Hybrid Retrieval**, **Learning-to-Rank** are entirely absent.
  - **RAG** (Retrieval-Augmented Generation) and **Embeddings** are entirely missing.
  - Vector Databases (**FAISS, Pinecone, Milvus, Qdrant**) are completely unmapped.
- **Inconsistent Classification:** **Elasticsearch** and **OpenSearch** are extracted as `PRODUCTION_TECH`, but they are **not** present in `RETRIEVAL_TERMS`. Thus, a candidate who built an Elasticsearch cluster gets points for production engineering but zero points for search/retrieval from that keyword.
- **False Positives:** The `\brank(?:ing|ed|s)?\b` regex easily matches phrases like "ranked 1st in my class" or "university ranking", giving the candidate retrieval points incorrectly.

### B. Recommendation & Matching Systems
**Where Extracted:** `RECOMMENDATION_TERMS`  
**Current Logic:** `\brecommend(?:ation|ations|er|ers|ing)?\b`, `\bmatching\b`, `\bcandidate\s+matching\b`, etc.

**Audit Findings:**
- **False Positives:** The exact word `matching` captures irrelevant usages like "pattern matching", "string matching", or "invoice matching". Similarly, `recommendation` captures "made recommendations to management" or "letter of recommendation".
- **Dependence on Exact Wording:** Requires exact keyword hits, missing broader graph-based or collaborative filtering techniques unless "recommendation" is explicitly stated.

### C. Evaluation Metrics
**Where Extracted:** `EVALUATION_TERMS`  
**Current Logic:** `ndcg`, `mrr`, `map`, `ab_testing`, `offline_evaluation`, `online_evaluation`, `experiment`.

**Audit Findings:**
- **Severe False Negatives:** **Precision**, **Recall**, **F1**, **AUC**, and **ROC** are entirely missing from `EVALUATION_TERMS`. 
- **Inconsistent Extraction:** Interestingly, `precision` and `recall` are mapped under `SPECIFICITY_METRICS`, meaning they contribute to a candidate's "specificity" score but they completely fail to contribute to the candidate's `evaluation_score`.
- **False Positives:** "Experiment" often matches basic scientific experiments (e.g., "chemistry experiment") rather than ML scale evaluations.

### D. Production Ownership & Scale Metrics
**Where Extracted:** `PRODUCTION_ACTIONS`, `PRODUCTION_TECH`, `SPECIFICITY_METRICS`, `QUANTITY_RE`  
**Current Logic:** Exact action verbs (`built`, `designed`, `owned`), some distributed tech, and regexes for quantities (e.g. `10k`, `50ms`).

**Audit Findings:**
- **Dependence on Exact Wording:** `PRODUCTION_ACTIONS` misses extremely common verbs like "created", "engineered", "developed", "programmed". 
- **Scale FPs:** `QUANTITY_RE` incorrectly rewards phrases like "100% attendance" or "2 hours" as scale/specificity. "Scaled" captures generic statements ("scaled the team").

### E. Duplicate and Contradictory Extraction Logic
- **Duplication:** `latency` and `throughput` exist in both `PRODUCTION_SIGNALS` and `SPECIFICITY_METRICS`.
- **Flawed Evidence Support Logic:** `MAJOR_CLAIMS` relies on exactly the same regexes as the base terms. `evidence_support_score` checks if the skill text contains a claim (e.g., `\bsearch\b`) and verifies if it exists in the job description. Because `Elasticsearch` is not listed under `MAJOR_CLAIMS["search"]`, a candidate who accurately lists "Elasticsearch" in their skills does not get recognized as making a "search" claim, artificially suppressing their evidence support score.

---

## MANDATORY DOUBLE-CHECK SUMMARY

**1. What was originally believed?**  
It was believed that the feature extraction pipeline robustly and comprehensively captured key signals for Search, Retrieval, ML, and Recommendation Systems engineering roles.

**2. What was actually verified?**  
Verified that severe gaps exist in modern retrieval technology mapping. Vector databases (FAISS, Pinecone, Milvus), modern techniques (RAG, Embeddings, Hybrid Retrieval, BM25, Learning-to-Rank) are completely missing. Core legacy search engines (Elasticsearch, Solr, OpenSearch) fail to contribute to the `retrieval_score`. Key ML evaluation metrics (Precision, Recall) do not contribute to the `evaluation_score`.

**3. Which assumptions turned out to be wrong?**  
The assumption that the hardcoded regex dictionaries adequately cover the domain was wrong. The assumption that `evidence_support_score` correctly maps skills to job descriptions was wrong (due to overly narrow regexes missing specific technologies like Elasticsearch).

**4. What code/files actually changed?**  
None.

**5. Did any ranking formula change?**  
NO

**6. Did any extracted feature change?**  
NO

**7. Did validation metrics improve?**  
N/A (This was an evidence-only audit; no changes were applied).

**8. Is this conclusion supported by evidence or intuition?**  
Supported entirely by evidence. The source code of `extract_candidate_features.py` was directly audited against the required domain terminology.

**9. Remaining risks introduced.**  
None, as the codebase remains untouched.

**10. Should this be merged into production?**  
NO (There is no code to merge. However, the findings heavily warrant a future refactor of the extraction dictionaries).

**11. Confidence**  
High
