# Venue Policies

Last verified: 2026-04-10

User-provided constraints always override bundled defaults.

## Quick Matrix

| Venue | Cycle | Public response limit | Important notes | Official source |
| --- | --- | --- | --- | --- |
| ICLR | 2026 | numeric limit not publicly stated in the author guide; word limit exists per comment | multiple comments allowed; during discussion the main paper may expand to 10 pages; changes must be clearly communicated | https://iclr.cc/Conferences/2026/AuthorGuide |
| ICLR | 2025 | numeric limit not publicly stated in the author guide; word limit exists per comment | multiple comments allowed; authors may revise title, abstract, content, and supplementary material during discussion; remain civil and considerate | https://iclr.cc/Conferences/2025/AuthorGuide |
| NeurIPS | 2025 | 10,000 characters per review | no additional files; no links in rebuttal; do not reveal identifying information; no paper or supplement revisions during rebuttal | https://nips.cc/Conferences/2025/PaperInformation/NeurIPS-FAQ |
| ICML | 2026 | 5,000 characters per round | rebuttal, reviewer follow-up, and author follow-up all use 5,000-character rounds; do not revise the paper or supplement during discussion | https://icml.cc/Conferences/2026/PeerReviewFAQ |
| ICML | 2025 | 5,000 characters per round | similar three-round response structure; reviewer instructions emphasize brief, targeted clarification | https://icml.cc/Conferences/2025/ReviewerInstructions |
| AAAI | project preset | 2,500 characters per reviewer | project default requested by user; verify against the current official venue before submission | user-configured default |
| CVPR / ICCV / ECCV | project preset | one-page rebuttal-PDF equivalent | project default: short summary to all reviewers, then reviewer blocks; verify exact yearly official format before submission | user-configured default |
| ARR / ACL / EMNLP | 2026 guidance | numeric limit not publicly stated in ARR guidance | text only; no external links or images; minor add-on experiments only when directly requested; focus on factual errors and serious misunderstandings | https://aclrollingreview.org/authors |
| OpenReview default rebuttal form | generic | 2,500 characters | this is the default form template only; venues can override it | https://docs.openreview.net/reference/default-forms/default-rebuttal-form |

## Usage Rules

### ICLR

- Prefer iterative discussion style over one giant block.
- If the venue year is ICLR 2025 or 2026, note that paper updates may be possible during discussion, but the changes must be communicated clearly.
- Because the public numeric cap is not stated in the author guide, use the user's explicit limit when available.

### NeurIPS 2025

- Treat the response as per-review.
- Avoid links and attached files.
- Do not promise a revised manuscript during rebuttal.

### AAAI

- Default to per-reviewer formatting.
- Use `2500` characters per reviewer as the current project preset unless the user overrides it.
- Keep the response extremely dense and point-to-point.

### ICML 2025 / 2026

- Keep each round concise and tightly scoped.
- Because the budget is 5,000 characters, shared-issue compression matters.
- Avoid treating rebuttal as a full revision letter.

### CVPR / ICCV / ECCV

- Default to a short summary to all reviewers first, then reviewer-by-reviewer blocks.
- Use `W1 / W2 / W3` point-to-point structure inside each reviewer block.
- Treat the overall space as roughly a one-page rebuttal-PDF equivalent unless the user provides a stricter explicit limit.

### ARR / ACL / EMNLP

- Keep the response text-only.
- Focus on factual correction and clarification.
- Do not over-index on extra experiments unless directly requested and realistically feasible.

### Generic Fallback

If the venue is not covered:

1. prefer explicit user constraints
2. otherwise draft conservatively
3. clearly say that the exact official rule still needs verification
