import re

with open('extract_candidate_features.py', 'r') as f:
    content = f.read()

new_registry_code = """
from dataclasses import dataclass, field
import hashlib

@dataclass
class Alias:
    canonical_concept: str
    pattern: re.Pattern[str]
    requires_context: bool = False
    validation_statistics: dict = field(default_factory=dict)

@dataclass
class Concept:
    canonical_name: str
    aliases: list[Alias]
    family: str
    category: str
    confidence: str
    requires_context: bool = False
    rejection_reason: str = None

# --- CONCEPT REGISTRY ---
REGISTRY_VERSION = "1.0.0"

CONCEPT_REGISTRY = [
    # Search Engines
    Concept("elasticsearch", [
        Alias("elasticsearch", _rx(r"\\belasticsearch\\b", r"\\belastic\\s+search\\b"))
    ], "search_engine", "search_infrastructure", "verified"),
    Concept("opensearch", [Alias("opensearch", _rx(r"\\bopensearch\\b"))], "search_engine", "search_infrastructure", "verified"),
    Concept("solr", [Alias("solr", _rx(r"\\bsolr\\b"))], "search_engine", "search_infrastructure", "verified"),
    Concept("lucene", [Alias("lucene", _rx(r"\\blucene\\b")), Alias("lucene", _rx(r"\\bapache\\s+lucene\\b"))], "search_engine", "search_infrastructure", "pending", rejection_reason="zero dataset evidence"),
    Concept("vespa", [Alias("vespa", _rx(r"\\bvespa\\b"))], "search_engine", "search_infrastructure", "pending", rejection_reason="zero dataset evidence"),
    
    # Vector Databases
    Concept("faiss", [Alias("faiss", _rx(r"\\bfaiss\\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("pinecone", [Alias("pinecone", _rx(r"\\bpinecone\\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("milvus", [Alias("milvus", _rx(r"\\bmilvus\\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("qdrant", [Alias("qdrant", _rx(r"\\bqdrant\\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("weaviate", [Alias("weaviate", _rx(r"\\bweaviate\\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("redis_vector", [Alias("redis_vector", _rx(r"\\bredis\\s+vector(?:\\s+search)?\\b", r"\\bvector\\s+redis\\b", r"\\bredisearch\\b", r"\\bredis\\s+search\\b"))], "vector_database", "search_infrastructure", "alias"),
    
    # Retrieval Algorithms
    Concept("bm25", [Alias("bm25", _rx(r"\\bbm25\\b"))], "retrieval_algorithm", "search_logic", "verified"),
    Concept("hnsw", [Alias("hnsw", _rx(r"\\bhnsw\\b", r"\\bhierarchical\\s+navigable\\s+small\\s+world\\b"))], "retrieval_algorithm", "search_logic", "verified"),
    Concept("ann", [Alias("ann", _rx(r"\\bann\\b", r"\\bapproximate\\s+nearest\\s+neighbou?rs?\\b"))], "retrieval_algorithm", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("ivf", [Alias("ivf", _rx(r"\\bivf\\b"))], "retrieval_algorithm", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("scann", [Alias("scann", _rx(r"\\bscann\\b"))], "retrieval_algorithm", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Ranking Techniques
    Concept("learning_to_rank", [Alias("learning_to_rank", _rx(r"\\blearning[- ]to[- ]rank\\b", r"\\bltr\\b"))], "ranking_technique", "search_logic", "verified"),
    Concept("cross_encoder", [Alias("cross_encoder", _rx(r"\\bcross[- ]encoder\\b", r"\\bcrossencoder\\b"))], "ranking_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("llm_ranker", [Alias("llm_ranker", _rx(r"\\bllm\\s+rank(?:er|ing)?\\b"))], "ranking_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("hard_negative_mining", [Alias("hard_negative_mining", _rx(r"\\bhard\\s+negative\\s+mining\\b"))], "ranking_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Representation Techniques
    Concept("embeddings", [Alias("embeddings", _rx(r"\\bembeddings?\\b"))], "representation_technique", "search_logic", "verified"),
    Concept("colbert", [Alias("colbert", _rx(r"\\bcolbert(?:v2)?\\b"))], "representation_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("splade", [Alias("splade", _rx(r"\\bsplade\\b"))], "representation_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("dual_encoder", [Alias("dual_encoder", _rx(r"\\bdual[- ]encoder\\b"))], "representation_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Retrieval Concepts
    Concept("retrieval", [Alias("retrieval", _rx(r"\\binformation\\s+retrieval\\b", r"\\bretrieval\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("search", [Alias("search", _rx(r"\\bsearch\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("ranking", [Alias("ranking", _rx(r"\\brank(?:ing|ed|s)?\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("reranking", [Alias("reranking", _rx(r"\\bre[\\s-]?rank(?:ing|ed|s)?\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("relevance", [Alias("relevance", _rx(r"\\brelevance\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("query_understanding", [Alias("query_understanding", _rx(r"\\bquery\\s+understanding\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("query_expansion", [Alias("query_expansion", _rx(r"\\bquery\\s+expansion\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("semantic_search", [Alias("semantic_search", _rx(r"\\bsemantic\\s+search\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("vector_search", [Alias("vector_search", _rx(r"\\bvector\\s+search\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("rag", [Alias("rag", _rx(r"\\b(?:rag|retrieval[\\s-]?augmented\\s+generation)\\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("semantic_indexing", [Alias("semantic_indexing", _rx(r"\\bsemantic\\s+indexing\\b"))], "retrieval_concept", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("candidate_retrieval", [Alias("candidate_retrieval", _rx(r"\\bcandidate\\s+retrieval\\b"))], "retrieval_concept", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Recommendation Systems
    Concept("recommendation", [Alias("recommendation", _rx(r"\\brecommend(?:ation|ations|er|ers|ing)?\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("recommendation_systems", [Alias("recommendation_systems", _rx(r"\\brecommender\\s+systems?\\b", r"\\brecommendation\\s+systems?\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("personalization", [Alias("personalization", _rx(r"\\bpersonali[sz](?:ation|ed|ing)\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("matching", [Alias("matching", _rx(r"\\bmatching\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("candidate_matching", [Alias("candidate_matching", _rx(r"\\bcandidate\\s+matching\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("feed_ranking", [Alias("feed_ranking", _rx(r"\\bfeed\\s+ranking\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("marketplace", [Alias("marketplace", _rx(r"\\bmarketplace\\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    
    # Production Tech
    Concept("kafka", [Alias("kafka", _rx(r"\\bkafka\\b"))], "streaming", "production_tech", "verified"),
    Concept("spark", [Alias("spark", _rx(r"\\b(?:apache\\s+)?spark\\b"))], "data_processing", "production_tech", "verified"),
    Concept("pyspark", [Alias("pyspark", _rx(r"\\bpyspark\\b"))], "data_processing", "production_tech", "verified"),
    Concept("airflow", [Alias("airflow", _rx(r"\\b(?:apache\\s+)?airflow\\b"))], "orchestration", "production_tech", "verified"),
    Concept("flink", [Alias("flink", _rx(r"\\b(?:apache\\s+)?flink\\b"))], "streaming", "production_tech", "verified"),
    Concept("snowflake", [Alias("snowflake", _rx(r"\\bsnowflake\\b"))], "data_warehouse", "production_tech", "verified"),
    Concept("databricks", [Alias("databricks", _rx(r"\\bdatabricks\\b"))], "data_processing", "production_tech", "verified"),
    Concept("redis", [Alias("redis", _rx(r"\\bredis\\b"))], "cache", "production_tech", "verified"),
    Concept("postgres", [Alias("postgres", _rx(r"\\bpostgres(?:ql)?\\b"))], "database", "production_tech", "verified"),
]

REGISTRY_HASH = hashlib.sha256(repr([(c.canonical_name, [a.pattern.pattern for a in c.aliases]) for c in CONCEPT_REGISTRY]).encode()).hexdigest()
NUM_CONCEPTS = len(CONCEPT_REGISTRY)
NUM_ALIASES = sum(len(c.aliases) for c in CONCEPT_REGISTRY)

def build_feature_map(*families_or_categories):
    result = {}
    for c in CONCEPT_REGISTRY:
        if c.confidence in ("verified", "alias") and (c.family in families_or_categories or c.category in families_or_categories):
            patterns = [a.pattern.pattern for a in c.aliases]
            result[c.canonical_name] = re.compile("|".join(patterns), re.IGNORECASE)
    return result

SEARCH_ENGINES = build_feature_map("search_engine")
VECTOR_DATABASES = build_feature_map("vector_database")
RETRIEVAL_ALGORITHMS = build_feature_map("retrieval_algorithm")
RANKING_TECHNIQUES = build_feature_map("ranking_technique")
REPRESENTATION_TECHNIQUES = build_feature_map("representation_technique")
RETRIEVAL_CONCEPTS = build_feature_map("retrieval_concept")
RECOMMENDATION_SYSTEMS = build_feature_map("recommendation_concept")
PRODUCTION_TECH_MAPPED = build_feature_map("production_tech")

PRODUCTION_TECH = {
    **PRODUCTION_TECH_MAPPED,
    **SEARCH_ENGINES,
    **VECTOR_DATABASES,
}
# --- END CONCEPT REGISTRY ---
"""

# Replace in content
start_idx = content.find('# --- CONCEPT REGISTRY ---')
end_idx = content.find('# --- END CONCEPT REGISTRY ---') + len('# --- END CONCEPT REGISTRY ---') + 1

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_registry_code.strip() + '\n' + content[end_idx:]
    with open('extract_candidate_features.py', 'w') as f:
        f.write(content)
    print("Replaced CONCEPT REGISTRY in extract_candidate_features.py")
else:
    print("Could not find registry boundaries.")
