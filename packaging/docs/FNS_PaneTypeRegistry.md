---
package: FNS_PaneTypeRegistry
summary: 'Named, persistent pane-type entries for TD''s panebar: any COMP can appear in the pane-type dropdown and be recalled with configurable owner, type, window actions and callbacks.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Recall a COMP from the pane-type dropdown
    anchor: why-use-it
    does: 'A COMP joins the pane bar''s pane-type dropdown; picking it turns the pane into that COMP with the entry''s owner, pane type, window behaviour and callbacks.'
  - name: Register a COMP from the dropdown
    anchor: how-to-use-it
    does: 'Right-click a built-in row to register the network the pane shows as a new entry of that type, kept with the project.'
  - name: Run one action on right-click
    anchor: how-to-use-it
    does: 'Right-click a registered row to run one step on its own, such as Set Owner, Tear Away or Open Floating Network Editor, or to unregister it.'
  - name: Open a floating network editor
    anchor: how-to-use-it
    does: The Floating network editor quick-launch command opens a floating network editor on the network you are in.
  - name: Register a tool as a pane type
    anchor: for-tool-authors
    does: 'A tool ships a host copy of the registry and registers on load, declaring its COMP, pane type, and the window actions or callback to run on recall.'
    authors: true
  - name: Callback on recall
    anchor: for-tool-authors
    does: 'An optional callback runs after the built-in actions, for what they cannot express: focusing a field, opening a panel, restoring state.'
    authors: true
---

## Why use it

The dropdown on every pane bar switches a pane between Network Editor,
Geometry Viewer, Panel and the rest. Getting your own control panel or tool UI
into a pane takes more steps than that: switch the pane to Panel, point it at
the right COMP, maybe maximise it or open its parameters, and repeat the same
steps every session.

PaneTypeRegistry lets a COMP join that dropdown as a **named, persistent
entry**. Pick it and the pane becomes that COMP, with the owner, pane type,
window behaviour and callback the entry declares. Entries are recalled by
name and come back when the project opens, so the UI you reach for every
session is one dropdown pick away. The registry also adds an **OP Browser**
row, which TouchDesigner's own list leaves out.

## How to use it

The registry is part of the toolkit's core and installs with it. Tools that
register a pane type simply appear in the dropdown:
[PreviewPanel](/docs/fns-previewpanel/) and its **PopViewer** are two. Pick
one and the pane turns into it.

To add an entry of your own:

1. In any pane, go to the COMP you want to recall, so that it is the network
   the pane shows.
2. Open the pane-type dropdown and right-click the row of the type you want
   the entry to use, for example **Panel**.
3. Choose **Register "*name*" as Panel...**, edit the menu name if you like,
   and press **Register**.

The registry puts a small host inside the COMP, so the entry re-registers
every time the project opens. A new entry recalls as *Owner + Type*: it points
the pane at the COMP and switches the pane to that type.

Right-click a registered row for one-off actions on the pane you are in:
**Recall (as registered)**, or a single step on its own (**Owner + Type**,
**Set Owner**, **Change Type**, **Maximize**, **Tear Away**, **Float**, **Open
Parameters**, **Run Callback**), plus **Open Floating Network Editor** on the
entry's COMP and **Unregister**. The steps the entry runs on recall are
ticked.

The quick-launch command **Floating network editor** opens a floating network
editor on the network you are in.

## For tool authors

A tool that wants its UI available as a pane type ships a host copy of this
registry and registers on load. The host's Registration page declares the
entry: the **COMP** that owns the pane (the host's parent by default), the
**Canonical Name** shown in the dropdown (the host COMP's name when empty),
and the **Pane Type** applied on recall. A few things to know:

- The Panel pane type needs a Panel COMP; the other types accept any COMP.
- To place the entry among the custom rows, set **Menu Order**: 0 is first,
  -1 appends. TouchDesigner's own rows are not moved.
- To choose what recall does, use the toggles under **Default Actions**: Set
  Owner, Change Type, Maximize, Tear Away, Float and Open Parameters. Tear Away
  always sets the owner and type first, so the torn-off pane shows the right
  COMP.
- With **Auto-register** on, the COMP is registered at once and the entry
  follows these settings as they change. With it off, use **Register** or
  Python.

On recall the built-in actions run first, in that order, and then the
callback. Press **Create Callback** for a callbacks DAT with an
`onPaneRecall(ctx)` skeleton, assigned to **Callback**; it never overwrites a
DAT that already has text. The hook is for what the flags cannot express, and
one that raises is contained: the recall still completes.

```python
def onPaneRecall(ctx):
	# ctx: pane (reassigned after a type change), pane_comp (the pane bar COMP
	# that triggered it), owner (the registered COMP or None), canonical,
	# info (the raw entry), registry (the extension)
	owner = ctx.get('owner')
	if owner is not None and hasattr(owner, 'Open'):
		owner.Open()
```

The global lives in `/sys` as `op.FNS_PANETYPEREGISTRY`. From Python, guarded:

```python
reg = getattr(op, 'FNS_PANETYPEREGISTRY', None)
if reg is not None:
	reg.RegisterPanel(op('mypanel'), 'My Panel', pane_type='PANEL', maximize=True)
```

`RegisterPanel()` also takes `set_owner`, `change_type`, `tear_away`,
`float_pane`, `open_parameters`, `callback` and `menu_order`.
`UnregisterPanel()` removes an entry and `RecallPanel(pane, name)` recalls one
into a pane. `/sys` is rebuilt on every open, so a script registration has to
run again each time; a host does that for you.
