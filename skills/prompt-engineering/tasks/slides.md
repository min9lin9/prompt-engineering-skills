---
task: slides
version: 1
---

# Slide Prompting

## Goal
Create a presentation-generation prompt that turns the requested message into a coherent slide narrative with explicit content and visual requirements.

## Required inputs
- presentation objective
- audience
- source/content constraints
- slide count or duration when supplied
- visual/brand requirements when supplied

## Rules
- Define the narrative arc before slide-level decoration.
- Give each slide one primary communication job.
- Distinguish source-backed content from placeholders or assumptions.
- Specify visual hierarchy, chart/table needs, and asset constraints only where useful.
- Keep presentation content separate from tool-specific export commands.

## Validation
- Presentation objective and audience are reflected.
- Slide sequence forms a coherent argument or story.
- Required source facts and calls to action are preserved.
- Slide count and format requirements are respected.

## Do not
- invent metrics or customer claims for visual polish;
- require a fixed presentation tool;
- treat a slide prompt request as authorization to create or publish files.
