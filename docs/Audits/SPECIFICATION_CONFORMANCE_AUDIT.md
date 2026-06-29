# Specification Conformance Audit

## Objective
Determine whether implementing the multiplicative evaluation formulation will make the production implementation exactly match the documented `FINAL_RANKING_DESIGN.md` architecture.

## Line-by-Line Mathematical Component Comparison

### Component 1: Base Domain Relevance
- **Specification (`FINAL_RANKING_DESIGN.md`)**: `Base_Domain = Primary + 0.2 * Secondary`
- **Current Implementation (`rank_candidates_v3.py`)**: `raw = np.maximum(r, rec) * 0.75 + e * 0.25`
- **Classification**: **INTENTIONAL DESIGN CHANGE**
- **Why they differ**: The calibration phase (documented in `CALIBRATION_REPORT.md`) intentionally stripped the `0.2 * Secondary` breadth bonus and artificially capped the `max` score at 0.75 to balance domain distributions and stabilize Gold Pair accuracy. The specification document was never updated to reflect these calibrated reality.
- **Will changing it restore conformance?**: Yes, but at the cost of breaking the calibrated weights.

### Component 2: Evaluation Score
- **Specification**: `Relevance = min(1.0, Base_Domain * (1 + 0.5 * eval))`
- **Current Implementation**: `raw = ... + e * 0.25` with `eval_bonus = 0.0`
- **Classification**: **IMPLEMENTATION DRIFT**
- **Why they differ**: The additive evaluation bonus was stripped out during calibration to fix score instability. The engineer was supposed to implement the multiplicative amplifier (`1 + 0.5 * eval`), but drifted by leaving `e * 0.25` directly inside the base score calculation and setting `eval_bonus` to `0.0`.
- **Will changing it restore conformance?**: Yes.

### Component 3: Credibility Weights
- **Specification**: `Credibility = 0.4 * prod + 0.4 * spec + 0.2 * evid`
- **Current Implementation**: `0.40 * p + 0.35 * s + 0.25 * e` with a `-0.05` unsupported claims penalty.
- **Classification**: **INTENTIONAL DESIGN CHANGE**
- **Why they differ**: The codebase explicitly shifted weights to rely more heavily on `evidence_support_score` (0.25) to penalize generative text and keyword stuffers.
- **Will changing it restore conformance?**: Yes.

### Component 4: Final Score Architecture
- **Specification**: `Final_Score = Relevance * Credibility * Penalty_Multiplier`
- **Current Implementation**: `base = relevance * 0.55 + (relevance * credibility) * 0.45` and `final = (base - additive_penalties)`
- **Classification**: **IMPLEMENTATION DRIFT**
- **Why they differ**: `FINAL_RANKING_DESIGN.md` explicitly demands a pure multiplicative product to obliterate synthetic keyword stuffers. The code implements a hybrid linear sum, failing to fully enforce the design.
- **Will changing it restore conformance?**: Yes.

---

## Regression Check Results
If the multiplicative evaluation formulation (`Base_Domain = Primary + 0.2 * Secondary` and `Relevance = Base_Domain * (1 + 0.5 * eval)`) is restored:
- **Gold Pair accuracy does not decrease**: **FAILED**. 7 critical Gold Pairs fail immediately (e.g. "Moderate Prod Search vs Max Keyword Prototype").
- **Validation suite still passes**: **FAILED**.
- **Top 100 overlap**: The specification's logic completely scrambles the carefully calibrated `v3` baseline because it restores vulnerabilities to keyword stuffers.

---

## Final Decision
**DO NOT IMPLEMENT**

---

## Mandatory Double Check

1. **What was originally believed?** Restoring the multiplicative evaluation bonus would seamlessly fix a minor bug and align the code with the architecture.
2. **What was actually verified?** The production codebase `v3` and the `FINAL_RANKING_DESIGN.md` specification are entirely mathematically divorced. The codebase relies on fragile, highly calibrated additive weights to pass Gold Pairs.
3. **Was any assumption incorrect?** Yes. We assumed the rest of the codebase adhered to the specification. It does not.
4. **Does the implementation currently differ from the specification?** Yes, completely. Base domain weights, credibility weights, penalty logic, and final composition logic all differ.
5. **Will this change restore architectural conformance?** No. Changing only the evaluation formula to match the spec breaks the surrounding calibrated math and causes catastrophic Gold Pair failures. Restoring full architectural conformance would require rewriting the entire ranking script and recalibrating all weights from scratch.
6. **Does this introduce any new behavior not described in the architecture?** No, it attempts to enforce the architecture, but the architecture itself breaks the production validation suite.
7. **Does this reduce implementation debt?** No. It introduces severe regression debt.
8. **Should this be merged?** Absolutely not.
9. **Confidence**: Absolute. The validation suite definitively proves that the theoretical specification cannot safely be overlaid onto the currently calibrated codebase.
