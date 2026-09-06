---
provider: moonshot
model: kimi-k3
version: 1
---

# Kimi K3 Delta

## Confirmed
- API model ID is `kimi-k3`.
- Kimi K3 has thinking mode always enabled.
- Top-level `reasoning_effort` supports `low`, `high`, and `max`; default is `max`.
- K3 supports a 1M-token context window and native visual understanding.
- For multi-turn reasoning/tool workflows, the complete assistant message returned by the API should be passed to the next request rather than preserving only `content`.
- Structured output supports JSON Schema with strict mode; parse final `message.content`, not `reasoning_content`.

Official source:
- https://platform.kimi.ai/docs/guide/kimi-k3-quickstart

## Evaluated
None yet.

## Experimental
- Task-specific effort defaults are not yet established. Do not automatically map all difficult tasks to `max` without eval evidence.

## Boundary
- `medium` is not a valid native K3 reasoning effort.
- Thinking cannot be disabled for K3.
- K2.6 thinking controls are not K3 controls.
