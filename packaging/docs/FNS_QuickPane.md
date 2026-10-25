---
package: FNS_QuickPane
summary: 'Peek into a COMP without splitting panes by hand: hold the modifiers and drag, or press an arrow shortcut.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
hotkeys:
  - keys: ctrl.shift.left ctrl.shift.right ctrl.shift.up ctrl.shift.down
    does: Split the pane on that side and open the selected COMP in it; press again to close it
feature_list:
  - name: Split by drag gesture
    anchor: how-to-use-it
    does: 'With a COMP selected, hold the modifiers and drag toward a side: a pane opens there, already inside the COMP and homed. The same drag closes it.'
  - name: Split by arrow keys
    anchor: how-to-use-it
    does: 'With a COMP selected, `Ctrl+Shift` and an arrow key splits on that side and drops you into the component; the same key closes the pane it opened.'
  - name: Open a pane on each side at once
    anchor: how-to-use-it
    does: 'Keeps a pane on each side at once, and marks the panes it opened with a green border so you can tell them from your own.'
  - name: Split pane command
    anchor: how-to-use-it
    does: 'A Split pane quick-launch command asks for the direction, right by default, so you can split without either gesture.'
---

## Why use it

To look inside a component while keeping the network you are working in, you
split the pane, navigate the new pane into the component and home it. That is
several clicks every time you want a quick look at what a Base COMP does, and
as many again to close it.

QuickPane makes it one move. Select a COMP, then drag or press an arrow key:
a pane opens beside the current one, already inside the component and homed.
The same move closes it again.

## How to use it

- **Drag:** select a COMP, hold `Alt+Ctrl+Shift` (`Cmd+Ctrl+Shift` on
  macOS) and drag the mouse toward the side where you want the new pane. It
  opens on that side, inside the COMP and homed. To close it, hold the same
  keys and drag in the same direction again.
- **Keys:** with a COMP selected, `Ctrl+Shift+Left`, `Right`, `Up` or `Down`
  splits on that side and drops you into the component. The same key again
  closes the pane it opened. Nothing happens unless the current operator is a
  COMP, so the keys are safe to lean on.

QuickPane keeps one pane per side, so you can have one open on the right and
another below at the same time. The panes it opened carry a green border around
their pane bar, which tells you which ones the keys will close.

To change how much of the pane a new split takes, set **Ratio Horz/Vert**: the
first value for a horizontal split, the second for a vertical one.

From quick-launch ([CommandPalette](/docs/fns-commandpalette/)), **Split
pane** asks for the direction and defaults to right, and **Toggle QuickPane**
switches the tool on or off.
