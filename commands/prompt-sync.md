# /prompt-sync — v4 Safe Distribution Sync

Synchronize Prompt Engineering Skills v4 artifacts to an explicitly supplied destination.

$ARGUMENTS

## Default

`dry-run` is the default. No commit, push, publish, overwrite, or delete is implied by invoking this command.

## Inputs

Resolve:
- source repository root;
- explicit destination path or repository;
- destination type: shared directory or dedicated mirror;
- mode: dry-run or apply;
- whether generated knowledge packs are required.

If the destination is not explicit, stop with a plan instead of guessing a personal path or repository.

## Safety rules

1. Never hard-code a GitHub owner, home directory, Obsidian vault, Windows user, or Claude directory.
2. Shared directories are additive only. Never use delete synchronization against a shared skills/commands directory.
3. Destructive mirror synchronization is permitted only for an explicitly identified dedicated mirror and only after the destination is verified.
4. Detect dirty Git worktrees before overwriting repository files.
5. If source and destination resolve to the same location, perform no sync.
6. Build generated knowledge packs with `python scripts/build.py` when the destination needs distribution artifacts.
7. Show the planned file changes before apply mode.
8. `git commit` and `git push` require separate explicit user authorization; sync completion never implies publication.

## Dry-run output

Return:
- source;
- destination;
- destination type;
- files to add/update;
- files that would be removed, if any;
- generated artifacts to build;
- dirty-worktree findings;
- blocked unsafe operations.

## Apply mode

Only apply the previously described sync operation. Do not expand scope during execution.

After apply, report changed files and leave commit/push as separate actions unless explicitly requested.
