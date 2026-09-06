---
provider: qwen
version: 1
status: confirmed-first
---

# Qwen Provider Profile

## Confirmed
- Qwen models can be served through Qwen Cloud and, for open-weight releases, through local runtimes such as Transformers, vLLM, and SGLang.
- Runtime capabilities and request parameters are not assumed to be identical across managed and local serving.
- Provider/model/runtime identity must remain separate in the Prompt Contract and Registry.
- Qwen3.8-Flash-Next is an open-weight post-trained model. Its official model card lists compatibility with Transformers, vLLM, SGLang, and related runtimes.
- The official Qwen model card distinguishes Qwen3.8-Flash-Next from the managed Qwen3.8-Flash production service; the latter adds production features such as managed long context and built-in tools.

Official sources:
- https://huggingface.co/Qwen/Qwen3.8-Flash-Next

## Evaluated
None yet. No Qwen-specific prompt strategy is promoted without v4 outcome evaluation.

## Experimental
- Whether local Qwen runtimes benefit from different instruction density than Qwen Cloud.
- Whether explicit planning scaffolds improve long-horizon coding relative to minimal success-criteria prompts.

## Boundary
- Do not infer cloud tool support from an open-weight model card.
- Do not infer local parser/tool-call behavior from Qwen Cloud behavior.
- Do not grant execution, filesystem, network, or publishing permissions.
- Task rules belong in Task Profiles; only Qwen/runtime deltas belong here.
