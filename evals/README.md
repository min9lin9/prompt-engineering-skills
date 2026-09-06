# v4 Evaluation Framework

This directory defines the evaluation contract for Prompt Engineering Skills v4.

The framework compares three prompt-generation strategies under the same target-model conditions:

1. **legacy** — the preserved PR-006 prompt-engineering strategy.
2. **neutral** — a minimal model-neutral prompt that captures only the user's task, constraints, source boundary, and output contract.
3. **v4** — Prompt Contract + Core + Task Profile + relevant Provider/Model Delta + User Contract.

The framework does not assume v4 is better. A model-specific strategy is promoted to `Evaluated` only after target-model outcome evidence supports it.

## Evaluation layers

### Layer 1 — Static

Checks whether the generated prompt and metadata satisfy structural contracts:

- requested target model/runtime is represented correctly;
- unsupported options are not silently introduced;
- source and permission boundaries are preserved;
- output contracts are represented;
- model-specific optimization claims have evidence status.

### Layer 2 — Generator

Evaluates whether the prompt generator preserves the user's request while producing the intended strategy candidate.

### Layer 3 — Target-model outcome

Runs candidate prompts against the same target model/runtime and scores the outputs against the same rubric.

PR-008 implements the data and result contracts for all three layers. It does not call paid provider APIs and does not mark any model as integration- or quality-verified.

## Dataset split

- `cases/development.yaml` — visible cases used for framework development and debugging.
- `cases/holdout.yaml` — cases reserved for final comparison before a default switch. Do not tune prompt profiles against holdout outcomes.

Because this is an open-source repository, the holdout is process-separated rather than secret. Contributors must not use holdout scores to iteratively tune a profile and then report those same scores as final evidence.

## Baseline fairness

Every comparison must hold constant:

- target model and model version;
- provider/runtime;
- tools available to the model;
- source material;
- task input;
- output constraints;
- sampling/reasoning settings unless the evaluated compatibility question specifically concerns those settings.

If one of these differs, record the run as a different experiment rather than a direct strategy comparison.

## Result records

One result record represents one strategy candidate against one target model for one case and one repeat.

Required fields are documented in `result-schema.md`.

## Promotion rule

A rule may move from `Experimental` to `Evaluated` only when:

- the experiment is reproducible from recorded metadata;
- the evaluated task/runtime scope is explicit;
- the strategy is compared against at least the neutral baseline;
- the evidence does not depend only on the development case used to invent the strategy;
- permission/safety regressions are absent;
- the result is stored or linked in a reviewable form.

`Evaluated` means evidence exists for a bounded condition. It does not mean a strategy is universally optimal.