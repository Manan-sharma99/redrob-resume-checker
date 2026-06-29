import json
import re
from collections import defaultdict
import pandas as pd

def safe_str(val):
    return str(val) if val is not None else ""

def get_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([safe_str(s.get("name")) for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([safe_str(j.get("description")) for j in c["career_history"]]))
    return " ".join(text).lower()

def get_original_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([safe_str(s.get("name")) for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([safe_str(j.get("description")) for j in c["career_history"]]))
    return " ".join(text)

def main():
    stats = defaultdict(lambda: {"mentions": 0, "credit": 0, "fn": 0, "fp": 0})
    
    terms = {
        "BM25": re.compile(r"\bbm25\b", re.I),
        "Elasticsearch": re.compile(r"\belasticsearch\b", re.I),
        "OpenSearch": re.compile(r"\bopensearch\b", re.I),
        "Solr": re.compile(r"\bsolr\b", re.I),
        "FAISS": re.compile(r"\bfaiss\b", re.I),
        "Pinecone": re.compile(r"\bpinecone\b", re.I),
        "Milvus": re.compile(r"\bmilvus\b", re.I),
        "Qdrant": re.compile(r"\bqdrant\b", re.I),
        "Vector Search": re.compile(r"\bvector\s+search\b", re.I),
        "Embeddings": re.compile(r"\bembeddings?\b", re.I),
        "Hybrid Retrieval": re.compile(r"\bhybrid\s+(?:retrieval|search)\b", re.I),
        "Learning-to-Rank": re.compile(r"\b(?:learning[- ]to[- ]rank|ltr)\b", re.I),
        "RAG": re.compile(r"\b(?:rag|retrieval[- ]augmented\s+generation)\b", re.I),
        "Precision": re.compile(r"\bprecision\b", re.I),
        "Recall": re.compile(r"\brecall\b", re.I),
        "MAP": re.compile(r"\b(?:MAP(?:@\d+)?|mean\s+average\s+precision)\b"), # case sensitive for MAP
        "NDCG": re.compile(r"\bndcg(?:@\d+)?\b", re.I),
        "MRR": re.compile(r"\bmrr\b|\bmean\s+reciprocal\s+rank\b", re.I),
    }

    print("Scanning candidates...")
    with open("candidates.jsonl", "r") as f:
        for i, line in enumerate(f):
            c = json.loads(line)
            lower_text = get_text(c)
            orig_text = get_original_text(c)
            
            for term, pattern in terms.items():
                target_text = orig_text if term == "MAP" else lower_text
                
                matches = pattern.findall(target_text)
                if matches:
                    stats[term]["mentions"] += 1
                    
                    # Logic for credit:
                    if term in ["BM25", "Solr", "FAISS", "Pinecone", "Milvus", "Qdrant", "Embeddings", "Hybrid Retrieval", "Learning-to-Rank", "RAG"]:
                        # 0 credit currently for retrieval
                        stats[term]["fn"] += 1
                        
                    elif term in ["Elasticsearch", "OpenSearch"]:
                        # They get credit for PRODUCTION_TECH, but 0 for RETRIEVAL.
                        # Since we are auditing search/retrieval features, they get 0 credit.
                        stats[term]["fn"] += 1
                        
                    elif term == "Vector Search":
                        # Mapped exactly to RETRIEVAL_TERMS["vector_search"]
                        stats[term]["credit"] += 1
                        # FP if it's not actually vector search? Very rare.
                        # FN if they say vector db? (But vector db isn't Vector Search term).
                        pass
                        
                    elif term in ["Precision", "Recall"]:
                        # Mapped to SPECIFICITY_METRICS, 0 for EVALUATION.
                        stats[term]["fn"] += 1
                        
                    elif term == "MAP":
                        stats[term]["credit"] += 1
                        # check FPs. "MAP" could be "Data MAP" etc.
                        for m in matches:
                            if m == "MAP":
                                # likely FP if they just list MAP in skills, but let's assume a fraction are FPs.
                                # To be rigorous, if they mention 'MAP' but no other eval/ml terms, highly likely FP.
                                if not re.search(r"ml|machine learning|ndcg|mrr|evaluation", lower_text):
                                    stats[term]["fp"] += 1
                                    break
                                    
                    elif term in ["NDCG", "MRR"]:
                        stats[term]["credit"] += 1
                        # FPs negligible

    # Additional generic FP checks for "ranking", "recommendation", "matching" just to inform the report
    
    print("Results:")
    for t in terms:
        print(f"{t}: Mentions={stats[t]['mentions']}, Credit={stats[t]['credit']}, FN={stats[t]['fn']}, FP={stats[t]['fp']}")
        
if __name__ == "__main__":
    main()
