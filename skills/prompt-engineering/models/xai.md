---
provider: xai
family: grok
version: 1
---

# xAI / Grok Provider Profile

## Confirmed

- xAI exposes Grok models through both Responses API and Chat Completions.
- Grok 4.6 supports function calling, structured outputs, web search, X search, and code execution through xAI-supported interfaces.
- Grok 4.6 supports `reasoning_effort` values `low`, `medium`, `high`, and `xhigh`; default is `high`.
- Reasoning cannot be disabled on Grok 4.6.
- Reasoning models reject `presencePenalty`, `frequencyPenalty`, and `stop`.

Official references:
- https://docs.x.ai/developers/grok-4-6
- https://docs.x.ai/developers/model-capabilities/text/reasoning
- https://docs.x.ai/developers/model-capabilities/text/structured-outputs

## Evaluated

None yet. Provider integration and target-model quality evaluation remain pending.

## Experimental

- Prompt-level guidance for balancing Grok 4.6 tool use against reasoning depth should be evaluated before becoming a default.

## Boundary

This profile describes provider/runtime facts only. It does not select Grok automatically, rank it against other models, or grant tool/runtime permissions.