---
provider: google
model: gemini-3.8-flash
version: 1
verified_at: 2026-09-06
---

# Gemini 3.8 Flash Delta

## Scope
Only Gemini 3.8 Flash behavior/runtime constraints that differ from the Google provider profile and v4 Core.

## Confirmed
- Model ID: `gemini-3.8-flash`.
- Supported thinking levels: `low`, `medium`, `high`.
- Default thinking level: `medium`.
- `minimal` is not supported and returns an error.
- Structured outputs, function calling, search grounding, file search, code execution, and URL context are supported.
- Migration guidance removes deprecated sampling parameters and replaces `thinking_budget` with `thinking_level`.

Official references:
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- https://ai.google.dev/gemini-api/docs/latest-model

## Evaluated
- None yet. No Gemini 3.8 Flash-specific prompt wording has passed v4 outcome evaluation.

## Experimental
- Test whether explicit planning instructions improve complex agent/coding tasks beyond the model's default iterative verification.
- Test whether concise output contracts reduce unnecessary verbosity without harming completion quality.

## Invalid combinations
- `thinking_level: minimal`
- Legacy `thinking_budget` as if it were the current Gemini 3.8 control

## Boundary
Do not copy Google runtime settings into prompt text or duplicate media Task Profile rules.
