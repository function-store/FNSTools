---
package: FNS_Misc
summary: 'Two toolbar utilities: a global Mouse CHOP to drive interaction, and a toggle for the network backdrop.'
features:
  - name: Why use it
    anchor: why-use-it
    icon: QuickMouse.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Global Mouse CHOP
    anchor: global-mouse-chop
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

## Why use it

Misc is a grab bag of small toolbar helpers, each too small to be a tool of
its own: a mouse you can map without building anything, and a switch for the
previews drawn behind your network.

## How to use it

Both helpers are buttons on the toolbar, Global Mouse CHOP and Background
Viewer. To move them, hide one or regroup them, run
**Open toolbar configurator** from quick-launch. It opens
[FNS_Hub](/docs/fns-hub/) on its Toolbar tab, where
[ToolbarRegistry](/docs/fns-toolbarregistry/) decides which widgets sit on the
bar, in what order, and which are shown.

The Global Hog CHOP that used to sit here moved to
[CookBar](/docs/cookbar/): Ctrl+right-click its toolbar button.

## Global Mouse CHOP

For a quick interaction test, placing a Mouse In CHOP in your network just
to try something leaves one more operator to clean up afterwards. The Global
Mouse CHOP button skips that step.

Click it and a small popup opens with the channels of a global **Mouse In
CHOP**. Drag a channel straight out of the popup and drop it onto a
parameter. The button is a toggle: click it again to switch the global mouse
off.

## Background Viewer

The network editor can draw TOPs and CHOPs behind your network, which is
handy for watching an output while you wire and in the way when you need to
read the nodes. The Background Viewer button turns those backdrop viewers on
or off for the current pane in one click.

Right-click it to turn off the display flag on every TOP in the network you
are in, including those inside its components. It is the fast way back from
a pane full of previews.
