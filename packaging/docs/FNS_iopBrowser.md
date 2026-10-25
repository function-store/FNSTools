---
package: FNS_iopBrowser
summary: Browse the internal operators and the OP tree of the network you are in, from a popup opened off the pane bar.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Browse the iops in reach
    anchor: how-to-use-it
    does: 'A button on the pane bar lists the iops available from the COMP you are in, those of every parent from the nearest up.'
  - name: Drag or jump to an iop
    anchor: how-to-use-it
    does: 'Drag any listed iop straight into the network editor, or use the list to navigate to it.'
  - name: Find an operator in the OP tree
    anchor: how-to-use-it
    does: 'The popup carries the network''s OP tree with search, for finding an operator without leaving the pane.'
  - name: Add an iop by drop
    anchor: how-to-use-it
    does: 'Dropping an operator on the button makes it an internal operator shortcut of the network you are in, root included; CustomParTools, if installed, asks for the name.'
  - name: Open from ParentHierarchy
    anchor: how-to-use-it
    does: ParentHierarchy opens the browser for you when both are installed.
  - name: Share one browser across panes
    anchor: how-to-use-it
    does: 'Each pane bar carries only the button, and every button calls the same browser.'
---

## Why use it

Internal operator shortcuts (iops) let anything inside a component reach a key
operator by a short name. Working deep inside a project, though, you cannot see
which iops are in reach without opening the Common page of each parent in turn,
and adding one means another trip to the parent's parameters.

iopBrowser puts both on a button beside the path bar: click it to see every iop
you can use from where you are, drop an operator on it to add one.

## How to use it

- **See what is in reach:** click the button to the left of the path bar. The
  popup lists the iops available from the COMP you are currently in, which means
  the internal operators of every parent, from the nearest one up.
- **Use one:** drag any of them straight into your network editor, or use the
  list as a quick overview and a way to navigate to them.
- **Find an operator:** the popup also carries the OP tree for the network, with
  search, so it doubles as a way to find an operator without leaving the pane.
- **Add an iop:** drop an operator on the button and it becomes an internal
  operator shortcut of the network you are in, the root included.
  [CustomParTools](/docs/fns-custompartools/) asks for the shortcut name when it
  is installed; without it the operator's own name is used.

iopBrowser works on its own, and is opened for you by
[ParentHierarchy](/docs/fns-parenthierarchy/) when both are installed.

Only the button is copied into each pane bar. The browser itself exists once and
every button calls into it, so each new pane adds only a button. To move the
button or hide it, use the **Navbar** tab of [Hub](/docs/fns-hub/).
