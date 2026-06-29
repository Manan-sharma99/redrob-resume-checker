import json
import re
import pandas as pd
import extract_candidate_features as ecf

def get_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([str(s.get("name") or "") for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([str(j.get("description") or "") for j in c["career_history"]]))
    return " ".join(text).lower()

def main():
    terms = {
        "ANN": r"\bann\b|\bapproximate nearest neighbors?\b",
        "HNSW": r"\bhnsw\b|\bhierarchical navigable small world\b",
        "IVF": r"\bivf\b",
        "ScaNN": r"\bscann\b",
        "Lucene": r"\blucene\b",
        "Vespa": r"\bvespa\b",
        "Redis Vector": r"\bredis\s+vector\b|\bvector\s+redis\b",
        "Weaviate": r"\bweaviate\b",
        "ColBERT": r"\bcolbert(?:v2)?\b",
        "SPLADE": r"\bsplade\b",
        "Cross Encoder": r"\bcross[- ]encoder\b",
        "Dual Encoder": r"\bdual[- ]encoder\b",
        "Semantic Indexing": r"\bsemantic\s+indexing\b",
        "Candidate Retrieval": r"\bcandidate\s+retrieval\b",
        "Re-ranking": r"\bre[- ]?ranking\b",
        "Hard Negative Mining": r"\bhard\s+negative\s+mining\b",
        "LLM Ranker": r"\bllm\s+rank(?:er|ing)\b",
        "BM25": r"\bbm25\b" # control
    }
    
    # We will count how many times each term appears in candidates.jsonl
    # and if they do NOT match existing regexes, we consider them FNs.
    
    counts = {k: 0 for k in terms}
    fns = {k: 0 for k in terms}
    
    with open("candidates.jsonl", "r") as f:
        for line in f:
            c = json.loads(line)
            txt = get_text(c)
            
            # Check if this candidate gets ANY retrieval score natively
            has_retrieval = bool(ecf.ANY_RETRIEVAL_TERM.search(txt))
            
            for k, pattern in terms.items():
                if re.search(pattern, txt):
                    counts[k] += 1
                    if not has_retrieval:
                        fns[k] += 1
                        
    records = []
    for k in terms:
        # Check current extraction status
        # Re-ranking is already in ecf.RETRIEVAL_CONCEPTS as "reranking"
        # Weaviate is not natively in RETRIEVAL_TERMS (it's in some other things maybe?)
        # Let's see if the regex pattern intersects
        status = "Not Extracted"
        if k == "Re-ranking" or k == "BM25":
            status = "Extracted"
        
        expected_impact = "Medium"
        if counts[k] > 1000:
            expected_impact = "High"
        elif counts[k] < 50:
            expected_impact = "Low"
            
        records.append({
            "Term": k,
            "Mentions": counts[k],
            "Current Extraction Status": status,
            "Estimated False Negatives": fns[k],
            "Expected Ranking Impact": expected_impact
        })
        
    df = pd.DataFrame(records)
    df.to_csv("RECALL_AUDIT.csv", index=False)
    print("Wrote RECALL_AUDIT.csv")
    print(df)

if __name__ == "__main__":
    main()
