# pstack role map for OpenCode

OpenCode picks a model per **agent**, not per subagent call. These agents live in `~/.config/opencode/agents/` and carry an optional `model:` line (`provider/model` or `provider/model#variant`). With no `model:` line they inherit the session model. Run `/setup-pstack` to set them.

## Role to agent

| Role (from the skills) | Agent | Notes |
|---|---|---|
| feature, refactoring | `poteto-agent` | code writer |
| bug-fix | `poteto-agent` | code writer |
| perf-issue | `poteto-agent` | code writer |
| hillclimb | `poteto-agent` | code writer |
| hardest tasks | `poteto-judge` | read-only judgment |
| judgment and prose | `poteto-judge` | read-only |
| how explorer | `explore` | built-in, read-only |
| how explainer | `poteto-judge` | read-only |
| why investigators | `general` | needs MCP access |
| why synthesizer | `poteto-judge` | read-only; MCP allowed |
| reflect tooling lens | `poteto-agent` | |
| reflect judgment, divergent, synthesizer | `poteto-judge` | read-only |
| swarm workers | `poteto-agent` | read-only checks use `explore` |
| arena runners | `poteto-agent` seats | writers; a second writer agent gives a model race |
| arena cross-judge | `poteto-judge` | read-only |
| architect runners | `poteto-agent` seats | writers |
| interrogate reviewers | `poteto-judge` (A) + `poteto-agent` (B) | read-only review either way |
| comment review | `comment-sicko` | read-only |
| CI watching | `ci-watcher` | read-only |
| strict maintainability audit | `thermo-nuclear-code-quality-review` | read-only |

## Multi-model panels

Panels draw their diversity from distinct agent models. Two writer seats that need different models want a second writer agent: copy `poteto-agent.md` to `poteto-agent-b.md` (keep `mode: subagent`) and set its `model:` line. Panels that only read reuse `poteto-judge` and `poteto-agent` with their configured models.

## Bundle size

A panel with N seats runs N subagents. Fewer seats cost fewer tokens. `inherit-parent` agents run on the session model, which is the cheapest sane default.

## History

Cursor's per-role rule lived at `~/.cursor/rules/pstack-models.mdc`. This install replaces it with the agent `model:` lines plus this table.
