---
provider: xai
family: grok-4
model: grok-4.6
version: 1
---

# Grok 4.6 Delta

## Scope

Only differences that materially affect Grok 4.6 compatibility belong here. Core and Task rules remain authoritative for general prompt behavior.

## Confirmed

- Model ID: `grok-4.6`.
- Context window: 500,000 tokens.
- Modalities: text and image input; text output.
- Reasoning effort: `low`, `medium`, `high`, `xhigh`; default `high`.
- Reasoning cannot be disabled.
- Function calling and structured outputs are supported.
- Responses API and Chat Completions are supported.
- `presencePenalty`, `frequencyPenalty`, and `stop` are incompatible with reasoning models.

Official references:
- https://docs.x.ai/developers/models/grok-4.6
- https://docs.x.ai/developers/model-capabilities/text/reasoning

## Evaluated

None yet.

## Experimental

- Whether explicit tool-use guidance improves quality at lower reasoning effort requires evaluation.

## Boundary

Do not add `none` as a reasoning effort, silently coerce incompatible sampling parameters, or claim that prompt caching is active unless the runtime request actually provides the relevant cache key/header.