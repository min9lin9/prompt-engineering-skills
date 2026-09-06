---
provider: zai
model: glm-5.3-flash
version: 1
---

# GLM-5.3-Flash Delta

## Confirmed
- Model code is `glm-5.3-flash`.
- GLM-5.3-Flash is natively multimodal and accepts video, image, text, and file input; output is text.
- Context length is 1M tokens and maximum output is 128K tokens.
- `thinking.type` supports `enabled` only; thinking cannot be disabled.
- Text parameters are documented as consistent with GLM-5.3; provider guidance lists `reasoning_effort: max` as recommended and GLM-5.3 defines native effort values `low`, `high`, and `max`.
- Structured output and function calling are supported.

Official source:
- https://docs.z.ai/guides/vlm/glm-5.3-flash

## Evaluated
None yet.

## Experimental
- Visual inspect-and-refine loops are candidate task strategies for UI, slides, documents, and media workflows, but are not promoted as universal defaults until evaluated.

## Boundary
- Reject attempts to disable thinking.
- Do not treat provider-recommended sampling/effort values as universal prompt defaults; keep them as runtime hints unless the user explicitly requests runtime configuration.
