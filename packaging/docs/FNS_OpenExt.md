---
package: FNS_OpenExt
summary: Press Ctrl+E on a COMP to open its promoted extension in your external editor.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Editing and syncing back
    anchor: editing-and-syncing-back
feature_list:
  - name: Open extension by hotkey
    anchor: how-to-use-it
    does: '`Ctrl+E` on a COMP opens its first promoted extension in the external editor TouchDesigner is set to use; on a COMP without one nothing happens.'
  - name: Command palette entry
    anchor: how-to-use-it
    does: 'Also published as the quick-launch command Open extension of current, so it runs from the command palette without the hotkey.'
  - name: Sync edits back with VSCodeTools
    anchor: editing-and-syncing-back
    does: 'With the extension synced to a file by VSCodeTools, every save in your editor lands back in the running component.'
---

## Why use it

While you write a component's extension, you open it over and over: dive into
the COMP, find the extension DAT among its children, open it in your editor,
come back up. OpenExt saves that dive. With the COMP current in the network
editor, `Ctrl+E` (`Cmd+E` on macOS) opens its extension's Python in your
external editor.

## How to use it

1. Click a COMP that has a promoted extension, so it is the current operator.
2. Press `Ctrl+E` (`Cmd+E` on macOS). The extension opens in your editor.
3. To run it without the key, use **Open extension of current** from
   quick-launch, for example in [CommandKit](/docs/fns-commandkit/).

What it opens, and where:

- It acts on the current operator in the active pane, and only on a COMP. If
  the component has several extensions it opens the first one marked
  *Promote*. If it has none, nothing happens, so the key is safe to lean on
  while you move through a network.
- It finds the DAT through the extension's object, written the usual way:
  `op('./MyExt').module.MyExt(me)`. An extension set up in another form is
  skipped.
- It opens the DAT by pulsing the DAT's own **Edit** parameter, so the file
  lands in whichever external editor TouchDesigner is set to use in its
  Preferences. OpenExt has no editor setting of its own to get out of step
  with it.

## Editing and syncing back

OpenExt is the quick way in. [VSCodeTools](/docs/fns-vscodetools/) makes the
editor the place you actually write the code, and the two sit alongside each
other:

1. Once per extension, go to the extension DAT inside the COMP and press
   `Ctrl+Shift+E` (VSCodeTools' sync key, when its shortcut is switched on).
   VSCodeTools writes the DAT to a file in a subfolder named after the COMP
   and switches on Sync to File.
2. From then on, `Ctrl+E` on the COMP opens that file. Each save in your editor
   updates the DAT in TouchDesigner and the extension reinitialises with the
   new code, and anything you change in the DAT is written back to the file.
3. With VSCodeTools' stubs deployed for the COMP, the editor also autocompletes
   the extension's members.
