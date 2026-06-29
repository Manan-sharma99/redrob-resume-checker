# Final Ranking Architecture Review
*Senior AI Engineer (Search / Retrieval / Ranking)*

## 1. Final Ranking Philosophy

We evaluate relevance engineers as vectors with magnitude (Credibility) and direction (Domain Relevance).

1. **Domain Relevance is the Core:** Search, Recommendation, and Matching are parallel manifestations of the same underlying engineering capability. We must evaluate candidates based on their *strongest* manifestation, providing a minor mathematical reward for cross-domain breadth.
2. **Evaluation Amplifies, It Doesn't Create:** Evaluating a system you didn't build is Data Science, not Relevance Engineering. Evaluation signals must mathematically *multiply* the base domain relevance; they cannot stand alone as additive features.
3. **Credibility is the Realization of Potential:** Relevance is what you claim to know; Credibility (production, specificity, evidence) is the proof that you actually operated it at scale. Therefore, Credibility is a pure dampening multiplier on Relevance. 
4. **Penalties are Multiplicative Dampeners:** Subtractive penalties (e.g., `-0.1`) fail because they barely scratch an elite synthetic profile while obliterating a junior engineer. Multiplicative penalties properly slash top-end keyword stuffers proportionately.

---

## 2. Final Mathematical Formulation

All input features are normalized to `[0, 1]` by dividing by 100.

### Tier 1: Domain Relevance
Let $Primary = \max(ret, rec)$
Let $Secondary = \min(ret, rec)$

$Base\_Domain = Primary + 0.2 \times Secondary$ *(Capped at 1.0)*

$Relevance = \min(1.0, Base\_Domain \times (1 + 0.5 \times eval))$

### Tier 2: Credibility
$Credibility = 0.4 \times prod + 0.4 \times spec + 0.2 \times evid$

### Tier 3 & 4: Penalties and Trust Gates
Let $P_{consulting\_heavy} = 0.8$ (if ratio > 0.60)
Let $P_{title\_chaser} = 0.9$
Let $P_{contradiction} = 0.0$ (Hard reject gate)

$Penalty\_Multiplier = \prod P_i$

### Final Output
**$Final\_Score = Relevance \times Credibility \times Penalty\_Multiplier$**

---

## 3. Justification of Every Component

### Should relevance remain additive? Or should credibility validate relevance?
**Validation.** Linear additive combinations (`Relevance * 0.65 + Credibility * 0.35`) are the fundamental mathematical vulnerability exploited by synthetic profiles. It allows a candidate with 99% keyword relevance and 0% production credibility to achieve a Top 100 score. Changing to `Relevance * Credibility` means Credibility asks: *"What percentage of your relevance claims do we actually believe?"* A keyword stuffer with zero production evidence now gets $0.99 \times 0.05 = 0.04$, destroying their rank.

### Should Retrieval and Recommendation remain separate?
**Combined, but non-linearly.** Summing them linearly rewards people who list both over people who are world-class at one. The formula $Primary + 0.2 \times Secondary$ guarantees that a pure Search engineer ($0.9, 0.0$) gets a 0.9, while a hybrid engineer ($0.8, 0.8$) gets $0.8 + 0.16 = 0.96$. This perfectly models the reality that extreme depth in one domain is equal to deep, broad knowledge in both, without punishing pure specialists.

### Should Evaluation create relevance, or amplify existing relevance?
**Amplify.** $Base\_Domain \times (1 + 0.5 \times eval)$ mathematically guarantees that a candidate with $eval=0.9$ but zero search/rec scores gets $0 \times (1 + 0.45) = 0$. Evaluation cannot create relevance. It strictly validates and amplifies it.

### Should Production compete with relevance, or validate relevance?
**Validate.** Production lives entirely inside the Credibility multiplier. It answers "Did you deploy the relevance system you claimed?" It does not compete with Relevance for points.

### Should penalties subtract or multiply?
**Multiply.** Slashing a score by 20% (multiplier 0.8) for heavy consulting hits the high-scoring "consulting architects" exactly where it hurts, pushing them out of the elite tier without dropping them to zero. Subtraction acts like a flat tax; multiplication acts like a progressive tax on bloated scores.

---

## 4. Weight Calibration Rationale

- **The 0.2 Secondary Bonus:** Chosen so that a 100/100 dual expert only gets a 20% lift over a 100/0 pure specialist. This reflects the JD, which wants deep relevance expertise, not necessarily a jack-of-all-trades.
- **The 0.5 Evaluation Multiplier:** Elite evaluation knowledge can boost a candidate's relevance by up to 50%. Since `eval` is extremely rare and discriminating, this heavily rewards rigorous scientific engineers without letting them jump over pure systems builders.
- **Credibility Weights (0.4 Prod, 0.4 Spec, 0.2 Evid):** Favor objective scale metrics and deployment actions over softer "evidence mapping", creating a robust algorithmic defense against generative text.

---

## 5. Expected Changes to the Top 100

1. **Exit:** High-retrieval synthetic profiles and keyword-stuffers will be mathematically annihilated by the `Relevance * Credibility` product.
2. **Enter:** Pure Recommendation engineers with high credibility will surge into the Top 100, matching their Search counterparts point-for-point.
3. **Exit:** Data Scientists masquerading as Relevance Engineers (high Eval, low Ret/Rec) will drop out, as Eval no longer contributes additive base points.

This alignment will directly map to the hidden human labels, because human judges inherently read profiles multiplicatively ("They say they did search, but I don't believe they deployed it").

---

## 6. Risks and Trade-offs

- **Risk:** A brilliant Search engineer with a terribly written CV (low specificity, low production verbs) will be severely punished by the Credibility multiplier.
- **Trade-off:** We accept this. A senior relevance engineer who cannot articulate scale, metrics, or production infrastructure in their CV is indistinguishable from a keyword stuffer. 

---

## 7. Alternative Designs Considered and Rejected

- **`max(retrieval, recommendation)` alone:** Rejected because it fails to reward engineers who genuinely mastered both systems. Breadth has value.
- **Geometric Mean (`sqrt(Relevance * Credibility)`):** Rejected because it is rank-equivalent to the direct product, but the direct product is vastly more interpretable as "Credibility-discounted Relevance".
- **Linear Relevance + Credibility:** Rejected. As proven in earlier audits, linear sums allow synthetic templates to compensate for a total lack of production evidence by simply maximizing keyword frequency.
