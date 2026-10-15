# pstack for OpenCode

**pstack** is [Lauren Tan's](https://x.com/poteto) set of agent skills for rigorous engineering work: verification-first bug fixing, disciplined delegation, multi-model review panels, and 24 one-rule principles. It was built for Cursor. **This repo ports it to [OpenCode](https://opencode.ai):** the same skills, patched so the subagents, model roles, transcripts, and loops all work in OpenCode v2.

One command installs 72 skills, 5 subagents, and 72 slash commands.

## Install

Requirements: OpenCode v2, `git`, `python3`, `node`.

```bash
git clone https://github.com/devalade/pstack-opencode.git
cd pstack-opencode
./install.sh
```

Then:

1. Start a new OpenCode session (or `opencode2 service restart` if anything looks stale).
2. Run `/setup-pstack` to map your models onto the `poteto-agent` and `poteto-judge` subagents and pick a budget.
3. Start a task with `/poteto-mode build <feature>. verify your changes and show me proof.`

Targets and upstream can be overridden:

| Variable | Default |
|---|---|
| `PSTACK_SKILLS_DIR` | `~/.agents/skills` |
| `OPENCODE_AGENTS_DIR` | `~/.config/opencode/agents` |
| `OPENCODE_COMMANDS_DIR` | `~/.config/opencode/commands` |
| `UPSTREAM_REF` | `99743e9c` (the port's pinned commit; set `main` to attempt the newest upstream) |

## What you get

**Skills (72).** All 54 pstack skills (including the 24 `principle-*` leaves and the 23 `poteto-mode` playbooks) plus the 18 [cursor-team-kit](https://github.com/cursor/plugins/tree/main/cursor-team-kit) skills pstack references: `deslop`, `control-ui`, `control-cli`, `fix-ci`, `loop-on-ci`, `review-and-ship`, `thermo-nuclear-code-quality-review`, and friends. Almost all are `disable-model-invocation: true`, matching pstack's design: they load when you invoke them, not on the model's whim.

**Subagents (5).** `poteto-agent` (code delegates), `poteto-judge` (read-only review, judgment, and explanation seats), `comment-sicko` (comment reviewer for `/no-comments`), `ci-watcher` (PR check monitoring), `thermo-nuclear-code-quality-review` (harsh maintainability audit).

**Commands (72).** Every skill is a slash command: `/poteto-mode`, `/how`, `/why`, `/interrogate`, `/unslop`, `/tdd`, `/teach`, `/create-verification-skill`, `/principle-prove-it-works`, and so on. Skills also load by `@skill-id` mention or plain request.

## Usage

```
/poteto-mode fix this regression. repro first, then root-cause it and prove the fix with runtime evidence.

/poteto-mode i'm going to bed. land the stack even if ci flakes. i want everything merged by morning.

/how do we cancel runs? do we have an n+1 when we look up every run to cancel?

/interrogate review this pr.
```

New here? Type `/poteto-help` with a question.

## How the port maps Cursor to OpenCode

| Cursor | OpenCode |
|---|---|
| Custom Modes, `Enter`/`Opt+Enter` on a skill | Slash commands and `@skill-id` mentions (per task; no persistent mode) |
| `Task` subagents with per-role model slugs | The `subagent` tool with agent ids; models live in `~/.config/opencode/agents/*.md` |
| `~/.cursor/rules/pstack-models.mdc` role rule | `model:` lines on the pstack agents plus `poteto-mode/references/opencode-models.md` |
| `~/.cursor/projects/*/agent-transcripts/*.jsonl` | The OpenCode session store (`~/.local/share/opencode/opencode.db`, read-only) |
| Project skills in `.cursor/skills/` | Project skills in `.opencode/skills/` |
| `/loop` (built-in) | Bounded polling loops and the `ci-watcher` subagent |
| Cloud agents, `environment: "cloud"` | Local child sessions; one worktree per writer |

`/setup-pstack` is rewritten for OpenCode: it detects models with `opencode2 models` and writes `model:` lines into the agent files. Panels get their model diversity from `poteto-agent` vs `poteto-judge` (add a second writer agent file for multi-model writing races).

## What install.sh does

1. Fetches `cursor/plugins` (sparse: `pstack` + `cursor-team-kit`) at `UPSTREAM_REF`.
2. Copies all 72 skills into `PSTACK_SKILLS_DIR`, replacing existing copies of the same names.
3. Vendors the pstack guide into `poteto-help/references/guide/` (with an OpenCode note).
4. Applies the OpenCode rewrites from `files/` and `patches/` (the patch scripts fail loudly if upstream text moved).
5. Copies the 5 subagents into `OPENCODE_AGENTS_DIR`.
6. Generates one slash command per skill into `OPENCODE_COMMANDS_DIR`.

Re-running `install.sh` is idempotent at the same ref: skills are restored from a fresh clone before patching. Point `UPSTREAM_REF` at a newer commit to upgrade; if upstream text moved, the patch scripts name the exact string and fail loudly rather than half-applying.

## Not ported

- pstack's `automations/benny` (Cursor automations) and cursor-team-kit's `.mdc` rules (Cursor always-apply rules).
- `/make-bot-ui` is installed as-is, but it is inherently Grok Bot specific.

## Credits and license

The skills are [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack); the companion skills are [cursor-team-kit](https://github.com/cursor/plugins/tree/main/cursor-team-kit) by Eric Zakariasson and the Cursor team. Both are MIT licensed and vendored here with patches. This is an unofficial community port, not affiliated with Cursor or Lauren Tan.

The port tooling in this repo is MIT. See `LICENSE` and `UPSTREAM.md`.
