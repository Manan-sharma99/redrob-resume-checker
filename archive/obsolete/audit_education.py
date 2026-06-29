import json
import pandas as pd
import re
from collections import defaultdict

def get_degree_level(degree_str):
    if not degree_str:
        return 0
    d = str(degree_str).lower()
    
    # PhD
    if re.search(r'\b(phd|ph\.d|doctorate|d\.phil|doctor)\b', d):
        return 3
    
    # Masters
    if re.search(r'\b(master|m\.e|m\.tech|m\.sc|m\.a|mba|mca|m\.s|ms|pgdm|pg)\b', d):
        return 2
        
    # Bachelors
    if re.search(r'\b(bachelor|b\.e|b\.tech|b\.sc|b\.a|bba|bca|b\.s|bs|ug)\b', d):
        return 1
        
    return 0

def check_candidate(education_list):
    flags = []
    
    valid_degrees = []
    for ed in education_list:
        start = ed.get('start_year')
        end = ed.get('end_year')
        try:
            start = int(start) if start else None
        except:
            start = None
        try:
            end = int(end) if end else None
        except:
            end = None
            
        if start is not None and end is not None:
            if end < start:
                flags.append('end_before_start')
                
        level = get_degree_level(ed.get('degree'))
        if level > 0 and end is not None:
            valid_degrees.append({
                'level': level,
                'start': start,
                'end': end,
                'degree': ed.get('degree'),
                'inst': ed.get('institution')
            })
            
    # Check hierarchy
    for i in range(len(valid_degrees)):
        for j in range(i + 1, len(valid_degrees)):
            d1 = valid_degrees[i]
            d2 = valid_degrees[j]
            
            high = d1 if d1['level'] > d2['level'] else d2 if d2['level'] > d1['level'] else None
            low = d2 if d1['level'] > d2['level'] else d1 if d2['level'] > d1['level'] else None
            
            if high and low:
                if high['end'] < low['end']:
                    if high['level'] == 2 and low['level'] == 1:
                        flags.append("masters_before_bachelors")
                    elif high['level'] == 3 and low['level'] == 2:
                        flags.append("phd_before_masters")
                    elif high['level'] == 3 and low['level'] == 1:
                        flags.append("phd_before_bachelors")
                    else:
                        flags.append("hierarchy_violation")
                
                # Check impossible overlap
                # if high degree ends the SAME year as low degree, it could be integrated, so don't flag.
                # if high degree starts BEFORE low degree starts, but ends AFTER, could be dual degree.
                
    return list(set(flags))

def main():
    affected = {}
    
    print("Reading candidates.jsonl...")
    with open('candidates.jsonl', 'r') as f:
        for line in f:
            c = json.loads(line)
            cid = c['candidate_id']
            edu = c.get('education', [])
            flags = check_candidate(edu)
            if flags:
                affected[cid] = flags

    total_cands = sum(1 for _ in open('candidates.jsonl'))
    print(f"Total candidates: {total_cands}")
    print(f"Affected candidates: {len(affected)}")
    
    # Load rankings and features
    ranks = pd.read_parquet('ranked_candidates_v3.parquet')
    feats = pd.read_parquet('candidate_features.parquet')
    
    df = pd.merge(ranks, feats[['candidate_id', 'contradiction_score']], on='candidate_id', how='left')
    
    top100 = set(df.sort_values('rank').head(100)['candidate_id'])
    top1000 = set(df.sort_values('rank').head(1000)['candidate_id'])
    
    affected_in_top100 = 0
    affected_in_top1000 = 0
    affected_with_penalty = 0
    
    breakdown = defaultdict(int)
    
    for cid, flags in affected.items():
        if cid in top100:
            affected_in_top100 += 1
        if cid in top1000:
            affected_in_top1000 += 1
            
        c_score = df[df['candidate_id'] == cid]['contradiction_score'].values
        if len(c_score) > 0 and c_score[0] > 0:
            affected_with_penalty += 1
            
        for f in flags:
            breakdown[f] += 1
            
    print("--- Stats ---")
    print(f"Affected candidates: {len(affected)} ({len(affected)/total_cands*100:.2f}%)")
    print(f"Breakdown: {dict(breakdown)}")
    print(f"Affected candidates with existing contradiction penalty: {affected_with_penalty}")
    print(f"Affected in Top 100: {affected_in_top100}")
    print(f"Affected in Top 1000: {affected_in_top1000}")
    print(f"Candidates who would receive NEW penalty: {len(affected) - affected_with_penalty}")

if __name__ == "__main__":
    main()
