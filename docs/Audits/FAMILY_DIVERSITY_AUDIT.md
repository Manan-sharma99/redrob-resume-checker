# Family Diversity & Saturation Audit

Do candidates get higher scores for listing many concepts in the *same* family, or *diverse* families?

|   concept_count |   family_count |   retrieval_score |
|----------------:|---------------:|------------------:|
|               0 |              0 |           0       |
|               1 |              1 |           2       |
|               2 |              1 |          23.0428  |
|               2 |              2 |           4.00584 |
|               3 |              1 |           7.47423 |
|               3 |              2 |           7.19865 |
|               3 |              3 |           6.06122 |
|               4 |              1 |          13.9817  |
|               4 |              2 |          11.1948  |
|               4 |              3 |          10.8094  |
|               4 |              4 |           8.47826 |
|               5 |              1 |          22.1     |
|               5 |              2 |          15.4272  |
|               5 |              3 |          13.4426  |
|               5 |              4 |          24.0476  |
|               5 |              5 |          20.5     |
|               6 |              1 |          34.2667  |
|               6 |              2 |          19.7138  |
|               6 |              3 |          15.0879  |
|               6 |              4 |          21.125   |
|               6 |              5 |          26.5714  |
|               7 |              2 |          25.1133  |
|               7 |              3 |          18.5505  |
|               7 |              4 |          30.8182  |
|               7 |              5 |          39.2     |
|               8 |              2 |          34.5714  |
|               8 |              3 |          24.5238  |
|               8 |              4 |          49.25    |
|               8 |              5 |          51       |
|               9 |              3 |          34.7706  |
|               9 |              4 |          47.75    |
|               9 |              5 |          67.3333  |
|               9 |              6 |          87.3333  |
|              10 |              3 |          43.3333  |
|              10 |              4 |          72       |
|              10 |              5 |          90       |
|              10 |              6 |          79.3333  |
|              11 |              4 |          62       |
|              11 |              5 |          91.2381  |
|              11 |              6 |          97       |
|              12 |              5 |          98.2857  |
|              12 |              6 |          97.75    |
|              13 |              4 |         100       |
|              13 |              5 |          97       |
|              13 |              6 |          99.25    |
|              14 |              5 |         100       |
|              14 |              6 |          98.8     |
|              15 |              5 |         100       |
|              15 |              6 |         100       |
|              16 |              6 |         100       |

**Observation**: The current `domain_score` simply adds up the logarithmic weights of unique regex matches. Therefore, candidates *do* receive score inflation simply by packing multiple tools from the same family (e.g. FAISS, Pinecone, Milvus).
