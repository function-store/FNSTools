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

## Performing a show

FNSTools has a **Perform Mode** for shows. The tools that only help you
build (the overlays on the network editor, the radial menu, the watchers
behind hovering and dragging, Autosave) stop, and everything your show uses
keeps running. Switch it from the FNS button's right-click menu, from the
quick-launch palette, or with **Perform Mode** on the FNSTools page of the
`/FNSTools` root. The FNS button turns red while it is on.

- **It follows TouchDesigner's Perform Mode.** Press F1 and FNSTools
  performs too; leave it and FNSTools goes back to how it was. Turn off
  **Follow TD Perform Mode** on the same page to keep them separate.
- **Use it in Designer mode too.** If you run a show with the network editor
  open and your output in a window of its own, switch Perform Mode on by
  hand: TouchDesigner's Perform Mode never starts, but the authoring tools
  still get out of the way.
- **It is saved with the project.** Save a show file with Perform Mode on
  and it opens ready to perform. It never carries over to your other
  projects.
- **Nothing is lost.** No tool's settings change, so switching Perform Mode
  off brings every overlay and helper back exactly as you left it.

The full list of what stops is on the
[Hub page](/docs/fns-hub/#perform-mode).

## Single downloads

A free tool can also be downloaded on its own from the picker. That copy works by itself and does not update itself.

If you install FNSTools later in the same project:

- The picker does not install a second copy of a tool that is already there. It tells you where the copy is.
- The FNSTools console lists the copy under **Updates**, **Needs attention**. **Take over** moves it into `/FNSTools`, settings included, and from then on it is updated like the rest. If FNSTools already has its own copy of that tool, Take over deletes the single one instead.
- Until you take it over, the single copy hands its shortcut to the FNSTools copy, so the toolkit keeps working.

## For AI agents and scripts

The same rules apply to an assistant or a script working in your project: change tools through their parameters, never inside `/FNSTools`. The short version for agents is at [/llms.txt](/llms.txt), and the toolkit container carries the same rules in its `README`.

An agent that should know the toolkit itself, every package's methods, commands, hotkeys and parameters, gets that from the agent skill: run **Install agent skill** and read [Use FNSTools from a coding agent](/docs/guides/agent-skill/).
