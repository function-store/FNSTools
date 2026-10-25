---
package: FNS_NavbarRegistry
summary: 'The pane-bar surface registry. The raw master, promoted to /sys; clone it to add your own pane-bar widgets.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Widgets in every pane bar
    anchor: why-use-it
    does: 'Registered widgets are placed in every pane bar TouchDesigner has open and in the default bar new panes start from, so they show in panes you open later too.'
  - name: Navbar layout in Hub
    anchor: how-to-use-it
    does: 'Hub''s Navbar tab reorders pane-bar items, flips them between the left and right side, groups them and shows or hides them.'
  - name: Layout follows you
    anchor: how-to-use-it
    does: Your pane-bar arrangement is saved with your settings and comes with you to every project.
  - name: Panel COMP to navbar package
    anchor: for-tool-authors
    does: Dropping any panel COMP on the FNS button registers it as its own self-installing navbar package.
  - name: Host copy registration
    anchor: for-tool-authors
    does: 'A tool that wants a pane-bar widget ships a host copy of this registry, picks a side and a kind, and registers on load.'
    authors: true
  - name: Widget copy in each pane
    anchor: for-tool-authors
    does: 'Each pane bar gets its own copy of a widget, so a breadcrumb can show its own pane''s path; RefreshWidget() re-copies after you edit it.'
    authors: true
---

## Why use it

TouchDesigner gives every pane its own pane bar, the strip across the top of
the pane with the network path in it, and keeps one more default bar that new
panes are built from. A tool that wants a button there has to put a copy into
every one of those bars, again for each pane you open later, and agree with
every other tool on the order and on which side of the path it sits. When the
tool goes, every copy has to be found and removed.

NavbarRegistry does that for the tools that live on the pane bar, such as
[ParentHierarchy](/docs/fns-parenthierarchy/),
[iopBrowser](/docs/fns-iopbrowser/) and
[CustomParTools](/docs/fns-custompartools/). It decides which widgets appear,
in what order, on which side and whether they are shown, and places them in
the default bar and in every live bar, so a widget shows up in every pane,
including the ones you open later.

## How to use it

The registry is part of the toolkit's core and installs with it. You arrange
the pane bar from [Hub](/docs/fns-hub/):

1. Left-click the **FNS** button at the right end of the main-menu bar and pick
   the **Navbar** tab.
2. Drag rows to reorder the items.
3. Click an item's side to flip it between the left of the path and the right.
4. Hide what you do not use, or group items that belong together.

The layout is saved with your settings through
[ConfigRegistry](/docs/fns-configregistry/) and follows you to every project.
A tool's own **Registry** page carries **Navbar Order**, **Navbar Side** and
**Displayed** for that tool; edits made in Hub are written back there (see
[What it adds to a registered tool](#registry-section)).

## For tool authors

The quickest way to put your own panel on the pane bar is to drop the panel
COMP on the FNS button and pick **Navbar** from the menu. It gets a
self-registering host and becomes its own self-installing navbar package. A
COMP that should also go on the toolbar is dropped a second time.

A tool that ships a pane-bar widget carries a host copy of this registry and
registers on load. The host publishes its **Widget COMP** (the host's parent
by default) under a unique **Canonical Name**, and **Auto-register** keeps it
published. Two settings are particular to the pane bar:

- To choose where it docks, set **Navbar Side**: left of the path area, after
  TouchDesigner's own left-hand icons, or right of it, before TouchDesigner's
  right-hand icons.
- To say what the COMP is, set **Item Kind**. A *widget* is a panel in the
  bar's left-to-right flow, and its height follows the bar. An *overlay* is a
  panel outside the flow, such as a click-through layer over the path cells:
  it is shown and hidden but never reordered. *Logic* is a non-panel COMP that
  only needs a running copy inside every pane bar.

The global registry lives in `/sys` as `op.FNS_NAVBARREGISTRY`. From Python:

```python
reg = getattr(op, 'FNS_NAVBARREGISTRY', None)
if reg is not None:
	reg.RegisterWidget(op('mywidget'), 'MyWidget', side='left', kind='widget')
```

`/sys` is rebuilt on every open, so a script registration has to run again
each time; a host does that for you. `SetWidgetSide()`, `SetWidgetOrder()`,
`SetWidgetDisplay()` and `SideSequences` cover the rest.

**The bars hold copies of your widget.** Each pane bar needs its own instance
(a breadcrumb has to show its own pane's path), so the registry copies the
widget into every bar. Two things follow:

- After you edit the widget, call
  `op.FNS_NAVBARREGISTRY.RefreshWidget('MyWidget')`. Until then every bar keeps
  running the copy it was given at registration.
- A reference that climbs out of the widget resolves against the bar, so
  `op('../Sibling')` finds nothing in a bar copy. Reach the rest of your package
  through its global OP shortcut. The reverse holds too: `../panenav` and
  `../emptypanel` exist only inside a bar, so keep bar-specific wiring behind
  an `if`.
