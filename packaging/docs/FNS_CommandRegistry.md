---
package: FNS_CommandRegistry
summary: 'Collects the commands your tools declare, and TouchDesigner''s own, and serves them to whatever can run them: the CommandPalette inside TouchDesigner and the TDXL launcher''s tray palette. Tools never depend on it being installed.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: How the command pieces fit
    anchor: how-the-command-pieces-fit
  - name: How tools are found
    anchor: how-tools-are-found
  - name: What a command carries
    anchor: what-a-command-carries
  - name: Built-in commands
    anchor: built-in-commands
  - name: Reading and running commands
    anchor: reading-and-running-commands
feature_list:
  - name: Share one list across palettes
    anchor: how-the-command-pieces-fit
    does: 'The CommandPalette and TDX Launcher Ultra read the same commands, and favourites, hidden commands and presets made in one show in the other.'
  - name: Tag-based tool discovery
    anchor: how-tools-are-found
    does: 'Finds tools tagged fnscommands and harvests their commands, so a tool installed before any palette or launcher still appears when one arrives.'
  - name: Curation that survives moves
    anchor: what-a-command-carries
    does: 'Favourites, hidden flags and presets are keyed on tool name and command id, so they survive a tool being moved in the network.'
  - name: Presets per copy or pinned
    anchor: tools-with-several-copies
    does: 'A preset runs on every copy of a tool, or is pinned to one instance label and waits quietly where no copy carries it.'
  - name: Built-in TouchDesigner commands
    anchor: built-in-commands
    does: 'Serves TouchDesigner''s own actions, such as the Textport, dialogs, pane changes, saving, recent files, realtime, perform mode and cook rate, badged TD in the palette.'
  - name: Newest version wins for duplicates
    anchor: built-in-commands
    does: 'When two packages offer the same canonical command, the newest package version is served and the other set aside, so the list never doubles.'
  - name: Tools work without it
    anchor: how-tools-are-found
    does: 'Every call a tool makes is guarded, so with no registry in the session nothing happens and nothing errors.'
    authors: true
  - name: Commands derived from methods
    anchor: what-a-command-carries
    does: 'Builds each command''s label, help and prompted parameters from the method''s name, docstring and signature, with type hints setting input styles.'
    authors: true
  - name: 'Declared context, surface and state'
    anchor: what-a-command-carries
    does: 'Tools declare what a command acts on, where it is offered, where its live value lives, its capability group and a cross-package canonical id.'
    authors: true
  - name: Commands for each tool copy
    anchor: tools-with-several-copies
    does: 'Each copy of a multi-copy tool registers its commands under its own path, labelled by FnsInstance() and grouped under one name by FnsToolName().'
    authors: true
  - name: Declaration validation
    anchor: tools-with-several-copies
    does: 'Enforces limits at harvest (24 commands per tool, 6 parameters, 5 contexts, 8 surfaces) and rejects malformed declarations with a reason.'
    authors: true
  - name: Consumer API
    anchor: reading-and-running-commands
    does: 'Commands(), Run(key, args), RescanTools(), Shadowed(), Rev() and Version() let a palette or launcher list, run and re-harvest commands and check the contract version.'
    authors: true
---

## Why use it

A tool with a handful of actions tends to grow its own way of reaching them:
a hotkey for one, a pulse on a parameter page for another, a toolbar button
for the one people use most. A dozen tools later nobody remembers which key
does what, and a palette that wanted to list every action would have to know
every tool by name. A tool that called into such a palette directly would
also break in every project where the palette is missing.

CommandRegistry sits in the middle. A tool marks a promoted method as a
command and forgets about it. The registry finds those tools, reads their
commands out of the live class by reflection, validates them, and serves one
flat list to whatever is present to run them: the
[CommandPalette](/docs/fns-commandpalette/) inside TouchDesigner and the tray
palette of [TDX Launcher Ultra](https://launcher.functionstore.xyz). It adds
TouchDesigner's own actions to that list, so there is something to run even
in a project with no other tool.

If you use the toolkit, this is the piece that makes tool commands show up
when you type into a palette. There is nothing to set up.

## How to use it

- It comes with the toolkit's core, promoted to `/sys` with the global
  shortcut `op.FNS_COMMANDREGISTRY`. The launcher's companion carries the
  same copy, so running the launcher over a session brings one too.
- To run commands, open a consumer: the CommandPalette inside TouchDesigner,
  or the launcher's tray palette, where `>` lists commands and `?` lists
  tools.
- **Status** on the Command Registry page shows how many commands and tools
  are registered, with the change revision.
- The registry rescans on init. If you dropped a tool into the project by hand
  and its commands are missing, pulse **Rescan Tools**.
- To publish commands from a component of your own, put
  [CommandKit](/docs/fns-commandkit/) inside it and mark the methods you want
  exposed. FNS tools do the same through their ExtUtils.

## How the command pieces fit

Four pieces make the command system, and this registry is the one in the
middle: tools write into it, palettes read from it, and neither side knows
the other.

| Piece | Role | Where it lives |
|---|---|---|
| **CommandRegistry** (this page) | Collects every command tools declare, plus TouchDesigner's own, and serves one list to whatever can run them | A core package promoted to `/sys`, installed with the toolkit's core; the launcher's companion carries the same copy |
| [CommandKit](/docs/fns-commandkit/) | Lets any component publish commands: mark a method, or declare a spec | A direct child of your own component. FNS tools carry the same module in their ExtUtils and announce themselves, so they never need the kit |
| [CommandPalette](/docs/fns-commandpalette/) | A consumer inside TouchDesigner: a hotkey, a ranked list, Enter runs the command | Installed like any tool |
| [TDX Launcher Ultra](https://launcher.functionstore.xyz) | A consumer outside TouchDesigner: its tray palette lists the same commands under `>` and `?` and runs them in the session you summoned it over | A separate desktop app with its own releases |

A project can hold any subset. A tool alone announces into nothing and
works as before; the registry alone serves the built-ins to nobody; a palette
alone opens with no tool commands to list. The registry reaches a project two
ways, as this core package and inside the launcher's companion, and a project
with both sees a single registry, since the newer copy wins and the other is
set aside. Favourites, hidden commands and presets are one machine-wide file
that both consumers read and write, keyed by tool name and command id, so
curation made in one shows in the other.

## How tools are found

Discovery works by tag. A tool that declares commands is tagged
`fnscommands`, so a registry that arrives later, or is replaced by a newer
version, rediscovers every tool by rescanning tags and re-harvesting. That is
why a tool can be installed before any consumer exists and still show up the
moment one does. Registrations whose tool no longer exists are dropped the
next time the list is built.

The registry ships as its own core package. **It stands apart from the
surface registries**: it carries no `RegistryBase`, injects no chrome, and
claims no part of the TouchDesigner UI. It shares the `/sys/FNS_Registries`
home with them and nothing else.

The authoring side is a separate package, [CommandKit](/docs/fns-commandkit/),
and the split is deliberate: a tool needs the kit and *no* registry. Every
call a tool makes is guarded, so with no registry in the session nothing
happens and nothing errors.

## What a command carries

Most of a command is derived from the method, with little left to declare:
the label from its CamelCase name, the help from its docstring's first line,
and prompted parameters from the signature, with type hints becoming input
styles and a missing default marking a parameter required.

What a tool declares on top of that is the part a consumer cannot guess:

- **`context`**: what the command acts on, so a consumer can resolve that
  subject before invoking and grey the command out when it is absent.
  `network` is the current pane's component, `selected` the operators
  selected there, `current` the single current operator, `rollover-op` and
  `rollover-par` the operator or parameter under the cursor. A list means any
  of them will do.
- **`surface`**: where it should be offered. A different axis from `context`:
  one says what it needs, the other where it appears. `quick` (the
  quick-launch list) is the default; the launcher also knows `session`, its
  Current-view companion bar, and `context-menu`, its session right-click
  menu. Consumers ignore surfaces they do not serve.
- **`state`**: where the command's live value lives, so a toggle can render as
  ON/OFF and a setter can show its number: a custom parameter name on the
  tool, or `{'method': 'GetX'}` for a promoted method. Read at query time, so
  it is never stale, which also means it has to be cheap.
- **`capability`**: a shared group id that lets a consumer render a family of
  commands together as one group.
- **`builtin`**: TouchDesigner's own functionality, so a consumer can list it
  apart. FNS tools do not set it; the registry's own built-ins do.
- **`canonical`**: a cross-package identity for a command two packages might
  both offer. Opt-in and never derived from the id, because the same id
  (`toggleactive`, say) legitimately exists on many tools.

Every command has two names. The wire key, `path#id`, is what a consumer
hands back to run it. Curation keys on `tool#id`, the tool's name and the
command id, so favourites, hidden flags and presets survive a tool being
moved in the network; both palettes use that identity. Ids and tool names
are therefore permanent: renaming either orphans a user's curation, so a
shipped id is public API.

### Tools with several copies

Some tools are meant to be placed more than once, one copy per output or per
target. Each copy registers the same commands under its own path, so running
one always reaches the copy it belongs to. Two optional promoted methods on the
copy make them readable in a palette:

- **`FnsInstance()`** returns a short label for this copy, such as the output
  it drives. It is read every time the list is built, so it follows renames
  and target changes, and it travels with each command as `instance`. Palettes
  show it beside the label: `Freeze scope · Main out`.
- **`FnsToolName()`** returns one tool name for every copy, for when the COMP
  names differ (`Scope1`, `Scope2`). Without it each copy counts as a separate
  tool, and a favourite on one never reaches the others.

Favourites and hidden flags always apply to every copy, in every project. A
preset can either run on every copy, listed once per copy, or be pinned to one
label with `tool#id@instance`. A pinned preset waits quietly in projects
where no copy carries that label.

Limits are enforced at harvest: 24 commands per tool, 6 parameters per
command, 5 contexts and 8 surfaces per command. A malformed declaration is
rejected with a reason, so nothing broken is served.

## Built-in commands

The registry ships with TouchDesigner's own actions as commands, so a palette
has something to run in a project with no other tool installed: opening the
Textport, the Errors and Performance Monitor dialogs, the Palette Browser,
Preferences and Window Placement, tearing a pane away or changing its type,
saving the project with or without its external toxes, loading a recent file,
toggling realtime, perform mode and always-on-top, setting the cook rate and
master volume, opening the project or TouchDesigner folder, and copying,
viewing or editing the current operator. **Add Embody**, **Add TDMCP** and
**Add TDX Launcher Utility** download the latest release of that component
and add it to the project root; each is hidden while its component is
already in the project.

The built-ins are flagged `builtin`, so a consumer can keep them apart from
your tools' commands: the FNS palette badges them `TD`, lists them after tool
commands and leaves them out of `?`.

Every built-in also declares a canonical id. When two packages offer the same
command, the one with the newest package version is served, with every copy of
that package kept, and the other is set aside and listed by `Shadowed()`, so
installing a newer registry beside an older one never doubles the list. The
TDXL launcher's companion carries this same package, so a project with both
installed sees a single registry and a single set of built-ins.

## Reading and running commands

This is the side a palette, a launcher or any other consumer talks to.

- `op.FNS_COMMANDREGISTRY.Commands()` returns the full list.
- `Run(key, args)` invokes one by its wire key, `path#id`; `kwargs` can be
  passed as well.
- `RescanTools()` re-harvests after a tool's command set changes at runtime.
- `Shadowed()` lists what canonical-id arbitration withheld and what beat it.
- `Rev()` is a change counter that goes up on every change to the registry,
  so a consumer knows when to rebuild its list.
- `Version()` reports the contract version (1.12.0 as of this writing), so a
  consumer can tell which fields it can rely on.
- `Register(owner, commands)` replaces one owner's command set and
  `Unregister(owner)` drops it. CommandKit and the ExtUtils announcer call
  these for you.

Unknown fields are ignored, in both directions. A consumer that predates
`context` simply does not see it, and a tool that declares a surface no
consumer serves loses nothing, which is what makes it safe to declare new
fields early.

Handlers run synchronously on TouchDesigner's main thread, so a command
returns quickly and defers long work; a returned dict with `ok: False` marks
the run failed, and nothing raises into the consumer.
