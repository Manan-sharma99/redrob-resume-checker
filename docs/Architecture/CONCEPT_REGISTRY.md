# Concept Registry

This registry tracks the canonical extraction patterns used across the feature engineering pipeline.

## 1. Search Engines
**Canonical Mapping**: `SEARCH_ENGINES`
- **elasticsearch**: `\belasticsearch\b`
- **opensearch**: `\bopensearch\b`
*(Contributes to: `retrieval_score`, `production_score`, `evidence_support_score`)*

## 2. Vector Databases
**Canonical Mapping**: `VECTOR_DATABASES`
- **faiss**: `\bfaiss\b`
- **pinecone**: `\bpinecone\b`
- **milvus**: `\bmilvus\b`
- **qdrant**: `\bqdrant\b`
*(Contributes to: `retrieval_score`, `production_score`, `evidence_support_score`)*

## 3. Retrieval Algorithms
**Canonical Mapping**: `RETRIEVAL_ALGORITHMS`
- **bm25**: `\bbm25\b`
*(Contributes to: `retrieval_score`, `evidence_support_score`)*

## 4. Ranking Techniques
**Canonical Mapping**: `RANKING_TECHNIQUES`
- **learning_to_rank**: `\blearning[- ]to[- ]rank\b`, `\bltr\b`
*(Contributes to: `retrieval_score`, `evidence_support_score`)*

## 5. Representation Techniques
**Canonical Mapping**: `REPRESENTATION_TECHNIQUES`
- **embeddings**: `\bembeddings?\b`
*(Contributes to: `retrieval_score`, `evidence_support_score`)*

## 6. Retrieval Concepts
**Canonical Mapping**: `RETRIEVAL_CONCEPTS`
- **retrieval**: `\binformation\s+retrieval\b`, `\bretrieval\b`
- **search**: `\bsearch\b`
- **rag**: `\b(?:rag|retrieval[\s-]?augmented\s+generation)\b`
- **vector_search**: `\bvector\s+search\b`
- *(...and standard baseline ranking/relevance terms)*
*(Contributes to: `retrieval_score`, `evidence_support_score`)*

## 7. Recommendation Systems
**Canonical Mapping**: `RECOMMENDATION_SYSTEMS`
- **recommendation**: `\brecommend(?:ation|ations|er|ers|ing)?\b`
- *(...and standard baseline matching/personalization terms)*
*(Contributes to: `recommendation_score`, `evidence_support_score`)*

## Note on Zero-Duplication
The extraction engine is now structured hierarchically. `PRODUCTION_TECH` dynamically imports `SEARCH_ENGINES` and `VECTOR_DATABASES`. `RETRIEVAL_TERMS` imports all retrieval-oriented blocks. `MAJOR_CLAIMS` now checks the unified `ANY_RETRIEVAL_TERM` regex, entirely eliminating hardcoded duplication across the codebase.
