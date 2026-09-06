---
provider: openai
version: 1
verified_at: 2026-09-06
---

# OpenAI Provider Profile

## Scope
Provider-level facts shared by OpenAI models. Task behavior belongs in Task Profiles; model-specific differences belong in model deltas.

## Confirmed
- Keep prompt text separate from runtime configuration such as model ID and reasoning settings.
- Resolve supported reasoning values from `registry/models.yaml`; do not assume one effort scale applies to every OpenAI model.
- Use structured-output and tool capabilities only when the selected model/runtime declares them.
- The v4 registry currently uses `openai-responses` as the default runtime for GPT-6 Astra and GPT-5.6 family entries.

Official references:
- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/guides/latest-model

## Evaluated
- None yet. No provider-wide prompt strategy has passed v4 outcome evaluation.

## Experimental
- Outcome-first prompt scaffolding migrated from the legacy GPT guide is a candidate for evaluation, not a provider-wide default.
- Reduced procedural scaffolding should be compared against a neutral minimal baseline before promotion.

## Boundary
Do not duplicate Core principles here. Do not grant execute, write, publish, commit, or push permission.
