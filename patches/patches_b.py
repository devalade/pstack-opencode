#!/usr/bin/env python3
"""Patch pstack playbooks + team-kit + scripts (part B) for OpenCode."""
import os
import sys
from pathlib import Path

POOL = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PSTACK_SKILLS_DIR", "~/.agents/skills")).expanduser()
PATCHES = []

def P(file, old, new, expected=1):
    PATCHES.append((file, old, new, expected))

# ---- arena
P("arena/SKILL.md",
  "Spawn all N subagents in one message with `run_in_background: true`, each with the task,",
  "Spawn all N subagents in one message with `background: true`, each with the task,")

# ---- create-verification-skill / maintain-verification-skill
P("create-verification-skill/SKILL.md", ".cursor/skills/", ".opencode/skills/", 3)
P("maintain-verification-skill/SKILL.md", ".cursor/skills/", ".opencode/skills/", 1)

# ---- poteto-help references
P("poteto-help/references/recipes.md", "/loop until done.", "keep going until done.")
P("poteto-help/references/prompting.md", "give `/loop` that predicate.", "give the loop that predicate.")

# ---- bug-fix
P("poteto-mode/playbooks/bug-fix.md",
  "Don't guess. Drive a long or stubborn hunt with Cursor's `/loop` command.",
  "Don't guess. Drive a long or stubborn hunt by looping within this session (repeat passes until the mechanism is pinned).")
P("poteto-mode/playbooks/bug-fix.md",
  "using your configured bug-fix model (default `grok-4.7-xhigh-fast`) with a specific scope.",
  "using the `poteto-agent` subagent with a specific scope.")

# ---- shipping
P("poteto-mode/playbooks/shipping.md",
  "One verifier per PR, each a Cursor cloud agent, runs the change",
  "One verifier per PR, each a fresh `poteto-agent` child session, runs the change")
P("poteto-mode/playbooks/shipping.md",
  "under `/loop` until it reports `COMPLETE` at the ceiling.",
  "polling in a bounded loop until it reports `COMPLETE` at the ceiling.")

# ---- multi-phase-plan
P("poteto-mode/playbooks/multi-phase-plan.md",
  "3. Explore in subagents with `subagent_type: \"poteto-agent\"` and an explicit model per the Subagents section (the **guard-the-context-window** principle skill).",
  "3. Explore in `poteto-agent` (or `explore`) subagents per the Subagents section (the **guard-the-context-window** principle skill).")
P("poteto-mode/playbooks/multi-phase-plan.md",
  "per the **swarm** skill, on the `swarm workers` model (default `grok-4.7-xhigh-fast`).",
  "per the **swarm** skill, on its worker subagent.")
P("poteto-mode/playbooks/multi-phase-plan.md",
  "arm the audit tick as `/loop 1h` with the tick prompt below. Never leave the cadence to memory.",
  "arm the audit tick at 1h intervals with the tick prompt below (a polling loop; OpenCode has no `/loop`). Never leave the cadence to memory.")

# ---- authoring-a-skill
P("poteto-mode/playbooks/authoring-a-skill.md",
  "1. Use the **create-skill** skill (Cursor's built-in for authoring SKILL.md files).",
  "1. Use the **writing-great-skills** skill (installed globally) as the authoring rubric, and the steps below for pstack's house shape.")

# ---- worktree-cleanup
P("poteto-mode/playbooks/worktree-cleanup.md",
  "misses one that lives at `.cursor/worktrees/myrepo/x`",
  "misses one that lives at a tool-managed path like OpenCode's own worktree directory")
P("poteto-mode/playbooks/worktree-cleanup.md",
  "`~/Library/Application Support/Cursor` (`state.vscdb.backup`, and `snapshots/roots/<root>` where a `<root>` named for a folder you opened as a workspace balloons), package caches",
  "application caches under `~/Library/Application Support/` that the user confirms are disposable, package caches")

# ---- opening-a-pr
P("poteto-mode/playbooks/opening-a-pr.md",
  "Multiple `Task` calls on the same branch each get their own worktree",
  "Multiple subagent spawns on the same branch each get their own worktree")

# ---- autopilot-full
P("poteto-mode/playbooks/autopilot-full.md",
  "Each owner is a Cursor cloud agent that builds,",
  "Each owner is a `poteto-agent` child session that builds,")
P("poteto-mode/playbooks/autopilot-full.md",
  "arm `/loop 1h` to audit until no delegated work is left",
  "arm a 1h audit cadence until no delegated work is left (a polling loop; OpenCode has no `/loop`)")

# ---- hillclimb / feature / perf-issue / refactoring
P("poteto-mode/playbooks/hillclimb.md",
  "using your configured hillclimb model (default `grok-4.7-xhigh-fast`) with a tight scope.",
  "using the `poteto-agent` subagent with a tight scope.")
P("poteto-mode/playbooks/feature.md",
  "using your configured feature model (default `grok-4.7-xhigh-fast`) with a specific scope",
  "using the `poteto-agent` subagent with a specific scope")
P("poteto-mode/playbooks/perf-issue.md",
  "using your configured perf-issue model (default `grok-4.7-xhigh-fast`).",
  "using the `poteto-agent` subagent.")
P("poteto-mode/playbooks/refactoring.md",
  "using your configured refactoring model (default `grok-4.7-xhigh-fast`) with a specific scope",
  "using the `poteto-agent` subagent with a specific scope")

# ---- babysit
P("poteto-mode/playbooks/babysit.md",
  "This playbook replaces Cursor's built-in babysit skill for these requests, so do not route there even though its description matches the same words.",
  "This playbook replaces any runtime's own PR-status skill for these requests, so do not route there even though its description matches the same words.")
P("poteto-mode/playbooks/babysit.md",
  "Run `drive` and `background` under `/loop` in dynamic mode.",
  "Run `drive` and `background` as polling loops in dynamic mode (bounded waits or a `ci-watcher` subagent; OpenCode has no `/loop`).")

# ---- orchestrate
P("poteto-mode/playbooks/orchestrate.md",
  "Agents are spawned, resumed, and drained only through the Task tool.",
  "Agents are spawned, resumed, and drained only through the `subagent` tool.")
P("poteto-mode/playbooks/orchestrate.md",
  "Always `environment: \"cloud\"` unless the task needs this machine: `control-ui` or `control-cli` runtime verification (from `cursor-team-kit`). Reading local transcripts under `agent-transcripts/`. Simulators and local IDE state. Auth that exists only here. Cloud agents cannot read the local store, so their briefs inline what they need or point at repo paths. Prefer fewer, broader workers. One writer per worktree or branch (principle-separate-before-serializing-shared-state). Run a unit's verifier on a different model family from its worker.",
  "Workers run as local child sessions. Runtime verification (`control-ui`/`control-cli`), the local session store, simulators and local IDE state, and machine-bound auth all work directly. Prefer fewer, broader workers. One writer per worktree or branch (principle-separate-before-serializing-shared-state). Run a unit's verifier on a different subagent (and model, once configured) from its worker.")
P("poteto-mode/playbooks/orchestrate.md",
  "Probe read-only: the ledger, `units.tsv`, `gh`, pushed branches, the cloud agent's status in the Cursor dashboard. Transcript mtime is not liveness.",
  "Probe read-only: the ledger, `units.tsv`, `gh`, pushed branches, the child session's status via the `subagent` tool. Transcript mtime is not liveness.")
P("poteto-mode/playbooks/orchestrate.md",
  "After a Cursor restart: local agents are dead, cloud work is not. Re-read the standing orders and `units.tsv`, recompute the frontier, reattach cloud work by PR and branch rather than agent id,",
  "After an OpenCode service restart: local child sessions are dead; pushed branches and PRs are not. Re-read the standing orders and `units.tsv`, recompute the frontier, reattach work by PR and branch rather than agent id,")

# ---- visual-parity
P("poteto-mode/playbooks/visual-parity.md",
  "`/loop` per component until the diff is zero.",
  "Iterate per component until the diff is zero.")

# ---- eval
P("poteto-mode/playbooks/eval.md",
  "4. **Spawn N parallel candidates** on different models per the **arena** skill's Phase B.",
  "4. **Spawn N parallel candidates** on different subagents per the **arena** skill's Phase B.")
P("poteto-mode/playbooks/eval.md",
  "5. **Spawn one blinded judge** on a different model family per the **arena** skill's Phase C.",
  "5. **Spawn one blinded judge** on a different subagent per the **arena** skill's Phase C.")
P("poteto-mode/playbooks/eval.md",
  "Read each candidate's local transcript under the active workspace's `agent-transcripts/` directory (the system prompt names this path). Do not glob across `~/.cursor/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects.",
  "Read each candidate's local transcript from the OpenCode session store (`~/.local/share/opencode/opencode.db`, read-only; `session.directory` names the candidate's dir). Read only sessions from this workspace; other directories are unrelated private chats.")

# ---- session-pickup
P("poteto-mode/playbooks/session-pickup.md",
  "1. Locate the prior trail. A local transcript under the active workspace's `agent-transcripts/` directory (the system prompt names the path. Do not glob across `~/.cursor/projects/*/`, that crosses workspace boundaries and reads private chats from unrelated projects), a cloud-agent URL, or a pushed branch.",
  "1. Locate the prior trail. A prior session in the OpenCode session store (`~/.local/share/opencode/opencode.db`, read-only; match `session.directory` to this workspace and pick by `time_updated`; never read other directories), a stored brief, or a pushed branch.")

# ---- show-me-your-work
P("show-me-your-work/SKILL.md",
  "At the end of the run, before handing back, check the log told the truth. Read this run's transcript under the active workspace's `agent-transcripts/` directory (the system prompt names the path). Don't glob across `~/.cursor/projects/*/`. That reads unrelated private chats.",
  "At the end of the run, before handing back, check the log told the truth. Read this run's sessions from the OpenCode session store (`~/.local/share/opencode/opencode.db`, read-only; `session` rows for this directory at or after the run's start, subagent chats included). Read only this workspace's sessions; others are unrelated private chats.")
P("show-me-your-work/SKILL.md",
  "spawn a subagent on a different model family from the one that did the work",
  "spawn a subagent on a different agent (and model, once `/setup-pstack` configures one) from the one that did the work")

# ---- why (MCP discovery)
P("why/SKILL.md",
  "Before spawning investigators, list the available MCPs from the Cursor environment. Use the available-tools map when present. Otherwise inspect the `mcps/` directory Cursor exposes for enabled MCP servers.",
  "Before spawning investigators, list the available MCPs. Use the available-tools map when present; otherwise run `opencode2 mcp list` or read the `mcp` section of the OpenCode config for enabled servers.")

# ---- reflect routing label
P("reflect/SKILL.md",
  "`new skill via create-skill: <kebab-name>`: hand creation to the `authoring-a-skill` playbook.",
  "`new skill via the authoring playbook: <kebab-name>`: hand creation to the `authoring-a-skill` playbook.")

# ---- poteto-mode playbook list: pause safely
P("poteto-mode/SKILL.md",
  "on an explicit pause, going offline, a Cursor restart, or imminent context compaction.",
  "on an explicit pause, going offline, a service restart, or imminent context compaction.")

# ---- workflow-from-chats
P("workflow-from-chats/SKILL.md",
  "Extract durable working preferences from recent Cursor chats and convert them into skills, rules, or workflow docs.",
  "Extract durable working preferences from recent chats and convert them into skills, rules, or workflow docs.")

# ---- scripts
P("poteto-mode/scripts/check-plan.mjs",
  'const PROGRAM_MARKERS = ["git show origin/main:", "/loop 1h", "status message"];',
  'const PROGRAM_MARKERS = ["git show origin/main:", "audit tick", "status message"];')
P("poteto-mode/scripts/check-plan.test.ts",
  "\\`git show origin/main:\\` /loop 1h status message",
  "\\`git show origin/main:\\` audit tick status message")
P("poteto-mode/scripts/worktree-audit.sh",
  "# Transcripts dir: ~/.cursor/projects/<slugified-repo-path>/agent-transcripts.\nslug=$(printf '%s' \"$main_wt\" | sed 's#^/##; s#/#-#g')\ntranscripts=\"$HOME/.cursor/projects/$slug/agent-transcripts\"",
  "# Session store: OpenCode records one row per chat with its working directory.\ndb=\"$HOME/.local/share/opencode/opencode.db\"")
P("poteto-mode/scripts/worktree-audit.sh",
  "\t# Most recent chat whose transcript operated in this worktree. Match path\n\t# followed by \"/\" or a quote so glint-482 does not match glint-482-r37.\n\tlast=\"-\"; last_ts=0\n\tif [ -d \"$transcripts\" ]; then\n\t\tf=$(rg -l -e \"${wt}/\" -e \"${wt}\\\"\" \"$transcripts\" 2>/dev/null \\\n\t\t\t| xargs stat -f '%m %N' 2>/dev/null | sort -rn | head -1)\n\t\tif [ -n \"$f\" ]; then last_ts=$(echo \"$f\" | awk '{print $1}')\n\t\t\tlast=$(date -r \"$last_ts\" '+%Y-%m-%d' 2>/dev/null); fi\n\tfi",
  "\t# Most recent OpenCode chat in this worktree (session.directory is exact).\n\tlast=\"-\"; last_ts=0\n\tif [ -f \"$db\" ]; then\n\t\tlast_ms=$(sqlite3 \"file:$db?mode=ro\" \"select coalesce(max(time_updated),0) from session where directory = '$wt';\" 2>/dev/null)\n\t\tlast_ms=${last_ms:-0}\n\t\tif [ \"$last_ms\" -gt 0 ] 2>/dev/null; then\n\t\t\tlast_ts=$((last_ms / 1000))\n\t\t\tlast=$(date -r \"$last_ts\" '+%Y-%m-%d' 2>/dev/null || echo \"-\")\n\t\tfi\n\tfi")

def main():
    failures = []
    applied = 0
    for file, old, new, expected in PATCHES:
        path = POOL / file
        if not path.exists():
            failures.append((file, "missing file", old[:80]))
            continue
        text = path.read_text()
        count = text.count(old)
        if count == 0:
            failures.append((file, f"no match", old[:100]))
            continue
        if expected and count != expected:
            failures.append((file, f"count {count} != {expected}", old[:100]))
            continue
        path.write_text(text.replace(old, new))
        applied += 1
    print(f"applied={applied} failures={len(failures)}")
    for f in failures:
        print("FAIL:", f[0], "|", f[1], "|", f[2])
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
