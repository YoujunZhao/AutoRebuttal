# AutoRebuttal Autoexperiment Design

## Goal

Add an `autoexperiment` parameter that lets AutoRebuttal automatically trigger a supplementary evidence lane when reviewers ask for new experiments.

The evidence lane should be exposed as a first-class command surface:

- `/experiment-bridge`

## Why This Exists

The current workflow can identify experiment requests and insert `XX` or `[RESULT-TO-FILL]` placeholders, but it cannot yet escalate those requests into a structured experiment run workflow.

This gap matters because many rebuttals live or die on supplementary evidence rather than wording alone.

## Recommended Approach

Use a bounded, workflow-level experiment bridge instead of pretending the rebuttal engine itself can directly run arbitrary ML code.

That means:

- add `autoexperiment=true|false` to the main rebuttal surfaces
- normalize it into draft/revision bundles
- add a new `/experiment-bridge` command
- add a helper script that extracts experiment requests from review text into an experiment bundle
- if `autoexperiment=true`, the rebuttal workflow can hand off to the bridge before final drafting

## Rejected Alternatives

### 1. Docs-only parameter

Rejected because the user explicitly wants the workflow to auto-run supplementary experiments, not just advertise a flag.

### 2. Hardwire a full experiment runner into AutoRebuttal

Rejected because this repository is a rebuttal workflow package, not a paper-specific training/evaluation framework. A direct runner would either be fake or dangerously overclaim.

## Honest Execution Boundary

`autoexperiment=true` means:

- detect reviewer requests for new empirical evidence
- build an experiment bundle
- route that bundle through `/experiment-bridge`

It does **not** mean AutoRebuttal may fabricate experiment results.

If there is no runnable experiment workspace, no detectable experiment entrypoint, or no paper code to execute, the workflow must:

- report the blocker clearly
- preserve placeholders such as `XX` or `[RESULT-TO-FILL]`
- continue drafting honestly

## Scope

This feature should touch:

- `/rebuttal`
- `/rebuttal_revise`
- README / README.zh-CN
- skill contract and input contract
- a new `/experiment-bridge` command
- a new experiment request bundle helper
- tests for parameter parsing and docs surfaces

## Non-Goals

- no promise of generic experiment execution for arbitrary codebases
- no fabricated results
- no new dependency unless required by the existing repo toolchain

## Success Criteria

- callers can pass `autoexperiment=true`
- the bundle builders preserve a normalized `auto_experiment` flag
- `/experiment-bridge` exists and is documented
- the repo documents the bounded execution behavior honestly
- tests lock the new contract in place
