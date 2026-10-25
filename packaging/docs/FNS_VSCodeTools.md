---
package: FNS_VSCodeTools
summary: 'Open the project in VS Code, sync DATs to files in one key, deploy autocomplete stubs, and clear the syncs before you ship.'
features:
  - name: Why use it
    anchor: why-use-it
    icon: VSCodeTools.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Where the files go
    anchor: where-the-files-go
  - name: Autocomplete with stubs
    anchor: autocomplete-with-stubs
  - name: Clearing a sync before you ship
    anchor: clearing-a-sync-before-you-ship
feature_list:
  - name: Open the project in VS Code
    anchor: how-to-use-it
    does: 'One click creates the project''s workspace file and opens it in VS Code or Cursor.'
  - name: Sync a DAT to a file
    anchor: how-to-use-it
    does: '`Ctrl+Shift+E` writes the DAT you are on to a file named after it, and from then on the DAT and the file stay in sync both ways.'
  - name: File type and folder picked for you
    anchor: where-the-files-go
    does: 'The file extension comes from the DAT''s language or contents, and an extension''s script goes in a subfolder named after its COMP.'
  - name: Choose the name and path
    anchor: where-the-files-go
    does: '`Ctrl+Shift+Alt+E` asks for the file''s name and path before syncing.'
  - name: Python typing stubs
    anchor: autocomplete-with-stubs
    does: 'Deploys stubs for your extensions and TouchDesigner''s built-in Python typings, so the editor autocompletes them, through an integration of Stubser.'
  - name: Clear syncs before shipping
    anchor: clearing-a-sync-before-you-ship
    does: 'Drops the syncs and the tool''s tags for the selected DATs, a network, or the whole project, so the content lives in the .toe again.'
---

## Why use it

A text DAT is fine for ten lines and hard work for three hundred: no search
across files, no autocomplete, no git diff. So extension code usually moves to
VS Code, and that brings its own chores: a workspace for the project, a file
path and Sync to File on every DAT, a sensible folder layout, and a way back
before you hand the `.toe` to someone else.

VSCodeTools does those chores. One button opens the project's workspace in VS
Code, one key syncs the DAT you are on to a properly named file, typing stubs
make your extensions and TouchDesigner's Python autocomplete, and one pulse
puts everything back into the `.toe` before you ship.

## How to use it

1. Set VS Code (`code.exe`) or Cursor as the text editor in TouchDesigner's
   Preferences. That is the only requirement: with **Auto-detect** on,
   VSCodeTools takes the editor from there and names the workspace after the
   project file.
2. Click the VSCodeTools button on the toolbar. The first time, it creates
   `<project name>.code-workspace` in the project folder (or uses a workspace
   file already there) and opens it in your editor. On Windows, when it finds
   the `python.exe` of an installed TouchDesigner, it also sets that as the
   workspace's Python interpreter. **Open project in
   VSCode** in quick-launch does the same, and **Auto-open** opens it every
   time the project starts.
3. Go to a DAT you want to edit in VS Code, so it is the current operator, and
   press `Ctrl+Shift+E` (with **Use Ctrl+Shift+E Shortcut** on). Shift-click
   on the button and **Externalize selected** in quick-launch do the same. The
   DAT is written to a file, Sync to File is switched on, the DAT turns pink and
   it opens in your editor.
4. Edit in VS Code. Every save updates the DAT in TouchDesigner, and changes
   made to the DAT in TouchDesigner are written to the file.

The button does a different job for each click:

- Click: open the workspace.
- Right-click: open VSCodeTools' parameters, where the editor and the workspace
  are set up.
- Shift-click: sync the current DAT to a file.
- Ctrl+Shift+Alt-click: the same, asking for the file's name and path first.
- Alt-click: clear the sync of the selected DATs.
- Middle-click: deploy stubs for the selected DATs and COMPs.

For opening a component's extension straight from the network, see
[OpenExt](/docs/fns-openext/), which works hand in hand with a synced
extension. There is also a [video breakdown](https://youtu.be/aZtraQ2N4Oc) on
YouTube.

## Where the files go

- **Folder:** files are written to **Script Sync Base Folder**, relative to the
  project folder. An extension's script gets a subfolder named after the COMP
  it belongs to, so the extension of `mixer1` lands in
  `<folder>/mixer1/`.
- **Name:** the operator's name.
- **File type:** taken from the DAT's declared language, or from its contents
  when the language says nothing specific. Python becomes `.py`, a table
  `.tsv`, and a GLSL shader `.vert` or `.frag` (from `_vert` or `_frag` in the
  DAT's name, or from the shader itself) or `.glsl`. JSON, YAML, XML and HTML
  get their own extensions too. Anything unrecognised is saved as `.py`.

If a file of that name already exists, a dialog asks for another name: **OK**
uses the name you typed, **Overwrite** syncs to the existing file, **Cancel**
stops. To pick the name and path up front, press `Ctrl+Shift+Alt+E` or
Ctrl+Shift+Alt-click the button.

Every DAT the tool syncs carries its tags (shown read-only as **Tags** on the
Clear page). That is how the Clear page tells its syncs apart from files you
set up by hand.

## Autocomplete with stubs

Typing stubs tell your editor what your components and TouchDesigner's own
Python contain, so it can autocomplete them. This part is an integration of
[AlphaMoonbaseBerlin's](https://github.com/AlphaMoonbaseBerlin)
[Stubser](https://olib.amb-service.net/component/stubser) and
[typings](https://github.com/AlphaMoonbaseBerlin/Python_TouchdesignerStubsFromWiki).

<!-- TODO: screenshot lost (expired GitHub JWT, ~Jul 2024) -- re-capture and add here. -->

1. Once per project, pulse **Install** under TD Typings on the Stubs page. It
   writes TouchDesigner's built-in typings into a `typings` folder in the
   project, so `td` module members autocomplete. After a TouchDesigner upgrade,
   **Force** writes them again over the old ones.
2. Select the COMPs whose extensions you are writing, or DATs, and pulse
   **Deploy Stubs** (or middle-click the button). Your editor can then
   autocomplete their members.
3. To include members whose names start with `_`, switch on **Private**.
   **Unpromoted** decides whether the lowercase members, the ones not reachable
   straight off the COMP, are included.

## Clearing a sync before you ship

A synced DAT reads its content from its file. Ship the `.toe` without the
script files and it opens looking for files that are not there.

The Clear page puts the content back into the `.toe`. It drops the sync and
this tool's tags at the scope you pick, from **selected DATs** through **in
current pane** and **in current pane and all children** to **all in project**.
Cleared DATs turn grey again, the files stay on disk, and each clear is one
undo step. Only DATs carrying all of the tool's tags are touched, so a sync
you set up by hand stays as it is.
