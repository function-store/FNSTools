---
package: FNS_Updater
summary: Clicking this icon will open this Wiki page.
features:
  - name: Wiki
    anchor: wiki
    icon: Wiki.png
  - name: Self-Update Feature
    anchor: self-update-feature
  - name: Notes after an update
    anchor: notes-after-an-update
  - name: Agent skill
    anchor: agent-skill
feature_list:
  - name: Update indicator on the help icon
    anchor: wiki
    does: 'The toolbar ? icon gets a yellow border when any installed package has an update; clicking it prompts to update, otherwise it opens the wiki.'
  - name: Update only changed packages
    anchor: self-update-feature
    does: 'Fetches only the packages that changed from the store, verifies each download''s hash and replaces just those, leaving uninstalled packages uninstalled.'
  - name: Settings kept across updates
    anchor: self-update-feature
    does: Saves all tool configs to a JSON file before updating and reloads each replaced tool's saved configs afterwards.
  - name: Release notes after an update
    anchor: notes-after-an-update
    does: 'Shows that release''s notes once on the first project open after an update; Show Notes After Update turns it off, and Hub''s Updates tab keeps them.'
  - name: Install agent skill
    anchor: agent-skill
    does: 'The Install agent skill command copies a reference to every installed package (promoted methods, commands, hotkeys, parameters, the registries) into the project''s .claude/skills folder or your user skills folder, so a coding agent such as Claude Code knows the toolkit before it touches the project.'
---

## Wiki

Clicking this icon will open this Wiki page. If the border of this icon is yellow it means one or more of your installed packages have an update available. Clicking it in that state will prompt you for an update.

## Self-Update Feature

If there is an update available for any package installed in your project, the `?` icon in the toolbar will have a yellow border. Clicking the icon will prompt you for an update, you can say `No` in which case it will take you to the Wiki as usual, otherwise the following is going to happen:
- Save all configs (custom parameters of tools) to a `json` file
- Fetch only the packages that actually changed from the store (verifying each download's hash), and replace just those; a package you never installed stays uninstalled
- Reload each replaced tool's saved configs

This way we can ensure that your settings are retained between updates, alongside the externally retained data, outlined in the next chapter.

## Notes after an update

The first time a project opens after an update landed, a small popup shows that release's notes. It appears once per update, never on a plain project open.

Turn off **Show Notes After Update** on the updater's parameters to skip it. The setting roams with your other toolkit settings, so one click silences the popup in every project on the machine. The notes stay readable at any time on the Hub's Updates tab.

## Agent skill

The toolkit ships a skill for coding agents: a folder of plain text pages, generated from the shipped build at every release, that tells an agent such as Claude Code what each installed package does, how it is reached, which promoted methods, quick-launch commands, hotkeys and parameters it has, and what the registries own. The store refresh keeps the machine's copy at `<user palette>/FNSTools/agent-skill/fnstools/`, beside the operator family folder.

The quick-launch command **Install agent skill** (`InstallAgentSkill`) copies it into a project:

- `where`: `project` (the default) writes `<project folder>/.claude/skills/fnstools/`; `user` writes `~/.claude/skills/fnstools/`, which every project on the machine sees.
- `agents_md`: off by default. On, the command appends one short block to the project's `AGENTS.md` that points at the skill, for agents that read that file; it never adds the block twice.

The command is idempotent: a copy of the same release is reported current, an older copy is replaced, a newer one is kept. It touches nothing outside the `fnstools` folder it owns, and logs where the copy went. [Use FNSTools from a coding agent](/docs/guides/agent-skill/) walks through the setup.
