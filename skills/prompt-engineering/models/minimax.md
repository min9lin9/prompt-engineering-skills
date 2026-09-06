---
provider: minimax
family: minimax-m2
version: 1
---

# MiniMax Provider Profile

## Confirmed

- MiniMax's current text-model documentation lists `MiniMax-M2.7` and `MiniMax-M2.7-highspeed` as the latest M-series text models.
- MiniMax exposes native text APIs plus OpenAI-compatible and Anthropic-compatible protocols.
- M2.7-series models are reasoning models and support tool calling.
- In multi-turn tool/function-call workflows, the complete assistant response should be preserved in history to maintain reasoning continuity.
- The current native text API documentation does not advertise JSON-schema structured output for M2.7; structured-output support must therefore be treated as runtime/model-specific rather than assumed from OpenAI compatibility.

Official references:
- https://platform.minimax.io/docs/guides/models-intro
- https://platform.minimax.io/docs/api-reference/text-post
- https://platform.minimax.io/docs/api-reference/text-openai-api
- https://platform.minimax.io/docs/token-plan/other-tools

## Evaluated

None yet.

## Experimental

- Prompt-level instructions for selecting shallow versus deep reasoning by task remain candidates for evaluation, not capability facts.

## Boundary

Protocol compatibility does not imply semantic equivalence with OpenAI or Anthropic. Do not infer structured-output, reasoning-control, or message-history behavior from protocol shape alone.