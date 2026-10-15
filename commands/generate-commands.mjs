#!/usr/bin/env node
// Regenerate OpenCode slash commands for the vendored pstack + cursor-team-kit skills.
//
// Reads <name>/SKILL.md frontmatter from the skills pool (~/.agents/skills) for the
// skill names listed in packs.json, and writes one command per skill to
// ~/.config/opencode/commands/<name>.md.
//
// Usage: node generate-commands.mjs [--out <dir>]
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const here = path.dirname(new URL(import.meta.url).pathname);
const packs = JSON.parse(fs.readFileSync(path.join(here, "packs.json"), "utf8"));
const skillsArg = process.argv.indexOf("--skills-dir");
const skillsRoot = skillsArg > -1 ? process.argv[skillsArg + 1] : path.join(os.homedir(), ".agents", "skills");
const outArg = process.argv.indexOf("--out");
const outDir = outArg > -1 ? process.argv[outArg + 1] : path.join(os.homedir(), ".config", "opencode", "commands");

function frontmatter(text) {
  if (!text.startsWith("---")) return {};
  const end = text.indexOf("\n---", 3);
  if (end === -1) return {};
  const raw = text.slice(4, end);
  const out = {};
  for (const line of raw.split("\n")) {
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (m) out[m[1]] = m[2].trim();
  }
  return out;
}

function clean(value) {
  if (!value) return "";
  let v = value.trim();
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
    v = v.slice(1, -1);
  }
  v = v.replace(/\\"/g, '"').replace(/\s+/g, " ");
  return v;
}

function yamlString(value) {
  return '"' + value.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
}

const names = packs.flatMap((pack) => pack.skills);
let written = 0;
const missing = [];
fs.mkdirSync(outDir, { recursive: true });

for (const name of names) {
  const skillPath = path.join(skillsRoot, name, "SKILL.md");
  if (!fs.existsSync(skillPath)) {
    missing.push(name);
    continue;
  }
  const fm = frontmatter(fs.readFileSync(skillPath, "utf8"));
  let desc = clean(fm.description) || clean(fm.name) || name;
  if (desc.length > 200) desc = desc.slice(0, 200).replace(/\s+\S*$/, "") + "...";
  const body = [
    "---",
    `description: ${yamlString(desc)}`,
    "---",
    "",
    `Use the \`${name}\` skill for this task: load it with the \`skill\` tool (id \`${name}\`); if the tool rejects it, read \`~/.agents/skills/${name}/SKILL.md\` and follow it.`,
    "",
    "$ARGUMENTS",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(outDir, `${name}.md`), body);
  written += 1;
}

console.log(`wrote ${written} commands to ${outDir}`);
if (missing.length) {
  console.log(`missing skills (no SKILL.md): ${missing.join(", ")}`);
}
