# v4 Qwen / Kimi / GLM / DeepSeek Profiles

> PR-005 scope: first-class provider/model profiles for Qwen, Kimi, GLM, and DeepSeek.

## Evidence policy

Only current official provider documentation is promoted to **Confirmed**. Provider recommendations are not automatically promoted to universal prompt defaults. No prompt strategy in this PR is marked **Evaluated** because target-model outcome evaluation has not yet run.

## Qwen

Qwen3.8-Flash-Next is represented as an open-weight model whose runtime capabilities are explicitly runtime-dependent. Qwen Cloud production behavior is not silently inherited by local Transformers/vLLM/SGLang deployments.

## Kimi

Kimi K3 is modeled with always-on thinking and native reasoning efforts `low`, `high`, and `max` (default `max`). Multi-turn tool/reasoning flows preserve the complete assistant message as documented by Kimi.

## GLM

GLM-5.3 and GLM-5.3-Flash use native reasoning efforts `low`, `high`, and `max`, and thinking cannot be disabled. GLM-5.3 is text-only; GLM-5.3-Flash is natively multimodal.

## DeepSeek

DeepSeek V4-Pro and V4-Flash distinguish native reasoning efforts (`low`, `high`, `max`) from compatibility mappings (`medium`, `xhigh`). Thinking is enabled by default but can be disabled. Sampling parameters accepted for compatibility in thinking mode are not treated as effective controls when official docs state they have no effect.

## Maturity

All profiles remain:

- `spec_verified: true`
- `integration_verified: false`
- `quality_evaluated: false`

Static validation only establishes repository consistency and documented compatibility constraints; it does not imply successful live API integration or better task outcomes.
