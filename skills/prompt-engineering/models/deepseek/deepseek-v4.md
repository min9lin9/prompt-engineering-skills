---
provider: deepseek
family: deepseek-v4
version: 1
---

# DeepSeek V4 Delta

## Confirmed
- Current API model IDs include `deepseek-v4-pro` and `deepseek-v4-flash`.
- Both models support thinking and non-thinking modes; thinking is enabled by default.
- Native `reasoning_effort` values are `low`, `high`, and `max`, with default `high` in the Chat Completions reference.
- Compatibility inputs `medium` and `xhigh` may be mapped to native effort rather than rejected; callers must not present those mappings as native model levels.
- In thinking mode, `temperature`, `top_p`, `presence_penalty`, and `frequency_penalty` have no effect even if accepted for compatibility.
- With tool calls, previous `reasoning_content` should be carried forward according to DeepSeek's documented tool-loop behavior; without tools it is not required for context continuation.
- V4-Pro and V4-Flash support JSON output and tool calls; Responses API support is documented for the current V4 releases.

Official sources:
- https://api-docs.deepseek.com/guides/thinking_mode/
- https://api-docs.deepseek.com/api/create-chat-completion/
- https://api-docs.deepseek.com/updates/

## Evaluated
None yet.

## Experimental
- Whether preserving full reasoning state across all non-tool multi-turn tasks improves outcomes; official behavior does not require it, so no universal rule is promoted.

## Boundary
- Distinguish native effort values from compatibility mappings.
- Treat ignored sampling values as warnings, not effective controls, in thinking mode.
- Do not expose chain-of-thought content as a required user-facing artifact.
