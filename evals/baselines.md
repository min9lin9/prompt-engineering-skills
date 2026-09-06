# v4 Evaluation Baselines

## Legacy

Source: `commands/prompt-legacy.md`.

Purpose: measure regression against the preserved pre-v4 system.

Rules:

- do not edit the legacy snapshot during an experiment;
- if a new target model is not natively recognized by the legacy prompt, record the comparison as `forced-legacy` rather than pretending the legacy system supported it;
- record any manual substitution required to make the candidate executable.

## Neutral

Purpose: test whether model-specific or repository-specific scaffolding adds value beyond a minimal well-specified prompt.

The neutral baseline may contain only:

1. task goal;
2. supplied context/source boundary;
3. explicit constraints;
4. output contract;
5. explicit permission boundary when relevant.

It must not contain:

- provider/model-specific prompt tips;
- expert personas unless required by the task itself;
- simulated debate;
- model ranking claims;
- arbitrary reasoning-effort recommendations;
- task-irrelevant validation rituals.

## v4

Source: the explicit `--v4` Router path.

Composition:

```text
Prompt Contract
+ Core
+ one Task Profile
+ relevant Provider/Model Delta
+ User Contract
```

By default, only Confirmed compatibility rules are mandatory. Evaluated strategies may be included only when their recorded evaluation scope matches the current experiment. Experimental strategies must be separately flagged when tested.

## Fair comparison rule

A three-way comparison is valid only if the candidate prompts target the same task, model/runtime, tools, source data, and requested output contract.

If token limits or provider-specific hard requirements make exact parity impossible, document the difference in the run metadata.