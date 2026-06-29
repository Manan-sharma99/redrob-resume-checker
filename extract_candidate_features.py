#!/usr/bin/env python3
"""Stream candidate JSONL records into an interpretable Parquet feature table."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError as exc:  # pragma: no cover - exercised only without dependency
    raise SystemExit(
        "PyArrow is required. Install dependencies with: "
        "python -m pip install -r requirements.txt"
    ) from exc


DEFAULT_AS_OF_DATE = date(2026, 6, 24)
MONTH_DAYS = 365.2425 / 12
SHORT_TENURE_MONTHS = 12


def _rx(*patterns: str) -> re.Pattern[str]:
    return re.compile(r"(?:" + "|".join(patterns) + r")", re.IGNORECASE)


def _rx_case(*patterns: str) -> re.Pattern[str]:
    return re.compile(r"(?:" + "|".join(patterns) + r")")


PRODUCTION_ACTIONS = {
    "built": _rx(r"\bbuilt\b", r"\bbuild(?:ing|s)?\b"),
    "designed": _rx(r"\bdesign(?:ed|ing|s)?\b"),
    "owned": _rx(r"\bown(?:ed|ing|s)?\b"),
    "led": _rx(r"\bled\b", r"\blead(?:ing|s)?\b"),
    "architected": _rx(r"\barchitect(?:ed|ing|s)?\b"),
    "deployed": _rx(r"\bdeploy(?:ed|ing|s|ment)?\b"),
    "operated": _rx(r"\boperat(?:ed|ing|es|ion)\b"),
    "maintained": _rx(r"\bmaintain(?:ed|ing|s)?\b"),
}

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
        Alias("elasticsearch", _rx(r"\belasticsearch\b", r"\belastic\s+search\b"))
    ], "search_engine", "search_infrastructure", "verified"),
    Concept("opensearch", [Alias("opensearch", _rx(r"\bopensearch\b"))], "search_engine", "search_infrastructure", "verified"),
    Concept("solr", [Alias("solr", _rx(r"\bsolr\b"))], "search_engine", "search_infrastructure", "verified"),
    Concept("lucene", [Alias("lucene", _rx(r"\blucene\b")), Alias("lucene", _rx(r"\bapache\s+lucene\b"))], "search_engine", "search_infrastructure", "pending", rejection_reason="zero dataset evidence"),
    Concept("vespa", [Alias("vespa", _rx(r"\bvespa\b"))], "search_engine", "search_infrastructure", "pending", rejection_reason="zero dataset evidence"),
    
    # Vector Databases
    Concept("faiss", [Alias("faiss", _rx(r"\bfaiss\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("pinecone", [Alias("pinecone", _rx(r"\bpinecone\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("milvus", [Alias("milvus", _rx(r"\bmilvus\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("qdrant", [Alias("qdrant", _rx(r"\bqdrant\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("weaviate", [Alias("weaviate", _rx(r"\bweaviate\b"))], "vector_database", "search_infrastructure", "verified"),
    Concept("redis_vector", [Alias("redis_vector", _rx(r"\bredis\s+vector(?:\s+search)?\b", r"\bvector\s+redis\b", r"\bredisearch\b", r"\bredis\s+search\b"))], "vector_database", "search_infrastructure", "alias"),
    
    # Retrieval Algorithms
    Concept("bm25", [Alias("bm25", _rx(r"\bbm25\b"))], "retrieval_algorithm", "search_logic", "verified"),
    Concept("hnsw", [Alias("hnsw", _rx(r"\bhnsw\b", r"\bhierarchical\s+navigable\s+small\s+world\b"))], "retrieval_algorithm", "search_logic", "verified"),
    Concept("ann", [Alias("ann", _rx(r"\bann\b", r"\bapproximate\s+nearest\s+neighbou?rs?\b"))], "retrieval_algorithm", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("ivf", [Alias("ivf", _rx(r"\bivf\b"))], "retrieval_algorithm", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("scann", [Alias("scann", _rx(r"\bscann\b"))], "retrieval_algorithm", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Ranking Techniques
    Concept("learning_to_rank", [Alias("learning_to_rank", _rx(r"\blearning[- ]to[- ]rank\b", r"\bltr\b"))], "ranking_technique", "search_logic", "verified"),
    Concept("cross_encoder", [Alias("cross_encoder", _rx(r"\bcross[- ]encoder\b", r"\bcrossencoder\b"))], "ranking_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("llm_ranker", [Alias("llm_ranker", _rx(r"\bllm\s+rank(?:er|ing)?\b"))], "ranking_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("hard_negative_mining", [Alias("hard_negative_mining", _rx(r"\bhard\s+negative\s+mining\b"))], "ranking_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Representation Techniques
    Concept("embeddings", [Alias("embeddings", _rx(r"\bembeddings?\b"))], "representation_technique", "search_logic", "verified"),
    Concept("colbert", [Alias("colbert", _rx(r"\bcolbert(?:v2)?\b"))], "representation_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("splade", [Alias("splade", _rx(r"\bsplade\b"))], "representation_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("dual_encoder", [Alias("dual_encoder", _rx(r"\bdual[- ]encoder\b"))], "representation_technique", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Retrieval Concepts
    Concept("retrieval", [Alias("retrieval", _rx(r"\binformation\s+retrieval\b", r"\bretrieval\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("search", [Alias("search", _rx(r"\bsearch\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("ranking", [Alias("ranking", _rx(r"\brank(?:ing|ed|s)?\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("reranking", [Alias("reranking", _rx(r"\bre[\s-]?rank(?:ing|ed|s)?\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("relevance", [Alias("relevance", _rx(r"\brelevance\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("query_understanding", [Alias("query_understanding", _rx(r"\bquery\s+understanding\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("query_expansion", [Alias("query_expansion", _rx(r"\bquery\s+expansion\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("semantic_search", [Alias("semantic_search", _rx(r"\bsemantic\s+search\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("vector_search", [Alias("vector_search", _rx(r"\bvector\s+search\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("rag", [Alias("rag", _rx(r"\b(?:rag|retrieval[\s-]?augmented\s+generation)\b"))], "retrieval_concept", "search_logic", "verified"),
    Concept("semantic_indexing", [Alias("semantic_indexing", _rx(r"\bsemantic\s+indexing\b"))], "retrieval_concept", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    Concept("candidate_retrieval", [Alias("candidate_retrieval", _rx(r"\bcandidate\s+retrieval\b"))], "retrieval_concept", "search_logic", "pending", rejection_reason="zero dataset evidence"),
    
    # Recommendation Systems
    Concept("recommendation", [Alias("recommendation", _rx(r"\brecommend(?:ation|ations|er|ers|ing)?\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("recommendation_systems", [Alias("recommendation_systems", _rx(r"\brecommender\s+systems?\b", r"\brecommendation\s+systems?\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("personalization", [Alias("personalization", _rx(r"\bpersonali[sz](?:ation|ed|ing)\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("matching", [Alias("matching", _rx(r"\bmatching\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("candidate_matching", [Alias("candidate_matching", _rx(r"\bcandidate\s+matching\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("feed_ranking", [Alias("feed_ranking", _rx(r"\bfeed\s+ranking\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    Concept("marketplace", [Alias("marketplace", _rx(r"\bmarketplace\b"))], "recommendation_concept", "recommendation_logic", "verified"),
    
    # Production Tech
    Concept("kafka", [Alias("kafka", _rx(r"\bkafka\b"))], "streaming", "production_tech", "verified"),
    Concept("spark", [Alias("spark", _rx(r"\b(?:apache\s+)?spark\b"))], "data_processing", "production_tech", "verified"),
    Concept("pyspark", [Alias("pyspark", _rx(r"\bpyspark\b"))], "data_processing", "production_tech", "verified"),
    Concept("airflow", [Alias("airflow", _rx(r"\b(?:apache\s+)?airflow\b"))], "orchestration", "production_tech", "verified"),
    Concept("flink", [Alias("flink", _rx(r"\b(?:apache\s+)?flink\b"))], "streaming", "production_tech", "verified"),
    Concept("snowflake", [Alias("snowflake", _rx(r"\bsnowflake\b"))], "data_warehouse", "production_tech", "verified"),
    Concept("databricks", [Alias("databricks", _rx(r"\bdatabricks\b"))], "data_processing", "production_tech", "verified"),
    Concept("redis", [Alias("redis", _rx(r"\bredis\b"))], "cache", "production_tech", "verified"),
    Concept("postgres", [Alias("postgres", _rx(r"\bpostgres(?:ql)?\b"))], "database", "production_tech", "verified"),
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

PRODUCTION_TECH = {
    "kafka": _rx(r"\bkafka\b"),
    "spark": _rx(r"\b(?:apache\s+)?spark\b"),
    "pyspark": _rx(r"\bpyspark\b"),
    "airflow": _rx(r"\b(?:apache\s+)?airflow\b"),
    "flink": _rx(r"\b(?:apache\s+)?flink\b"),
    "snowflake": _rx(r"\bsnowflake\b"),
    "databricks": _rx(r"\bdatabricks\b"),
    "redis": _rx(r"\bredis\b"),
    "postgres": _rx(r"\bpostgres(?:ql)?\b"),
    **SEARCH_ENGINES,
    **VECTOR_DATABASES,
}

PRODUCTION_SIGNALS = {
    "real_time": _rx(r"\breal[\s-]?time\b"),
    "streaming": _rx(r"\bstream(?:ing|s)?\b"),
    "latency": _rx(r"\blaten(?:cy|cies)\b"),
    "throughput": _rx(r"\bthroughput\b"),
    "on_call": _rx(r"\bon[\s-]?call\b"),
    "monitoring": _rx(r"\bmonitor(?:ing|ed|s)?\b"),
    "schema_drift": _rx(r"\bschema\s+drift\b"),
    "incident": _rx(r"\bincidents?\b"),
    "scalability": _rx(r"\bscalab(?:ility|le)\b"),
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
    "ndcg": _rx(r"\bndcg(?:@\d+)?\b"),
    "mrr": _rx(r"\bmrr\b", r"\bmean\s+reciprocal\s+rank\b"),
    "map": _rx_case(r"\bMAP(?:@\d+)?\b", r"(?i:\bmean\s+average\s+precision\b)"),
    "ab_testing": _rx(r"\ba\s*/\s*b\s+test(?:ing|s|ed)?\b", r"\bab\s+test(?:ing|s|ed)?\b"),
    "offline_evaluation": _rx(r"\boffline\s+evaluation\b"),
    "online_evaluation": _rx(r"\bonline\s+evaluation\b"),
    "experiment": _rx(r"\bexperiment(?:ation|ing|s|ed)?\b"),
}

SPECIFICITY_METRICS = {
    "latency": _rx(r"\blatency\b", r"\b\d+(?:\.\d+)?\s*(?:ms|milliseconds?|seconds?|secs?)\b"),
    "throughput": _rx(r"\bthroughput\b"),
    "scale": _rx(r"\bscale\b", r"\bscal(?:ed|ing)\b"),
    "volume": _rx(r"\bvolume\b"),
    "availability": _rx(r"\bavailability\b", r"\buptime\b"),
    "accuracy": _rx(r"\baccuracy\b"),
    "conversion": _rx(r"\bconversion\b"),
    "precision_recall": _rx(r"\bprecision\b", r"\brecall\b"),
}

QUANTITY_RE = _rx(
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:k|m|b|million|billion|thousand)",
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:kb|mb|gb|tb|pb)",
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:ms|milliseconds?|seconds?|secs?|minutes?|hours?)",
    r"(?<![\w.])\d+(?:\.\d+)?\s*%",
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:qps|rps|tps)",
    r"(?<![\w.])\d+(?:\.\d+)?(?:\s*x)",
    r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?=\s+(?:users?|requests?|events?|records?|rows?|"
    r"transactions?|systems?|services?|pipelines?|models?|nodes?|servers?|clients?|daily|monthly))",
)

IMPROVEMENT_RE = _rx(
    r"\b(?:reduc(?:ed|ing)|improv(?:ed|ing)|increas(?:ed|ing)|decreas(?:ed|ing)|"
    r"grew|cut|boost(?:ed|ing)|lower(?:ed|ing))\b.{0,80}?\d",
    r"\bfrom\s+\d[^.;]{0,50}?\bto\s+\d",
)

ANY_RETRIEVAL_TERM = re.compile("|".join(pattern.pattern for pattern in RETRIEVAL_TERMS.values()), re.IGNORECASE)
ANY_RECOMMENDATION_TERM = re.compile("|".join(pattern.pattern for pattern in RECOMMENDATION_TERMS.values()), re.IGNORECASE)

MAJOR_CLAIMS = {
    "retrieval": ANY_RETRIEVAL_TERM,
    "recommendation": ANY_RECOMMENDATION_TERM,
    "ml": _rx(r"\bml\b", r"\bmachine\s+learning\b", r"\bdeep\s+learning\b"),
}

CONSULTING_COMPANIES = (
    "tcs",
    "tata consultancy services",
    "infosys",
    "wipro",
    "accenture",
    "cognizant",
    "capgemini",
)

TITLE_LEVEL_PATTERNS: Sequence[tuple[int, re.Pattern[str]]] = (
    (7, _rx(r"\bchief\b", r"\bceo\b", r"\bcto\b", r"\bcio\b", r"\bcdo\b", r"\bc[ -]?level\b")),
    (6, _rx(r"\bvice\s+president\b", r"\bvp\b")),
    (5, _rx(r"\bdirector\b", r"\bhead\b")),
    (4, _rx(r"\bprincipal\b", r"\bstaff\b", r"\blead\b", r"\bmanager\b", r"\barchitect\b")),
    (3, _rx(r"\bsenior\b", r"\bsr\.?\b")),
    (1, _rx(r"\bjunior\b", r"\bjr\.?\b", r"\bassociate\b", r"\bintern\b", r"\btrainee\b")),
)

OUTPUT_SCHEMA = pa.schema(
    [
        ("candidate_id", pa.string()),
        ("production_score", pa.float32()),
        ("retrieval_score", pa.float32()),
        ("recommendation_score", pa.float32()),
        ("evaluation_score", pa.float32()),
        ("specificity_score", pa.float32()),
        ("evidence_support_score", pa.float32()),
        ("total_months_experience", pa.int32()),
        ("average_tenure_months", pa.float32()),
        ("job_count", pa.int16()),
        ("short_tenure_count", pa.int16()),
        ("title_progression_score", pa.float32()),
        ("consulting_ratio", pa.float32()),
        ("consulting_only_flag", pa.bool_()),
        ("behavior_score", pa.float32()),
        ("contradiction_score", pa.float32()),
    ]
)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value)
        return result if math.isfinite(result) else default
    except (TypeError, ValueError):
        return default


def _parse_date(value: Any, default_present: date | None = None) -> date | None:
    if not value:
        return None
    val_str = str(value).strip()
    if not val_str:
        return None
        
    val_lower = val_str.lower()
    if val_lower in ("present", "current", "ongoing"):
        return default_present

    # Extract just the date-like part if it contains time
    val_str = val_str[:10]
    
    try:
        # YYYY-MM-DD
        if len(val_str) == 10 and val_str[4] == '-' and val_str[7] == '-':
            return datetime.strptime(val_str, "%Y-%m-%d").date()
        # YYYY-MM
        elif len(val_str) >= 7 and val_str[4] == '-':
            return datetime.strptime(val_str[:7], "%Y-%m").date()
        # YYYY
        elif len(val_str) >= 4 and val_str[:4].isdigit():
            return datetime.strptime(val_str[:4], "%Y").date()
    except ValueError:
        pass
    return None


def _months_between(start: date, end: date) -> int:
    if end < start:
        return 0
    return max(0, round((end - start).days / MONTH_DAYS))


def _term_stats(text: str, terms: Mapping[str, re.Pattern[str]]) -> tuple[int, int]:
    unique = 0
    occurrences = 0
    for pattern in terms.values():
        matches = pattern.findall(text)
        if matches:
            unique += 1
            occurrences += len(matches)
    return unique, occurrences


def _skill_text(skills: Sequence[Mapping[str, Any]]) -> str:
    return " | ".join(str(skill.get("name") or "") for skill in skills)


def _career_text(jobs: Sequence[Mapping[str, Any]]) -> str:
    return " ".join(str(job.get("description") or "") for job in jobs)


def _support_points(skill_text: str, terms: Mapping[str, re.Pattern[str]], cap: float = 10.0) -> float:
    unique, _ = _term_stats(skill_text, terms)
    return min(cap, unique * 2.0)


def production_score(
    jobs: Sequence[Mapping[str, Any]], description_text: str, skill_text: str
) -> float:
    action_unique, action_occ = _term_stats(description_text, PRODUCTION_ACTIONS)
    tech_unique, tech_occ = _term_stats(description_text, PRODUCTION_TECH)
    signal_unique, signal_occ = _term_stats(description_text, PRODUCTION_SIGNALS)

    cooccurrence_jobs = 0
    for job in jobs:
        text = str(job.get("description") or "")
        has_action = ANY_PRODUCTION_ACTION.search(text) is not None
        has_tech_or_signal = ANY_PRODUCTION_TECH_OR_SIGNAL.search(text) is not None
        cooccurrence_jobs += int(has_action and has_tech_or_signal)

    description_points = (
        4.0 * action_unique
        + 1.0 * min(8, max(0, action_occ - action_unique))
        + 5.0 * tech_unique
        + 1.0 * min(8, max(0, tech_occ - tech_unique))
        + 5.0 * signal_unique
        + 1.0 * min(8, max(0, signal_occ - signal_unique))
        + 6.0 * min(3, cooccurrence_jobs)
    )
    return round(min(100.0, min(90.0, description_points) + _support_points(skill_text, PRODUCTION_TECH)), 2)


def domain_score(
    description_text: str,
    skill_text: str,
    terms: Mapping[str, re.Pattern[str]],
    unique_weight: float,
) -> float:
    unique, occurrences = _term_stats(description_text, terms)
    description_points = unique_weight * unique + 2.0 * min(5, max(0, occurrences - unique))
    return round(
        min(100.0, min(90.0, description_points) + _support_points(skill_text, terms)),
        2,
    )


def specificity_score(description_text: str) -> float:
    quantities = len(QUANTITY_RE.findall(description_text))
    metric_unique, metric_occ = _term_stats(description_text, SPECIFICITY_METRICS)
    improvements = len(IMPROVEMENT_RE.findall(description_text))
    points = (
        8.0 * min(5, quantities)
        + 7.0 * metric_unique
        + 1.0 * min(5, max(0, metric_occ - metric_unique))
        + 20.0 * min(2, improvements)
    )
    return round(min(100.0, points), 2)


def evidence_support_score(description_text: str, skill_text: str) -> float:
    claims = [name for name, pattern in MAJOR_CLAIMS.items() if pattern.search(skill_text)]
    if not claims:
        return 0.0
    supported = sum(bool(MAJOR_CLAIMS[name].search(description_text)) for name in claims)
    return round(100.0 * supported / len(claims), 2)


def _job_interval(
    job: Mapping[str, Any], as_of_date: date
) -> tuple[date | None, date | None, int]:
    start = _parse_date(job.get("start_date"), as_of_date)
    end = as_of_date if job.get("is_current") else _parse_date(job.get("end_date"), as_of_date)
    supplied = max(0, int(_safe_float(job.get("duration_months"), 0)))
    derived = _months_between(start, end) if start and end else supplied
    return start, end, supplied or derived


def _union_months(intervals: Iterable[tuple[date, date]]) -> int:
    ordered = sorted(intervals)
    if not ordered:
        return 0
    merged: list[list[date]] = [[ordered[0][0], ordered[0][1]]]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])
    return sum(_months_between(start, end) for start, end in merged)


def _title_level(title: str) -> int:
    for level, pattern in TITLE_LEVEL_PATTERNS:
        if pattern.search(title):
            return level
    return 2


def title_progression_score(jobs: Sequence[Mapping[str, Any]]) -> float:
    ordered = sorted(
        jobs,
        key=lambda job: _parse_date(job.get("start_date"), date.min) or date.min,
    )
    if len(ordered) <= 1:
        return 50.0
    levels = [_title_level(str(job.get("title") or "")) for job in ordered]
    deltas = [max(-2, min(2, b - a)) for a, b in zip(levels, levels[1:])]
    return round(max(0.0, min(100.0, 50.0 + 25.0 * sum(deltas) / len(deltas))), 2)


def _normalized_company(value: Any) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()
    return re.sub(r"\b(?:limited|ltd|inc|llc|pvt|private)\b", "", text).strip()


def _is_consulting_company(value: Any) -> bool:
    company = _normalized_company(value)
    return any(company == name or company.startswith(name + " ") for name in CONSULTING_COMPANIES)


def career_features(
    jobs: Sequence[Mapping[str, Any]], as_of_date: date
) -> tuple[int, float, int, int, float, float, bool]:
    details = [_job_interval(job, as_of_date) for job in jobs]
    durations = [duration for _, _, duration in details]
    valid_intervals = []
    standalone_durations = []
    for start, end, duration in details:
        if start is not None and end is not None and end >= start:
            valid_intervals.append((start, end))
        else:
            standalone_durations.append(duration)
            
    total_months = _union_months(valid_intervals) + sum(standalone_durations)
    average_tenure = sum(durations) / len(durations) if durations else 0.0
    short_count = sum(0 < duration < SHORT_TENURE_MONTHS for duration in durations)

    weighted_total = sum(durations)
    consulting_months = sum(
        duration
        for job, duration in zip(jobs, durations)
        if _is_consulting_company(job.get("company"))
    )
    consulting_ratio = consulting_months / weighted_total if weighted_total else 0.0
    consulting_only = bool(jobs) and all(_is_consulting_company(job.get("company")) for job in jobs)

    return (
        total_months,
        round(average_tenure, 2),
        len(jobs),
        short_count,
        title_progression_score(jobs),
        round(consulting_ratio, 4),
        consulting_only,
    )


def behavior_score(signals: Mapping[str, Any]) -> float:
    response = max(0.0, min(1.0, _safe_float(signals.get("recruiter_response_rate"))))
    github_raw = _safe_float(signals.get("github_activity_score"), -1.0)
    github = max(0.0, min(1.0, github_raw / 100.0)) if github_raw >= 0 else 0.0
    saved = max(0.0, min(1.0, _safe_float(signals.get("saved_by_recruiters_30d")) / 10.0))
    interview = max(0.0, min(1.0, _safe_float(signals.get("interview_completion_rate"))))
    open_to_work = float(bool(signals.get("open_to_work_flag")))
    notice = max(0.0, min(1.0, 1.0 - _safe_float(signals.get("notice_period_days")) / 180.0))

    points = (
        25.0 * response
        + 20.0 * github
        + 20.0 * saved
        + 25.0 * interview
        + 5.0 * open_to_work
        + 5.0 * notice
    )
    return round(points, 2)


def contradiction_score(
    profile: Mapping[str, Any],
    jobs: Sequence[Mapping[str, Any]],
    education: Sequence[Mapping[str, Any]],
    total_months: int,
    as_of_date: date,
) -> float:
    points = 0.0

    claimed_months = max(0.0, _safe_float(profile.get("years_of_experience")) * 12.0)
    mismatch = abs(claimed_months - total_months)
    points += min(45.0, max(0.0, mismatch - 12.0) * 45.0 / 48.0)

    current_count = 0
    valid_intervals: list[tuple[date, date]] = []
    for job in jobs:
        start = _parse_date(job.get("start_date"), as_of_date)
        raw_end = _parse_date(job.get("end_date"), as_of_date)
        
        end_str = str(job.get("end_date") or "").strip().lower()
        is_current_str = end_str in ("present", "current", "ongoing")
        is_current = bool(job.get("is_current")) or is_current_str
        
        if is_current:
            current_count += 1

        if start is not None and start > as_of_date:
            points += 10.0
            
        if bool(job.get("is_current")) and raw_end is not None and not is_current_str and raw_end < as_of_date:
            points += 6.0

        end = as_of_date if is_current else raw_end
        if start is not None and end is not None:
            if end < start:
                points += 15.0
            else:
                valid_intervals.append((start, end))
                supplied = max(0, int(_safe_float(job.get("duration_months"), 0)))
                derived = _months_between(start, end)
                if supplied and abs(supplied - derived) > 4:
                    points += 5.0

    if current_count > 1:
        points += min(15.0, 7.5 * (current_count - 1))
    if jobs and current_count == 0:
        points += 5.0

    valid_intervals.sort()
    furthest_end: date | None = None
    for next_start, next_end in valid_intervals:
        overlap_days = (furthest_end - next_start).days if furthest_end else 0
        if overlap_days > 60:
            points += min(10.0, overlap_days / 365.0 * 5.0)
        if furthest_end is None or next_end > furthest_end:
            furthest_end = next_end

    for item in education:
        start_year = int(_safe_float(item.get("start_year"), 0))
        end_year = int(_safe_float(item.get("end_year"), 0))
        if not start_year or not end_year:
            pass # Remove arbitrary missing date penalty
        elif end_year < start_year:
            points += 15.0
        else:
            if end_year - start_year > 10:
                points += 5.0
            if start_year > as_of_date.year + 1 or end_year > as_of_date.year + 1:
                points += 10.0

    return round(min(100.0, points), 2)


def extract_features(record: Mapping[str, Any], as_of_date: date) -> dict[str, Any]:
    profile = record.get("profile") or {}
    jobs = record.get("career_history") or []
    education = record.get("education") or []
    skills = record.get("skills") or []
    signals = record.get("redrob_signals") or {}

    description_text = _career_text(jobs)
    skill_text = _skill_text(skills)
    (
        total_months,
        average_tenure,
        job_count,
        short_count,
        progression,
        consulting_ratio,
        consulting_only,
    ) = career_features(jobs, as_of_date)

    return {
        "candidate_id": str(record.get("candidate_id") or ""),
        "production_score": production_score(jobs, description_text, skill_text),
        "retrieval_score": domain_score(description_text, skill_text, RETRIEVAL_TERMS, 12.0),
        "recommendation_score": domain_score(
            description_text, skill_text, RECOMMENDATION_TERMS, 15.0
        ),
        "evaluation_score": domain_score(description_text, skill_text, EVALUATION_TERMS, 18.0),
        "specificity_score": specificity_score(description_text),
        "evidence_support_score": evidence_support_score(description_text, skill_text),
        "total_months_experience": total_months,
        "average_tenure_months": average_tenure,
        "job_count": job_count,
        "short_tenure_count": short_count,
        "title_progression_score": progression,
        "consulting_ratio": consulting_ratio,
        "consulting_only_flag": consulting_only,
        "behavior_score": behavior_score(signals),
        "contradiction_score": contradiction_score(
            profile, jobs, education, total_months, as_of_date
        ),
    }


def _write_batch(writer: pq.ParquetWriter, rows: list[dict[str, Any]]) -> None:
    writer.write_table(pa.Table.from_pylist(rows, schema=OUTPUT_SCHEMA))
    rows.clear()


def run_pipeline(
    input_path: Path,
    output_path: Path,
    batch_size: int,
    as_of_date: date,
    progress_every: int,
    limit: int | None = None,
) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    count = 0
    writer: pq.ParquetWriter | None = None

    try:
        writer = pq.ParquetWriter(
            output_path,
            OUTPUT_SCHEMA,
            compression="zstd",
            use_dictionary=["candidate_id"],
            write_statistics=True,
        )
        with input_path.open("r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
                rows.append(extract_features(record, as_of_date))
                count += 1
                if len(rows) >= batch_size:
                    _write_batch(writer, rows)
                if progress_every and count % progress_every == 0:
                    print(f"Processed {count:,} candidates", file=sys.stderr)
                if limit is not None and count >= limit:
                    break
        if rows:
            _write_batch(writer, rows)
        writer.close()
        writer = None
    finally:
        if writer is not None:
            writer.close()

    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/candidates.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("outputs/candidate_features.parquet"))
    parser.add_argument("--batch-size", type=int, default=5_000)
    parser.add_argument(
        "--as-of-date",
        type=date.fromisoformat,
        default=DEFAULT_AS_OF_DATE,
        help="Date used for current-role durations and future-date checks (YYYY-MM-DD).",
    )
    parser.add_argument("--progress-every", type=int, default=10_000)
    parser.add_argument("--limit", type=int, help="Process only the first N records (for testing).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be positive")
    if args.limit is not None and args.limit <= 0:
        raise SystemExit("--limit must be positive")
    if not args.input.is_file():
        raise SystemExit(f"Input file not found: {args.input}")
    count = run_pipeline(
        args.input,
        args.output,
        args.batch_size,
        args.as_of_date,
        args.progress_every,
        args.limit,
    )
    print(f"Wrote {count:,} rows to {args.output}")


if __name__ == "__main__":
    main()
