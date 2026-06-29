import pandas as pd
import json
import re

def get_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([str(s.get("name") or "") for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([str(j.get("description") or "") for j in c["career_history"]]))
    return " ".join(text).lower()

def main():
    df2 = pd.read_parquet('ranked_candidates_v2.parquet')
    df3 = pd.read_parquet('ranked_candidates_v3.parquet')
    
    top100_v2 = df2.sort_values('rank').head(100)
    top100_v3 = df3.sort_values('rank').head(100)
    
    set2 = set(top100_v2['candidate_id'])
    set3 = set(top100_v3['candidate_id'])
    
    entrants = set3 - set2
    removals = set2 - set3
    
    print(f"Entrants: {len(entrants)}")
    print(f"Removals: {len(removals)}")
    
    # Get scores for these candidates
    scores_v2 = top100_v2.set_index('candidate_id').to_dict('index')
    scores_v3 = top100_v3.set_index('candidate_id').to_dict('index')
    
    # fallback for removals in v3 and entrants in v2
    all_scores_v2 = df2.set_index('candidate_id').to_dict('index')
    all_scores_v3 = df3.set_index('candidate_id').to_dict('index')
    
    # Load raw text
    cand_text = {}
    with open('candidates.jsonl', 'r') as f:
        for line in f:
            c = json.loads(line)
            cid = c['candidate_id']
            if cid in entrants or cid in removals:
                cand_text[cid] = get_text(c)
                
    new_terms = [
        r'\belasticsearch\b', r'\bopensearch\b', r'\bfaiss\b', r'\bpinecone\b', 
        r'\bmilvus\b', r'\bqdrant\b', r'\bbm25\b', r'\blearning[- ]to[- ]rank\b', 
        r'\bltr\b', r'\bembeddings?\b', r'\brag\b', r'\bretrieval[\s-]?augmented\s+generation\b',
        r'\bvector\s+search\b'
    ]
    
    print("\n" + "="*50)
    print("NEW ENTRANTS (Moved into Top 100)")
    print("="*50)
    
    for cid in entrants:
        old_rank = all_scores_v2.get(cid, {}).get('rank', 'N/A')
        new_rank = scores_v3[cid]['rank']
        print(f"\nCandidate: {cid} | Rank: {old_rank} -> {new_rank}")
        txt = cand_text[cid]
        
        matches = []
        for term in new_terms:
            for m in re.finditer(term, txt):
                start = max(0, m.start() - 40)
                end = min(len(txt), m.end() + 40)
                matches.append(txt[start:end].replace('\n', ' '))
                
        # deduplicate matches by just showing first few
        matches = list(set(matches))
        print("Matches for new concepts:")
        for m in matches[:5]:
            print(f"  ... {m} ...")
            
    print("\n" + "="*50)
    print("REMOVALS (Fell out of Top 100)")
    print("="*50)
    
    for cid in removals:
        old_rank = scores_v2[cid]['rank']
        new_rank = all_scores_v3.get(cid, {}).get('rank', 'N/A')
        print(f"\nCandidate: {cid} | Rank: {old_rank} -> {new_rank}")

if __name__ == "__main__":
    main()
