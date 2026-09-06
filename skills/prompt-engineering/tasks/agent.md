---
task: agent
version: 1
---

# Agent

## Goal
Define or guide a multi-step tool-using workflow that completes the requested objective within explicit capability and permission boundaries.

## Required inputs
- objective
- available tools/capabilities when known
- side-effect permissions
- completion criteria

## Rules
- Treat tool availability as runtime state, not as something the prompt can invent.
- Distinguish read, write, publish, send, commit, push, purchase, and destructive actions.
- Prefer the fewest tool calls needed to meet the objective reliably.
- Define recovery behavior for empty results, tool failures, and blocked permissions when relevant.
- Delegate only when a real delegation mechanism exists and materially helps the task.

## Validation
- Workflow reaches a defined completion state.
- Every side effect is covered by an explicit permission boundary.
- Failure and blocked states are represented when material.
- No unavailable tool or independent reviewer is claimed to exist.

## Do not
- treat generated prompt text as execution authorization;
- simulate independent agents and report them as real delegation;
- encode provider-specific tool protocols in this task profile.
