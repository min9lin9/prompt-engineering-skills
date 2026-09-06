---
provider: minimax
family: minimax-m2
model: MiniMax-M2.7
version: 1
---

# MiniMax M2.7 Delta

## Scope

Only M2.7 compatibility facts belong here. General prompting remains in Core and Task profiles.

## Confirmed

- Model ID: `MiniMax-M2.7`; high-speed sibling: `MiniMax-M2.7-highspeed`.
- Context window: 204,800 tokens in the official AI SDK model table.
- M2.7 is a reasoning model and is recommended with streaming output.
- Tool calling is supported.
- OpenAI-compatible and Anthropic-compatible protocols are available.
- Multi-turn function-call conversations should append the complete model response to preserve reasoning continuity.
- The current native text API documents JSON-schema `response_format` for `MiniMax-Text-01`, not M2.7; do not mark M2.7 structured output as confirmed without runtime-specific evidence.

Official references:
- https://platform.minimax.io/docs/guides/models-intro
- https://platform.minimax.io/docs/api-reference/text-post
- https://platform.minimax.io/docs/api-reference/text-ai-sdk

## Evaluated

None yet.

## Experimental

- Whether explicit 'direct answer' versus 'deeper reasoning' instructions materially improve M2.7 cost/quality should be tested by task family.

## Boundary

Do not invent a `MiniMax-M3` model identifier. Do not infer OpenAI-style reasoning-effort parameters or structured-output guarantees unless documented for the selected runtime.