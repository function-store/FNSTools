---
package: FNS_Misc
summary: 'Two toolbar utilities: a global Mouse CHOP to drive interaction, and a toggle for the network backdrop.'
features:
  - name: Global Mouse CHOP
    anchor: global-mouse-chop
    icon: QuickMouse.png
  - name: Background Viewer
    anchor: background-viewer
feature_list:
  - name: Global Mouse In CHOP
    anchor: global-mouse-chop
    does: 'A popup with a global Mouse In CHOP whose channels you drag straight onto parameters, with no operator to place first.'
  - name: Background viewer toggle
    anchor: background-viewer
    does: Turns the current pane's backdrop TOP and CHOP viewers on or off in one click.
  - name: Clear TOP display flags
    anchor: background-viewer
    does: Right-click the Background Viewer button to turn off the display flag on every TOP in the current network.
---

## Global Mouse CHOP

A handy tool for quick interaction tests: a global **Mouse In CHOP** whose
channels you can drag straight out of the popup and drop onto parameters,
with no operator to place first.

## Background Viewer

A toolbar toggle for the current pane's backdrop viewers: TOPs and CHOPs drawn
behind the network, on or off in one click. Right-clicking it turns off the
display flag on every TOP in the network you are in, which is the fast way back
from a pane full of previews.

Both live on the toolbar. Which widgets sit on the bar, in what order, and
which are shown is up to
[ToolbarRegistry](/docs/fns-toolbarregistry/).

The Global Hog CHOP that used to sit here moved to
[CookBar](/docs/cookbar/): Ctrl+right-click its toolbar button.
