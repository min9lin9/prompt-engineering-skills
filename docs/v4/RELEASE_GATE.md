# v4 Release Gate

The v4 Router may become the no-flag `/prompt` default only after target-model outcome evidence satisfies this gate.

## Why this gate exists

The repository already validates structure, model metadata, task separation, distribution, operational permissions, and evaluation schemas. Those checks do not prove that v4 prompts outperform or match legacy/neutral prompts on real target models.

## Required evidence

The release candidate must include:

1. `legacy`, `neutral`, and `v4` strategy results;
2. holdout cases;
3. repeated runs per case;
4. exact target model/runtime metadata;
5. prompt hashes and repository/profile revisions;
6. zero user-safety / permission / source-boundary hard-gate failures;
7. sufficient provider/model coverage;
8. no material v4 regression against the neutral baseline;
9. a human-readable release report.

## Provider coverage

Initial release-gate coverage requires evidence across at least four provider families and six target models. OpenAI, Anthropic, Google, and Qwen are required families for the first default-switch decision. Moonshot/Kimi, Z.ai/GLM, DeepSeek, xAI, MiniMax, and Mistral are additional candidates and remain first-class registry targets even if they are not all required to unlock the first switch.

This threshold is a release-policy choice, not a claim that four providers are sufficient for every future version.

## Support maturity

`spec_verified` and `static_validation` may be established from documentation and static tests. `integration_verified` requires an actual runtime request. `quality_evaluated` requires reproducible target-model outcome evidence.

Do not promote a model merely because its profile or Registry entry passes CI.

## Default-switch invariant

While `evals/release-gate.yaml` has `status: blocked`, `commands/prompt.md` must keep the no-flag default as `legacy`.

Changing the Router default before release-gate approval is a CI failure.

## Approval artifact

When sufficient evidence exists, create a release report under `evals/results/<experiment-id>/summary.md`, update the release-gate manifest with that report path and verified models, and change status only after `scripts/validate_release_gate.py` passes against the recorded evidence.

The subsequent default-switch should occur in a separate PR so the evidence decision and behavior change remain independently reviewable.
