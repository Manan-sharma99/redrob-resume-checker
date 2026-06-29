# GOLD PAIR VALIDATION SET

This document contains 50 deterministic pairwise ranking tests designed to validate future ranking algorithms against the expected hiring philosophy. **Any ranking system MUST pass these tests before being considered for production.**


## 1. Production Search Engineer vs Prototype Builder

### Test 1: Elite Production Search vs Prototype Search
- **Candidate A**: `retrieval=80, production=90, specificity=85`
- **Candidate B**: `retrieval=80, production=10, specificity=15`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Both have identical keyword relevance, but A operated systems at scale.
- **JD Section**: production systems, operational ownership
- **Features that SHOULD influence**: production_score, credibility_score
- **Features that SHOULD NOT influence**: retrieval_score
- **Potential Failure Mode**: Linear addition lets B stay close.

### Test 2: Moderate Prod Search vs Max Keyword Prototype
- **Candidate A**: `retrieval=60, production=70`
- **Candidate B**: `retrieval=95, production=5`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: 60% relevance with production beats 95% keyword match who never deployed.
- **JD Section**: production systems
- **Features that SHOULD influence**: production_score
- **Features that SHOULD NOT influence**: raw retrieval
- **Potential Failure Mode**: System defaults to retrieval.

### Test 3: Production RecSys vs Prototype Hybrid
- **Candidate A**: `recommendation=75, production=80`
- **Candidate B**: `retrieval=70, recommendation=70, production=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Real production in one domain beats toy experience in multiple.
- **JD Section**: production ML infrastructure
- **Features that SHOULD influence**: production_score
- **Features that SHOULD NOT influence**: breadth bonuses
- **Potential Failure Mode**: Breadth bonus overpowers credibility.


## 2. Recommendation Engineer vs Search Engineer

### Test 4: Elite Rec vs Elite Search
- **Candidate A**: `recommendation=90, retrieval=10`
- **Candidate B**: `retrieval=90, recommendation=10`
- **Expected Winner**: **Tie**
- **Confidence**: High
- **Reasoning**: Search and Recommendation are parallel domains.
- **JD Section**: Recommendation Systems, Search Systems
- **Features that SHOULD influence**: max(retrieval, recommendation)
- **Features that SHOULD NOT influence**: arbitrary base weights
- **Potential Failure Mode**: System uses fixed 0.60 ret / 0.15 rec weight.

### Test 5: Good Rec vs Mediocre Search
- **Candidate A**: `recommendation=70, retrieval=0`
- **Candidate B**: `retrieval=40, recommendation=0`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Strong RecSys strictly beats weak Search.
- **JD Section**: Recommendation Systems
- **Features that SHOULD influence**: recommendation_score
- **Features that SHOULD NOT influence**: retrieval defaults
- **Potential Failure Mode**: System defaults to retrieval.

### Test 6: Rec-Leaning vs Search-Leaning
- **Candidate A**: `recommendation=80, retrieval=50`
- **Candidate B**: `retrieval=80, recommendation=50`
- **Expected Winner**: **Tie**
- **Confidence**: High
- **Reasoning**: Both have strong primary domains.
- **JD Section**: Search, Recommendation
- **Features that SHOULD influence**: domain breadth
- **Features that SHOULD NOT influence**: domain bias
- **Potential Failure Mode**: Linear weighting punishes Rec-Leaning.

### Test 7: Pure Rec vs Broad Search Prototype
- **Candidate A**: `recommendation=90, production=80`
- **Candidate B**: `retrieval=60, recommendation=40, production=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Elite Rec specialist beats broad prototype generalist.
- **JD Section**: production systems
- **Features that SHOULD influence**: credibility_score
- **Features that SHOULD NOT influence**: breadth bonus
- **Potential Failure Mode**: Failing to dampen relevance by credibility.


## 3. Evidence-backed profile vs Keyword-stuffed profile

### Test 8: Solid Evidence vs Max Keyword Stuffing
- **Candidate A**: `retrieval=65, evidence_support=80, production=75`
- **Candidate B**: `retrieval=99, evidence_support=5, production=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Keyword stuffers fail evidence checks.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: evidence_support_score
- **Features that SHOULD NOT influence**: retrieval_score
- **Potential Failure Mode**: Keyword density allows B to slip into Top 100.

### Test 9: Moderate Evidence vs Zero Evidence
- **Candidate A**: `recommendation=50, evidence_support=50`
- **Candidate B**: `recommendation=50, evidence_support=0`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Candidate A attempted to back up claims.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: evidence_support_score
- **Features that SHOULD NOT influence**: recommendation_score
- **Potential Failure Mode**: Evidence score is ignored.

### Test 10: High Spec vs High Evidence Mapping
- **Candidate A**: `specificity=80, evidence_support=20`
- **Candidate B**: `specificity=20, evidence_support=80`
- **Expected Winner**: **Tie**
- **Confidence**: Medium
- **Reasoning**: Both show credibility in different ways.
- **JD Section**: operational ownership
- **Features that SHOULD influence**: specificity_score, evidence_support
- **Features that SHOULD NOT influence**: N/A
- **Potential Failure Mode**: System relies entirely on one credibility feature.

### Test 11: High Keyword Density vs Moderate Balanced
- **Candidate A**: `retrieval=95, credibility=10`
- **Candidate B**: `retrieval=60, credibility=60`
- **Expected Winner**: **Candidate B**
- **Confidence**: High
- **Reasoning**: Moderate relevance with strong credibility beats unbacked keyword stuffing.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility_score
- **Features that SHOULD NOT influence**: retrieval_score
- **Potential Failure Mode**: Raw multiplication is not balanced.


## 4. Strong production metrics vs Strong skill list

### Test 12: Metrics Operator vs Skill Lister
- **Candidate A**: `retrieval=50, specificity=90`
- **Candidate B**: `retrieval=85, specificity=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Specificity proves they built it.
- **JD Section**: operational ownership
- **Features that SHOULD influence**: specificity_score
- **Features that SHOULD NOT influence**: retrieval_score
- **Potential Failure Mode**: Relevance dominates credibility.

### Test 13: Latency/Scale Expert vs Concept Lister
- **Candidate A**: `recommendation=60, specificity=85, production=80`
- **Candidate B**: `recommendation=85, specificity=15, production=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Real engineers talk about scale.
- **JD Section**: production systems
- **Features that SHOULD influence**: specificity_score
- **Features that SHOULD NOT influence**: recommendation
- **Potential Failure Mode**: Failure to gate relevance.

### Test 14: Avg Rel + Elite Metrics vs Elite Rel + Zero Metrics
- **Candidate A**: `retrieval=50, specificity=95`
- **Candidate B**: `retrieval=95, specificity=5`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: A is proven. B is likely synthetic.
- **JD Section**: production systems
- **Features that SHOULD influence**: specificity_score
- **Features that SHOULD NOT influence**: raw relevance
- **Potential Failure Mode**: System loves perfect relevance scores.

### Test 15: Production Metric Heavy vs BM25 Keyword Lister
- **Candidate A**: `retrieval=40, specificity=90`
- **Candidate B**: `retrieval=70, specificity=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Metrics show reality. BM25 is just a keyword.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear scoring.


## 5. Search engineer vs Generic LLM engineer

### Test 16: Pure Search vs Generic GenAI
- **Candidate A**: `retrieval=80, production=70`
- **Candidate B**: `retrieval=20, evaluation=10, production=70`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: JD explicitly dislikes generic GenAI.
- **JD Section**: Search Systems
- **Features that SHOULD influence**: retrieval_score
- **Features that SHOULD NOT influence**: production_score
- **Potential Failure Mode**: B gets too much credit for AI.

### Test 17: Hybrid Search/Rec vs LLM Wrapper Builder
- **Candidate A**: `retrieval=60, recommendation=50`
- **Candidate B**: `retrieval=15, evidence_support=90`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: LLM wrapper lacks core domain.
- **JD Section**: Retrieval, Recommendation
- **Features that SHOULD influence**: retrieval_score
- **Features that SHOULD NOT influence**: evidence_support
- **Potential Failure Mode**: Evidence boosts irrelevant candidates.

### Test 18: Search Eval Expert vs LLM Prompt Engineer
- **Candidate A**: `evaluation=70, retrieval=50`
- **Candidate B**: `evaluation=10, retrieval=10, production=50`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Evaluation in retrieval is highly prized.
- **JD Section**: Evaluation Frameworks
- **Features that SHOULD influence**: evaluation_score
- **Features that SHOULD NOT influence**: production_score
- **Potential Failure Mode**: Failure to multiply evaluation by relevance.


## 6. Product company vs Consulting-only career

### Test 19: Product Search vs Consulting Search
- **Candidate A**: `retrieval=70, consulting_only_flag=False, production=70`
- **Candidate B**: `retrieval=70, consulting_only_flag=True, production=70`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: JD explicitly dislikes consulting-only.
- **JD Section**: consulting-only careers (dislike)
- **Features that SHOULD influence**: consulting_only_flag
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: System ignores penalty.

### Test 20: Product RecSys vs Heavy Consulting RecSys
- **Candidate A**: `recommendation=70, consulting_ratio=0.1`
- **Candidate B**: `recommendation=70, consulting_ratio=0.8`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Heavy consulting is a soft negative.
- **JD Section**: operational ownership
- **Features that SHOULD influence**: consulting_ratio
- **Features that SHOULD NOT influence**: recommendation
- **Potential Failure Mode**: Consulting ratio is not penalized.

### Test 21: Weak Product vs Elite Consulting
- **Candidate A**: `retrieval=30, production=30, consulting_only=False`
- **Candidate B**: `retrieval=90, production=80, consulting_only=True`
- **Expected Winner**: **Candidate B**
- **Confidence**: Medium
- **Reasoning**: Consulting is a negative, not a hard reject.
- **JD Section**: Search Systems vs consulting
- **Features that SHOULD influence**: retrieval, production
- **Features that SHOULD NOT influence**: consulting_only_flag
- **Potential Failure Mode**: Consulting flag acts as a fatal 0 multiplier.

### Test 22: Product Matching vs Consulting Matching
- **Candidate A**: `retrieval=60, recommendation=60, consulting=False`
- **Candidate B**: `retrieval=60, recommendation=60, consulting=True`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Product experience wins ties.
- **JD Section**: production systems
- **Features that SHOULD influence**: consulting_only_flag
- **Features that SHOULD NOT influence**: relevance
- **Potential Failure Mode**: No penalty applied.


## 7. Consistent timeline vs Contradictory timeline

### Test 23: Normal Career vs Time Traveler
- **Candidate A**: `retrieval=60, contradiction_score=0`
- **Candidate B**: `retrieval=99, contradiction_score=50`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Contradiction > 30 is a hard reject.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: contradiction_score
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Contradiction is ignored.

### Test 24: Normal RecSys vs Slight Overlap
- **Candidate A**: `recommendation=70, contradiction_score=0`
- **Candidate B**: `recommendation=75, contradiction_score=10`
- **Expected Winner**: **Candidate B**
- **Confidence**: Medium
- **Reasoning**: Minor overlaps (10) are normal in tech.
- **JD Section**: Recommendation Systems
- **Features that SHOULD influence**: recommendation_score
- **Features that SHOULD NOT influence**: contradiction_score
- **Potential Failure Mode**: System aggressively penalizes minor date overlaps.

### Test 25: Consistent Junior vs Contradictory Senior
- **Candidate A**: `retrieval=40, contradiction_score=0`
- **Candidate B**: `retrieval=80, contradiction_score=40`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Score 40 contradiction means multiple impossible timelines. Reject.
- **JD Section**: keyword stuffing (dislike)
- **Features that SHOULD influence**: contradiction_score
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Hard reject gate is missing.

### Test 26: Zero Contradiction Search vs High Contradiction Prototype
- **Candidate A**: `retrieval=70, contradiction=0`
- **Candidate B**: `retrieval=80, contradiction=35`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Hard reject threshold.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: contradiction_score
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: No hard reject.


## 8. Hybrid Retrieval engineer vs Pure BM25 engineer

### Test 27: Vector+BM25 vs Pure BM25
- **Candidate A**: `retrieval=85, specificity=80`
- **Candidate B**: `retrieval=60, specificity=60`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Hybrid retrieval yields higher scores.
- **JD Section**: Hybrid Retrieval
- **Features that SHOULD influence**: retrieval_score
- **Features that SHOULD NOT influence**: N/A
- **Potential Failure Mode**: Score saturation prevents A from pulling ahead.

### Test 28: Hybrid Rec+Vector vs Standard IR
- **Candidate A**: `retrieval=70, recommendation=60`
- **Candidate B**: `retrieval=70, recommendation=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Breadth bonus applies.
- **JD Section**: Hybrid Retrieval
- **Features that SHOULD influence**: recommendation_score
- **Features that SHOULD NOT influence**: N/A
- **Potential Failure Mode**: No breadth bonus.


## 9. Evaluation expert with production vs Evaluation expert without production

### Test 29: Eval + Prod vs Pure Eval (Data Scientist)
- **Candidate A**: `evaluation=80, retrieval=60, production=70`
- **Candidate B**: `evaluation=90, retrieval=10, production=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Eval without a system is data science.
- **JD Section**: Evaluation Frameworks
- **Features that SHOULD influence**: production_score
- **Features that SHOULD NOT influence**: evaluation_score
- **Potential Failure Mode**: Eval is treated as additive.

### Test 30: Search Builder vs Pure Eval Analyst
- **Candidate A**: `retrieval=80, evaluation=0`
- **Candidate B**: `retrieval=0, evaluation=90`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Eval is a bonus multiplier on relevance.
- **JD Section**: Search Systems
- **Features that SHOULD influence**: retrieval
- **Features that SHOULD NOT influence**: evaluation
- **Potential Failure Mode**: Eval creates relevance.

### Test 31: RecSys Eval vs Eval Generalist
- **Candidate A**: `recommendation=70, evaluation=60`
- **Candidate B**: `retrieval=10, recommendation=10, evaluation=80`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Domain relevance is required for eval to amplify.
- **JD Section**: Evaluation
- **Features that SHOULD influence**: recommendation
- **Features that SHOULD NOT influence**: evaluation
- **Potential Failure Mode**: Additive eval logic.

### Test 32: High Eval/Low Cred vs Low Eval/High Cred
- **Candidate A**: `evaluation=80, credibility=20`
- **Candidate B**: `evaluation=20, credibility=80`
- **Expected Winner**: **Candidate B**
- **Confidence**: Medium
- **Reasoning**: Credibility validates. Eval without cred is suspect.
- **JD Section**: production systems
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: evaluation
- **Potential Failure Mode**: Eval overwhelms credibility.


## 10. High credibility vs High keyword density

### Test 33: Proven Operator vs Resume Optimizer
- **Candidate A**: `retrieval=60, production=80, specificity=80`
- **Candidate B**: `retrieval=95, production=10, specificity=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: A is the exact target persona.
- **JD Section**: operational ownership
- **Features that SHOULD influence**: credibility_score
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum allows B to win.

### Test 34: Solid Backend Search vs Search Keyword Spammer
- **Candidate A**: `retrieval=55, credibility=85`
- **Candidate B**: `retrieval=100, credibility=5`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: 100 retrieval with 5 credibility is mathematically impossible for a real human.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Lack of multiplicative dampener.

### Test 35: RecSys Operator vs RecSys Spammer
- **Candidate A**: `recommendation=60, credibility=75`
- **Candidate B**: `recommendation=95, credibility=15`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility must gate the domain relevance.
- **JD Section**: production
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: recommendation
- **Potential Failure Mode**: Domain bias or linear logic.


## 11. Broad relevance engineer vs Single-domain specialist

### Test 36: 100/100 Hybrid vs 100/0 Specialist
- **Candidate A**: `retrieval=90, recommendation=90, production=80`
- **Candidate B**: `retrieval=90, recommendation=0, production=80`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: A has mastered two relevance domains.
- **JD Section**: Search, Recommendation
- **Features that SHOULD influence**: domain breadth bonus
- **Features that SHOULD NOT influence**: pure max()
- **Potential Failure Mode**: System uses pure max().

### Test 37: 80/0 Specialist vs 50/50 Generalist
- **Candidate A**: `retrieval=80, recommendation=0`
- **Candidate B**: `retrieval=50, recommendation=50`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Deep expertise beats mediocre knowledge in both.
- **JD Section**: Search Systems
- **Features that SHOULD influence**: max(retrieval, recommendation)
- **Features that SHOULD NOT influence**: domain breadth bonus
- **Potential Failure Mode**: Breadth bonus is too large.

### Test 38: 70/70 Hybrid vs 80/0 Specialist
- **Candidate A**: `retrieval=70, recommendation=70`
- **Candidate B**: `retrieval=80, recommendation=0`
- **Expected Winner**: **Candidate A**
- **Confidence**: Medium
- **Reasoning**: A 70/70 hybrid is generally more valuable than an 80/0 specialist.
- **JD Section**: Hybrid Retrieval
- **Features that SHOULD influence**: breadth bonus
- **Features that SHOULD NOT influence**: pure max
- **Potential Failure Mode**: No breadth bonus.


## 12. Recent relevance work vs Old relevance work

### Test 39: High Total/High Prod vs High Total/Low Prod
- **Candidate A**: `experience=120, production=80`
- **Candidate B**: `experience=120, production=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Low production implies old/stale hands-on work.
- **JD Section**: Production ML
- **Features that SHOULD influence**: production
- **Features that SHOULD NOT influence**: experience
- **Potential Failure Mode**: Experience dominates.

### Test 40: Moderate Tenure/High Spec vs Long Tenure/Low Spec
- **Candidate A**: `tenure=24, specificity=85`
- **Candidate B**: `tenure=84, specificity=30`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Metrics show recent/current impact.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: specificity
- **Features that SHOULD NOT influence**: tenure
- **Potential Failure Mode**: Tenure bias.


## 13. Production ownership vs Research-only profile

### Test 41: Production Engineer vs Research Scientist
- **Candidate A**: `retrieval=70, production=80, specificity=70`
- **Candidate B**: `retrieval=80, production=10, specificity=40`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: JD wants production ML infrastructure.
- **JD Section**: Production ML Infrastructure
- **Features that SHOULD influence**: production
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: System fails to validate relevance.

### Test 42: Applied Scientist vs Pure Academic
- **Candidate A**: `recommendation=80, production=60`
- **Candidate B**: `recommendation=90, production=5`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Applied scientist built it.
- **JD Section**: Production ML
- **Features that SHOULD influence**: production
- **Features that SHOULD NOT influence**: recommendation
- **Potential Failure Mode**: Raw domain score wins.


## 14. Infrastructure engineer vs Model fine-tuning engineer

### Test 43: Search Infra vs LLM Fine-Tuner
- **Candidate A**: `retrieval=70, production=80`
- **Candidate B**: `retrieval=20, production=80`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Infra for search beats generic ML finetuning.
- **JD Section**: Retrieval Infrastructure
- **Features that SHOULD influence**: retrieval
- **Features that SHOULD NOT influence**: production
- **Potential Failure Mode**: Production overpowers domain.

### Test 44: RecSys Infra vs General ML Ops
- **Candidate A**: `recommendation=75, production=85`
- **Candidate B**: `recommendation=15, production=95`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Domain relevance is Tier 1.
- **JD Section**: Recommendation Systems
- **Features that SHOULD influence**: recommendation
- **Features that SHOULD NOT influence**: production
- **Potential Failure Mode**: Production masks lack of domain.


## 15. Behavioral twin where only evidence quality differs

### Test 45: Original Profile vs Generative Copy
- **Candidate A**: `retrieval=80, specificity=85, evidence=80`
- **Candidate B**: `retrieval=80, specificity=20, evidence=30`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Generative copies duplicate keywords but fail specificity.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: specificity
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Credibility multiplier is too weak.

### Test 46: Original RecSys vs Copied RecSys
- **Candidate A**: `recommendation=85, production=85`
- **Candidate B**: `recommendation=85, production=25`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Original has operational verbs.
- **JD Section**: operational ownership
- **Features that SHOULD influence**: production
- **Features that SHOULD NOT influence**: recommendation
- **Potential Failure Mode**: Linear scoring.

### Test 47: Authentic Hybrid vs Synthetic Hybrid
- **Candidate A**: `retrieval=60, recommendation=60, credibility=80`
- **Candidate B**: `retrieval=60, recommendation=60, credibility=10`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Authentic always wins.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: domain
- **Potential Failure Mode**: Weak credibility interaction.


## 16. Edge Case Validations 1

### Test 48: Boundary Test 1
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 2

### Test 49: Boundary Test 2
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 3

### Test 50: Boundary Test 3
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 4

### Test 51: Boundary Test 4
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 5

### Test 52: Boundary Test 5
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 6

### Test 53: Boundary Test 6
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 7

### Test 54: Boundary Test 7
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 8

### Test 55: Boundary Test 8
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 9

### Test 56: Boundary Test 9
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 10

### Test 57: Boundary Test 10
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 11

### Test 58: Boundary Test 11
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.


## 16. Edge Case Validations 12

### Test 59: Boundary Test 12
- **Candidate A**: `retrieval=85, credibility=80`
- **Candidate B**: `retrieval=95, credibility=20`
- **Expected Winner**: **Candidate A**
- **Confidence**: High
- **Reasoning**: Credibility dampens relevance.
- **JD Section**: evidence-backed claims
- **Features that SHOULD influence**: credibility
- **Features that SHOULD NOT influence**: retrieval
- **Potential Failure Mode**: Linear sum.

