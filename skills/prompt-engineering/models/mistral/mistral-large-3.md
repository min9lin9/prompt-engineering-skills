---
provider: mistral
family: mistral-3
model: mistral-large-3
version: 1
---

# Mistral Large 3 Delta

## Scope

This delta records Mistral Large 3 compatibility facts only.

## Confirmed

- Public model card name: Mistral Large 3; current API model alias family includes `mistral-large-2512`.
- Context window: 256k tokens.
- Multimodal general-purpose model.
- Structured outputs, function calling, chat completions, agents/conversations, document QnA, prefix, and batching are supported on documented endpoints.

Official reference:
- https://docs.mistral.ai/models/mistral-large-3-25-12

## Evaluated

None yet.

## Experimental

- No model-specific prompt strategy is promoted yet.

## Boundary

Do not infer adjustable `reasoning_effort` support for Large 3 from Medium 3.5 or Small 4 documentation.