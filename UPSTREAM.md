# Upstream provenance

Source: [cursor/plugins](https://github.com/cursor/plugins). Initial port pinned commit `99743e9c151c8537cbbf1f98bb38f34ef3368453` (main at port time); `install.sh` defaults to `main` and accepts `UPSTREAM_REF`.

| Pack | Version at port | License | Upstream root |
|---|---|---|---|
| pstack | 0.15.25 | MIT | `pstack/` |
| cursor-team-kit | 1.2.0 | MIT | `cursor-team-kit/` |

## What the port patches

- Subagent spawning: `Task` / `subagent_type` -> the OpenCode `subagent` tool with agent ids (`poteto-agent`, `poteto-judge`, `comment-sicko`, `ci-watcher`, built-in `explore` / `general`); `run_in_background` / `is_background` -> `background: true`.
- Models: per-role Cursor slugs (`grok-4.7-*`, `claude-opus-5-5-*`) and `~/.cursor/rules/pstack-models.mdc` -> `model:` lines on the OpenCode agent files plus the role map in `files/skills/poteto-mode/references/opencode-models.md`; `setup-pstack` rewritten for OpenCode.
- Transcripts: `~/.cursor/projects/*/agent-transcripts/*.jsonl` -> the OpenCode session store (`~/.local/share/opencode/opencode.db`, read-only `mode=ro`). Applies to `recall`, `automate-me`, `reflect`, `show-me-your-work`, `session-pickup`, `eval`, and `poteto-mode/scripts/worktree-audit.sh`.
- Project skills: `.cursor/skills/` -> `.opencode/skills/` (`create-verification-skill`, `maintain-verification-skill`, `automate-me`).
- `/loop` (Cursor built-in): replaced with bounded polling loops / `ci-watcher` guidance; `poteto-mode/scripts/check-plan.mjs` marker updated (`audit tick`).
- Cloud agents / `environment: "cloud"` / cloud-agent URLs: replaced with local child sessions and worktrees.
- `AskQuestion` -> the `question` tool. Cursor's built-in `create-skill` -> the `writing-great-skills` skill plus pstack's `authoring-a-skill` playbook.
- `poteto-help` rewritten for the OpenCode install (commands, agents, guide links, no Custom Modes); the guide is vendored into `poteto-help/references/guide/` with an OpenCode note.

Kept as-is on purpose: `make-bot-ui` (inherently Grok Bot specific) and the `bugbot-triage` reference.

## Layout

- `install.sh` - fetch upstream, copy skills, apply rewrites, install agents, generate commands.
- `files/` - the full-file rewrites (`setup-pstack`, `opencode-models.md`, the guide note, the 5 agent definitions).
- `patches/patches_a.py`, `patches/patches_b.py` - the mechanical edits. They take the skills directory as `$1` (default `~/.agents/skills`) and fail loudly when an upstream string has moved.
- `commands/generate-commands.mjs` + `commands/packs.json` - generate one OpenCode slash command per skill.

## Updating

1. Re-run `install.sh` (skills are restored from a fresh clone before patching, so repeats are safe).
2. If a patch script reports failures, read the exact string it names, update the patch or the `files/` copy, and re-run.
