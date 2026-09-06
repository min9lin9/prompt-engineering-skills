# v4 Default Switch and Legacy Cleanup

This document defines the release transition after live evidence exists. It does not authorize the switch.

## Current state

- No-flag `/prompt` remains on the legacy route.
- `--v4` remains opt-in.
- `--shadow` remains available for comparison.
- `evals/release-review.yaml` is the human approval record.

## Transition sequence

1. Complete live holdout evaluation with legacy / neutral / v4 candidates.
2. Import judged evidence and generate a release report.
3. Pass the machine release assessment.
4. Complete explicit human material-regression review.
5. Change `evals/release-review.yaml` to approved in a reviewed change.
6. Open a dedicated default-switch PR.
7. That PR changes only the default route; it does not delete the legacy implementation.
8. Observe the v4 default with `--legacy` and `--shadow` still available.
9. Perform archive/deletion cleanup only in a later PR with independent review.

## Cleanup classes

### Preserve through observation

- `commands/prompt-legacy.md`
- `legacy/instructions/GPTs-Prompt-Generator.md`
- `legacy/instructions/Gems-Prompt-Generator.md`

### Archive candidate

- historical model-specific guides that have been decomposed into Provider / Model Delta profiles.

Archive candidates must be checked for remaining references before movement.

### Delete candidate

None are pre-approved. Deletion requires a separate cleanup PR after observation.

## Rollback

The first v4-default release must preserve an explicit `--legacy` route. A rollback can therefore restore the no-flag route to legacy without reconstructing deleted assets.

## Safety invariant

`release/default-switch-plan.yaml` and `scripts/plan_default_switch.py` are advisory/dry-run assets. They may report readiness and proposed changes but must not edit the Router, Registry, filesystem, Git history, or remote repository.
