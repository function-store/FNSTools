---
package: FNS_ToolbarRegistry
summary: 'The toolbar surface registry and mirror rail. The raw master, promoted to /sys; clone it to put your own tools on the bar.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Bookmark bar slots, order and visibility
    anchor: why-use-it
    does: 'Keeps which widgets sit on TouchDesigner''s bookmark bar, in what order and which are shown, so installing or removing a tool never leaves a hole or a dead button.'
  - name: Mirror rail
    anchor: why-use-it
    does: 'Each button on the bar is a live view of the widget inside its tool, so no button COMP is ever copied into the bar.'
  - name: Arrange the bar in Hub
    anchor: how-to-use-it
    does: 'The Toolbar tab of Hub reorders and groups widgets, sets their width and adds dividers between them.'
  - name: Hide buttons you never use
    anchor: how-to-use-it
    does: 'Hiding a button from its row in Hub takes it off the bar while the tool stays installed.'
  - name: Layout follows you
    anchor: how-to-use-it
    does: Your arrangement is saved with your settings and comes with you to every project.
  - name: Reset the toolbar layout
    anchor: how-to-use-it
    does: Reset toolbar puts every tool back in the slot it shipped in.
  - name: Drop a panel on the FNS button
    anchor: for-tool-authors
    does: 'Dropping any panel COMP on the FNS button gives it a self-registering host and puts it on the bar, the quickest way to add a tool of your own.'
    authors: true
  - name: Register from a host or from Python
    anchor: for-tool-authors
    does: 'A host copy inside a tool registers it on load; RegisterWidget(), SetWidgetDisplay() and WidgetTarget() do the same work from code.'
    authors: true
---

## Why use it

Most FNS tools put a button on TouchDesigner's bookmark bar, the row of icons
under the main menu. If each tool copied its own button in, every one of them
would need a slot that does not collide with the others, and removing a tool
would leave its button behind, dead, or a gap where it was. TouchDesigner's UI
is never saved with a project either, so each tool would have to redo the job
on every launch.

ToolbarRegistry is the one owner of that bar. Tools publish a widget into it,
and the registry decides what sits where, in what order and whether it is
shown. It also runs the **mirror rail**: each button on the bar is a mirror, a
live view of the widget inside its tool, so the bar always reflects the
registry and nothing is copied into it. Install a tool and its button appears
in its slot; remove it and the bar closes up.

## How to use it

The registry is part of the toolkit's core and installs with it. You meet it
through the tools that put buttons on the bar, and through
[Hub](/docs/fns-hub/), where the bar is arranged.

1. Left-click the **FNS** button at the right end of the main-menu bar to open
   Hub, and pick the **Toolbar** tab.
2. Drag rows to reorder the bar.
3. Hide a button you never use from its row. The tool stays installed; only
   its button leaves the bar.
4. Add dividers between widgets, put related tools in a group, or set a
   widget's width.
5. Right-click a name to open that tool's docs.

Your arrangement is saved with your settings through
[ConfigRegistry](/docs/fns-configregistry/) and follows you to every project.

- **To change one tool without opening Hub:** its **Registry** page carries
  **Toolbar Order**, **Displayed** and **Bar Width** for that tool alone, and
  every edit you make in Hub is written back there. The whole section is
  listed under [What it adds to a registered tool](#registry-section).
- **To start over:** right-click the Toolbar tab, choose **Parameters** and
  press **Reset toolbar**. Every tool goes back to the slot it shipped in, and
  TouchDesigner's own icons, the dividers and the groups go back to the shipped
  layout. Your own arrangement is lost, so it asks first.

## For tool authors

There are three ways to put a tool on the bar:

- **Drop it on the FNS button.** Drop any panel COMP on the FNS button, or
  anywhere on the Hub window, and pick **Toolbar** from the menu that opens.
  The COMP receives a self-registering host, is placed after the bar's last
  entry and appears at once. It stays where it is in your network.
- **Stamp a host from a script:**
  `op.FNS.op('FNS_ToolbarRegistry').StampHost(tool, canonical_name='MyTool')`.
- **Copy the host** out of any shipped tool and repoint it.

A host is a small copy of this registry living inside the tool. **Widget COMP**
names the panel to publish (the host's parent by default), **Canonical Name**
gives it a unique name, and **Auto-register** keeps it published for as long
as the tool exists. The host registers when it loads. In a project that has
no registry yet, the first host to load installs one in `/sys`, reachable as
`op.FNS_TOOLBARREGISTRY`; when two versions meet, the newer one takes over and
keeps every registration.

Building the widget:

- The bar draws every widget 19 pixels tall, so build it at that height. Its
  width follows the widget unless **Bar Width** is set.
- The widget stays in your tool, and the bar shows it through a Select COMP
  mirror in `/ui/dialogs/bookmark_bar`. Clicks reach the widget through the
  mirror, and its references to the rest of your tool keep resolving.

From Python, guard the call, since no registry is guaranteed to exist in a
given project:

```python
reg = getattr(op, 'FNS_TOOLBARREGISTRY', None)
if reg is not None:
	reg.RegisterWidget(op('button_mytool'), 'MyTool', order=20)
```

The registry lives in `/sys`, which TouchDesigner does not save with the
project, so a registration made from a script has to run again on every open.
A host does that for you. `UnregisterWidget()`, `SetWidgetOrder()`,
`SetWidgetDisplay()` and the `Widgets` snapshot are the rest of the manager
API. `WidgetTarget('MyTool')` returns the live widget behind a canonical name:
use it in a parameter expression and the reference follows the widget when it
moves or is renamed.
