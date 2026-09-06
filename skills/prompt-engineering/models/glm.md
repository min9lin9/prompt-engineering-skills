---
provider: zai
version: 1
status: confirmed-first
---

# GLM Provider Profile

## Confirmed
- Z.AI exposes GLM models through provider-native and compatibility protocols documented per model.
- Runtime protocol selection and model capability selection are separate concerns.
- GLM-5.3 documents OpenAI Chat Completions, OpenAI Responses, and Anthropic Message protocol endpoints.
- Reasoning controls must be validated per model rather than assumed from protocol compatibility.

Official sources:
- https://docs.z.ai/guides/llm/glm-5.3
- https://docs.z.ai/guides/vlm/glm-5.3-flash

## Evaluated
None yet.

## Experimental
- Whether explicit visual-validation loops materially improve GLM-5.3-Flash artifact tasks beyond the task profile baseline.

## Boundary
- OpenAI/Anthropic protocol compatibility does not make GLM reasoning parameters identical to OpenAI/Anthropic models.
- Do not infer multimodality from the provider family; GLM-5.3 is documented as text-only while GLM-5.3-Flash is natively multimodal.
- Provider profiles cannot grant tool or filesystem permissions.
