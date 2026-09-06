---
provider: google
version: 1
verified_at: 2026-09-06
---

# Google Provider Profile

## Scope
Provider-level Gemini facts. Media/task behavior remains in Task Profiles; model-specific thinking and migration constraints belong in deltas.

## Confirmed
- Gemini 3 models use `thinking_level` rather than treating reasoning as a universal numeric token budget.
- Supported thinking levels differ by model and must be resolved from the registry/model delta.
- Structured outputs and tool capabilities are model-specific capabilities and must not be assumed for every Gemini model.
- Prompt text and generation/runtime configuration remain separate concerns.

Official references:
- https://ai.google.dev/gemini-api/docs/thinking
- https://ai.google.dev/gemini-api/docs/models

## Evaluated
- None yet. No Google-wide prompt strategy has passed v4 outcome evaluation.

## Experimental
- Legacy guidance favoring explicit context/task separators remains a candidate formatting strategy, not a provider requirement.
- Long-context placement strategies should be evaluated by task and context length before promotion.

## Boundary
Do not duplicate Task Profile media rules or convert runtime parameters into prompt prose.
