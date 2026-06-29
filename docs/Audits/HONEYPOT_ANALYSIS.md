# Redrob Honeypot Analysis

## Purpose

Understand likely honeypot strategies used in the dataset.

Avoid simplistic detection methods.

Design a ranking system robust against synthetic profiles and keyword stuffing.

---

# Known Facts

The challenge documentation explicitly mentions:

- Keyword stuffers
- Behavioral twins
- Honeypots
- Synthetic profiles

Approximately:

```text
~80 honeypots
```

exist in a 100,000 candidate pool.

This means:

The honeypots are likely sophisticated.

---

# Rejected Honeypot Theory 1

## Timeline Contradictions

Examples:

- Future employment dates
- Impossible education dates
- PhD before Bachelor's
- 10 years experience after 3 years employment

### Why It Helps

Catches obvious fake profiles.

### Why It Fails

Too easy.

Challenge designers know participants will check dates.

### Conclusion

Necessary.

Not sufficient.

---

# Rejected Honeypot Theory 2

## Keyword Stuffing Detection

Example:

```text
LangChain
Pinecone
FAISS
RAG
GPT
OpenAI
```

appearing everywhere.

### Why It Helps

README explicitly warns about keyword stuffers.

### Why It Fails

Real candidates may legitimately have these technologies.

### Better Approach

Measure:

```text
Keyword Support
```

instead of keyword count.

---

# Rejected Honeypot Theory 3

## Rare Keyword Ranking

Assumption:

Rare keywords imply strong candidates.

Examples:

- NDCG
- MRR
- LTR

### Why It Fails

Rare ≠ important.

Strong candidates often never mention these terms.

### Conclusion

Treat as bonus evidence only.

---

# Rejected Honeypot Theory 4

## Search Engineer Detection

Assumption:

Search Engineer titles identify strong candidates.

### Why It Fails

Real data shows:

```text
Search Engineer ≈ 0
Ranking Engineer ≈ 0
```

### Conclusion

Strong candidates are hiding inside:

- Software Engineer
- Backend Engineer
- Data Engineer
- ML Engineer

---

# Rejected Honeypot Theory 5

## Consulting Company Detection

Assumption:

TCS = bad.

### Why It Fails

The JD explicitly allows:

```text
Product Company
→ Consulting Company
```

career paths.

### Better Approach

Detect:

```text
Consulting-only career
```

not consulting presence.

---

# Rejected Honeypot Theory 6

## Consistency Is Everything

Assumption:

Consistency determines rank.

### Why It Fails

A candidate can be:

```text
Perfectly consistent
```

and still irrelevant.

Example:

Civil Engineer.

### Better Interpretation

Consistency is:

```text
Trustworthiness
```

not

```text
Relevance
```

---

# Strongest Current Theory

## Evidence Support Model

Core question:

```text
Does the career history support the claimed expertise?
```

---

# Example: Strong Candidate

Claim:

```text
Recommendation Systems
```

Career Evidence:

- Personalization
- Feed Ranking
- Matching Systems

Result:

```text
High Confidence
```

---

# Example: Suspicious Candidate

Claim:

```text
Recommendation Systems
```

Career Evidence:

- ERP
- Payroll
- Reporting

Result:

```text
Low Confidence
```

---

# Evidence Support Framework

Every major claim should have supporting evidence.

Examples:

---

## Retrieval

Claim:

```text
Retrieval
```

Supporting Evidence:

- Search Infrastructure
- Embedding Systems
- Vector Search
- Relevance Work

---

## Ranking

Claim:

```text
Ranking
```

Supporting Evidence:

- NDCG
- MRR
- Relevance Optimization
- Evaluation Frameworks

---

## Recommendation

Claim:

```text
Recommendation Systems
```

Supporting Evidence:

- Personalization
- Matching
- Feed Ranking

---

## Production

Claim:

```text
Production Systems
```

Supporting Evidence:

- Kafka
- Streaming
- On-call
- Latency
- Scale

---

# Advanced Theory

## Evidence Graph

Represent profiles as:

```text
Claim
↓
Evidence
↓
Confidence
```

Example:

```text
Retrieval
↓
Milvus
Vector Search
Search Infrastructure
↓
High Confidence
```

versus

```text
Retrieval
↓
Skill List Only
↓
Low Confidence
```

---

# Behavioral Twins

Possible hidden trap:

Two candidates with:

- Same skills
- Same title
- Same experience

but different:

- Consistency
- Behavioral signals
- Evidence support

Goal:

Punish shallow rankers.

---

# Final Honeypot Philosophy

Do NOT ask:

```text
What keywords does this candidate have?
```

Ask:

```text
What evidence proves the candidate has done this work?
```

Reward:

```text
Supported Claims
```

Penalize:

```text
Unsupported Claims
```

This approach is harder to game and more closely resembles real hiring decisions.