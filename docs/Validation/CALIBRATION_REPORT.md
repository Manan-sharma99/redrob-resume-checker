# Calibration Report: Senior AI Engineer Ranking

## 1. Variant Comparison

| Metric | Variant A (Baseline) | Variant B (Balanced Domains) | Variant C (Credibility Emphasis) |
|---|---|---|---|
| Avg Retrieval | 65.3 | 65.3 | 64.7 |
| Avg Recommendation | 16.5 | 15.4 | 16.0 |
| Avg Evaluation | 23.8 | 23.5 | 23.7 |
| Avg Credibility | 0.468 | 0.470 | **0.478** |
| Top100 Overlap w/ Baseline | - | 95% | 94% |

### Archetype Distribution
*Archetypes defined by dominating base scores (e.g., Search-Leaning = Retrieval > Recommendation).*

| Archetype | Variant A (Baseline) | Variant B | Variant C |
|---|---|---|---|
| **Hybrid / Matching** | 5 | 5 | 5 |
| **Recommendation (Pure)** | 2 | 2 | 2 |
| **Recommendation-Leaning**| 0 | 1 | 3 |
| **Search (Pure)** | 47 | 49 | 49 |
| **Search-Leaning** | 46 | 43 | 41 |

*Note: The total Recommendation presence (Pure + Leaning + Hybrid) increases from 7 in Baseline to 10 in Variant C.*

---

## 2. Top100 Differences

- **Candidates entering Top 100 in Variant C**: 6
- **Candidates leaving Top 100 in Variant C**: 6

**Who entered?**
The 6 candidates entering the Top 100 in Variant C are primarily **Recommendation-Leaning** and **Search-Leaning** engineers with exceptionally high `credibility_score`s. Because we shifted to `max(retrieval, recommendation)`, Recommendation experts were no longer mathematically suppressed by the 0.15 vs 0.60 base multiplier mismatch. 

**Who left?**
The 6 candidates leaving the Top 100 were high-retrieval "Search" profiles with poor credibility scores. These were borderline candidates surviving purely on the strength of keyword-matching (often generative synthetic profiles) that were finally pushed out when the credibility weight was increased.

---

## 3. Why the Chosen Variant is Better

**Recommended Variant: Variant C (Credibility Emphasis)**

**Justification:**
1. **JD Alignment:** The JD explicitly targets "Recommendation systems" and "Matching systems". Variant C mathematically removes the unfair 4x penalty against Recommendation engineers by using a `max()` gate, fulfilling the JD's requirement for domain balance.
2. **Top100 Diversity:** Variant C increases the presence of Recommendation-leaning engineers while maintaining a strong Search core, better reflecting a hybrid retrieval/ranking JD.
3. **Candidate Quality:** By shifting the macro weights from `65/35` to `55/45` (Relevance vs Credibility), Variant C acts as a scalpel. It preserves 94% of the elite leaderboard but surgically excises 6 keyword-stuffers with low credibility, replacing them with operators who have concrete production metrics and evidence-backed claims.
4. **Ranking Stability:** Removing the arbitrary `eval_bonus` (which acted as an unstable additive kingmaker) and using `max()` stabilizes the math. The system no longer relies on linear sums of mismatched distributions.

---

## 4. Exact Code Changes Made

**For Variant C (`rank_candidates_v3.py`), the following modifications were applied to the baseline:**

1. **Relevance Logic:** Replaced the linear `(0.60 * ret) + (0.15 * rec) + (0.25 * eval)` formula with a domain-agnostic max function:
   ```python
   raw = np.maximum(df["retrieval_score"] / 100.0, df["recommendation_score"] / 100.0) * 0.75 + (df["evaluation_score"] / 100.0) * 0.25
   ```
2. **Bonus Removal:** Stripped the hardcoded `0.03` and `0.06` additive evaluation bonuses to prevent them from overriding system depth.
3. **Macro Weights:** Shifted the relevance/credibility balance to demand higher proof of work while keeping relevance dominant:
   ```python
   RELEVANCE_WEIGHT = 0.55      # Down from 0.65
   CREDIBILITY_WEIGHT = 0.45    # Up from 0.35
   ```

---

## 5. Expected Impact on Leaderboard Performance

- **Elimination of "Paper Tigers":** Candidates who memorised search keywords but failed to provide production scale metrics or infrastructure evidence will drop in rank.
- **Fair Ground for RecSys Engineers:** A candidate who spent 5 years building feed ranking and personalisation pipelines (high recommendation score) will now rank identically to a candidate who spent 5 years building Elasticsearch pipelines, accurately reflecting the dual-nature of the JD.
- **Reduction of Synthetic Dominance:** Because generative profiles naturally struggle to invent highly specific production latency numbers and complex infrastructure interactions without creating timeline contradictions, raising the credibility weight successfully suppresses identical synthetic behavioral twins at the borderline.
