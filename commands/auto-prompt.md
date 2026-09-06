---
description: Optional batch prompt-generation workflow using the v4 Router and Registry
allowedTools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# /auto-prompt — v4 Optional Batch Workflow

Generate multiple prompts for a user-supplied catalogue, occupation set, curriculum, or spreadsheet-style export.

$ARGUMENTS

## Scope

This is an optional workflow built on the v4 Prompt Contract, Task Profiles, Model Registry, and `/prompt --v4` behavior.
It is not required for core prompt generation and must not depend on external `.claude/agents` or `.claude/skills` files.

## Inputs

Resolve from the request:
- subject/catalogue dimension;
- target models or model families;
- number of prompts per target;
- task categories;
- difficulty or complexity labels, if the user wants them;
- output fields;
- export format.

Do not assume a fixed author/source name.
Do not restrict targets to GPT, Gemini, Claude, or Perplexity; use `registry/models.yaml` when explicit model targets are requested.

## Prompt generation

For each row/item:
1. Build a Prompt Contract.
2. Select one primary Task Profile.
3. Apply a verified Model Delta only when the target model is known.
4. Preserve the requested semantics across model variants.
5. Validate required fields and duplicate titles.

Complexity labels do not mandate a syntax. Do not map high difficulty to XML or low difficulty to natural language by default.

## Export

Default to a simple tabular structure:
- item id
- category / occupation / subject
- prompt title
- prompt body
- target model
- complexity label, if requested
- source/author, only if supplied

If spreadsheet generation is available in the host, export `.xlsx`; otherwise return a CSV/Markdown-compatible table or structured data without pretending a spreadsheet was created.

## Permission boundary

Generating the batch output does not authorize publication, external upload, repository mutation, or overwriting an existing file unless separately requested.
