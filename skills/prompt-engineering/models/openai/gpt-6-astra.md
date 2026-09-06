---
provider: openai
model: gpt-6-astra
version: 1
verified_at: 2026-09-06
---

# GPT-6 Astra Delta

## Scope
Only behavior or runtime constraints that differ materially from the OpenAI provider profile and v4 Core.

## Confirmed
- Model ID: `gpt-6-astra`.
- Supported `reasoning.effort`: `low`, `medium`, `high`, `xhigh`, `max`.
- `none` is not supported.
- For tool-calling workflows, use the Responses API path documented for Astra.
- When migrating prompts, remove unsupported sampling controls instead of trying to encode them as prompt text.

Official references:
- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra

## Evaluated
- None yet. No Astra-specific prompt wording has passed v4 outcome evaluation.

## Experimental
- Prefer explicit completion criteria over long procedural scripts for complex end-to-end work; validate against the neutral baseline before promotion.
- Minimize overlapping skill/instruction rules where possible; measure clarification rate and task completion before treating this as an optimized default.

## Invalid combinations
- `reasoning.effort: none`
- Treating unsupported runtime parameters as valid because an older GPT profile accepted them

## Boundary
This delta cannot expand permissions or override Task/Profile source constraints.
