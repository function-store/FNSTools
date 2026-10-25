---
package: FNS_PaneSearchRegistry
summary: Publish a control into the find bar of every network editor pane, beside the bar's own Home toggle, one copy per pane.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Controls in every find bar
    anchor: why-use-it
    does: 'Copies a published panel COMP into every network editor pane''s find bar after Home, one copy per pane, including panes that open their bar later.'
  - name: Stock find bar when unused
    anchor: why-use-it
    does: 'With nothing contributed, every find bar stays as TouchDesigner made it, and the search itself is always left to the bar or to SearchFix.'
  - name: Register through a host copy
    anchor: for-tool-authors
    does: 'A tool ships a host copy whose Registration page names the panel COMP, a canonical name, its order and whether it is displayed.'
    authors: true
  - name: Python widget API
    anchor: for-tool-authors
    does: 'RegisterWidget(), UnregisterWidget(), RefreshWidget() and Instance() add, remove, refresh and find a find bar contribution from Python.'
    authors: true
  - name: Reach the find bar's operators
    anchor: for-tool-authors
    does: A script in the contributed panel reaches the bar's search field and the pane's network path through me.parent(2).
    authors: true
---

## Why use it

Every network editor pane has a find bar, the one that opens with the search
field, the arrows and the Home toggle. TouchDesigner builds it separately for
each pane, the first time that pane opens it. A tool that wants a control in
it, a checkbox or a depth field, has to add one to every pane's bar, including
bars that do not exist yet because their pane has not opened one, and has to
agree on order with every other tool doing the same.

PaneSearchRegistry makes the bar open to contributions. A tool publishes a
panel COMP, and a copy of it appears in every pane's find bar, after Home. Each
pane gets its own copy, so a control can keep its own state per pane, and a
pane that opens its find bar later gets the copies too. TouchDesigner's UI is
never saved with a project, so the copies are rebuilt on every open.

It adds controls to the bar and nothing else. The search itself is left to
the bar, or to a tool that replaces it, such as
[SearchFix](/docs/fns-searchfix/). **With nothing contributed, every find bar
stays as TouchDesigner made it.**

## How to use it

The registry is part of the toolkit's core and installs with it, and there is
nothing to set up. SearchFix is its first contributor: the checkboxes and the
depth field SearchFix adds to the find bar arrive through this registry, in
every pane's bar, including panes you open later. Contributions sit after
Home, in the order their tools ask for.

## For tool authors

A tool that wants a control in the find bar ships a small host copy of this
registry, the same shape as a toolbar or navbar entry. The host's Registration
page names the contribution: the **Widget COMP** to copy (the host's parent by
default), a **Canonical Name**, its **Find Bar Order** among the
contributions, and whether it is **Displayed**. **Auto-register** keeps it
published. A copy is stamped from the master with
`op.FNS.op('FNS_PaneSearchRegistry').StampHost(tool, canonical_name='mytool')`.

From Python, guarded:

```python
reg = getattr(op, 'FNS_PANESEARCHREGISTRY', None)
if reg is not None:
	reg.RegisterWidget(panel, 'mytool', order=10)
```

`UnregisterWidget()` takes it out of every bar, and `RefreshWidget()` replaces
every pane's copy after the panel changed. Until you refresh, each bar keeps
the copy it was given; a copy is also kept, with its state, for as long as its
source is the same operator. `Instance(findbar, 'mytool')` returns the copy in
one pane's find bar. `/sys` is rebuilt on every open, so a script registration
has to run again each time; a host does that for you.

The copy lives inside the find bar, so a script in it reaches the bar's own
operators with `me.parent(2)` from a DAT inside the panel: the search field is
`search/text1`, and the network the pane shows is in `path`.
