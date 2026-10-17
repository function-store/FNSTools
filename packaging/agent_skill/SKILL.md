---
name: fnstools
description: "Drive an installed FNSTools toolkit from a coding agent. Use when a TouchDesigner project holds FNS_ COMPs or op.FNS_ shortcuts, when the user mentions FNSTools, the Hub, the FNS toolbar or quick-launch commands, or asks what an FNS tool does and how to call it from code."
---

# FNSTools

FNSTools is a toolkit of TouchDesigner components by Function Store
(https://functionstore.tools): workflow tools, additions to TouchDesigner's own
UI, and operators. It is installed once per machine into the user palette
folder, `<user palette>/FNSTools` (TouchDesigner's `app.userPaletteFolder`),
and placed into a project as one root COMP whose children are the installed
packages. This bundle was generated from the release named in `VERSION`;
`references/index.md` lists every package it covers.

The skill does not depend on a bridge. With an MCP bridge into TouchDesigner
(Envoy or any other) the agent calls the methods below directly; without one
it writes the same calls into scripts or DATs the user runs.

## Where things are

- `op.FNS` is the toolkit root COMP in the project. `op.FNS.op('FNS_BeatMod')`
  reaches an installed package by its COMP name. The root carries two pulses,
  `Picktools` (install and remove tools) and `Opensettings` (every tool's
  settings on one page), and a table DAT named `installed` that records each
  installed package with the artifact hash, release and time it came from.
- Package COMP names keep the `FNS_` prefix (`FNS_BeatMod`); every listing a
  user reads shows the public name (BeatMod). Shortcuts, file names and
  command keys keep the prefix too.
- Not every package is a child of the root: a member of the FNS operator
  family is placed from the FNS tab of the OP Create dialog, like a stock
  operator, and a few tools are installed beside the toolkit at the project
  root. The package page's "Reach it" section says where each one is.
- The machine folder `<user palette>/FNSTools/` holds `store/` (one tox per
  package plus `manifest.json`, the mirror the installer and updater read),
  `config/FNStools_config.json` (roaming settings), `tables/` (externalised
  tables such as the hotkey table), `OpTemplates/` (the global template
  library), `FNS/` (the operator family, one tox and one json sidecar per
  member) and `agent-skill/` (this bundle).
- `op.FNS_UPDATER` is the updater: `Installed()` is the project's install
  record, `Compare()` reports what the store has newer bytes for without
  touching the network, `CheckUpdates()` fetches the manifest and compares,
  `UpdateProject()` replaces only the packages that differ, keeping settings.

## How a package is reached

- A package with a global shortcut is reached by it from anywhere in the
  project: `op.FNS_UPDATER`, `op.FNS_HOTKEY_MANAGER`, `op.FNS_BEATMOD`. The
  package page and `references/index.md` name it. A package without one is
  reached by its COMP (`op.FNS.op('CookBar')`) or by the placed copy.
- The promoted API of a package is the set of `UpperCamelCase` members of its
  extension, called on the COMP itself: `op.FNS_UPDATER.Compare()`. A
  `lowerCamelCase` member is the package's own wiring (reached only as
  `comp.ext.<ExtensionName>.method()`, where the name is the extension's
  Extension Name parameter, not its class name); a `_leading` member is
  private. Each package page lists the promoted API with signatures and the
  first line of each docstring, reflected from the shipped build.
- Promoted members are resolved by the COMP's attribute lookup, so they do
  not appear in `dir(comp)`; the package page is the listing.
- A package's own settings are its custom parameters: `op.FNS_BEATMOD.par.Bpm`.
  Each page ends with the parameter list (name, label, style, default, help).
- `Access` on a page names the tier the package needs: Free, or a Patreon
  tier. A tier package installs only for an account that holds it; the page's
  Docs link is the same page the user sees on the website.

## The registries

Thirteen registries own the toolkit's shared surfaces: the toolbar, the pane
bars, the main menu, the OP Create dialog, the pane-type menu, the console,
the Hub's tabs, the Palette Browser, the timeline, the find bar, the network
overlay, the quick-launch commands and the settings file. Each runs as one
global promoted into `/sys/FNS_Registries` and is reached by its shortcut
(`op.FNS_CONFIGREGISTRY`, `op.FNS_TOOLBARREGISTRY`, ...). A tool joins a
surface by registering with the registry (`RegisterWidget`, `RegisterTab`,
`RegisterTool`, ...) and the registry owns the surface, its tables and its
files from then on. `references/registries.md` has every registry, what it
owns, how a tool joins it and what a consumer reads from it.

## Quick-launch commands

Tools declare commands, and `op.FNS_COMMANDREGISTRY` collects them for the
in-TouchDesigner command palette (FNS_CommandPalette) and the TDX launcher.

- `op.FNS_COMMANDREGISTRY.Commands()` is the live list: one dict per command
  with `key`, `tool`, `id`, `label`, `help`, `path` and, where the command
  declares it, `state`.
- `op.FNS_COMMANDREGISTRY.Run(key, args=None, kwargs=None)` runs one. The
  key is the declaring COMP's path, `#`, and the command's id:
  `op.FNS.op('FNS_Updater').path + '#checkforupdates'` for a package's own
  command, and for one a COMP inside the package declares (the built-in
  TouchDesigner commands under FNS_CommandRegistry, for example)
  `op.FNS.op('FNS_CommandRegistry/FNS_BuiltinCommands/TD_Session').path + '#togglerealtime'`.
  `Commands()` rows carry the live key.
- A command is a promoted method of the COMP that declares it, so the
  method can also be called on that COMP directly.
- `references/commands.md` lists every command of every public package with
  its label, id, help, method, declaring COMP and parameters; the package
  page repeats its own.

## Op alternatives

A stock operator type may have FNS alternatives: a package page's
"Alternative for" section and the index line name the types. When the user
creates such an operator from the OP Create dialog with the gate held (the
`Shortcutalternatives` parameter on the op-menu registry's Alternatives page,
default `alt ctrl`), a popup offers the alternatives, and the chosen one is
placed in the operator's place with every input and output reconnected. A
package that is only in the store is offered too and fetched before it is
placed; placing is a place, not an install. From code,
`op.FNS_OPMENUREGISTRY.Alternatives` is the merged `{opType: [alternative,
...]}` and `op.FNS_OPMENUREGISTRY.PlaceAlternative(orig_op, alternative)`
does the placement.

## Settings and hotkeys

- Settings persist through `op.FNS_CONFIGREGISTRY`: every registered tool's
  custom parameters are written as one section of the aggregated file
  (`ConfigPath` is its absolute path), globally in
  `<user palette>/FNSTools/config/FNStools_config.json` or inside the `.toe`
  when the root's `Configscope` parameter is `project`
  (`SetConfigScope('global' | 'project', prompt=False)` flips it).
  `SaveAll()` and `LoadAll()` snapshot and re-apply every tool; `SaveTool(name)`
  and `LoadTool(name)` do one. A setting is changed by setting the tool's
  parameter; the registry writes the file.
- Hotkeys are custom parameters on the tools, holding a combo such as `alt.g`
  or `ctrl.shift.g`. `op.FNS_HOTKEY_MANAGER.Discover()` lists every binding in
  the project with its owner, parameter and current value, `ComputeConflicts()`
  the combos bound more than once, `ApplyBinding(display_path, par_name, combo)`
  rebinds one, `ResetToDefault(display_path, par_name)` restores the
  parameter's default, and `SaveHotkeys()` writes the gathered table under
  `<user palette>/FNSTools/tables/`. Each package page's Hotkeys section is
  that discovery, taken at build time.
- The Hub is the manager window: the FNS button in the main-menu bar opens
  it, as does `op.FNS.op('FNS_Hub').Open(tab=None)`. The console is the
  toolkit's web front, served from inside the project:
  `op.FNS_CONSOLE.Open(tab=None)` shows it and `Url()` is its address while
  it serves.

## One fact the network does not show

`op.FNS` exists only while the toolkit root is in the project. A package can
also run on its own, as a single tox dropped into a project with no toolkit
root, and then there is no `op.FNS` and no registry globals. Code that may run
in both places tests `hasattr(op, 'FNS')` before using either.

## Finding out more

`references/index.md` (one line per package: category, summary, docs link,
shortcut, what it is an alternative for), then `references/<Package>.md`
(what it does, how it is reached, the promoted API, commands, hotkeys,
requirements, parameters), then the page's Docs link for the full
user-facing documentation.
