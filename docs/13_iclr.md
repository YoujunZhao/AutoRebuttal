# Constraint Summary

- Venue: ICLR
- Output format: Markdown
- Input paper: `130.pdf` (`Dissecting Local Properties of Adversarial Examples`)
- Input review artifact: `13.pdf` (OpenReview page export; OCR-split into reviewers `Rh4T`, `JTzC`, and `CGeY`)
- Verified paper evidence used in the draft:
  - frequency-domain evidence in Fig. 1-2 / Sec. 3.1
  - spatial perturbation evidence in Fig. 3 / Sec. 3.2
  - local-response formulation in Sec. 4.1 and mechanism discussion in Fig. 4 / Sec. 4.2
  - Table 1-3 evidence on layer-wise response differences, successful-vs-failed attacks, and transferability
  - smoothness/robustness discussion in Fig. 5 / Sec. 4.4-4.5
- Active limitation: no explicit rebuttal character limit was provided, so the draft is concise but not budget-locked.
- Guardrail: no new experiments, numerical gains, or citations are invented below. When additional evidence would help, it is marked as a clarification or placeholder.

# Concern Map

| Reviewer | Main concerns | Draft move |
| --- | --- | --- |
| `Rh4T` | novelty overlap with prior work; missing comparison to stronger adversarial-training baselines; unclear meaning of `local` | acknowledge overlap in observations, sharpen novelty around the local-response view, clarify scope as analysis rather than SOTA defense, define local terms explicitly |
| `JTzC` | writing is hard to follow; several claims in Sec. 4.2/4.5 need stronger justification or softer wording; novelty vs prior work is unclear; Table 1-3 aggregation/variance unclear | editorial cleanup, sharpen claim scope, contrast with prior work, explicitly state aggregation protocol and add variance/error-bar clarification |
| `CGeY` | Section 3 appears weak relative to prior work; terms such as locally-disordered / locally-consistent / smoothness are not rigorous enough; setup may not fully answer the research question | reframe Section 3 as motivation, make Sec. 4 definitions more rigorous, narrow the claimed scope, add clearer limitations and experiment rationale |

# Shared Issues Across Reviewers

1. The main shared risk is not that the paper has no signal, but that the current draft does not separate prior observations from the paper's claimed new perspective clearly enough.
2. The strongest common fix is to recast the paper's core contribution as the **local intermediate response perspective** that connects perturbation structure, kernel smoothness, and robustness, rather than as the raw observation that robust and standard models produce different perturbation patterns.
3. The second shared fix is clarity: define `locally-consistent`, `locally-disordered`, and `local response differences` more explicitly in Sec. 4, and soften qualitative mechanism claims when they are empirical interpretations rather than formal proofs.
4. The third shared fix is experimental framing: make the setup and table aggregation protocol explicit, and clarify that the paper is an analysis paper on CIFAR-10/ResNet-18 with PGD-based evaluation, not a claim of state-of-the-art robust accuracy.

# Final Rebuttal Draft

We thank the reviewers for the careful reading and constructive feedback. We agree that the current draft can do a much better job on two fronts: (1) clearly separating what is already known from what is new in our paper, and (2) making the definitions and empirical claims in Sec. 4 more precise. Our intended contribution is not that prior work never observed differences between standard and adversarially trained models, but that we connect the frequency/spatial properties of perturbations to a **local intermediate response** view and use that view to interpret robustness, successful vs. failed attacks, transferability, and kernel smoothness in one framework. In the revision, we will make this scope explicit, sharpen the contrast to prior work, and substantially improve the writing and definitions.

## Reviewer Rh4T

**W1. Novelty relative to prior work**

We agree that some observations in Sec. 3 are related to prior work. In particular, prior papers have discussed high-frequency structure, smoother kernels in robust models, and semantically meaningful perturbations. Our intended novelty is therefore not the isolated observation itself, but the unified interpretation that links: (i) frequency and spatial perturbation structure, (ii) layer-wise local response differences, and (iii) the effect of smoother kernels on robustness and transferability. We will revise the introduction and related work to state this much more explicitly and to avoid overstating novelty for the Sec. 3 observations alone.

**W2. Comparison to stronger adversarial-training baselines**

This is a fair suggestion. Our current goal is explanatory analysis rather than claiming a new defense or state-of-the-art robust accuracy, and the current experiments are all conducted with the same CIFAR-10 / ResNet-18 / PGD setting so that the local-response comparisons stay controlled. We will clarify this scope directly in the paper. If additional baseline runs can be completed during the discussion period, we will add a compact comparison table `[TABLE-PLACEHOLDER]`; otherwise, we will avoid any wording that could be read as a claim of superiority over stronger adversarial-training methods.

**W3. Meaning of `local`**

We agree that this needs to be defined more clearly. In Sec. 4.1, our `local response difference` is the response difference obtained when corresponding local receptive-field features from a natural example and a potential/adversarial example are convolved with the same kernel. In the revision, we will move this definition forward, make the notation easier to follow, and explicitly describe `locally-consistent` perturbations as perturbations whose neighboring pixels tend to vary coherently with image structure, versus `locally-disordered` perturbations that exhibit sharper local variation. We will also make clear that this is an empirical/operational distinction used in our analysis rather than a new formal robustness definition.

## Reviewer JTzC

**W1. Writing clarity and editorial quality**

We agree with this assessment. The current draft compresses too many ideas into Sec. 3-4 and does not give the reader enough roadmap before the mechanism discussion. We will improve the writing substantially by: (i) separating observation, hypothesis, and empirical evidence more clearly, (ii) adding a short roadmap before Sec. 4, and (iii) revising long informal statements into shorter claims tied directly to figures/tables.

**W2. Claims in Sec. 4.2 / 4.5 need stronger support or softer wording**

This is also a fair point. Our goal in Sec. 4.2 and 4.5 is to provide an empirical interpretation of why perturbation structure and kernel smoothness affect robustness through local response differences, supported by Fig. 4, Table 1-3, and Fig. 5. We agree that several sentences currently read too strongly. In the revision, we will soften these statements from universal-sounding claims to empirically supported interpretations, add citations where prior work already supports the intuition, and make the boundary between evidence and conjecture explicit.

**W3. Difference from Tsipras et al. (2019) and Wang et al. (2020a)**

We appreciate this point and will revise the positioning carefully. Relative to Tsipras et al. (2019), our paper does not only contrast the visual/semantic character of perturbations, but studies how those perturbation patterns relate to layer-wise local response differences, successful vs. failed attacks, and transferability. Relative to Wang et al. (2020a), we do not only note that robust models have smoother kernels; we study how kernel smoothness interacts with perturbation locality in the induced local responses. We agree that the current draft does not explain this distinction sharply enough, and we will make this contrast explicit in the introduction, related work, and discussion.

**Q1. Are Table 1-3 averaged? Over how many samples? What is the variance?**

Thank you for pointing this out. The current captions and setup do not state the aggregation protocol clearly enough. We will revise the experimental section and table captions to explicitly report how the values in Table 1-3 are aggregated, the number of evaluated samples, and the corresponding variance / spread statistics. More importantly, we will make the purpose of these tables clearer: Table 1 compares standard vs. robust models in layer-wise local response differences, Table 2 compares successful vs. failed attacks, and Table 3 compares original vs. transferred attacks.

**M1. Figure / presentation clarity**

We will also improve figure readability and captions so that comparisons across plots are easier to follow.

## Reviewer CGeY

**W1. Section 3 overlaps with prior work**

We agree that, if read in isolation, the current Sec. 3 can appear incremental. In the revision, we will explicitly present Sec. 3 as empirical motivation for the local-response analysis in Sec. 4, not as the sole novelty claim. The main technical message we want to preserve is that the observed frequency/spatial differences become more informative when interpreted through local response differences and kernel smoothness.

**W2. Several terms are not rigorous enough**

We agree. This is one of the most important issues to fix. We will tighten the definitions of `locally-disordered`, `locally-consistent`, and `smooth` kernels, and we will clearly separate intuitive descriptions from the formal quantity we actually measure, namely the local response difference introduced in Sec. 4.1. We will also revise statements in Sec. 4.2-4.5 so that they better match the evidence currently provided by Fig. 4, Table 1-3, and Fig. 5.

**W3. Experimental setup may not fully answer the question**

We appreciate this concern. Our experiments are intentionally controlled around a single backbone/dataset/attack pipeline (ResNet-18 on CIFAR-10 with PGD-based generation/evaluation) because the goal is interpretability of the mechanism rather than broad benchmarking. We will clarify this scope and explicitly discuss the limitation that the current evidence is strongest as a controlled case study. We will also add a clearer limitations paragraph explaining what conclusions the current setup does and does not support.

# Open Placeholders That Still Need Author Input

- `[TABLE-PLACEHOLDER]` if the authors decide to add additional robust-training baseline comparisons during the discussion period.
- Exact aggregation details for Table 1-3 if they are available from logs and can be inserted directly into the rebuttal or paper revision.
- Any concrete wording for promised manuscript edits if the authors want the rebuttal to mention specific section/paragraph changes.
