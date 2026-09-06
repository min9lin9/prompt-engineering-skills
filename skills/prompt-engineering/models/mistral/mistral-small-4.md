---
provider: mistral
family: mistral-4
model: mistral-small-4
version: 1
---

# Mistral Small 4 Delta

## Scope

Only Mistral Small 4 compatibility facts belong here.

## Confirmed

- Public model card: Mistral Small 4; API model identifier: `mistral-small-2603`.
- Context window: 256k tokens.
- Hybrid model combining instruct, reasoning, and coding capabilities.
- Structured outputs, function calling, built-in tools, agents/conversations, predicted outputs, document QnA, prefix, and batching are supported on documented endpoints.
- Current Mistral reasoning documentation states `mistral-small-latest` supports adjustable `reasoning_effort`, including documented `none` and `high` behavior.

Official references:
- https://docs.mistral.ai/models/mistral-small-4-0-26-03
- https://docs.mistral.ai/studio/conversations/reasoning

## Evaluated

None yet.

## Experimental

- Mapping the `mistral-small-latest` reasoning behavior to every pinned Small 4 deployment should remain conservative until integration fixtures confirm the selected endpoint/version.

## Boundary

Do not silently assume every alias or self-hosted runtime exposes the same reasoning parameter semantics as Mistral's hosted API.