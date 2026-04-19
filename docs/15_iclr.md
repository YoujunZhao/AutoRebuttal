# Constraint Summary

- Venue: `ICLR`
- Output format: `md`
- Input assumption: `150.pdf` is the paper and `15.pdf` is an OpenReview export containing the decision page plus three official reviews.
- Formatting assumption: follow the repo's ICLR default of a short global summary first, then reviewer-by-reviewer blocks.
- Safety assumption: do not promise new experiments, new theorems, or new numerical gains that are not already supported by the paper.

# Concern Map

## Shared issues across reviewers

1. Clarify the role and scope of the smoothness / Lipschitz assumption.
2. Distinguish theorem-level guarantees from what is empirically validated.
3. Explain the greedy-search family more concretely, including runtime / iteration tradeoffs.
4. Make Table 3's claim more calibrated: it is empirical corroboration, not a clean causal isolation of `I(f;S)`.

## Reviewer-by-reviewer concerns

### Reviewer SsEb

- Main concern: the theory appears to rely heavily on Lipschitz continuity, and the paper does not clearly explain what the local Lipschitz quantities look like in the experiments.
- Main request: add time-complexity and runtime discussion, and clarify whether the greedy loop tends to stop early.
- Signal: weak accept / marginally above threshold; likely movable with targeted clarification.

### Reviewer FWFM

- Main concern: Theorem 1 is unclear about whether the statement is over the sampled training set `S` or the underlying data distribution.
- Main concern: the pessimistic / optimistic assessments may read as heuristics unless the paper explains what they do and do not estimate.
- Main concern: the practical meaning / estimability of the smoothness constants (`m`, `M`) is unclear.
- Signal: positive overall, but wants the theory stated more carefully.

### Reviewer W7KQ

- Main concern: the implementation details and role of gradient-based attack in Table 1 are not sufficiently clear for discrete data.
- Main concern: Table 3 may overstate what is shown if the reduction in model/data dependence is not isolated cleanly.
- Signal: positive on novelty, but wants sharper methodological explanation.

# Shared Issues

- The paper already states the core scope carefully enough to support a calibrated response:
  - Section 3.3 says the guarantees are for solving the pessimistic / optimistic assessment objectives via greedy search under the smoothness condition.
  - The paper does **not** need to claim exact robustness certification for arbitrary classifiers without qualification.
- Existing evidence for runtime / early stopping is already in the appendix:
  - Appendix F.3, Table 4 gives query complexity.
  - Appendix F.3, Table 5 gives running time.
  - Appendix F.3, Table 6 gives average iterations.
- Existing evidence for the interpretation of pessimistic vs optimistic assessment is already in the paper:
  - Section 3.2 distinguishes knowledgeable vs oblivious adversaries.
  - Observation 1 ties the pessimistic assessment at `Gamma = 0` to an empirical estimate of expected adversarial risk.
- Existing evidence for the enhancement story is already present but should be framed cautiously:
  - Table 3 reports assessment changes after robustness-enhancement methods.
  - It supports empirical consistency with the theory's model-dependence factor, but not a pure isolated intervention on `I(f;S)`.

# Final Rebuttal Draft

## Summary to all reviewers

We thank the reviewers for the careful reading and constructive feedback. Our paper studies robustness assessment for classifiers with **categorical** inputs, where adversarial modification is inherently combinatorial and standard continuous-space robustness analyses do not directly apply. The paper makes three main claims:  
(1) Theorem 1 characterizes adversarial vulnerability through three factors: input informativeness, perturbed-feature sensitivity, and the information geometry of the classifier.  
(2) Under a mild smoothness condition, the pessimistic and optimistic assessment problems can be cast as weakly submodular maximization problems (Theorem 2), which yields approximation guarantees for the proposed greedy-search solvers (Theorems 3 and 4).  
(3) The experiments on real-world categorical datasets support the predicted trends, including the gap between knowledgeable and oblivious adversaries, the role of feature informativeness, and the effect of robustness-enhancement methods.

We agree that the presentation can better separate **what is theoretically guaranteed** from **what is empirically corroborated**. In the revision, we will make this distinction much more explicit. In particular, we will clarify that our guarantees are conditional on the smoothness assumption and concern the **quality of solving the assessment objective**, rather than claiming an unconditional exact certification result for arbitrary models. We will also surface the existing complexity and runtime analysis more prominently, and tighten the wording around Table 3 so it is presented as empirical corroboration rather than a clean causal isolation of `I(f_y;S)`.

## Reviewer SsEb

**W1. Dependence on Lipschitz continuity / local Lipschitz quantities.**  
We agree that the role of the smoothness assumption should be stated more explicitly. Our theoretical guarantees are indeed conditional on the smoothness condition introduced in Section 3.3. The point of this assumption is to connect the assessment objectives to weak submodularity and thereby obtain approximation guarantees for greedy search. We do **not** intend to claim that arbitrary models admit the same guarantee without qualification. The paper already states that any classifier with a finite Lipschitz constant satisfies the smoothness condition and notes that, in practice, `M_(Omega,zeta)` can be related to a local Lipschitz constant and `m_(Omega,zeta)` to a local strong-convexity constant (Section 3.3). We will revise the text to make this interpretation more explicit and to clarify that the empirical section validates the implications of the theory rather than directly estimating these local constants for every experimental instance.

**W2. Time complexity and running time comparison.**  
This analysis is already included in Appendix F.3, and we agree it should be surfaced more clearly. Table 4 gives the query complexity of FSGS, OMPGS, and GradAttack. Tables 5 and 6 then report runtime and iteration behavior. The results show the intended tradeoff: FSGS has the largest per-iteration cost but tends to terminate in fewer iterations; OMPGS achieves a much better runtime/query tradeoff while maintaining similar assessment behavior; GradAttack is faster per iteration but requires more iterations and yields weaker assessment quality. We will move this discussion into the main text or reference it more prominently.

**Q1. Does the greedy loop break early in practice?**  
Yes. Appendix F.3, Table 6 reports the average number of iterations, and the accompanying discussion states that FSGS generally stops earlier than OMPGS and GradAttack. The paper further explains that this is because FSGS evaluates all candidate features and therefore tends to obtain larger marginal gain per iteration, albeit at higher query cost. We will make this early-stopping behavior clearer in the main paper.

## Reviewer FWFM

**W1. What exactly is Theorem 1 with respect to: the sampled training set or the underlying distribution?**  
Thank you for pointing out that this is easy to misread. The intent of Theorem 1 is to characterize the adversarial risk of a classifier trained on a sampled set `S`, where `(x, y)` and `S` are drawn from the same underlying data-generating distribution. The theorem is not meant to be read as a finite-sample concentration statement over repeated draws of `S`, nor as an asymptotic convergence claim. We will revise the statement and surrounding discussion to distinguish more clearly between the sampled training set, the induced trained classifier, and the expected adversarial risk over the data distribution.

**W2. Are the pessimistic and optimistic assessments heuristic?**  
Our intent is that they are two operational assessment settings, not two ad hoc heuristics. Section 3.2 defines them through different adversary models: a knowledgeable adversary for the pessimistic assessment and an oblivious adversary for the optimistic assessment. Observation 1 further ties the pessimistic score at `Gamma = 0` to an empirical estimate of expected adversarial risk. At the same time, we agree that the paper should not suggest a stronger claim than it proves: we do not prove that these two scores converge to a single asymptotic target as sample size grows. We will revise the wording to present them as two theoretically motivated assessment regimes rather than as asymptotically equivalent estimators.

**W3. Can the smoothness constants be estimated in practice?**  
We agree this deserves a clearer explanation. Section 3.3 already notes that `M_{Ω_ζ}` can be computed as a local Lipschitz constant and `m_{Ω_ζ}` as a local strong-convexity constant (for `f` or `-f`, depending on the sign convention in the definition). In the current paper, however, these constants primarily play a theorem-level role in establishing solvability and approximation quality; we do not directly estimate them in the empirical study. We will state this more explicitly and avoid leaving the impression that the experiments rely on directly measuring these constants.

## Reviewer W7KQ

**W1. What is the role of the gradient-based attack in Table 1 for discrete data?**  
We agree that this comparison should be explained more clearly. In Table 1, GradAttack is included only as a baseline for the pessimistic assessment setting; it is not the main assessment method proposed in the paper. Our main solvers are FSGS / RandGS and OMPGS / RandOMPGS. For discrete inputs, the gradient is used as a guidance signal on the relaxed / indicator-based representation to rank candidate modifications, whereas the final perturbation remains discrete. This is also the reason the paper emphasizes that OMPGS computes gradients with respect to the binary indicator variables rather than directly with respect to categorical values. We will clarify this point and sharpen the distinction between gradient-guided baselines and the proposed assessment algorithms.

**W2. Is Table 3 a fair test of the effect of reducing model / dataset dependence?**  
This is a fair concern, and we agree our wording can be more careful. Table 3 is intended as empirical evidence that robustness-enhancement methods which reduce model dependence are accompanied by improved robustness assessment scores. It is **not** intended as a claim that the table isolates `I(f_y;S)` as a single controlled causal factor. We will revise the discussion to present Table 3 as empirical corroboration of the theory's qualitative prediction, rather than as a direct causal identification result.

# Open Placeholders That Still Need Author Input

- If the authors have explicit empirical estimates or bounds for local Lipschitz / smoothness constants, they can be inserted into the responses to Reviewer SsEb and Reviewer FWFM. Otherwise, the safer version is the clarification-only wording above.
- If the authors want a stronger response on runtime, they can optionally quote a small subset of the Appendix F.3 numbers from Tables 5 and 6 directly in the final rebuttal.
- The OCR for Reviewer W7KQ's recommendation line is noisy, so the rebuttal above avoids relying on a specific recovered score.
