---
provider: mistral
family: mistral
version: 1
---

# Mistral Provider Profile

## Confirmed

- Mistral's current generalist lineup includes Mistral Large 3, Mistral Medium 3.5, and Mistral Small 4.
- These models support structured outputs and function calling through supported Mistral endpoints.
- Mistral Medium 3.5 and the current `mistral-small-latest` path support adjustable reasoning through `reasoning_effort`; documented values include `none` and `high`.
- Mistral Large 3, Medium 3.5, and Small 4 have 256k-token context windows in current documentation.

Official references:
- https://docs.mistral.ai/models
- https://docs.mistral.ai/studio/conversations/reasoning
- https://docs.mistral.ai/studio/conversations/structured-output

## Evaluated

None yet.

## Experimental

- Provider guidance recommending a particular reasoning level by task must remain experimental until v4 target-model evaluation is available.

## Boundary

Do not assume every Mistral family member exposes identical reasoning controls. Keep model-level reasoning capability in the model delta and Registry rather than provider-wide defaults.