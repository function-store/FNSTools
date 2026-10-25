---
package: FNS_GlobalOutSelect
summary: 'Your Global OP Shortcuts in a tree, with every Out operator inside them; drag a row out as a Select, or jump to it.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Tree of every shortcut and its outs
    anchor: how-to-use-it
    does: 'Lists the Global OP Shortcuts in your project in a tree, with the Out operators found inside each one.'
  - name: Drag a row out as a Select
    anchor: how-to-use-it
    does: Dropping a row into a network editor places a Select pointing at that operator.
  - name: Open a viewer, the parameters or a network editor
    anchor: how-to-use-it
    does: 'A row opens a viewer, the parameters, or a floating network editor at the operator''s location.'
  - name: Refresh only on demand
    anchor: how-to-use-it
    does: 'The tree is rebuilt only when you press Refresh, so it never takes a frame while you work.'
---

## Why use it

Global OP Shortcuts are how a project reaches its shared parts from anywhere:
an `op.Audio` component doing the analysis, an `op.Scenes` component holding
the visuals. The Out operators inside them are what the rest of the project
wants. To use one somewhere else, you navigate there, find the out, come back,
create a Select and point it at the operator.

GlobalOutSelect shows every shortcut in the project with the Out operators
inside it, in one tree. Drag a row into the network you are working in, and the
Select is there.

## How to use it

1. Open [Hub](/docs/fns-hub/) with the **FNS** button in the main-menu bar and
   go to the GlobalOutSelect tab.
2. Click **Refresh**. The tree fills with your Global OP Shortcuts, each with
   the Out operators found inside it.
3. Drag a row into a network editor. A Select pointing at that operator is
   placed where you drop it.

A row can also open a viewer, the parameters, or a floating network editor at
the operator's location, which is a quick way to check what an out carries
before you use it.

The list is refreshed only on demand, so the tool costs nothing while you are
not looking at it. Click **Refresh** again after you add shortcuts or outs.
