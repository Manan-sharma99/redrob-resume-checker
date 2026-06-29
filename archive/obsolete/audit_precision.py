import json
import re
import random

def get_text(c):
    text = []
    if c.get("skills"):
        text.append(" ".join([str(s.get("name") or "") for s in c["skills"]]))
    if c.get("career_history"):
        text.append(" ".join([str(j.get("description") or "") for j in c["career_history"]]))
    return " ".join(text).lower()

def main():
    rag_samples = []
    ltr_samples = []
    
    with open("candidates.jsonl", "r") as f:
        for line in f:
            c = json.loads(line)
            txt = get_text(c)
            
            if re.search(r'\brag\b', txt):
                rag_samples.append(txt)
            if re.search(r'\bltr\b', txt):
                ltr_samples.append(txt)
                
    random.seed(42)
    print("=== RAG SAMPLES ===")
    for txt in random.sample(rag_samples, min(10, len(rag_samples))):
        match = re.search(r'.{0,40}\brag\b.{0,40}', txt)
        if match: print("...", match.group(0), "...")
        
    print("\n=== LTR SAMPLES ===")
    for txt in random.sample(ltr_samples, min(10, len(ltr_samples))):
        match = re.search(r'.{0,40}\bltr\b.{0,40}', txt)
        if match: print("...", match.group(0), "...")

if __name__ == "__main__":
    main()
