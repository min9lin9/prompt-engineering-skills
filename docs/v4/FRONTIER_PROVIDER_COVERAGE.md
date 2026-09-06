# v4 Frontier Provider Coverage — PR-006

This milestone completes the initial v4 provider-coverage set by adding xAI/Grok, MiniMax, and Mistral profiles on top of PR-005.

## Evidence policy

Only current official provider documentation is promoted to **Confirmed**. No prompt strategy in this milestone is promoted to **Evaluated**. Integration and quality maturity remain false.

## xAI / Grok

Added:
- `skills/prompt-engineering/models/xai.md`
- `skills/prompt-engineering/models/xai/grok-4.6.md`

Confirmed compatibility:
- `grok-4.6`;
- reasoning effort `low / medium / high / xhigh`;
- default `high`;
- reasoning cannot be disabled;
- function calling and structured outputs;
- Responses API and Chat Completions.

## MiniMax

The earlier registry placeholder `minimax-m3` is removed. Current official MiniMax documentation lists `MiniMax-M2.7` and `MiniMax-M2.7-highspeed` as the current M-series text models.

Added:
- `skills/prompt-engineering/models/minimax.md`
- `skills/prompt-engineering/models/minimax/minimax-m2.7.md`

Important boundary:
- OpenAI-compatible and Anthropic-compatible protocols are transport compatibility, not semantic equivalence.
- M2.7 JSON-schema structured output is not marked confirmed because the current native text API documents `response_format` support for `MiniMax-Text-01`, not M2.7.

## Mistral

Added:
- `skills/prompt-engineering/models/mistral.md`
- `mistral/mistral-large-3.md`
- `mistral/mistral-medium-3.5.md`
- `mistral/mistral-small-4.md`

Confirmed:
- Large 3, Medium 3.5, and Small 4 are current generalist models with 256k context windows.
- Structured outputs and function calling are supported on documented endpoints.
- Adjustable reasoning is documented for Medium 3.5 and the current Small path.
- Adjustable reasoning is not inferred for Large 3 merely from sibling-model documentation.

## Support maturity

All profiles added in PR-006 remain:

```yaml
integration_verified: false
quality_evaluated: false
```

Static profile validation does not imply live API integration or model-quality superiority.

## Next milestone

PR-007 rewrites `/prompt` as the v4 Router using Prompt Contract + Core + Task Profile + one relevant Model Delta, while preserving the legacy command for shadow comparison.
