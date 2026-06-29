# Feature Extraction Evidence Audit

## Objective
To quantitatively verify the feature extraction gaps identified in `FEATURE_EXTRACTION_AUDIT.md`.

## Methodology
The dataset of 100,000 candidates (`candidates.jsonl`) was fully scanned for exact occurrences of each target term within candidates' `skills`, `career_history`, and `profile`. These occurrences were cross-referenced with the extraction logic defined in `extract_candidate_features.py` to identify true False Negatives (instances where candidates mention a term but receive 0 credit for the corresponding feature).

---

## Issue Verification & Ranking

Issues are ranked by highest expected leaderboard impact based on quantitative evidence.

### 1. Embeddings
- **Mentions**: 5,155
- **Receiving Credit**: 0
- **False Negatives**: 5,155
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS`.
- **Severity**: Critical
- **Expected Ranking Impact**: Major

### 2. Pinecone
- **Mentions**: 5,107
- **Receiving Credit**: 0
- **False Negatives**: 5,107
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS` and `PRODUCTION_TECH`.
- **Severity**: Critical
- **Expected Ranking Impact**: Major

### 3. FAISS
- **Mentions**: 5,101
- **Receiving Credit**: 0
- **False Negatives**: 5,101
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS`.
- **Severity**: Critical
- **Expected Ranking Impact**: Major

### 4. RAG (Retrieval-Augmented Generation)
- **Mentions**: 5,043
- **Receiving Credit**: 0
- **False Negatives**: 5,043
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS`.
- **Severity**: Critical
- **Expected Ranking Impact**: Major

### 5. Learning-to-Rank (LTR)
- **Mentions**: 1,440
- **Receiving Credit**: 0
- **False Negatives**: 1,440
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS` and `EVALUATION_TERMS`.
- **Severity**: High
- **Expected Ranking Impact**: Significant

### 6. BM25
- **Mentions**: 1,432
- **Receiving Credit**: 0
- **False Negatives**: 1,432
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS`.
- **Severity**: High
- **Expected Ranking Impact**: Significant

### 7. Milvus
- **Mentions**: 1,384
- **Receiving Credit**: 0
- **False Negatives**: 1,384
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS`.
- **Severity**: High
- **Expected Ranking Impact**: Significant

### 8. Qdrant
- **Mentions**: 1,379
- **Receiving Credit**: 0
- **False Negatives**: 1,379
- **False Positives**: 0
- **Extraction Rule**: Missing entirely from `RETRIEVAL_TERMS`.
- **Severity**: High
- **Expected Ranking Impact**: Significant

### 9. Elasticsearch
- **Mentions**: 1,353
- **Receiving Credit**: 0 (for `retrieval_score`)
- **False Negatives**: 1,353
- **False Positives**: 0
- **Extraction Rule**: Mapped to `PRODUCTION_TECH` but excluded from `RETRIEVAL_TERMS`.
- **Severity**: High
- **Expected Ranking Impact**: Significant

### 10. OpenSearch
- **Mentions**: 1,286
- **Receiving Credit**: 0 (for `retrieval_score`)
- **False Negatives**: 1,286
- **False Positives**: 0
- **Extraction Rule**: Mapped to `PRODUCTION_TECH` but excluded from `RETRIEVAL_TERMS`.
- **Severity**: High
- **Expected Ranking Impact**: Significant

### 11. Recall
- **Mentions**: 11
- **Receiving Credit**: 0 (for `evaluation_score`)
- **False Negatives**: 11
- **False Positives**: 0
- **Extraction Rule**: Mapped to `SPECIFICITY_METRICS` but excluded from `EVALUATION_TERMS`.
- **Severity**: Low
- **Expected Ranking Impact**: Negligible

### 12. Terms Not Mentioned in Dataset
The following terms were entirely missing from the dataset (0 mentions). Even though they are missing from extraction logic, fixing them will have no immediate impact on this specific dataset:
- **Solr**: 0 mentions
- **Hybrid Retrieval**: 0 mentions
- **Precision**: 0 mentions
- **MAP**: 0 mentions

### 13. Features Extracted Correctly
The following features are currently functioning as expected without significant FNs:
- **Vector Search**: 5,065 mentions, 5,065 receiving credit.
- **NDCG**: 15 mentions, 15 receiving credit.
- **MRR**: 11 mentions, 11 receiving credit.

---

## Prioritized Implementation Roadmap

1. **Add Modern Retrieval Terms**: Map `RAG`, `Embeddings`, `Learning-to-Rank`, and `BM25` to `RETRIEVAL_TERMS` (addresses >13k false negative intersections).
2. **Add Vector Databases**: Map `FAISS`, `Pinecone`, `Milvus`, and `Qdrant` to `RETRIEVAL_TERMS` (addresses >12k false negative intersections).
3. **Correct Legacy Search Inconsistencies**: Add `Elasticsearch` and `OpenSearch` to `RETRIEVAL_TERMS` so they contribute to retrieval/search relevance, not just production tech (addresses >2.6k false negatives).
4. *(Low Priority)*: Add `Precision`, `Recall`, `Solr`, `Hybrid Retrieval`, `MAP` to their respective dictionaries for long-term robustness, despite minimal dataset impact.

---

## MANDATORY DOUBLE-CHECK SUMMARY

**1. What was originally believed?**  
The feature extraction omissions reported in `FEATURE_EXTRACTION_AUDIT.md` were severe but required quantitative verification to prove they actually existed in the dataset and suppressed scores.

**2. What was actually verified?**  
Verified that over 5,000 candidates mention "Embeddings", "Pinecone", "FAISS", and "RAG" while receiving zero credit for these retrieval skills. 

**3. Which assumptions turned out to be wrong?**  
The assumption that Elasticsearch and Solr are the primary search engines to optimize for was wrong; modern vector databases and RAG concepts dominate the false negatives in this dataset. Solr literally has zero mentions in the entire dataset.

**4. What code/files actually changed?**  
None.

**5. Did any ranking formula change?**  
NO

**6. Did any extracted feature change?**  
NO

**7. Did validation metrics improve?**  
N/A (This was an evidence-only quantitative audit).

**8. Is this conclusion supported by evidence or intuition?**  
Supported entirely by quantitative evidence gathered by parsing the raw `candidates.jsonl` dataset and cross-referencing extraction mappings.

**9. Remaining risks introduced.**  
None, as no code was modified.

**10. Should this be merged into production?**  
NO (There is no code to merge).

**11. Confidence**  
High
