---
package: FNS_MainMenuRegistry
summary: 'TD main-menu surface registry, including project-name display. The raw master, promoted to /sys.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: 'Order, hide and place entries'
    anchor: why-use-it
    does: 'Holds the order, visibility and left or right placement of every main-menu entry, TouchDesigner''s own items and the ones tools publish alike.'
  - name: Edit from the Hub MainMenu tab
    anchor: how-to-use-it
    does: 'The MainMenu tab of Hub reorders, hides or groups entries, so a tool''s entry can sit between TouchDesigner''s own items.'
  - name: Restore TouchDesigner's order
    anchor: how-to-use-it
    does: 'The TD button in that tab puts TouchDesigner''s own items back in their original order, all visible.'
  - name: Publish an entry from a tool
    anchor: for-tool-authors
    does: 'A tool ships a small host copy of the registry beside its widget to get a main-menu entry, reachable globally as op.FNS_MAINMENUREGISTRY.'
    authors: true
  - name: Pin next to a stock item
    anchor: for-tool-authors
    does: 'Anchor After pins an entry directly after a named TouchDesigner item, such as tutorials, and heals if that item comes and goes.'
    authors: true
  - name: Lifecycle callbacks
    anchor: for-tool-authors
    does: 'An optional mainmenu_callbacks DAT hears when its entry is registered, unregistered, shown, hidden or moved to the other side.'
    authors: true
---

## Why use it

TouchDesigner's main-menu bar runs from File and Edit on the left, through the
wiki, forum, tutorials and fps items, to the corner on the right. Several
tools want a place on it: the **FNS** button that opens
[Hub](/docs/fns-hub/), the project name that
[BorderlessTD](/docs/fns-borderlesstd/) shows once the title bar is hidden, and
[Autosave](/docs/fns-autosave/)'s on/off button. Each one copying its own
widget in would mean each guessing a free position among TouchDesigner's
items, colliding when two guess the same, and leaving a gap when one is
removed.

MainMenuRegistry manages the bar as one surface. The order, visibility and
left or right placement of every entry live here in one place, TouchDesigner's
own built-in items included, so a tool's entry can sit exactly where you want
it.

## How to use it

The registry is part of the toolkit's core and installs with it. You arrange
the bar from Hub:

1. Left-click the **FNS** button at the right end of the main-menu bar and pick
   the **MainMenu** tab.
2. Drag rows to reorder. TouchDesigner's own items are in the list too, so an
   entry can sit between two of them, the way BorderlessTD's project name
   follows the tutorials item.
3. Flip an entry between the left and right of the bar, hide what you do not
   need, or group entries.
4. To undo your changes to TouchDesigner's own items, use the tab's **TD**
   button. It puts them back in their original order, visible and outside any
   group, and leaves your other entries alone.

The layout is saved with your settings through
[ConfigRegistry](/docs/fns-configregistry/) and follows you to every project.
A tool's **Registry** page carries the same settings for its own entry, such
as **Menu Bar Order**, **Menu Bar Side** and **Displayed** (see
[What it adds to a registered tool](#registry-section)).

## For tool authors

A tool that wants a main-menu entry ships a small host copy of this registry
alongside its widget, the way BorderlessTD's project name and the hub's own
FNS button do. The quickest start is to drop the panel COMP on the FNS button
and pick **MainMenu**; the COMP gets a self-registering host and appears at
once.

On the host, **Widget COMP** is the panel to publish (the host's parent by
default), **Canonical Name** its unique name, and **Auto-register** keeps it
published. Placement:

- **Menu Bar Side** set to left packs the entry after TouchDesigner's left
  cluster; right, the default, puts it before the corner on the right.
- To sit next to something specific, put a stock item's name in **Anchor
  After**, for example `tutorials`. The entry is pinned into the gap directly
  after that item, whatever its side says. The name is looked up live on every
  sync, so if the item disappears the entry falls back to its side and returns
  when the item does.
- The bar shows your panel through a Select COMP mirror at 19 pixels tall, the
  height of TouchDesigner's own items. The width follows the panel unless
  **Bar Width** is set.

The panel handles its own clicks; the mirror passes them through. The
optional callbacks DAT is for reacting to the registry. Press **Create
Callbacks** and the host puts a `mainmenu_callbacks` DAT into your tool and
points **Callback DAT** at it; pressing it again adopts the existing DAT and
never overwrites it. Every hook is optional, and one that raises is contained:

```python
def onRegistered(canonical, info):
	# fires on every publish, including the ones at project open; keep it idempotent
	return

def onUnregistered(canonical):
	return

def onDisplayChanged(canonical, visible):
	# shown or hidden from Hub; collapsing a group does not call this
	return

def onSideChanged(canonical, side):
	# 'left' or 'right'
	return
```

The global lives in `/sys` as `op.FNS_MAINMENUREGISTRY`. From Python, guarded:

```python
reg = getattr(op, 'FNS_MAINMENUREGISTRY', None)
if reg is not None:
	reg.RegisterWidget(op('mybutton'), 'MyButton', side='left', anchor='tutorials')
```

`/sys` is rebuilt on every open, so a script registration has to run again
each time; a host does that for you. `SetWidgetSide()`, `SetWidgetAnchor()`,
`SetWidgetDisplay()` and `SetWidgetOrder()` are the rest of the manager API.
