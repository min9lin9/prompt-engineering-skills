---
task: image
version: 1
---

# Image Prompting

## Goal
Create a visual-generation prompt that preserves the requested subject, composition, style constraints, text requirements, and delivery intent.

## Required inputs
- subject or scene
- desired visual outcome
- composition/aspect requirements when relevant
- text-in-image requirements when relevant

## Rules
- Make visible attributes concrete: subject, action, environment, composition, lighting, mood, material/texture, and text placement when needed.
- Preserve user-provided identity, branding, and factual constraints.
- Keep negative constraints limited to failures that matter for the requested image.
- Separate visual intent from provider/runtime parameters.

## Validation
- Primary subject and requested action are unambiguous.
- Composition and aspect constraints are represented when supplied.
- Required visible text is quoted exactly when exact text matters.
- No unsupported model-specific parameter is embedded as a universal rule.

## Do not
- force a fixed JSON format for every image model;
- add unrelated style elements;
- claim image generation occurred when only a prompt was requested.
