import json
import pandas as pd
import extract_candidate_features as ecf
import rank_candidates_v3 as rcv3

def main():
    syn_cands = [
        {
            "candidate_id": "SYN_001",
            "profile": {
                "current_title": "Elite Retrieval Engineer",
                "summary": "Built dense retrieval with faiss, pinecone. Re-ranking with learning-to-rank. Evaluated with NDCG and MAP. Scaled to 100M+ documents at 10ms latency."
            },
            "career_history": [],
            "skills": []
        },
        {
            "candidate_id": "SYN_002",
            "profile": {
                "current_title": "Elite Recommendation Engineer",
                "summary": "Designed candidate matching and feed ranking systems for marketplace. Used collaborative filtering, personalization, offline evaluation with NDCG."
            },
            "career_history": [],
            "skills": []
        },
        {
            "candidate_id": "SYN_003",
            "profile": {
                "current_title": "Generic LLM Engineer",
                "summary": "Prompt engineering, fine-tuning LLMs, langchain, hugging face transformers. Built chatbots."
            },
            "career_history": [],
            "skills": []
        },
        {
            "candidate_id": "SYN_004",
            "profile": {
                "current_title": "Keyword Stuffer",
                "summary": "search retrieval ranking faiss pinecone learning-to-rank ndcg map real-time streaming scale latency"
            },
            "career_history": [],
            "skills": []
        },
        {
            "candidate_id": "SYN_005",
            "profile": {
                "current_title": "Infrastructure Engineer",
                "summary": "Operated kafka, flink, postgres. High throughput, low latency systems. Kubernetes, docker."
            },
            "career_history": [],
            "skills": []
        },
        {
            "candidate_id": "SYN_006",
            "profile": {
                "current_title": "Research Scientist",
                "summary": "Published papers on embeddings and learning-to-rank algorithms. Evaluated offline on academic datasets."
            },
            "career_history": [],
            "skills": []
        },
        {
            "candidate_id": "SYN_007",
            "profile": {
                "current_title": "Consulting Architect",
                "summary": "Designed architecture for clients at TCS, Infosys, Wipro. Suggested elasticsearch."
            },
            "career_history": [],
            "skills": []
        }
    ]
    
    with open("synthetic.jsonl", "w") as f:
        for c in syn_cands:
            f.write(json.dumps(c) + "\n")
            
    # Extract features
    records = []
    for c in syn_cands:
        f = ecf.extract_features(c, as_of_date='2026-06-25')
        records.append(f)
        
    df_features = pd.DataFrame(records)
    
    # Run ranker
    df_features, _ = rcv3.apply_hard_reject(df_features)
    df_ranked = rcv3.compute_relevance_score(df_features)
    df_ranked = rcv3.compute_credibility_score(df_ranked)
    df_ranked = rcv3.compute_negative_signal_score(df_ranked)
    df_ranked = rcv3.compute_final_score(df_ranked)
    
    df_ranked = df_ranked.sort_values('final_score', ascending=False)
    df_ranked['synthetic_rank'] = range(1, len(df_ranked) + 1)
    
    # Merge titles
    title_map = {c['candidate_id']: c['profile']['current_title'] for c in syn_cands}
    df_ranked['profile_type'] = df_ranked['candidate_id'].map(title_map)
    
    df_ranked.to_csv("SYNTHETIC_STRESS_RESULTS.csv", index=False)
    print("Wrote SYNTHETIC_STRESS_RESULTS.csv")
    print(df_ranked[['profile_type', 'final_score', 'relevance_score', 'credibility_score', 'negative_signal_score']])

if __name__ == "__main__":
    main()
