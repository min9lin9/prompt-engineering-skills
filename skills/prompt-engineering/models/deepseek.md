---
provider: deepseek
version: 1
status: confirmed-first
---

# DeepSeek Provider Profile

## Confirmed
- DeepSeek V4 models are available through OpenAI-compatible and Anthropic-compatible APIs; V4-Pro and V4-Flash also support the Responses API.
- Protocol compatibility does not imply identical parameter semantics across protocols.
- V4 thinking mode is enabled by default and can be disabled through the documented protocol-specific controls.
- Native reasoning effort values are `low`, `high`, and `max`; compatibility layers may map other values onto these native levels.
- Thinking-mode sampling parameters such as temperature/top_p are documented as ineffective even when accepted for compatibility.

Official sources:
- https://api-docs.deepseek.com/
- https://api-docs.deepseek.com/guides/thinking_mode/
- https://api-docs.deepseek.com/updates/

## Evaluated
None yet.

## Experimental
- Whether Responses API or Anthropic-compatible transport materially changes prompt strategy for equivalent tasks.

## Boundary
- Keep transport compatibility separate from prompt behavior.
- Do not assume ignored compatibility parameters changed generation behavior.
- When tools are present, preserve reasoning state according to DeepSeek's documented multi-turn rules.
- Provider profiles cannot grant execution or write permissions.
