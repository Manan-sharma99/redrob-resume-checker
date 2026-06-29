#!/usr/bin/env python3
"""Pre-submission audit: data-grounded analysis of all 8 risk areas."""
import pandas as pd
import numpy as np

df     = pd.read_parquet("candidate_features.parquet")
ranked = pd.read_parquet("ranked_candidates.parquet")
merged = ranked.merge(df, on="candidate_id", how="left")

top100 = merged[merged["rank"] <= 100]
top20  = merged[merged["rank"] <= 20]
top500 = merged[merged["rank"] <= 500]

SEP = "\n" + "="*60 + "\n"

# ── ISSUE 1: Search vs Recommendation Imbalance ───────────────
print(SEP + "ISSUE 1: Search vs Recommendation Imbalance")

print("\nTop-100 retrieval_score stats:")
print(top100["retrieval_score"].describe().round(1).to_string())
print("\nTop-100 recommendation_score stats:")
print(top100["recommendation_score"].describe().round(1).to_string())

pure_ret  = (top100["retrieval_score"] > 60) & (top100["recommendation_score"] == 0)
both_sigs = (top100["retrieval_score"] > 40) & (top100["recommendation_score"] > 20)
rec_dom   = top100["recommendation_score"] > top100["retrieval_score"]

print(f"\nIn Top-100:")
print(f"  retrieval>60 AND rec==0 (pure retrieval): {pure_ret.sum()}")
print(f"  both retrieval>40 AND rec>20            : {both_sigs.sum()}")
print(f"  rec dominates retrieval                  : {rec_dom.sum()}")

# Candidates with strong rec but low retrieval in full pool
pool_rec_strong = df[(df["recommendation_score"] >= 40) & (df["retrieval_score"] < 20)]
pool_rc_r = pool_rec_strong.merge(ranked[["candidate_id","rank","final_score"]], on="candidate_id")
print(f"\nPool: rec>=40 + retrieval<20: {len(pool_rc_r)} candidates")
print(f"  In Top-100: {(pool_rc_r['rank'] <= 100).sum()}")
print(f"  In Top-500: {(pool_rc_r['rank'] <= 500).sum()}")
top5_rec = pool_rc_r.nsmallest(5, "rank")
print("  Best 5 of this group:")
print(top5_rec[["candidate_id","rank","retrieval_score","recommendation_score",
                 "evaluation_score","production_score","final_score"]].to_string())

# ── ISSUE 2: Evaluation Overweighting ────────────────────────
print(SEP + "ISSUE 2: Evaluation Score Overweighting")

eval_nonzero_pool  = (df["evaluation_score"] > 0).sum()
eval_nonzero_t100  = (top100["evaluation_score"] > 0).sum()
print(f"  Pool: eval>0: {eval_nonzero_pool} ({eval_nonzero_pool/len(df)*100:.1f}%)")
print(f"  Top-100: eval>0: {eval_nonzero_t100} ({eval_nonzero_t100:.0f}%)")
print(f"  Enrichment factor: {eval_nonzero_t100 / eval_nonzero_pool * len(df) / 100:.1f}x")

# Impact of eval_score: compare two hypothetical equal-retrieval candidates
# one with eval=36, one with eval=0
# relevance_score formula: 0.60*ret/100 + 0.25*eval/100 + 0.15*rec/100
# + eval bonus: 0.03 if eval>=18, 0.06 if eval>=36
ret = 70
eval_high = 36
eval_zero = 0
rs_high = 0.60*(ret/100) + 0.25*(eval_high/100) + 0.03 + 0.06  # 36 >= 36 so +0.06 bonus
rs_zero = 0.60*(ret/100) + 0.25*(eval_zero/100)
# credibility same
cred = 0.5
base_high = rs_high*0.65 + (rs_high*cred)*0.35
base_zero = rs_zero*0.65 + (rs_zero*cred)*0.35
print(f"\n  Hypothetical: ret=70, cred=0.5, penalty=0")
print(f"    eval=36 -> relevance={rs_high:.4f}, final={base_high:.4f}")
print(f"    eval=0  -> relevance={rs_zero:.4f}, final={base_zero:.4f}")
print(f"    Eval-36 advantage: {base_high - base_zero:.4f} final score points")

# Candidates who are high-eval but low-production
high_eval_low_prod = top100[(top100["evaluation_score"] >= 36) & (top100["production_score"] < 25)]
print(f"\n  Top-100 candidates: eval>=36 AND production<25: {len(high_eval_low_prod)}")
print(high_eval_low_prod[["candidate_id","rank","retrieval_score","evaluation_score",
                            "production_score","specificity_score"]].to_string())

# ── ISSUE 3: Career Recency ───────────────────────────────────
print(SEP + "ISSUE 3: Career Recency — No Temporal Weighting")

# Check if we have any recency features at all
print("  Features available:", df.columns.tolist())
print("  No start_date or recency features in parquet — recency is BLIND.")

# Can we infer recency from average_tenure_months and total_months_experience?
# A candidate with total=120, average=40 has 3 long roles — possibly older work
# A candidate with total=48, average=24 may have recent work
# But there's no way to distinguish 2019-2023 from 2015-2019 from features alone
print("\n  Top-100 total_months_experience stats:")
print(top100["total_months_experience"].describe().round(1).to_string())
print("\n  Top-100 average_tenure_months stats:")
print(top100["average_tenure_months"].describe().round(1).to_string())

# ── ISSUE 4: Relevance Depth ──────────────────────────────────
print(SEP + "ISSUE 4: Relevance Depth — No Duration Weighting on Retrieval Signal")

# Does tenure depth correlate with retrieval score?
corr_ret_tenure = df["retrieval_score"].corr(df["total_months_experience"])
corr_ret_avg    = df["retrieval_score"].corr(df["average_tenure_months"])
print(f"  Correlation: retrieval_score vs total_months_experience: {corr_ret_tenure:.3f}")
print(f"  Correlation: retrieval_score vs average_tenure_months  : {corr_ret_avg:.3f}")

# Look at high-retrieval, low-tenure vs high-retrieval, high-tenure
hi_ret_lo_ten = top100[top100["average_tenure_months"] < 20]
hi_ret_hi_ten = top100[top100["average_tenure_months"] >= 40]
print(f"\n  Top-100 with avg_tenure < 20 months: {len(hi_ret_lo_ten)}")
print(f"  Top-100 with avg_tenure >= 40 months: {len(hi_ret_hi_ten)}")

# 1-role candidate vs 5-role candidate, same retrieval score
# The 1-role candidate with 100 retrieval is treated identically
# to a 5-role candidate with the same score — even though the 5-role
# candidate has breadth and the 1-role may be a keyword stuffer
one_role = df[(df["job_count"] == 1) & (df["retrieval_score"] >= 60)]
one_role_r = one_role.merge(ranked[["candidate_id","rank"]], on="candidate_id")
print(f"\n  Single-role candidates with retrieval>=60: {len(one_role_r)}")
print(f"  Of those, in Top-100: {(one_role_r['rank'] <= 100).sum()}")
print(f"  Of those, in Top-500: {(one_role_r['rank'] <= 500).sum()}")

# ── ISSUE 5: Relevance Trajectory ────────────────────────────
print(SEP + "ISSUE 5: Relevance Trajectory — Not Captured")

# No trajectory feature available in parquet
# title_progression_score only measures seniority, not domain direction
print("  title_progression_score measures seniority escalation.")
print("  It does NOT measure domain direction (toward retrieval vs away from it).")
print("  A candidate moving from Search Eng -> ML Platform -> LLM Product:")
print("  title_progression_score = high (seniority up)")
print("  retrieval_score = high (past work)")
print("  No penalty for diverging from retrieval in recent roles.")
print("\n  Top-100 title_progression_score stats:")
print(top100["title_progression_score"].describe().round(1).to_string())

# ── ISSUE 6: NLP Inflation ────────────────────────────────────
print(SEP + "ISSUE 6: NLP Inflation")

# retrieval_score picks up 'semantic_search', 'vector_search', 'ranking'
# These are genuinely shared with NLP work
# But 'ranking' also fires on ranking emails, ranking candidates, etc.
# 'search' fires on any search context

# Evidence: candidates with high retrieval but low production + low specificity
nlp_inflation_cands = top100[
    (top100["retrieval_score"] >= 60) &
    (top100["production_score"] < 22) &
    (top100["specificity_score"] < 35)
]
print(f"  Top-100 with retrieval>=60, production<22, specificity<35: {len(nlp_inflation_cands)}")
print(nlp_inflation_cands[["candidate_id","rank","retrieval_score","production_score",
                             "specificity_score","evaluation_score","evidence_support_score"]].to_string())

# What fraction of top-100 have retrieval>=60 but evidence_support<50?
unconfirmed = top100[(top100["retrieval_score"] >= 60) & (top100["evidence_support_score"] < 50)]
print(f"\n  Top-100 with retrieval>=60 but evidence_support<50: {len(unconfirmed)}")
print(unconfirmed[["candidate_id","rank","retrieval_score","evidence_support_score",
                    "production_score","specificity_score"]].to_string())

# ── ISSUE 7: Synthetic Elite Profiles ────────────────────────
print(SEP + "ISSUE 7: Synthetic Elite Profile Vulnerability")

# What score profile would a synthetic need to reach Top-10?
top10 = merged[merged["rank"] <= 10]
print("  Top-10 score profile (what a synthetic must match):")
print(top10[["rank","candidate_id","relevance_score","credibility_score",
             "negative_signal_score","final_score",
             "retrieval_score","evaluation_score","recommendation_score",
             "production_score","specificity_score","evidence_support_score"]].to_string())

# Minimum thresholds to enter Top-100
t100_min = top100[["relevance_score","credibility_score","final_score",
                    "retrieval_score","evaluation_score"]].min()
print("\n  Minimum scores in Top-100:")
print(t100_min.round(3).to_string())

# ── ISSUE 8: Signal Coherence ─────────────────────────────────
print(SEP + "ISSUE 8: Signal Coherence")

# Compare: high_eval + high_spec (coherent) vs high_eval + low_spec (incoherent)
coherent   = top100[(top100["evaluation_score"] >= 18) & (top100["specificity_score"] >= 50)]
incoherent = top100[(top100["evaluation_score"] >= 18) & (top100["specificity_score"] < 30)]
print(f"  Top-100: eval>=18 AND spec>=50 (coherent eval+specificity): {len(coherent)}")
print(f"  Top-100: eval>=18 AND spec<30  (eval without specificity):  {len(incoherent)}")

# High retrieval + high eval but low production = evaluation vocabulary without systems
voc_not_systems = top100[
    (top100["retrieval_score"] >= 60) &
    (top100["evaluation_score"] >= 18) &
    (top100["production_score"] < 22)
]
print(f"\n  Top-100: retrieval>=60, eval>=18 but production<22: {len(voc_not_systems)}")
print(voc_not_systems[["candidate_id","rank","retrieval_score","evaluation_score",
                         "production_score","specificity_score","evidence_support_score"]].to_string())

# Full score correlation matrix for top-100
print("\n  Top-100 score correlation matrix:")
corr_cols = ["retrieval_score","recommendation_score","evaluation_score",
             "production_score","specificity_score","evidence_support_score",
             "average_tenure_months","contradiction_score"]
print(top100[corr_cols].corr().round(2).to_string())

print(SEP + "DONE")
