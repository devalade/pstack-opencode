#!/usr/bin/env python3
"""Patch pstack skills (part A) for OpenCode. Fails loudly per-patch, keeps going."""
import os
import sys
from pathlib import Path

POOL = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PSTACK_SKILLS_DIR", "~/.agents/skills")).expanduser()

PATCHES = []  # (file, old, new, expected)

def P(file, old, new, expected=1):
    PATCHES.append((file, old, new, expected))

# ---------------------------------------------------------------- poteto-mode
PM = "poteto-mode/SKILL.md"
P(PM,
  "Bundled skills live at `../<name>/SKILL.md` from this file, so put this file's absolute path in every `poteto-agent` prompt.",
  "Bundled skills live at `../<name>/SKILL.md` from this file, installed at `~/.agents/skills/<name>/SKILL.md`; this file is `~/.agents/skills/poteto-mode/SKILL.md`. Put this file's absolute path in every subagent prompt.")
P(PM,
  'About to `AskQuestion` on a "which approach", "how should I", or "what should this do" fork',
  'About to ask the user a "which approach", "how should I", or "what should this do" question')
P(PM,
  "Agent-facing prose also follows the **create-skill** skill (Cursor's built-in for authoring SKILL.md files).",
  "Agent-facing prose also follows the **writing-great-skills** skill and the bundled `playbooks/authoring-a-skill.md`.")
P(PM,
  "not Cursor's built-in babysit skill, whose description matches the same words.",
  "not any runtime's own PR-status skill, whose description matches the same words.")
P(PM,
  'or any task the user steps away from to review later ("going to bed", "trust it when i\'m back", "/loop until X")',
  'or any task the user steps away from to review later ("going to bed", "trust it when i\'m back", "keep going until X")')
P(PM,
  '**Use `subagent_type: "poteto-agent"` for any subagent you spawn inside a playbook step** (code-writing delegates, ad-hoc helpers). The chat that receives `/poteto-mode` runs the playbook. Never spawn a `poteto-agent` to run the playbook itself. Routed workflow skills (`how`, `why`, `interrogate`, `reflect`, `swarm`) set their own `subagent_type` for diverse-model review. Respect what the skill prescribes, don\'t override to `poteto-agent`.',
  '**Spawn every playbook-step subagent with the `subagent` tool.** Use the `poteto-agent` subagent for code-writing delegates and ad-hoc helpers, and `poteto-judge` for review, judgment, and explanation seats. The chat that receives `/poteto-mode` runs the playbook. Never delegate the playbook itself. Routed workflow skills (`how`, `why`, `interrogate`, `reflect`, `swarm`) name their own subagents; respect what the skill prescribes.')
P(PM,
  "**Defaults for every `Task` call.** `run_in_background: true`, agent mode (readonly strips MCP), file pointers not inlined context, explicit model per role (configurable via `/setup-pstack`. Defaults `grok-4.7-xhigh-fast` for code, `claude-opus-5-5-xhigh` for prose and judgment).",
  "**Defaults for every `subagent` call.** `background: true`, file pointers not inlined context, and the right subagent per role. OpenCode sets the model per subagent, not per call: configure `model:` lines in `~/.config/opencode/agents/poteto-agent.md` and `poteto-judge.md` via `/setup-pstack` (`references/opencode-models.md` maps the roles). Both inherit the session model until then.")
P(PM,
  "Code delegates tier by difficulty. The hardest changes (cross-cutting design, gnarly concurrency, subtle algorithms) go to your strongest judgment model (`claude-opus-5-5-xhigh`), whether the task needs judgment on vague intent or is a precisely specified sequence of steps to execute to the letter. Trivial mechanical edits go to your fast code model.",
  "Code delegates tier by difficulty. The hardest changes (cross-cutting design, gnarly concurrency, subtle algorithms) go to your strongest configured model, whether the task needs judgment on vague intent or is a precisely specified sequence of steps to execute to the letter. Trivial mechanical edits go to the cheapest one.")
P(PM,
  "Per-role lines in the `/setup-pstack` rule override these defaults and the model choices in the routed skills (`how`, `why`, `arena`, `swarm`, `architect`, `interrogate`, `reflect`). A role with no line keeps its default, and a role line of `inherit-parent` or `auto` runs that role on the parent chat model (omit Task `model`). Each code playbook's configured model comes from its line (`feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb`), and the hardest changes read `hardest tasks`. Prose and judgment read `judgment and prose`.",
  "The `/setup-pstack` role mapping decides which subagent and model each role uses (`feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `hardest tasks`, and the routed skills' roles, mapped in `references/opencode-models.md`). A role with no configured model inherits the session model.")
P(PM,
  "**Match the model to the job.** Before each spawn, start from the role's line or default and pick the reasoning level and speed the job needs. The `/setup-pstack` budget sets each role's starting level, xhigh by default. Raise it one step, up to max, for the hardest or subtlest work. Lower it one step for judgment and two or more steps for routine work. Use fast mode only when the job is urgent, meaning CI or trunk is red or a person is blocked on the result right now. Otherwise use standard speed, the same slug without `-fast`. Verification is the exception and stays on the `swarm workers` model and speed (`grok-4.7-xhigh-fast` by default). Change only the effort level and whether the slug is fast, and keep the family the role names, so a diverse panel stays diverse. If the family has no slug at that level and speed, use its nearest slug. A role on `auto` or `inherit-parent` stays on the parent model. If the Task tool rejects the adjusted slug, do not try another adjusted slug. Use the role's line or default and say so.",
  "**Match the agent to the job.** Before each spawn, choose the subagent; pick its configured model variant (`provider/model#variant` in the agent file) for the effort the job needs. Raise effort for the hardest or subtlest work, lower it for routine work. Verification stays on the cheaper worker setting. A spawn whose agent has no `model:` line inherits the session model. Panels stay diverse by splitting seats across `poteto-agent` and `poteto-judge` once their models differ.")
P(PM,
  'A long task to drive to completion without stopping ("run until done", "/loop until X").',
  'A long task to drive to completion without stopping ("run until done", "keep going until X").')
P(PM,
  "**Session pickup.** Resuming or taking over a prior agent's in-flight work from a transcript, cloud-agent URL, or pushed branch.",
  "**Session pickup.** Resuming or taking over a prior agent's in-flight work from a prior session, a stored brief, or a pushed branch.")

# ---------------------------------------------------------------- poteto-help
PH = "poteto-help/SKILL.md"
P(PH,
  'Read [`poteto-mode`](../poteto-mode/SKILL.md), do the work under it, and mention once that a Custom Mode keeps it on.',
  'Read [`poteto-mode`](../poteto-mode/SKILL.md), do the work under it, and mention once that `/poteto-mode` attaches the skill per task in OpenCode.')
P(PH,
  "The links here point into the installed plugin, which the user may not be able to open, so give the user the file's public copy: `https://github.com/cursor/plugins/blob/main/pstack/` followed by its path.",
  "The relative links here resolve inside the installed pack under `~/.agents/skills/`, which the user can open directly. The public upstream copy is `https://github.com/cursor/plugins/blob/main/pstack/` plus the same path.")
P(PH,
  "- No `~/.cursor/rules/pstack-models.mdc` means `/setup-pstack` hasn't run for this user, so every role uses its default model.",
  "- No `model:` lines in the OpenCode `poteto-*` agent files (`~/.config/opencode/agents/`) means `/setup-pstack` hasn't run for this user, so every role inherits the session model.")
P(PH,
  "1. Install with `/add-plugin pstack` in chat, or from Customize in the sidebar.\n2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes a rule. The rule applies to new chats.\n3. Start a real task with `/poteto-mode`, a goal, and a check that can pass or fail.\n\nInstalling changes nothing until the user invokes a skill. Only `/setup-pstack` loads from the user's words. The [README](../../README.md) and [guide page 1](../../docs/guide/01-setup.md) have the details.",
  "1. pstack is already installed for OpenCode: skills live under `~/.agents/skills/`, subagents under `~/.config/opencode/agents/`, and every skill is reachable as a slash command or `@skill-id` mention.\n2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It asks for a budget, maps a model to each subagent, and writes `model:` lines into the agent files.\n3. Start a real task with `/poteto-mode`, a goal, and a check that can pass or fail.\n\nInstalling changes nothing until the user invokes a skill. Only `/setup-pstack` loads from the user's words. [Guide page 1](references/guide/01-setup.md) has the details.")
P(PH,
  "pstack is built for Cursor. Its skills use the Agent Skills format, so other tools can read them. But most workflow skills, including `/poteto-mode`, `/how`, `/why`, and `/teach`, spawn Cursor subagents with per-role models, and Custom Modes and `/loop` are Cursor features, so those parts may not work there.",
  "This is the OpenCode build of pstack. Skills load as slash commands or `@skill-id` mentions and as files under `~/.agents/skills/`; subagents are OpenCode agents (`poteto-agent`, `poteto-judge`, `comment-sicko`, and friends) configured in `~/.config/opencode/agents/`. Cursor-only features (Custom Modes, `/loop`, cloud agents, Grok Bot) have no OpenCode equivalent, and the skills here were patched to say what to do instead.")
P(PH,
  "the chat runs on Auto or a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Save `/poteto-mode` for work that needs rigor.",
  "the chat runs on a cheaper model. Fewer panel seats run fewer subagents. Save `/poteto-mode` for work that needs rigor.")
P(PH,
  "Whether `/poteto-mode` stays on depends on how the user starts it:\n\n- Enter on `/poteto-mode` attaches the skill to one message. It fades as the chat moves on.\n- Option+Enter on Mac or Alt+Enter on Windows, or Use as Mode from the skill entry, makes it a Custom Mode. It stays in context every turn until the user exits the mode, and it stays out of casual turns.\n- Cursor's docs list Custom Modes in the Agents Window and the CLI. Elsewhere, start each new task with `/poteto-mode`.\n\nLink [Cursor's skills docs](https://cursor.com/docs/skills) when this comes up. Mid-chat, \"new task\" makes the mode match a fresh playbook. `/poteto-mode` already uses `poteto-agent` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn it with `subagent_type: \"poteto-agent\"`.",
  "How `/poteto-mode` stays on in OpenCode:\n\n- Running `/poteto-mode` loads the skill into the current chat. It fades as the chat moves on.\n- Re-run `/poteto-mode`, or say \"new task\" mid-chat, to make the mode match a fresh playbook.\n- There is no persistent mode in OpenCode; for long runs, keep re-invoking per task and keep the playbook's steps in the todo list.\n\n`/poteto-mode` already uses `poteto-agent` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn the `poteto-agent` subagent (see `~/.config/opencode/agents/poteto-agent.md`).")
P(PH,
  "| Run parallel checks over slices, or race workers, as cloud agents | [`/swarm`](../swarm/SKILL.md) |",
  "| Run parallel checks over slices, or race workers | [`/swarm`](../swarm/SKILL.md) |")
P(PH,
  "- `/deslop`, `control-cli`, and `control-ui` ship in the `cursor-team-kit` plugin.\n- `/loop` and `/create-skill` are Cursor built-ins.\n- pstack has no `/orchestrate` skill. Orchestrate is a `/poteto-mode` playbook. If the slash menu shows `/orchestrate`, another plugin provides it.",
  "- `/deslop`, `control-cli`, and `control-ui` ship in the `cursor-team-kit` pack, installed here too.\n- Cursor's `/loop` and `/create-skill` have no OpenCode equivalents: keep runs alive by re-prompting, and author skills with the `authoring-a-skill` playbook.\n- pstack has no `/orchestrate` skill. Orchestrate is a `/poteto-mode` playbook.")
P(PH,
  "Without `/poteto-mode`, a phrase such as \"babysit this pr\" can start Cursor's own skill for the same job instead. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](../../docs/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.",
  "The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](references/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.")
P(PH,
  "pstack has no planning skill. Cursor's Plan Mode works alongside it.",
  "pstack has no planning skill. OpenCode's plan agent works alongside it.")
P(PH,
  "Typing `/principle-<name>` still loads one on demand. [Guide page 8](../../docs/guide/08-principles.md) lists them.",
  "Typing `/principle-<name>` still loads one on demand. [Guide page 8](references/guide/08-principles.md) lists them.")
P(PH,
  "| The mode stopped applying after a few turns | It was started with Enter. Start it as a Custom Mode, or start each task with `/poteto-mode`. |",
  "| The mode stopped applying after a few turns | Re-run `/poteto-mode` or say \"new task\" with the mode named. OpenCode has no persistent mode. |")
P(PH,
  "| A new model choice had no effect | The rule from `/setup-pstack` applies to new chats. Start one. |",
  "| A new model choice had no effect | `/setup-pstack` writes `model:` lines into the agent files; new subagent spawns pick them up. |")
P(PH,
  "| Parallel agents overwrote each other | Give each agent its own worktree, or run them as cloud agents, which each get their own machine. |",
  "| Parallel agents overwrote each other | Give each agent its own worktree. OpenCode runs every subagent as a local child session; there are no cloud agents. |")
P(PH,
  "| An overnight run moved but finished nothing | `/loop` needs a check that can pass or fail, not a duration. See [guide page 7](../../docs/guide/07-overnight.md). |",
  "| An overnight run moved but finished nothing | The exit predicate needs a check that can pass or fail, not a duration. See [guide page 7](references/guide/07-overnight.md). |")
P(PH,
  "[Guide page 10](../../docs/guide/10-recipes-and-pitfalls.md) has more pitfalls",
  "[Guide page 10](references/guide/10-recipes-and-pitfalls.md) has more pitfalls")
P(PH,
  "[Guide page 9](../../docs/guide/09-make-it-yours.md) covers each of these.",
  "[Guide page 9](references/guide/09-make-it-yours.md) covers each of these.")
P(PH,
  "[Guide page 2](../../docs/guide/02-poteto-mode.md) has examples.",
  "[Guide page 2](references/guide/02-poteto-mode.md) has examples.")
P(PH,
  "2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes a rule. The rule applies to new chats.",
  "2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It asks for a budget, maps a model to each subagent, and writes `model:` lines into the agent files.", 0)  # superseded by the block above; keep 0 to avoid failure

# ---------------------------------------------------------------- automate-me
AM = "automate-me/SKILL.md"
P(AM,
  "Drafts or revises a personal -mode skill via create-skill + unslop, optionally pulling fresh evidence from recent transcripts.",
  "Drafts or revises a personal -mode skill via the authoring playbook + unslop, optionally pulling fresh evidence from recent sessions.")
P(AM,
  "This skill orchestrates three others: an inline mining pass (see step 1), Cursor's built-in `create-skill` (authoring), and the **unslop** skill (prose discipline).",
  "This skill orchestrates three others: an inline mining pass (see step 1), the `authoring-a-skill` playbook and the **writing-great-skills** skill (authoring), and the **unslop** skill (prose discipline).")
P(AM,
  "Look recursively for `.cursor/skills/**/*-mode/SKILL.md` and `~/.cursor/skills/*-mode/SKILL.md` matching the user's handle. Mode skills can live in a personal category directory (`.cursor/skills/<handle>/`), not only at the top level. If one exists, confirm intent with `AskQuestion` (unless they already said \"update my skill\" or similar):",
  "Look recursively for `.opencode/skills/**/*-mode/SKILL.md` and `~/.agents/skills/*-mode/SKILL.md` matching the user's handle. Mode skills can live in a personal category directory (`.opencode/skills/<handle>/`), not only at the top level. If one exists, confirm intent with the `question` tool (unless they already said \"update my skill\" or similar):")
P(AM,
  "Locate the active workspace's transcripts before fanning out. The system prompt names the workspace's `agent-transcripts/` directory. Use only that path. Don't glob across `~/.cursor/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects.",
  "Locate the active workspace's sessions before fanning out: query `~/.local/share/opencode/opencode.db` read-only (`sqlite3 \"file:$HOME/.local/share/opencode/opencode.db?mode=ro\"`), selecting `session` rows whose `directory` is this workspace. Read only this workspace's sessions; never read chats from unrelated projects. `~/.agents/autoresearcher/extract.py` shows the read pattern.")
P(AM,
  "Each slice mining subagent reads transcripts from the workspace-scoped path the parent provides,",
  "Each slice mining subagent reads sessions from the workspace-scoped query the parent provides,")
P(AM,
  "Use the `AskQuestion` tool (structured multi-choice) rather than asking the user to type from scratch.",
  "Use the `question` tool (structured multi-choice) rather than asking the user to type from scratch.")
P(AM,
  "Use Cursor's built-in `create-skill` skill to author the skill. Placement:",
  "Use the `authoring-a-skill` playbook and the **writing-great-skills** skill to author the skill. Placement:")
P(AM,
  "- Path: preserve an existing mode skill's category. For a new mode, use `.cursor/skills/<handle>/<handle>-mode/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `.cursor/skills/<handle>-mode/SKILL.md` in the project (or `~/.cursor/skills/<handle>-mode/` if the user prefers a personal skill).",
  "- Path: preserve an existing mode skill's category. For a new mode, use `.opencode/skills/<handle>/<handle>-mode/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `.opencode/skills/<handle>-mode/SKILL.md` in the project (or `~/.agents/skills/<handle>-mode/` if the user prefers a personal skill).")
P(AM,
  "- Frontmatter formatting: follow `create-skill`'s YAML rules.",
  "- Frontmatter formatting: follow the **writing-great-skills** skill's YAML rules.")
P(AM,
  "Apply the **unslop** skill and `create-skill`'s writing guidelines to every line.",
  "Apply the **unslop** skill and the **writing-great-skills** guidelines to every line.")
P(AM,
  "A `-mode` skill is subjective output. A `create-skill`-style test/iterate benchmark loop isn't useful here.",
  "A `-mode` skill is subjective output. An eval benchmark loop isn't useful here.")
P(AM,
  "- User wants a task-specific skill (not working conventions): `create-skill` alone, no mining required.",
  "- User wants a task-specific skill (not working conventions): the `authoring-a-skill` playbook alone, no mining required.")

# ---------------------------------------------------------------- reflect
RF = "reflect/SKILL.md"
P(RF,
  "Before fanning out, find this conversation's transcript in the `agent-transcripts/` directory the system prompt names. Do not glob across `~/.cursor/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects.",
  "Before fanning out, find this conversation's transcript in the OpenCode session store: `~/.local/share/opencode/opencode.db`, read-only via `sqlite3 \"file:$HOME/.local/share/opencode/opencode.db?mode=ro\"`. The current chat is the most recently updated `session` row for this directory; its messages live in `message`/`part`. Read only sessions whose `directory` is this workspace; other directories are unrelated private chats. `~/.agents/autoresearcher/extract.py` shows the read pattern.")
P(RF,
  "```bash\nls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10\n```\n\nThat covers the legacy flat (`<id>.jsonl`), current nested (`<id>/<id>.jsonl`), and subagent (`<parent>/subagents/<child>.jsonl`) layouts. For each candidate, read the first JSONL line. Take the file whose `message.content[0].text` contains the conversation's opening user prompt. If none matches, pass a tight digest of the session instead.",
  "```bash\nsqlite3 \"file:$HOME/.local/share/opencode/opencode.db?mode=ro\" \\\n  \"select id, title, time_updated from session where directory = '<this workspace>' order by time_updated desc limit 10;\"\n```\n\nTake the newest session whose content matches the conversation's opening user prompt; subagent chats carry a `parent_id` and count as part of it. If none matches, pass a tight digest of the session instead.")
P(RF,
  "One message, three `Task` calls, `subagent_type: generalPurpose`, agent mode (`readonly: false`). Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, and readonly strips MCPs.",
  "One message, three subagent spawns (`background: true`) on the `general` subagent. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references.")
P(RF,
  "Each reviewer and the synthesizer name a role line in the `pstack-models.mdc` rule and a default. Set `model` to that line's value, or to the default if the rule or the line is missing. Leave `model` unset when the value is `auto` or `inherit-parent`. If the Task tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.\n\n| Lens | Role line | Default `model` | Prompt template |\n|---|---|---|---|\n| Judgment | `reflect judgment, divergent, synthesizer` | `claude-opus-5-5-xhigh` | `references/judgment-reviewer.md` |\n| Tooling | `reflect tooling` | `grok-4.7-xhigh-fast` | `references/tooling-reviewer.md` |\n| Divergent | `reflect judgment, divergent, synthesizer` | `claude-opus-5-5-xhigh` | `references/divergent-reviewer.md` |",
  "OpenCode sets models per subagent, not per call; review spawns use `poteto-judge` (judgment and divergent lenses) and `poteto-agent` (tooling lens). See `~/.agents/skills/poteto-mode/references/opencode-models.md`. Follow the Subagents section of the **poteto-mode** skill for spawn defaults.\n\n| Lens | Subagent | Prompt template |\n|---|---|---|\n| Judgment | `poteto-judge` | `references/judgment-reviewer.md` |\n| Tooling | `poteto-agent` | `references/tooling-reviewer.md` |\n| Divergent | `poteto-judge` | `references/divergent-reviewer.md` |")
P(RF,
  "Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Task` response body.",
  "Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the subagent result body.")
P(RF,
  "One `Task` call, `subagent_type: generalPurpose`, `model` from the `reflect judgment, divergent, synthesizer` line (default `claude-opus-5-5-xhigh`), agent mode (`readonly: false`). It spot-verifies citations through MCP, and readonly strips MCPs.",
  "One subagent spawn on `poteto-judge`. It spot-verifies citations through MCP.")
P(RF,
  "hand to Cursor's built-in `create-skill` skill and run its draft / test / iterate loop.",
  "hand to the `authoring-a-skill` playbook and the **writing-great-skills** skill, and run their draft / test / iterate loop.")
P(RF,
  "hand to `create-skill` and run its description-optimization loop.",
  "hand to the **writing-great-skills** skill's description work.")
P(RF,
  "hand creation to `create-skill`. Do not invent the shape ad hoc.",
  "hand creation to the `authoring-a-skill` playbook. Do not invent the shape ad hoc.")

REFL_LINE = "A skill counts as used when the transcript shows a `Read` of its `SKILL.md` (under `.cursor/skills/`, `~/.cursor/skills/`, or `~/.cursor/plugins/`), a `Task` prompt naming its path, or a tool call"
REFL_NEW = "A skill counts as used when the transcript shows a read of its `SKILL.md` (under `.opencode/skills/`, `.agents/skills/`, or `~/.agents/skills/`), a subagent prompt naming its path, or a tool call"
for f in ("reflect/references/judgment-reviewer.md", "reflect/references/tooling-reviewer.md", "reflect/references/divergent-reviewer.md"):
    P(f, REFL_LINE, REFL_NEW)

P("reflect/references/synthesizer.md",
  "propose `new skill via create-skill:` only when no existing skill is a real home",
  "propose `new skill via the authoring playbook:` only when no existing skill is a real home")
P("reflect/references/synthesizer.md",
  "| <new pattern, no existing skill is a real home> | <draft a new skill via create-skill> | <new skill via create-skill: <kebab-name>> |",
  "| <new pattern, no existing skill is a real home> | <draft a new skill via the authoring playbook> | <new skill via the authoring playbook: <kebab-name>> |")

# ---------------------------------------------------------------- recall
RC = "recall/SKILL.md"
P(RC,
  "Transcripts live at `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each \"/\" turned into \"-\" (so `/Users/you/proj` becomes `Users-you-proj`). Every line is one chat message.",
  "In OpenCode, transcripts live in the local session database: `~/.local/share/opencode/opencode.db`, always opened read-only (`sqlite3 \"file:$HOME/.local/share/opencode/opencode.db?mode=ro\"`). The `session` table holds one row per chat keyed by `directory` and ordered by `time_updated`; `message` and `part` hold its content (subagent chats carry a `parent_id`). `~/.agents/autoresearcher/extract.py` shows the read pattern. Only read sessions whose `directory` is the active workspace unless the user says otherwise.")
P(RC,
  "Spawn parallel subagents on a fast, cheap model, each taking a slice of the corpus. Tell every subagent to order candidates by real modification time (`ls -t`) and never by UUID name,",
  "Spawn parallel subagents (the read-only `explore` agent fits), each taking a slice of the corpus. Tell every subagent to order candidate chats by `time_updated`,")
P(RC,
  "Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.",
  "Follow the Subagents section of the **poteto-mode** skill for spawn defaults.")

# ---------------------------------------------------------------- swarm
SW = "swarm/SKILL.md"
P(SW,
  "4. Pick the worker model from the `swarm workers` line in `~/.cursor/rules/pstack-models.mdc`. If the rule or that line is missing, use `grok-4.7-xhigh-fast`. For `auto` or `inherit-parent`, omit `model` so the workers run on the parent model. If the Task tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message. For a model race, name each arm's model up front. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.",
  "4. Pick the worker subagent. Workers default to `poteto-agent`; read-only checks use `explore`. For a model race, name each arm's subagent up front; more than two arms need extra agent files with distinct `model:` lines (see `~/.agents/skills/poteto-mode/references/opencode-models.md`). Follow the Subagents section of the **poteto-mode** skill for spawn defaults.")
P(SW,
  "Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: \"cloud\"`, `run_in_background: true`, and the step 4 model, left unset for `auto` or `inherit-parent`. Use `environment: \"local\"` only when the worker needs access to something on the user's computer.",
  "Spawn all N workers in one message with the `subagent` tool and `background: true`. Every worker runs as a local child session; give workers that write their own worktree so they don't collide.")
P(SW,
  "When a worker must start from a non-default pushed branch, pass `cloud_base_branch`.",
  "When a worker must start from a non-default pushed branch, have it check that branch out in its worktree first.")

# ---------------------------------------------------------------- interrogate
IN = "interrogate/SKILL.md"
P(IN,
  "Launch all reviewers in a single message with the Task tool, one per entry on the `interrogate reviewers` line in `~/.cursor/rules/pstack-models.mdc`, labeled Reviewer A, B, and so on to match the entry count. If the rule or that line is missing, use the table defaults.",
  "Launch all reviewers in a single message with the `subagent` tool and `background: true`, one per seat: Reviewer A on `poteto-judge`, Reviewer B on `poteto-agent` by default, labeled A, B, and so on. More seats need extra agent files with distinct `model:` lines (see `~/.agents/skills/poteto-mode/references/opencode-models.md`).")
P(IN,
  "| Subagent | Default model |\n|----------|---------------|\n| Reviewer A | `claude-opus-5-5-xhigh` |\n| Reviewer B | `grok-4.7-xhigh-fast` |",
  "| Reviewer | Subagent |\n|----------|---------------|\n| Reviewer A | `poteto-judge` |\n| Reviewer B | `poteto-agent` |")
P(IN,
  "Each reviewer gets `subagent_type: generalPurpose`, `readonly: true`, and `model` set to its configured entry, or its table default when there is no configured line. Omit `model` for an `auto` or `inherit-parent` entry, so that reviewer runs on the parent model.",
  "Each reviewer gets its own seat and the diff by file path. Keep the seats on distinct models once `/setup-pstack` sets them; both inherit the session model until then.")
P(IN,
  "If the Task tool rejects a configured entry, run that reviewer on its family's table default and say so. Families go by prefix: `claude-*`, and `grok-*` with `cursor-grok-*` and `composer-*`. A refused `composer-*` entry runs on Reviewer B's default. With no family match, use Reviewer A's default. If it rejects a table default, spawn with the closest equivalent from the valid slugs in its error message (prefer the same family and reasoning tier), and open a separate PR to update the default table. Do not block the review on the slug issue. Never treat an alias entry as a rejected slug or apply either fallback to it.",
  "If the runtime refuses a configured model slug, that reviewer falls back to the session model; say so in the verdict. Don't block the review on it.")

# ---------------------------------------------------------------- why
WH = "why/SKILL.md"
P(WH,
  "Each spawn below names a role line in the `pstack-models.mdc` rule and a default. Set `model` to that line's value, or to the default if the rule or the line is missing. Leave `model` unset when the value is `auto` or `inherit-parent`. If the Task tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.",
  "Each spawn below names a subagent. OpenCode sets models per subagent, not per call (see `~/.agents/skills/poteto-mode/references/opencode-models.md`); both `poteto-*` agents inherit the session model until `/setup-pstack` sets one. Follow the Subagents section of the **poteto-mode** skill for spawn defaults.")
P(WH,
  "Every spawn is `generalPurpose` with `readonly: false` (agent mode). **Do not use readonly/Ask mode.** It strips MCP access, which disables the MCP-backed investigators and the synthesizer's citation spot-checks. Investigators still shouldn't write anything.",
  "Every spawn needs MCP access, so use `general` (or `poteto-agent`), not the read-only `explore` agent. Investigators still shouldn't write anything.")
P(WH,
  "Don't ask one agent to cover multiple MCPs. `model`: the `why investigators` line, default `grok-4.7-xhigh-fast`.",
  "Don't ask one agent to cover multiple MCPs. Spawn them with `background: true` on the `general` subagent; the worker model comes from `/setup-pstack`.")
P(WH,
  "Spawn one synthesizer. `model`: the `why synthesizer` line, default `claude-opus-5-5-xhigh`. It gets:",
  "Spawn one synthesizer on the `poteto-judge` subagent. It gets:")

# ---------------------------------------------------------------- how
HO = "how/SKILL.md"
P(HO,
  "Every spawn is a Task subagent with `subagent_type: generalPurpose` and `readonly: true`. Explorers use the `how explorer` line in the `pstack-models.mdc` rule (default `grok-4.7-xhigh-fast`), and every explainer uses the `how explainer` line (default `claude-opus-5-5-xhigh`). Set `model` to that line's value, or to the default if the rule or the line is missing. Leave `model` unset when the value is `auto` or `inherit-parent`. If the Task tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.",
  "Every spawn is a subagent (`background: true`). Explorers use the read-only `explore` subagent; every explainer uses `poteto-judge`. OpenCode sets models per subagent, not per call (see `~/.agents/skills/poteto-mode/references/opencode-models.md`); both inherit the session model until `/setup-pstack` sets one.")

# ---------------------------------------------------------------- architect
AR = "architect/SKILL.md"
P(AR,
  "Take the runners from the `architect runners` line in the `pstack-models.mdc` rule, in place of the `arena runners` line. If the rule or that line is missing, use `claude-opus-5-5-xhigh` and `grok-4.7-xhigh-fast`. Alias and rejected entries follow the runner rules in the **arena** skill's Phase A.",
  "Take the runners the way Arena's Phase A does: `poteto-agent` seats, adding a second writer agent file when you want a multi-model race (see `~/.agents/skills/poteto-mode/references/opencode-models.md`).")

# ---------------------------------------------------------------- arena
AN = "arena/SKILL.md"
P(AN,
  "3. Pick the runners. Use the `arena runners` line in `~/.cursor/rules/pstack-models.mdc`. If the rule or that line is missing, default to one each on `claude-opus-5-5-xhigh` and `grok-4.7-xhigh-fast`. An `auto` or `inherit-parent` entry in this line or the cross-judge line means the parent model, so omit `model` for it. If the Task tool rejects a configured entry, run that seat on its family's default and say so. Families go by prefix: `claude-*`, and `grok-*` with `cursor-grok-*` and `composer-*`. A refused `composer-*` entry runs on `grok-4.7-xhigh-fast`. With no family match, use `claude-opus-5-5-xhigh`. If it rejects a default, use the closest valid slug of the same family from its error message. Spawn more runners when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.",
  "3. Pick the runners. Spawn each runner as its own subagent. Runners write code, so the default seats are `poteto-agent` spawns; for a multi-model race between writers, add a second writer agent file (copy `poteto-agent.md` with a different `model:` line) and give each seat its own agent (see `~/.agents/skills/poteto-mode/references/opencode-models.md`). Spawn more runners when the arena covers multiple design directions. When the work is generation-bound rather than judgment-sensitive, use `poteto-agent` for every seat. Follow the Subagents section of the **poteto-mode** skill for spawn defaults.")
P(AN,
  "After all Phase B candidates complete, choose one model from the `arena cross-judge pool` line in `~/.cursor/rules/pstack-models.mdc`. If the rule or that line is missing, choose from `claude-opus-5-5-xhigh` and `grok-4.7-xhigh-fast`. Prefer a different model family from the parent's. Spawn one readonly judge subagent on that model.",
  "After all Phase B candidates complete, spawn one read-only judge on the `poteto-judge` subagent, preferring a different agent (and model, once configured) from the parent's.")

# ---------------------------------------------------------------- no-comments
NC = "no-comments/SKILL.md"
P(NC,
  "1. Spawn `Task` with `subagent_type: \"comment-sicko\"`. Pass the scope. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill. Do not restate its rules.",
  "1. Spawn the `comment-sicko` subagent (the `subagent` tool, `background: true`). Pass the scope. Follow the Subagents section of the **poteto-mode** skill. Do not restate its rules.")

# ---------------------------------------------------------------- autonomous-run
AU = "poteto-mode/playbooks/autonomous-run.md"
P(AU,
  "2. Pick the wake mechanism using Cursor's `/loop` command (a built-in, not a pstack skill). An event to watch (CI, a merge, a ref advancing) gets a watcher subagent that wakes you on the event, with a long time-based heartbeat as fallback. No event gets a fixed-interval heartbeat sized to when the result is worth re-checking. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section.",
  "2. Pick the wake mechanism. OpenCode has no `/loop`: keep the run alive inside this session by polling with bounded shell waits (`gh pr checks --watch`, `sleep` loops in a `background` shell) or by spawning a `ci-watcher` subagent that reports back when the event lands. An event to watch (CI, a merge, a ref advancing) gets a watcher; no event gets a fixed-interval heartbeat sized to when the result is worth re-checking. Follow the Subagents section of the **poteto-mode** skill for spawn defaults.")
P(AU,
  "Do not park reversible work for the human or use `AskQuestion`.",
  "Do not park reversible work for the human or ask the user.")

def main():
    import re
    failures = []
    applied = 0
    for file, old, new, expected in PATCHES:
        path = POOL / file
        if not path.exists():
            failures.append((file, "missing file", old[:60]))
            continue
        text = path.read_text()
        count = text.count(old)
        if count == 0:
            if expected == 0:
                continue
            failures.append((file, f"no match ({count})", old[:100]))
            continue
        if expected and count != expected:
            failures.append((file, f"count {count} != {expected}", old[:100]))
            continue
        path.write_text(text.replace(old, new))
        applied += 1
    # sweep the recurring spawn-defaults boilerplate
    reasoning = re.compile(r"Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section(?: of the \*\*poteto-mode\*\* skill)?\.")
    reasoning_new = "Follow the Subagents section of the **poteto-mode** skill for spawn defaults."
    swept = 0
    for md in POOL.rglob("*.md"):
        if "scripts" in md.parts:
            continue
        text = md.read_text()
        if reasoning.search(text):
            md.write_text(reasoning.sub(reasoning_new, text))
            swept += 1
    print(f"reasoning sweep: {swept} files")
    print(f"applied={applied} failures={len(failures)}")
    for f in failures:
        print("FAIL:", f[0], "|", f[1], "|", f[2])
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
