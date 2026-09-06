---
provider: anthropic
family: claude-5
version: 1
verified_at: 2026-09-06
---

# Claude 5 Family Delta

## Scope
Claude 5 family differences that are not universal Anthropic provider rules.

## Confirmed
- `claude-opus-5` and `claude-sonnet-5` run with adaptive thinking by default.
- `claude-fable-5` and `claude-mythos-5` use adaptive thinking as the only thinking mode; disabling thinking is unsupported.
- Fable 5 and Mythos 5 do not support manual `budget_tokens` thinking or assistant prefill.
- Sonnet 5 rejects non-default `temperature`, `top_p`, and `top_k` values and removes manual extended thinking.
- Structured outputs are supported for Fable 5, Mythos 5, Opus 5, and Sonnet 5.

Official references:
- https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5
- https://platform.claude.com/docs/en/models/fable-5/migration-guide
- https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5
- https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs

## Evaluated
- None yet. Legacy Claude prompting recommendations have not been promoted through v4 outcome evaluation.

## Experimental
- Test whether short explicit scope statements outperform XML-heavy scaffolding for coding/review tasks.
- Test whether task-specific tool instructions improve tool-use recall without increasing unnecessary calls.

## Invalid combinations
- Fable 5 / Mythos 5 with `thinking: disabled`
- Fable 5 / Mythos 5 with manual `budget_tokens`
- Sonnet 5 with non-default sampling parameters

## Boundary
Do not claim access to raw chain-of-thought. Do not use model behavior to expand user permissions.
