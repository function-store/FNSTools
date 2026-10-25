---
package: FNS_Updater
summary: 'Updates the toolkit in place: only the packages that changed are replaced, and your settings are kept.'
features:
  - name: Why use it
    anchor: why-use-it
    icon: Wiki.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Notes after an update
    anchor: notes-after-an-update
  - name: Agent skill
    anchor: agent-skill
feature_list:
  - name: Check for updates
    anchor: how-to-use-it
    does: 'Compares every installed package with the published release, from the Updates tab or quick-launch, downloading only a small manifest.'
  - name: Update only changed packages
    anchor: how-to-use-it
    does: 'Fetches only the packages that changed from the store, verifies each download''s hash and replaces just those, leaving uninstalled packages uninstalled.'
  - name: Settings kept across updates
    anchor: how-to-use-it
    does: 'Saves every tool''s settings before anything is replaced, and each replaced tool comes back with them.'
  - name: Store for offline installs
    anchor: how-to-use-it
    does: 'Keeps the whole release in this machine''s store, so Pick Tools works without an internet connection.'
  - name: Patreon sign-in and licence keys
    anchor: how-to-use-it
    does: 'Holds this machine''s Patreon sign-in and Gumroad licence keys; the token lives in the operating system keystore, never in the project.'
  - name: Release notes after an update
    anchor: notes-after-an-update
    does: 'A pass that updated something prints the release and its notes in the Textport; the Updates tab keeps them, and one switch turns the line off.'
  - name: Install agent skill
    anchor: agent-skill
    does: 'The Install agent skill command copies a reference to every installed package (promoted methods, commands, hotkeys, parameters, the registries) into the project''s .claude/skills folder or your user skills folder, so a coding agent such as Claude Code knows the toolkit before it touches the project.'
---

## Why use it

Updating a TouchDesigner tool by hand means downloading its new `.tox`,
replacing the old copy in every project that has one, and setting its
parameters again. With a whole toolkit installed that is an afternoon of work,
and a setting you forget to copy over turns up later as a bug.

The updater does it from inside TouchDesigner. It compares what your project
has with the published release, fetches only what changed, replaces those
packages in place and keeps your settings. It also keeps the machine's package
store that Pick Tools and the [FNS operator family](/docs/fns-opfamily/) read
from, and it carries the agent skill for coding agents.

## How to use it

1. Pulse **Open Settings** on the toolkit container and switch to the
   **Updates** tab of the [console](/docs/fns-console/). **Check for updates**
   from quick-launch starts the same check.
2. The check compares every installed package with the published release. It
   downloads only the release's manifest, so it is cheap to run. Newer
   packages are listed with their release notes.
3. Update one package or all of them.

During an update pass:

- Every tool's settings are saved first, through
  [ConfigRegistry](/docs/fns-configregistry/).
- Only the packages that changed are fetched from the store, each download is
  checked against its hash, and just those packages are replaced. A package you
  never installed stays uninstalled: an update never adds a tool you did not
  choose.
- Packages are replaced one at a time, a few frames apart, with the updater's
  own package last.
- Each replaced tool comes back with your settings.

Anything you changed inside a tool's own network is replaced along with it;
[Working in your project](/docs/guides/working-in-your-project/) says what
survives and how to keep your own version of a tool. **Status** on the
updater's parameters shows how the last check, refresh or update went.

A few things you may want to change:

- **Installing on a machine that is offline at the venue.** Leave **Keep the
  Whole Release in the Store** on. After an install or an update pass the rest
  of the release (about 12 MB) is downloaded into this machine's store too, so
  Pick Tools works without a connection. **Refresh Store** fills the store now
  and touches no project.
- **Patreon tools.** You sign in from the picker with **Sign in with Patreon**,
  and the updater keeps that sign-in for this machine. Nothing secret is stored
  in the project: the token lives in the operating system keystore. **Sign
  Out** forgets the entitlement and leaves installed packages alone. Gumroad
  licence keys are per tool, so redeeming another one adds to the account.
  [Getting started](/docs/guides/getting-started/) covers how tiers unlock.

Coming from FNSTools v2: its updater, the yellow border on the toolbar's `?`
icon, only watches the GitHub releases page and keeps reporting that you are up
to date. [Moving from v2](/docs/guides/moving-from-v2/) covers the one-time
step to v3, after which this updater takes over.

## Notes after an update

When an update pass replaces at least one package without a failure, the
Textport gets one line naming the release and its notes. If the release's notes
are all per package, the line says so and points you to the Updates tab. It is
never a popup and never appears on project start.

Turn off **Show Notes After Update** to skip it. The setting roams with your
other toolkit settings, so one click silences the line in every project on the
machine. The notes stay readable at any time on the Updates tab, each next to
its package.

## Agent skill

The toolkit ships a skill for coding agents: a folder of plain text pages,
generated from the shipped build at every release, that tells an agent such as
Claude Code what each installed package does, how it is reached, which promoted
methods, quick-launch commands, hotkeys and parameters it has, and what the
registries own. The store refresh keeps the machine's copy at
`<user palette>/FNSTools/agent-skill/fnstools/`, beside the operator family
folder.

The quick-launch command **Install agent skill** copies it into a project. From
the Textport it is `op.FNS_UPDATER.InstallAgentSkill()`.

- `where`: `project` (the default) writes
  `<project folder>/.claude/skills/fnstools/`; `user` writes
  `~/.claude/skills/fnstools/`, which every project on the machine sees.
- `agents_md`: off by default. On, with `where` set to `project`, the command
  appends one short block to the project's `AGENTS.md` that points at the
  skill, for agents that read that file. It never adds the block twice.

Running it again is safe: a copy of the same release is reported current, an
older copy is replaced, and a newer one is kept. It touches nothing outside the
`fnstools` folder it owns, and logs where the copy went.
[Use FNSTools from a coding agent](/docs/guides/agent-skill/) walks through the
setup.
