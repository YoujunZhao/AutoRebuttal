# Constraint Summary

- Venue: ICLR
- Response style: brief global summary followed by reviewer blocks
- Active constraint: the current ICLR author guide states that each discussion comment has a word limit, but it does not publish one fixed overall rebuttal cap; this draft is therefore kept compact and easy to split into multiple comments if needed
- Guardrail: do not invent experiments, numerical gains, or citations
- Output format: Markdown

# Concern Map

- R1: novelty appears incremental relative to GraphSAGE/GAT-style attention; no theoretical justification; baseline set is too narrow
- R3: acknowledges the idea and empirical promise, but questions novelty, clarity of the four-module presentation, and completeness of experimental comparisons
- R2: finds the writing relatively clear, but still views the novelty as incremental, asks how `K` is chosen, and requests stronger unsupervised baselines

# Shared Issues

- The novelty difference from GraphSAGE, GAT, and related prior work needs to be stated much more sharply.
- Section 3 needs a clearer roadmap that ties Algorithm 1/2, Eqs. (1)-(11), Figure 1, and the memorable global bias together.
- The current experimental evidence is stronger than some reviewers inferred, but the baseline coverage is still narrower than ideal.
- The paper should frame its justification as empirical/mechanistic unless a formal theoretical guarantee is actually provided.

# Final Rebuttal Draft

We thank the reviewers for the careful and detailed feedback. The main concerns are novelty relative to prior graph embedding methods, clarity of the method description, and the breadth of the empirical comparisons. We agree that the current draft does not communicate these points sharply enough. In the revision, we will make three concrete changes:  
(1) explicitly distinguish CADE from GraphSAGE- and GAT-style approaches by emphasizing pairwise dual encoding over positive node pairs, `K x K` bi-attention over sampled neighborhood representations, and the memorable global bias for seen nodes;  
(2) reorganize Section 3 so the data flow from positive-pair generation to dual encoding, bi-attention, and global bias is easier to follow; and  
(3) clarify the rationale for the current inductive baselines and add additional comparisons when they can be run fairly under the same unsupervised inductive protocol.  

We also want to clarify that the current submission already reports node-classification results on four datasets (`Pubmed`, `Blogcatalog`, `Reddit`, `PPI`) and link-prediction results on two datasets (`Pubmed`, `PPI`). Table 2 focuses on varying unseen ratios for `Pubmed`/`Blogcatalog`, Figure 3 reports classification on all four datasets, and Table 3 reports link prediction on `Pubmed`/`PPI`. Below we address each reviewer in detail.

## Reviewer R1
W1. We agree that the current draft does not explain the novelty clearly enough. Our intended contribution is not simply "GraphSAGE plus attention." In CADE, two nodes in a positive pair are encoded jointly: each node produces `K` candidate neighborhood-based representations, and the model computes a `K x K` similarity matrix to identify the most relevant cross-node match before forming the final pairwise outputs. This differs from GraphSAGE, which produces a single node embedding by neighborhood aggregation, and from GAT, which attends over a single node's neighborhood rather than matching representations across a positive pair in an unsupervised setting. We will revise the introduction and related-work sections to make this distinction explicit, and we will tone down any overly broad novelty wording.
W2. The reviewer is right that the current paper does not provide a formal theorem for why the extensions must work. Our intended claim is empirical and mechanistic rather than a formal guarantee. We will revise the paper to state this more carefully, strengthen the intuition around the bi-attention matching in Eqs. (1)-(6) and the support-embedding objective in Eqs. (9)-(11), and avoid wording that could be read as claiming a stronger theoretical result than we actually prove.
W3. We chose `GraphSAGE` and `Graph2Gauss` because they naturally fit the fully unsupervised inductive setting studied in the paper, and we included raw features as an additional anchor. That said, we agree that the baseline set is narrower than ideal. We will clarify this design choice in the revision and broaden the empirical positioning. If compatible additional runs finish in time, we will report them as `[RESULT-TO-FILL]` for methods such as `DeepWalk`, `Node2Vec`, `DGI`, or other relevant baselines under a matched protocol. If those runs cannot be completed fairly within the discussion window, we will narrow the wording of our claims so that they refer to the currently evaluated strong inductive baselines rather than implying a broader universal comparison.

## Reviewer R3
W1. Thank you for summarizing both the strengths and the core novelty concern. We agree that the term "dual" needs to be explained more carefully. In our paper, "dual" refers to jointly encoding both nodes of a positive pair and learning a pairwise match between their multiple sampled representations; it does not refer to a primal/dual graph construction as in other prior work. We will make this distinction explicit and discuss the relation to the closest prior work more carefully. We will also sharpen the contrast to GraphSAGE and GAT: GraphSAGE yields a single neighborhood-aggregated embedding, while our method builds multiple candidate representations and uses pairwise bi-attention to select informative cross-node matches; GAT applies attention within one node's neighborhood, while our attention is between two nodes' sampled representations in an unsupervised positive-pair setting.
W2. We agree that the presentation of Section 3 can be improved substantially. In the revision we will add a short roadmap paragraph at the start of the model section, explicitly separate the four components of the method, enlarge and better explain Figure 1, and remove the sense of redundancy between Algorithm 2 and Eqs. (2)-(6) by clarifying that the equations define the scoring and aggregation operations while the algorithm gives the end-to-end data flow. We will also define symbols once and keep the notation consistent across Sections 3.1-3.4.
W3. We appreciate the request for stronger empirical context. We want to clarify that the submission does not evaluate only two benchmarks: for node classification, the paper reports `Pubmed`, `Blogcatalog`, `Reddit`, and `PPI`, while Table 3 additionally reports link prediction on `Pubmed` and `PPI`. However, we agree that the baseline coverage can be stronger, especially for unsupervised graph representation learning. We will add a clearer explanation of why the current paper emphasizes the unsupervised inductive setting, and, where the protocol is compatible, we will add additional comparisons such as `DGI` as `[RESULT-TO-FILL]`. If those experiments are not completed in time, we will explicitly state this as a limitation rather than over-claiming.

## Reviewer R2
W1. We appreciate the positive comments on the writing and agree that the novelty distinction needs to be sharper. Relative to unsupervised `GraphSAGE`, the proposed method does not only average multiple channels: it learns multiple candidate representations for both nodes in a positive pair, uses pairwise bi-attention to identify the most relevant cross-node match, and introduces a memorable global bias to preserve identity information for seen nodes while still generalizing inductively to unseen nodes. We will revise the paper so that these differences are stated earlier and more concretely.
Q1. In the submitted experiments, we set `K = 10` for `CADE-MS` and `CADE-MA` (Section 4.2). The paper also includes a sensitivity study of the effective second-layer sampling budget in Figure 4, where CADE-MS remains consistently stronger than GraphSAGE across a broad range of settings. We agree, however, that an ablation isolating `K` more directly would be valuable. If we can complete that run in time, we will report it as `[RESULT-TO-FILL]`; otherwise, we will clarify in the paper that the current submission studies the combined sampling budget rather than a pure one-factor `K` ablation.
W2. We agree that additional unsupervised baselines would improve the experimental section. Our current choice focused on methods that align most directly with the unsupervised inductive setting, whereas `DeepWalk` and `Node2Vec` are primarily transductive. We will make this protocol distinction explicit and, where a fair comparison can be implemented, add those results as `[RESULT-TO-FILL]`. If not, we will revise the text to state more clearly that the present empirical claim is about the inductive setting studied in this paper.

# Open Placeholders

- `[RESULT-TO-FILL]` for additional baseline comparisons such as `DGI`, `DeepWalk`, and `Node2Vec` under a fair matched protocol
- `[RESULT-TO-FILL]` for a cleaner `K` ablation if an isolated run is completed in time
- `[TABLE-PLACEHOLDER]` for an expanded baseline table if additional runs are added during the discussion phase
