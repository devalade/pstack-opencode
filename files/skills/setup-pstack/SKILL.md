---
name: setup-pstack
description: Configure which OpenCode subagent runs each pstack role and at what reasoning budget. Detects your available models and writes `model:` lines into the pstack agent files. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack (OpenCode)

Write `model:` lines into the pstack agent files under `~/.config/opencode/agents/`, and keep the role map at `~/.agents/skills/poteto-mode/references/opencode-models.md` current.

OpenCode chooses a model per **agent**, not per subagent call. pstack's many per-role model lines collapse into a small set of agents, and the role map records which agent serves each role.

## Steps

### 1. Detect available models

Run `opencode2 models`. Treat its output as the full set of valid slugs (`<provider>/<model>`, optionally with a `#<variant>` suffix such as `#high`). Never write a slug you have not seen there. If the command is unavailable, ask the user to paste the models they can use. `inherit-parent` is always valid: it means the agent runs on the session's model.

### 2. Load current state

Read `~/.config/opencode/agents/poteto-agent.md` and `~/.config/opencode/agents/poteto-judge.md`. Any existing `model:` line is the current choice for that agent. Read `~/.agents/skills/poteto-mode/references/opencode-models.md` for the role-to-agent map. A previous run's choices show up as those `model:` lines; keep roles whose model the user already chose differently from the default.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer the `question` tool over free text. Offer these four options with these exact labels, and name the current budget when the agent files record one. With no configured model, say that `large` matches the skill defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Translate the budget to each agent's model:

- On a model with variants, the budget picks the variant effort: `unlimited` → the highest-effort variant, `large` → the model's standard high-effort variant, `medium`/`small` → cheaper variants.
- On a model without variants, pick the closest detected model of the same family with the effort at or below the target, or mark the agent as needing a choice.
- `inherit-parent` does not change.

Map the roles onto the agents using the table in `references/opencode-models.md`: `poteto-agent` covers the code roles (feature, refactoring, bug-fix, perf-issue, hillclimb, swarm workers, tooling lenses), `poteto-judge` covers review, explanation, and judgment, `comment-sicko` covers comment review, and the read-only seats use the built-in `explore` / `general` agents.

**(c) Show the agents and confirm.** Show each agent with its model, marking any slug not in the detected set as needing a choice. Offer the detected models plus `inherit-parent` as the options. Prefer the `question` tool. If the user wants a wider model race across writer seats, offer to add a second writer agent: copy `poteto-agent.md` to `poteto-agent-b.md`, keep `mode: subagent`, and set a different `model:` line. Panel seats that name more agents than exist get that fallback.

### 4. Validate

Every real slug written must appear in `opencode2 models` output. `inherit-parent` always passes. If a chosen slug is not available, stop and ask again.

### 5. Write

1. For each agent, set or drop its `model:` frontmatter line. Shape: `model: <provider>/<model>#<variant>`. Overwrite the line; leave the rest of the file untouched.
2. Update the role table in `~/.agents/skills/poteto-mode/references/opencode-models.md` with the chosen agents and models. Re-runs overwrite the table so they stay idempotent.

### 6. Confirm

Tell the user the agent files were updated, that new subagent spawns and new sessions pick the choices up, and that re-running this skill updates them. Cursor's `~/.cursor/rules/pstack-models.mdc` does not exist in this install; do not write it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with `/create-verification-skill`." On yes, invoke the `create-verification-skill` skill. On no, move on without pushing.
