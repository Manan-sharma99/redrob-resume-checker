import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([str(s.get("name") or "") for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([str(j.get("description") or "") for j in c["career_history"]]))
    return " ".join(text).lower()

def main():
    df = pd.read_parquet('ranked_candidates_v3.parquet')
    top100_ids = set(df.sort_values('rank').head(100)['candidate_id'])
    
    texts = []
    cids = []
    with open('candidates.jsonl', 'r') as f:
        for line in f:
            c = json.loads(line)
            if c['candidate_id'] in top100_ids:
                texts.append(get_text(c))
                cids.append(c['candidate_id'])
                
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(texts)
    sim = cosine_similarity(tfidf)
    
    # zero out lower triangle and diagonal
    sim[np.tril_indices_from(sim)] = 0
    
    print("=== DUPLICATE RE-VERIFICATION ===")
    pairs = np.where(sim > 0.85)
    for i, j in zip(*pairs):
        print(f"Similarity: {sim[i, j]:.4f} | {cids[i]} <-> {cids[j]}")
        
    print(f"Found {len(pairs[0])} duplicate pairs in the Top 100.")

if __name__ == "__main__":
    main()
