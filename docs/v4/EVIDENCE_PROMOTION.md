# v4 Evidence Promotion and Default-Switch Governance

The v4 release process separates machine-verifiable evidence from the final human release decision.

## Machine assessment

`scripts/assess_release_evidence.py` checks:

- holdout-only evidence;
- legacy / neutral / v4 strategy coverage;
- minimum repeat coverage;
- minimum provider-family and target-model coverage;
- zero hard-gate failures;
- observed score deltas.

A machine pass is necessary but not sufficient for the default switch.

## Human review

`evals/release-review.yaml` remains `status: pending` until a reviewed release report exists and material regressions are explicitly assessed. The machine assessor never edits this file.

## Registry promotion proposal

`scripts/propose_registry_promotion.py` emits a review-only JSON proposal describing which models have evidence consistent with `integration_verified` and `quality_evaluated` promotion. It never edits `registry/models.yaml`.

## Default switch

The no-flag `/prompt` route may change from legacy to v4 only in a separate pull request after:

1. machine evidence passes;
2. the release report is reviewed;
3. `material_regression_review` is approved;
4. release review status is approved;
5. support-maturity changes are reviewed independently.

## Test-fixture isolation

Files below `tests/` are never valid release evidence. Assessment/promotion scripts reject those paths by default; CI may opt in with `--allow-test-fixtures` only to test code paths.
