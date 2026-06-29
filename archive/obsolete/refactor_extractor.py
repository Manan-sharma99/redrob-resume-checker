import re

def main():
    with open('extract_candidate_features.py', 'r') as f:
        content = f.read()
        
    # We want to replace everything between "PRODUCTION_ACTIONS = {" and "CONSULTING_COMPANIES = ("
    
    new_dicts = """
PRODUCTION_ACTIONS = {
    "built": _rx(r"\\bbuilt\\b", r"\\bbuild(?:ing|s)?\\b"),
    "designed": _rx(r"\\bdesign(?:ed|ing|s)?\\b"),
    "owned": _rx(r"\\bown(?:ed|ing|s)?\\b"),
    "led": _rx(r"\\bled\\b", r"\\blead(?:ing|s)?\\b"),
    "architected": _rx(r"\\barchitect(?:ed|ing|s)?\\b"),
    "deployed": _rx(r"\\bdeploy(?:ed|ing|s|ment)?\\b"),
    "operated": _rx(r"\\boperat(?:ed|ing|es|ion)\\b"),
    "maintained": _rx(r"\\bmaintain(?:ed|ing|s)?\\b"),
}

# --- CONCEPT REGISTRY ---
SEARCH_ENGINES = {
    "elasticsearch": _rx(r"\\belasticsearch\\b"),
    "opensearch": _rx(r"\\bopensearch\\b"),
}

VECTOR_DATABASES = {
    "faiss": _rx(r"\\bfaiss\\b"),
    "pinecone": _rx(r"\\bpinecone\\b"),
    "milvus": _rx(r"\\bmilvus\\b"),
    "qdrant": _rx(r"\\bqdrant\\b"),
}

RETRIEVAL_ALGORITHMS = {
    "bm25": _rx(r"\\bbm25\\b"),
}

RANKING_TECHNIQUES = {
    "learning_to_rank": _rx(r"\\blearning[- ]to[- ]rank\\b", r"\\bltr\\b"),
}

REPRESENTATION_TECHNIQUES = {
    "embeddings": _rx(r"\\bembeddings?\\b"),
}

RETRIEVAL_CONCEPTS = {
    "retrieval": _rx(r"\\binformation\\s+retrieval\\b", r"\\bretrieval\\b"),
    "search": _rx(r"\\bsearch\\b"),
    "ranking": _rx(r"\\brank(?:ing|ed|s)?\\b"),
    "reranking": _rx(r"\\bre[\\s-]?rank(?:ing|ed|s)?\\b"),
    "relevance": _rx(r"\\brelevance\\b"),
    "query_understanding": _rx(r"\\bquery\\s+understanding\\b"),
    "query_expansion": _rx(r"\\bquery\\s+expansion\\b"),
    "semantic_search": _rx(r"\\bsemantic\\s+search\\b"),
    "vector_search": _rx(r"\\bvector\\s+search\\b"),
    "rag": _rx(r"\\b(?:rag|retrieval[\\s-]?augmented\\s+generation)\\b"),
}

RECOMMENDATION_SYSTEMS = {
    "recommendation": _rx(r"\\brecommend(?:ation|ations|er|ers|ing)?\\b"),
    "recommendation_systems": _rx(r"\\brecommender\\s+systems?\\b", r"\\brecommendation\\s+systems?\\b"),
    "personalization": _rx(r"\\bpersonali[sz](?:ation|ed|ing)\\b"),
    "matching": _rx(r"\\bmatching\\b"),
    "candidate_matching": _rx(r"\\bcandidate\\s+matching\\b"),
    "feed_ranking": _rx(r"\\bfeed\\s+ranking\\b"),
    "marketplace": _rx(r"\\bmarketplace\\b"),
}
# --- END CONCEPT REGISTRY ---

PRODUCTION_TECH = {
    "kafka": _rx(r"\\bkafka\\b"),
    "spark": _rx(r"\\b(?:apache\\s+)?spark\\b"),
    "pyspark": _rx(r"\\bpyspark\\b"),
    "airflow": _rx(r"\\b(?:apache\\s+)?airflow\\b"),
    "flink": _rx(r"\\b(?:apache\\s+)?flink\\b"),
    "snowflake": _rx(r"\\bsnowflake\\b"),
    "databricks": _rx(r"\\bdatabricks\\b"),
    "redis": _rx(r"\\bredis\\b"),
    "postgres": _rx(r"\\bpostgres(?:ql)?\\b"),
    **SEARCH_ENGINES,
    **VECTOR_DATABASES,
}

PRODUCTION_SIGNALS = {
    "real_time": _rx(r"\\breal[\\s-]?time\\b"),
    "streaming": _rx(r"\\bstream(?:ing|s)?\\b"),
    "latency": _rx(r"\\blaten(?:cy|cies)\\b"),
    "throughput": _rx(r"\\bthroughput\\b"),
    "on_call": _rx(r"\\bon[\\s-]?call\\b"),
    "monitoring": _rx(r"\\bmonitor(?:ing|ed|s)?\\b"),
    "schema_drift": _rx(r"\\bschema\\s+drift\\b"),
    "incident": _rx(r"\\bincidents?\\b"),
    "scalability": _rx(r"\\bscalab(?:ility|le)\\b"),
}

ANY_PRODUCTION_ACTION = re.compile(
    "|".join(pattern.pattern for pattern in PRODUCTION_ACTIONS.values()),
    re.IGNORECASE,
)
ANY_PRODUCTION_TECH_OR_SIGNAL = re.compile(
    "|".join(
        pattern.pattern
        for pattern in (*PRODUCTION_TECH.values(), *PRODUCTION_SIGNALS.values())
    ),
    re.IGNORECASE,
)

RETRIEVAL_TERMS = {
    **SEARCH_ENGINES,
    **VECTOR_DATABASES,
    **RETRIEVAL_ALGORITHMS,
    **RANKING_TECHNIQUES,
    **REPRESENTATION_TECHNIQUES,
    **RETRIEVAL_CONCEPTS,
}

RECOMMENDATION_TERMS = {
    **RECOMMENDATION_SYSTEMS,
}

EVALUATION_TERMS = {
    "ndcg": _rx(r"\\bndcg(?:@\d+)?\\b"),
    "mrr": _rx(r"\\bmrr\\b", r"\\bmean\\s+reciprocal\\s+rank\\b"),
    "map": _rx_case(r"\\bMAP(?:@\d+)?\\b", r"(?i:\\bmean\\s+average\\s+precision\\b)"),
    "ab_testing": _rx(r"\\ba\\s*/\\s*b\\s+test(?:ing|s|ed)?\\b", r"\\bab\\s+test(?:ing|s|ed)?\\b"),
    "offline_evaluation": _rx(r"\\boffline\\s+evaluation\\b"),
    "online_evaluation": _rx(r"\\bonline\\s+evaluation\\b"),
    "experiment": _rx(r"\\bexperiment(?:ation|ing|s|ed)?\\b"),
}

SPECIFICITY_METRICS = {
    "latency": _rx(r"\\blatency\\b", r"\\b\d+(?:\\.\d+)?\\s*(?:ms|milliseconds?|seconds?|secs?)\\b"),
    "throughput": _rx(r"\\bthroughput\\b"),
    "scale": _rx(r"\\bscale\\b", r"\\bscal(?:ed|ing)\\b"),
    "volume": _rx(r"\\bvolume\\b"),
    "availability": _rx(r"\\bavailability\\b", r"\\buptime\\b"),
    "accuracy": _rx(r"\\baccuracy\\b"),
    "conversion": _rx(r"\\bconversion\\b"),
    "precision_recall": _rx(r"\\bprecision\\b", r"\\brecall\\b"),
}

QUANTITY_RE = _rx(
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:k|m|b|million|billion|thousand)\b",
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:kb|mb|gb|tb|pb)\b",
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:ms|milliseconds?|seconds?|secs?|minutes?|hours?)\b",
    r"(?<![\w.])\d+(?:\.\d+)?\s*%",
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:qps|rps|tps)\b",
    r"(?<![\w.])\d+(?:\.\d+)?(?:\s*x)\b",
    r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?=\s+(?:users?|requests?|events?|records?|rows?|"
    r"transactions?|systems?|services?|pipelines?|models?|nodes?|servers?|clients?|daily|monthly)\b)",
)

IMPROVEMENT_RE = _rx(
    r"\\b(?:reduc(?:ed|ing)|improv(?:ed|ing)|increas(?:ed|ing)|decreas(?:ed|ing)|"
    r"grew|cut|boost(?:ed|ing)|lower(?:ed|ing))\\b.{0,80}?\d",
    r"\\bfrom\\s+\d[^.;]{0,50}?\\bto\\s+\d",
)

ANY_RETRIEVAL_TERM = re.compile("|".join(pattern.pattern for pattern in RETRIEVAL_TERMS.values()), re.IGNORECASE)
ANY_RECOMMENDATION_TERM = re.compile("|".join(pattern.pattern for pattern in RECOMMENDATION_TERMS.values()), re.IGNORECASE)

MAJOR_CLAIMS = {
    "retrieval": ANY_RETRIEVAL_TERM,
    "recommendation": ANY_RECOMMENDATION_TERM,
    "ml": _rx(r"\\bml\\b", r"\\bmachine\\s+learning\\b", r"\\bdeep\\s+learning\\b"),
}

"""

    start_idx = content.find("PRODUCTION_ACTIONS = {")
    end_idx = content.find("CONSULTING_COMPANIES = (")
    
    if start_idx == -1 or end_idx == -1:
        print("ERROR: COULD NOT FIND INDICES")
        return
        
    new_content = content[:start_idx] + new_dicts.strip() + "\n\n" + content[end_idx:]
    
    with open('extract_candidate_features.py', 'w') as f:
        f.write(new_content)
        
    print("Successfully refactored extract_candidate_features.py")

if __name__ == "__main__":
    main()
