---
package: FNS_PaneSearchRegistry
summary: Publish a control into the find bar of every network editor pane, beside the bar's own Home toggle, one copy per pane.
features:
  - name: Pane Search Registry
    anchor: pane-search-registry
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Controls in every find bar
    anchor: pane-search-registry
    does: 'Copies a published panel COMP into every network editor pane''s find bar after Home, one copy per pane, including panes opened later.'
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

## Pane Search Registry

Every network editor pane has a find bar, the one that opens with the search
field, the arrows and the Home toggle. TouchDesigner builds it per pane the first
time that pane opens it. This registry makes the bar extensible: a tool publishes
a panel COMP and a copy of it appears in every pane's find bar, after Home.

Each pane gets its own copy, so a control can keep state per pane. A pane that
opens its find bar later gets the copies too. `/ui` is never saved with a project,
so the copies are rebuilt on every load.

It ships as its own core package, promoted to `/sys` (global shortcut
`op.FNS_PANESEARCHREGISTRY`), alongside the other surface registries. It adds
controls to the bar and nothing else: the search itself is left to the bar, or to
a tool that replaces it, like SearchFix.

**With nothing contributed, every find bar stays as TouchDesigner made it.**

## For tool authors

A tool that wants a control in the find bar ships a small **host** copy of this
registry, the same shape as a toolbar or navbar entry. The host's Registration
page names the contribution: the panel COMP, a canonical name, its order among
the contributions, and whether it is displayed.

From Python, `op.FNS_PANESEARCHREGISTRY.RegisterWidget(panel, 'mytool',
order=10)` does the same, with `UnregisterWidget()` to take it out and
`RefreshWidget()` to replace every pane's copy after the panel changed.
`Instance(findbar, 'mytool')` returns the copy in one pane's find bar.

The copy lives inside the find bar, so a script in it reaches the bar's own
operators with `me.parent(2)` from a DAT inside the panel: the search field is
`search/text1`, the network the pane shows is in `path`.
