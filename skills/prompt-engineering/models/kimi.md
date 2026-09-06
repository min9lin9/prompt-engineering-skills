---
provider: moonshot
version: 1
status: confirmed-first
---

# Kimi Provider Profile

## Confirmed
- Kimi API is OpenAI Chat Completions compatible at `https://api.moonshot.ai/v1`.
- Provider compatibility does not imply every OpenAI model parameter is supported by every Kimi model.
- Tool use, reasoning controls, structured output, and multimodal inputs are model-specific capabilities.
- Complete assistant messages may contain state needed for subsequent reasoning/tool turns and should not be reduced to final text unless the selected model documentation says that is safe.

Official sources:
- https://platform.kimi.ai/docs/api/overview
- https://platform.kimi.ai/docs/guide/kimi-k3-quickstart

## Evaluated
None yet.

## Experimental
- Whether Kimi K3 benefits from reduced procedural scaffolding for long-horizon coding and knowledge work.

## Boundary
- Do not transfer K2.6 thinking toggles to K3.
- Do not assume OpenAI-compatible request syntax means identical reasoning semantics.
- Provider profiles cannot expand execution or write permissions.
