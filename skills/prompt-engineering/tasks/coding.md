---
task: coding
version: 1
---

# Coding

## Goal
Produce or modify code that satisfies the requested behavior with the smallest appropriate change set.

## Required inputs
- requested behavior or bug
- relevant code/context when available
- constraints such as language, framework, compatibility, or files in scope

## Rules
- Inspect relevant existing code before proposing invasive changes when repository context is available.
- Preserve working behavior outside the requested scope.
- Prefer simple, maintainable implementations over speculative abstractions.
- Define failure behavior for material error paths.
- Keep generated code consistent with the surrounding project unless the user requests migration.

## Validation
- Requested behavior is implemented or clearly specified.
- Relevant targeted tests/checks are identified or run when execution is authorized.
- No unrelated feature expansion is introduced.
- Unverified environment assumptions are stated.

## Do not
- invent APIs, files, packages, or project conventions;
- treat a code-generation request as authorization to write or deploy;
- require a particular model-specific prompt syntax.
