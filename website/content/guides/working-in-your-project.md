---
title: Working with FNSTools in your project
order: 12
summary: What you can change on an FNSTools tool, what an update replaces, and how to keep your own version of a tool.
---

FNSTools installs its tools into one container at the root of your project, `/FNSTools`, and keeps them current. That works because every tool in the container belongs to FNSTools: an update replaces it whole. This page says what that means for the changes you make.

## What an update replaces

Each tool in `/FNSTools` is replaced whole when it updates. Anything changed inside it is gone afterwards:

- its network, its operators and their wiring
- its extensions and scripts
- its name: a renamed tool is still recognised, and comes back under its own name

So do not rename a tool, move it out of `/FNSTools`, or edit inside it, and expect the change to last.

## What you can change

- **Settings.** A tool's parameters are its settings. They are saved for you, in the shared settings file or in the project, as the **Config Scope** on the FNSTools root says, and they survive updates.
- **Hotkeys**, through the Hotkey Manager.
- **Your own templates and tables**, which live in your palette folder, outside the tools.

## Keeping your own version of a tool

To change a tool for good, make it yours:

1. Copy it out of `/FNSTools` into your own network and give it a new name.
2. On the copy's **Common** page, remove the `<FNS:GLOBAL>` tag from **Tags**. Without it, FNSTools leaves the copy alone: it is never offered for take over and it keeps its shortcut.
3. If the tool has a **Global OP Shortcut**, give the copy a different one. Two components with the same shortcut is an error in TouchDesigner, and the first one keeps it.

Your copy is then yours to edit. FNSTools does not update it.

## Single downloads

A free tool can also be downloaded on its own from the picker. That copy works by itself and does not update itself.

If you install FNSTools later in the same project:

- The picker does not install a second copy of a tool that is already there. It tells you where the copy is.
- The FNSTools console lists the copy under **Updates**, **Needs attention**. **Take over** moves it into `/FNSTools`, settings included, and from then on it is updated like the rest. If FNSTools already has its own copy of that tool, Take over deletes the single one instead.
- Until you take it over, the single copy hands its shortcut to the FNSTools copy, so the toolkit keeps working.

## For AI agents and scripts

The same rules apply to an assistant or a script working in your project: change tools through their parameters, never inside `/FNSTools`. The short version for agents is at [/llms.txt](/llms.txt), and the toolkit container carries the same rules in its `README`.
