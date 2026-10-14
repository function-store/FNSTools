---
package: FNS_GlobalOutSelect
summary: 'Your Global OP Shortcuts in a tree, with every Out operator inside them; drag a row out as a Select, or jump to it.'
features:
  - name: GlobalOutSelect
    anchor: globaloutselect
feature_list:
  - name: Tree of shortcuts and outs
    anchor: globaloutselect
    does: 'Lists your Global OP Shortcuts in a tree with the out operators found inside each, refreshed on demand with Refresh.'
  - name: Drag rows out as Selects
    anchor: globaloutselect
    does: Dragging a row into a network editor places a Select pointing at that operator.
  - name: 'Open viewer, parameters or network'
    anchor: globaloutselect
    does: 'A row opens a viewer, the parameters, or a floating network editor at the referenced location.'
---

## GlobalOutSelect

A tab of [Hub](/docs/fns-hub/) (the **FNS** button in the main-menu bar).

It lists your **Global OP Shortcuts** in a tree, with any `out` operators
found inside each one. Drag a row into a network editor to place a **Select**
pointing at that operator; a row also lets you open a viewer, open the
parameters, or open a floating network editor at the referenced location.

The list is refreshed only on demand, so the tool costs nothing while you are
not looking at it: click **Refresh** in the tab after adding shortcuts or outs.
