---
title: Use FNSTools from a coding agent
order: 14
summary: Install the agent skill so Claude Code or another coding agent knows the toolkit's packages, methods, commands and settings before it touches your project.
---

A coding agent that opens a project with FNSTools in it sees a container full of `FNS_` components, a dozen global shortcuts and hundreds of promoted methods, and nothing that says what they are. Left to itself it guesses: it rebuilds something a tool already does, calls a callback as if it were an API, or edits a settings file by hand. The agent skill is the explanation it was missing: a folder of plain text pages the toolkit generates from itself at every release, in the Agent Skills format that Claude Code reads on its own and other agents can be pointed at.

## What the skill contains

- `SKILL.md`: what the toolkit is, where it lives on the machine, how a package is reached (its global shortcut, or `op.FNS.op('Name')` for a child of the toolkit root), what the registries own, how quick-launch commands run, how op alternatives work, where settings and hotkeys live, and the one fact an agent cannot read off the network: `op.FNS` exists only while the toolkit root is in the project.
- `references/index.md`: one line per package, with its category, summary, docs link, shortcut and the operator types it is an alternative for.
- `references/<Package>.md`: one page per public package. What it does, how to reach it, its promoted API with every method's signature and a sentence for each, its commands, hotkeys, requirements and parameters.
- `references/commands.md`: every quick-launch command with its id and the key that runs it.
- `references/registries.md`: the registries, what each one owns and how a tool joins it.

Everything on a package page is generated from the shipped build, so it describes the tools you have and nothing else. A release is refused when the authored pages name a shortcut or a method the build does not carry.

## Onboard your agent from here

Paste this line into your coding agent. It fetches the setup instructions, installs the skill into the project you are in and reports where it went. TouchDesigner does not need to be open, and FNSTools does not need to be installed yet.

<div class="copyline"><code id="agent-prompt">Fetch and execute the instructions at https://functionstore.tools/agent-setup/prompt.md to set me up for FNSTools</code><button type="button" class="btn btn-secondary copy-btn" data-copy-from="agent-prompt">Copy</button></div>

The instructions are published at [agent-setup/prompt.md](/agent-setup/prompt.md). They install the same folder the command below does, verified against the release manifest, and they name no release: the manifest carries it, so the line above stays the same across updates.

## Install it in a project

1. Install FNSTools, as in [Getting started](/docs/guides/getting-started/). The skill arrives with the toolkit: the store refresh places it in your user palette, beside the operator family.
2. Run the quick-launch command **Install agent skill**. It is on the [command palette](/docs/fns-commandpalette/) and the TDX launcher, and from the Textport it is `op.FNS_UPDATER.InstallAgentSkill()`. It copies the skill to `.claude/skills/fnstools/` in the project folder. Pass `user` as the first argument to put it in `~/.claude/skills/fnstools/` instead, which covers every project on the machine.
3. Open the project in your agent. Claude Code finds `.claude/skills/fnstools/` by itself and reads the core page when the conversation turns to FNSTools. For an agent that reads `AGENTS.md`, run the command with its `agents_md` option on: it appends one short block to that file pointing at the skill, once.

Running the command again reports the copy as current. After an update of the toolkit, run it once more and the older copy is replaced; a copy from a newer release than the installed toolkit is left alone.

## With and without a bridge

With an MCP bridge into TouchDesigner (Envoy or any other), the agent calls the promoted methods directly: `op.FNS_COMMANDREGISTRY.Run(key)` for a command, `op.FNS_UPDATER.Compare()` for the update state, a tool's own parameters for its settings. Without a bridge it writes the same calls into scripts or DATs for you to run. The skill says so in its first lines, so the agent does not need to be told.

## Where the files are

| | |
|---|---|
| On the machine | `<user palette>/FNSTools/agent-skill/fnstools/`, kept current by the store refresh |
| In a project | `<project folder>/.claude/skills/fnstools/` |
| For every project | `~/.claude/skills/fnstools/` |
| In a release | `agent-skill.json` beside the installer files, listed in the release manifest |

`VERSION` inside the folder names the release the pages were generated from. The [Updater](/docs/fns-updater/#agent-skill) page describes the command's parameters.
