---
provider: qwen
model: qwen3.8-flash-next
version: 1
---

# Qwen3.8-Flash-Next Delta

## Confirmed
- Official model ID for the open-weight repository is `Qwen/Qwen3.8-Flash-Next`.
- The model is distributed in Transformers format and is documented as compatible with Transformers, vLLM, SGLang, TokenSpeed, and related runtimes.
- It is an image-text-to-text model; vision input support is part of the model card.
- Qwen Cloud's production `Qwen3.8-Flash` is related but is not the same runtime artifact. Managed production features must not be projected onto local `Flash-Next` deployments.

Official source:
- https://huggingface.co/Qwen/Qwen3.8-Flash-Next

## Evaluated
None yet.

## Experimental
- Runtime-specific thinking/tool-call defaults should be evaluated separately for Qwen Cloud, Transformers, vLLM, and SGLang.

## Boundary
- Treat tool calling, structured output, context limits, and thinking switches as runtime-dependent unless the selected runtime documents them explicitly.
- Do not silently substitute Qwen3.8-Flash cloud behavior for Qwen3.8-Flash-Next local behavior.
