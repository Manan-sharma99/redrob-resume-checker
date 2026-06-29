import json
import re

def main():
    fp_rank = 0
    fp_match = 0
    fp_rec = 0
    fn_es_not_search = 0
    
    with open('candidates.jsonl', 'r') as f:
        for i, line in enumerate(f):
            if i > 20000: break
            c = json.loads(line)
            jobs = c.get('career_history', [])
            text = " ".join([str(j.get('description', '')) for j in jobs])
            
            if re.search(r'\brank(?:ed|ing|s)?\b', text, re.I):
                if not re.search(r'search|retrieval|relevance|recommend', text, re.I):
                    # likely FP for ranking
                    fp_rank += 1
            if re.search(r'\bmatching\b', text, re.I):
                if not re.search(r'candidate|profile|resume', text, re.I):
                    fp_match += 1
            if re.search(r'\brecommend(?:ation|ed|ing|s)?\b', text, re.I):
                if re.search(r'management|client|team', text, re.I):
                    fp_rec += 1
            
            if re.search(r'\belasticsearch\b', text, re.I) and not re.search(r'\bsearch\b', text, re.I):
                fn_es_not_search += 1
                
    print(f"Potential FPs in first 20k:")
    print(f"Ranking FPs: {fp_rank}")
    print(f"Matching FPs: {fp_match}")
    print(f"Recommendation FPs: {fp_rec}")
    print(f"ES without search: {fn_es_not_search}")

if __name__ == '__main__':
    main()
