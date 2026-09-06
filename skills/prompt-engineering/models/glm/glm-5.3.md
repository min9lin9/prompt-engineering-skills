---
provider: zai
model: glm-5.3
version: 1
---

# GLM-5.3 Delta

## Confirmed
- Model code is `glm-5.3`.
- GLM-5.3 is text-only with a 1M-token context window and maximum output length of 128K tokens.
- Reasoning is always enabled; `thinking.type` supports `enabled` only.
- `reasoning_effort` supports `low`, `high`, and `max`; default is `max`.
- Z.AI documents OpenAI Chat Completion, OpenAI Responses, and Anthropic Message protocol endpoints for this model.

Official source:
- https://docs.z.ai/guides/llm/glm-5.3

## Evaluated
None yet.

## Experimental
- Whether provider-recommended `max` effort for complex coding remains cost-effective across the v4 holdout set.

## Boundary
- Reject `thinking.type: disabled` for GLM-5.3.
- Do not accept `medium` or `xhigh` as native GLM-5.3 effort values unless the selected compatibility layer explicitly documents mapping behavior.
