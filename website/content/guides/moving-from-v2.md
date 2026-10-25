---
title: Moving from v2
order: 15
summary: For projects that have the 2023 toolkit inside. Take it out, install v3, and see what carries over.
---

FNSTools v3 replaces the 2023 toolkit (`FunctionStore_tools_2023`, versions 2.x). The two cannot share a project: both claim the `FNS` shortcut and the same places in TouchDesigner's interface. Take the old toolkit out of a project before you put v3 in.

v3 needs TouchDesigner 2025 or newer. If you are staying on TouchDesigner 2023, keep using v2: version 2.12.0 is its last release, on [GitHub](https://github.com/function-store/FunctionStore_tools/releases/tag/v2.12.0) and on the [`dev2023` branch](https://github.com/function-store/FunctionStore_tools/tree/dev2023).

## The last v2 offers the move

v2.12.0 is the final release of the 2023 toolkit, and its one job is this hand-over. The v2 updater (the yellow border on the toolbar's `?` icon) installs it like any other update. Once it is in, on TouchDesigner 2025 or newer, a dialog offers **Move to v3**, and the `?` icon keeps its yellow border so you can come back to it later. The move saves your settings file, removes the 2023 toolkit and its toolbar from the project, drops the v3 installer at the root and opens its tool picker. After picking your tools, save the project and restart TouchDesigner once; the operator-create menu keeps its old entries until then.

On TouchDesigner 2023 the same release only tells you once that it is the last version. Everything keeps working.

If you would rather do it by hand, or your v2 is older than 2.4 and has no updater, the steps are below. v3 is not published as a GitHub release, so nothing older than v2.12.0 will ever point you at it.

## Take v2 out of a project

1. Save a copy of the project first.
2. At the root of the network (`/`), delete the `FunctionStore_tools_2023` component. If you renamed it, type `op.FNS` in the Textport to see where it is.
3. Save the project, then close and reopen it, so TouchDesigner rebuilds its interface without the old toolbar and navbar.

Do this for each project that has v2 inside, before you install v3 in it.

## Install v3

1. Drag [`FNSTools.tox`](https://storage.functionstore.tools/fnstools/latest/FNSTools.tox) into the root of the project.
2. The picker opens on the first drop. Pick your tools and install them; [Getting started](/docs/guides/getting-started/) walks through it.

## Your startup file

If your startup file has v2 inside (`FNS_TDDefault_2023.toe`, or your own file with the toolkit in it), every new project starts with the old toolkit. Make a new one: open an empty project, drop in `FNSTools.tox`, pick your tools, save it, and set it in `Preferences > General > Startup File Mode`.

## What carries over

- **The palette folder.** v2 kept its files in `FNStools_ext` in your user palette. The first time v3 runs, it renames that folder to `FNSTools` and keeps everything in it.
- **Your OpTemplates library.** OpTemplates finds the library you already have, including the `_2023` copy, before it creates a new one. Whatever it replaces is kept as `OPTemplates1.before-adopt.tox`.
- **Tool settings start fresh.** v2 saved them in `FNS_tools_config.json`. v3 tools start from their own defaults and save to a new file, `FNSTools/config/FNStools_config.json`. The old file stays where it was, so you can still look up a value.
- **Hotkeys.** [HotkeyManager](/docs/fns-hotkeymanager/) lists every binding in your install and flags conflicts.

## Help

Ask in the Troubleshoot channel on [Discord](https://discord.gg/b4CaCP3g3K), or open an [issue on GitHub](https://github.com/function-store/FunctionStore_tools/issues).
