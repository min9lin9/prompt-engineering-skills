---
provider: mistral
family: mistral-3
model: mistral-medium-3.5
version: 1
---

# Mistral Medium 3.5 Delta

## Scope

Only Mistral Medium 3.5 compatibility facts belong here.

## Confirmed

- Model ID: `mistral-medium-3-5`.
- Context window: 256k tokens.
- Multimodal frontier-class model optimized for agentic and coding use cases.
- Structured outputs and function calling are supported.
- Adjustable reasoning is available through `reasoning_effort`.
- Official reasoning documentation explicitly documents `none` and `high`; `high` is recommended by Mistral for agentic and code use cases.

Official references:
- https://docs.mistral.ai/models/mistral-medium-3-5-26-04
- https://docs.mistral.ai/studio/conversations/reasoning

## Evaluated

None yet.

## Experimental

- v4 must evaluate whether `high` is appropriate as a repository default rather than inheriting the provider's use-case recommendation unconditionally.

## Boundary

A provider recommendation is not automatically a v4 quality-evaluated default. Preserve user/runtime settings when valid.