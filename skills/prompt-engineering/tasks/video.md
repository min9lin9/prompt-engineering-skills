---
task: video
version: 1
---

# Video Prompting

## Goal
Create a time-aware visual prompt that defines subject continuity, action progression, camera behavior, scene changes, and audio requirements when relevant.

## Required inputs
- subject/scene
- duration or sequence expectation when relevant
- key action or transformation
- camera/audio constraints when supplied

## Rules
- Describe temporal progression explicitly when the result depends on sequence.
- Preserve subject identity and scene continuity across shots unless change is requested.
- Use storyboard structure only when multiple shots or temporal planning materially improves the prompt.
- Separate creative instructions from provider-specific generation settings.

## Validation
- Beginning, progression, and ending state are clear when sequence matters.
- Camera motion does not contradict subject action.
- Audio/dialogue requirements are represented if requested.
- Required continuity constraints are explicit.

## Do not
- require a storyboard for every single-shot request;
- invent provider capabilities;
- treat prompt creation as authorization to generate or publish video.
