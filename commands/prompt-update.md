---
description: Inspect official model/prompting changes and propose validated v4 updates
allowedTools: Read, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# /prompt-update — v4 Update Inspector

$ARGUMENTS

## Purpose

Research official provider documentation, compare it with the v4 Registry and model profiles, and produce a validated change proposal.

Default behavior is read-only. This command does not commit, push, publish, edit Obsidian, or mutate external repositories.

## Workflow

1. Parse scope from `$ARGUMENTS`.
2. Research only official provider documentation for the requested providers/models.
3. Compare findings with:
   - `registry/models.yaml`
   - `skills/prompt-engineering/models/`
   - relevant Core/Task files only when behavior changes affect them.
4. Classify each finding as:
   - Confirmed capability/runtime fact
   - Candidate Evaluated strategy
   - Experimental hypothesis
   - No change
5. Produce a candidate patch plan with affected files and validation steps.
6. Run or recommend the relevant static validators.
7. Stop with a report.

## Output contract

Return:

- checked provider/model;
- official source references;
- current repository state;
- detected differences;
- proposed file changes;
- confidence/evidence class;
- required validation;
- unresolved items.

## Mutation boundary

Do not edit files, commit, push, sync, or publish unless the user separately requests implementation after reviewing the proposed changes.

`/prompt-update` is an inspector, not a deployment command.
