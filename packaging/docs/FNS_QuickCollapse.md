---
package: FNS_QuickCollapse
summary: Collapse the selected nodes into a Base COMP with one keystroke.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
hotkeys:
  - keys: Ctrl+W
    does: Collapse the selection into a `Base COMP` straight away
  - keys: Ctrl+Shift+W
    does: Collapse, but ask for the COMP's name and parent shortcut first
feature_list:
  - name: Collapse the selection into a Base COMP
    anchor: how-to-use-it
    does: 'Moves the selected nodes into a new Base COMP, wired as they were, and takes you inside it.'
  - name: Name it as you collapse
    anchor: how-to-use-it
    does: 'A second key asks for the new COMP''s name and parent shortcut first, in a small dialog.'
  - name: Undo the whole collapse in one step
    anchor: how-to-use-it
    does: 'Undo reverses the whole collapse in one step and returns you to the network you collapsed from.'
  - name: Collapse from quick-launch
    anchor: how-to-use-it
    does: 'Collapse selected runs the same collapse from quick-launch.'
---

## Why use it

Most patches start flat: you build fast in one network while you work out what
you want. Once a section works, it deserves its own component, both to keep the
network readable and to give the section a name you can refer to.
TouchDesigner's *Collapse Selected* in the right-click menu does the move, and
naming the result and giving it a parent shortcut is a second trip through its
parameters.

QuickCollapse puts the collapse on a key, and a second key asks for the name
and the parent shortcut before anything moves.

## How to use it

1. Select the nodes and press `Ctrl+W`. They move inside a new Base COMP, wired
   exactly as they were, and the network editor takes you inside it. It runs
   TouchDesigner's own *Collapse Selected* underneath, so the result is the
   component you would have got from the right-click menu.
2. Press `Ctrl+Shift+W` to do the same with a small dialog first, for the new
   COMP's name and its parent shortcut. Worth the extra key whenever the result
   is something you will refer to later: naming it at creation time is cheaper
   than renaming it and fixing up references afterwards.
3. Changed your mind? The whole collapse is one undo step, and undoing it also
   returns you to the network you collapsed from, so you are never left inside
   a COMP that no longer exists.

The collapse is also in quick-launch as **Collapse selected**. Both keys can be
rebound from **Shortcut** and **Shortcut Customize**, and **Active** switches the
tool off while keeping it installed.
