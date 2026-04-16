# Constraint Summary

- Venue: `ICLR`
- Output format: `md`
- Format plan: brief global summary first, then reviewer blocks
- Budget note: the bundled venue notes say ICLR's public numeric cap is not explicitly stated, so this draft is written as a full-response Markdown draft and should be compressed to the exact OpenReview/comment limit before submission
- Evidence policy: no fabricated experiments, numbers, or citations; the draft only leans on claims already visible in the paper/review bundle
- Assumption used here: the safest rebuttal is clarification-heavy and revision-oriented, without promising new experiments that are not already available

# Concern Map

## Reviewer SsEb

- Stance: weak accept
- Movability: high
- Attitude: supportive but cautious
- W1: The theory appears to depend strongly on Lipschitz continuity, but the paper does not explain clearly what this means for the experimental models or how to interpret the relevant smoothness/Lipschitz quantity in practice.
- W2: The paper should provide clearer time-complexity and runtime evidence for the proposed method.
- Q1: For the greedy approach, does the loop typically terminate early in practice?
- M1: None explicitly separated; the review is mainly about theory assumptions and practical runtime interpretation.

## Reviewer FWFM

- Stance: initially skeptical, but highly movable
- Movability: very high
- Attitude: analytical and clarification-seeking
- W1: Theorem 1 is stated for a sampled training set `S`, but the review asks whether the robustness statement is conditioned on the realized training set or on the underlying data distribution.
- W2: The same conditioning issue appears to extend to the other theoretical statements as well.
- W3: The optimistic and pessimistic robustness calculations may look heuristic; the reviewer asks how close they are to the theoretical quantity and why they are preferable to using a practical attack probe alone.
- W4: The theory-to-experiment connection is too dense, the setting feels somewhat artificial, and the practical meaning or tightness of the gauge/constants is not obvious.
- M1: The review text indicates that after reading the author response, this reviewer raised the score to `8`, so clarification appears to be the main lever here.

## Reviewer W7KQ

- Stance: positive but not fully convinced
- Movability: high
- Attitude: constructive and practically oriented
- W1: Why is greedy search the right mechanism relative to gradient-based attacks on discrete/categorical inputs, and what exactly is the implementation role of `GradAttack` in Table 1?
- W2: If a gradient method works at all, how do we know the reported difference is due to the greedy strategy rather than a weaker gradient baseline?
- W3: Table 3's robustness-improvement comparison may confound reduced `I(f;S)` with other factors; the reviewer asks whether controlling only the final impact threshold is a fair comparison.
- M1: None explicitly separated; the review is focused on attack methodology and interpretation of the defense comparison.

## OCR Ambiguities

- The review PDF is OCR-derived. The content for `FWFM` and `W7KQ` is readable, but a few symbols and variable names are noisy.
- The `FWFM` review appears to reference constants that OCR renders unclearly, likely symbols similar to `m_g` and `M_g`.
- The `FWFM` page also contains a post-response note saying the reviewer raised the score after clarification. That note should not be mistaken for part of the original pre-rebuttal concerns.

# Shared Issues Across Reviewers

- The main shared issue is not hostility; it is a request to tighten the theory-to-practice bridge.
- Two reviewers want clearer interpretation of the theoretical objects: what is conditioned on the sampled training set, what is meant by the smoothness assumption, and how the theoretical quantities should be read in practice.
- Two reviewers want clearer practical justification of the attack/assessment procedure: why greedy search is appropriate for categorical inputs, and what the empirical/runtime evidence actually shows.
- The safest response strategy is:
  - clarify scope first: this paper is about robustness assessment/validation, not a new defense mechanism
  - explicitly separate what is proved theoretically from what is estimated empirically
  - surface existing runtime/iteration evidence already present in the paper
  - promise targeted textual clarifications, definitions, and presentation fixes rather than new unsupported experiments

# Final Rebuttal Draft

We thank all reviewers for the thoughtful and constructive feedback. Our paper studies *robustness assessment* for classifiers with categorical inputs rather than proposing a new defense mechanism. We agree that the current draft can do a better job separating the theoretical statements from their practical interpretation, and we will revise the paper to make that distinction much clearer. In particular, we will sharpen the explanation of what is conditioned on the realized training set versus the underlying data distribution, make the smoothness assumption and its role more explicit, and bring the runtime/attack-comparison discussion from the appendix into the main narrative where appropriate.

More broadly, our intent is to show two things: `(i)` an information-theoretic characterization of the factors that influence adversarial vulnerability on categorical inputs, and `(ii)` an assess-by-attack framework whose optimization problem can be handled accurately under the paper's stated smoothness condition. We do **not** claim that one can generally compute exact local Lipschitz constants for arbitrary deep models in practice, nor do we claim that the optimistic/pessimistic scores are universal substitutes for every possible empirical attack protocol. We will revise the text to state these boundaries more directly.

## Reviewer SsEb

**W1. Dependence on Lipschitz continuity / practical interpretation.**

Thank you for pointing this out. We agree that the current presentation makes the theory sound more dependent on a directly measurable local Lipschitz quantity than we intended. Our theoretical development uses a smoothness condition to establish the approximation guarantee of the discrete optimization procedure; in the experiments, we instantiate the framework with standard CNN/LSTM classifiers whose decision functions satisfy the paper's smoothness setup, but we do not rely on exact per-instance estimation of a local Lipschitz constant. We will revise the paper to make this distinction explicit and add discussion clarifying what is assumed theoretically versus what is measured empirically.

**W2 / Q1. Time complexity, runtime comparison, and early stopping of the greedy loop.**

We agree this should be surfaced more clearly. The current draft already includes a time-complexity analysis and runtime evidence in the appendix: Table 4 gives the query-complexity comparison among FSGS, OMPGS, and GradAttack, Table 5 reports average running time, and Table 6 reports the average number of iterations on successfully attacked instances. These results show that FSGS often terminates in fewer iterations, but incurs the largest runtime because each iteration is more expensive; GradAttack is faster per iteration but typically requires substantially more iterations; and OMPGS offers the best trade-off overall. We will move this discussion forward and explicitly answer the practical early-stop question in the main paper.

## Reviewer FWFM

**W1-W2. What is Theorem 1 conditioned on: the realized training set or the data distribution?**

This is an important clarification. The theorem is stated for a classifier trained with a sampled training set `S` under a deterministic training paradigm, so the bound is conditioned on the realized classifier induced by that sample, while `S` itself is drawn from the underlying distribution. We agree that the current wording does not make this conditioning sufficiently explicit. In revision, we will rewrite the theorem statement and surrounding text so that the roles of the sampled training set, the induced classifier, and the underlying data distribution are separated more cleanly. We will also make the same clarification consistently for the related theoretical results.

**W3. Are the optimistic and pessimistic robustness calculations heuristic, and how should they be interpreted?**

Our goal is not to present these two quantities as arbitrary heuristics, but as two operational robustness assessments corresponding to different adversary capabilities in the discrete setting. The pessimistic version reflects a more knowledgeable adversary that can optimize both feature choice and value change, whereas the optimistic version reflects a weaker adversary with limited ability to solve the outer combinatorial optimization. We agree that this interpretation should be stated more plainly, and that the relationship between the theoretical framing and the empirical assessment procedure should be spelled out more carefully. We will revise the paper to emphasize that these are adversary-model-dependent assessment scores, not blanket claims of asymptotic equivalence to a single theoretical scalar in every regime.

**W4. The paper is dense, the setting can feel artificial, and the practical meaning of the gauge/constants is unclear.**

We appreciate this comment and agree that the current draft is overly dense. We will streamline the exposition by reducing repetition in the mutual-information discussion, clarifying the practical motivation of the theoretical quantities, and explicitly defining all constants/gauge terms at first use. We will also strengthen the bridge from theory to finite-sample empirical behavior, so the reader can see more directly why the theoretical framing matters for the experiments rather than reading the two parts as loosely connected.

## Reviewer W7KQ

**W1-W2. Why greedy search instead of a gradient method, and how should GradAttack be interpreted?**

The core reason is that the attack/assessment problem is fundamentally discrete and combinatorial: for categorical inputs, the outer optimization is over *which features to change* and the inner optimization is over *which categorical values to assign*. Gradient-based methods can still be used as practical baselines after suitable relaxation or surrogate choices, but they do not directly solve the original discrete optimization problem. This is precisely why the paper focuses on a greedy strategy with approximation guarantees under the stated smoothness condition. We include GradAttack as a practical baseline, but not as an exact optimizer for the discrete objective. We will revise the paper to explain this distinction more explicitly and to make the role of GradAttack in Table 1 clearer.

Relatedly, the existing appendix results already show that the three methods behave differently in the expected way: GradAttack is typically cheaper per iteration but often needs more iterations, while OMPGS narrows the search space more effectively and achieves a better runtime-quality trade-off. We will make this comparison more explicit so the benefit of the greedy procedure is not left implicit.

**W3. Is the Table 3 comparison fair if changing `I(f;S)` also affects other factors?**

This is a fair concern. Our intent in Table 3 is not to claim that the intervention isolates `I(f;S)` in a perfectly causal sense; rather, it is to test whether robustness changes in the direction predicted when using robustness-enhancing mechanisms that are expected to reduce model/data dependence. We agree that the current wording may over-read that evidence. In revision, we will qualify the claim more carefully and describe Table 3 as supportive empirical evidence for the predicted association, rather than as a perfectly isolated intervention on a single factor.

# Open Placeholders That Still Need Author Input

- Exact submission-time compression target: the bundled venue notes do not provide a public numeric ICLR cap, so the final text still needs to be compressed to the actual OpenReview/comment limit used in the target cycle.
- Whether to promise specific textual revisions such as moving the runtime discussion from appendix to main text.
- Whether the authors want to explicitly mention the appendix table numbers in the public response.
- Whether to keep or soften the sentence defending the mutual-information component, depending on how central the authors want that framing to remain.
- The review PDF contains a post-response update from `FWFM`; if this draft is intended to simulate an earlier-stage rebuttal, that acknowledgment should not be echoed in the final submitted text.
