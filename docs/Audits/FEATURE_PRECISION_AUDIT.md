# Feature Precision & Context Audit

## Context Classification Summary
- **Mention only**: 4801 (83.8%)
- **Future interest**: 826 (14.4%)
- **Production experience**: 51 (0.9%)
- **Hands-on implementation**: 30 (0.5%)
- **Academic/project only**: 19 (0.3%)

## Production Evidence Co-occurrence
- **Embeddings + built**: 22 occurrences
- **Learning-to-Rank + designed**: 17 occurrences
- **RAG + built**: 14 occurrences
- **FAISS + designed**: 11 occurrences
- **Pinecone + built**: 11 occurrences
- **RAG + implemented**: 11 occurrences
- **BM25 + serving**: 5 occurrences
- **FAISS + architecture**: 3 occurrences
- **BM25 + architecture**: 3 occurrences
- **Embeddings + architecture**: 3 occurrences
- **RAG + serving**: 3 occurrences
- **Learning-to-Rank + latency**: 3 occurrences
- **Learning-to-Rank + offline evaluation**: 3 occurrences
- **Elasticsearch + built**: 2 occurrences
- **BM25 + built**: 2 occurrences
- **Elasticsearch + serving**: 1 occurrences
- **Elasticsearch + implemented**: 1 occurrences
- **BM25 + implemented**: 1 occurrences
- **Embeddings + online**: 1 occurrences
- **Elasticsearch + operated**: 1 occurrences

## False Positive & Synthetic Robustness Audit
- False Positives Detected (Mentions Only w/ High Hits): 759
- Estimated False Positive Rate: 3.79%
- Precision Estimate: 96.20%

## False Negative Audit
- False Negatives Detected (Prod Search Evidence but 0 Registry Hits): 0
- Estimated False Negative Rate: 0.00%
- Recall Estimate: 100.00%
