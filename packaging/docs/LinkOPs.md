---
package: LinkOPs
summary: 'Links the parameters of several operators so a change on one lands on all of them: name the operators by pattern, leave some out, leave some parameters out, keep the list current automatically, and optionally link constants only.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: What gets linked
    anchor: what-gets-linked
feature_list:
  - name: Link operators by pattern
    anchor: how-to-use-it
    does: 'Name the operators with patterns such as `noise*` or `level1 level2`, and a parameter changed on one is written to the others.'
  - name: Link expressions and modes
    anchor: what-gets-linked
    does: 'Values follow, and by default so do expressions and parameter modes.'
  - name: Exclude operators and parameters
    anchor: what-gets-linked
    does: 'Leave out operators that match the pattern anyway, and parameters such as `t? seed` to keep transforms and seeds independent.'
  - name: Constant-only linking
    anchor: what-gets-linked
    does: 'Link only parameters in constant mode on both sides, so an expression on one operator is never overwritten.'
  - name: Auto-update the operator list
    anchor: how-to-use-it
    does: 'With Auto on, the list follows operators as they are added, renamed or removed.'
  - name: Sync on demand
    anchor: how-to-use-it
    does: Operators added later join when you press Sync.
  - name: Match parameters by name across types
    anchor: what-gets-linked
    does: 'Operators of different types can share a link; the parameters they have in common by name are kept in step.'
---

## Why use it

Four Noise TOPs feeding four layers, a Level TOP on each output, a row of
identical Geometry COMPs: when they should move together, you either change
every one by hand or tie their parameters to a master with expressions. The
first is slow, and the second turns the copies into followers you can no
longer adjust directly.

LinkOPs keeps a set of operators in step. Change a parameter on any one of
them and the same parameter changes on the others. Every operator in the set
can lead.

## How to use it

1. Create LinkOPs from the **FNS** tab of the OP Create dialog, in the same
   network as the operators you want to link. It lands as one node, and it
   only looks for operators in the network it sits in.
2. In **OPs**, name the operators by pattern, separated by spaces: `noise*`
   for every operator whose name starts with noise, or `level1 level2` for
   exactly those two.
3. Change a parameter on any of them. The others follow.

Typing into **OPs** or **Except** rescans the network straight away.
Operators you add later join when you press **Sync**, or on their own with
**Auto** on, which also follows renames and deletions.

To pause the link and keep the setup, switch off **Active**.

## What gets linked

- **Parameters are matched by name.** Operators of different types can share
  a link, and only the parameters they have in common are kept in step.
- **Values, expressions and modes.** Values follow, and by default so do
  expressions and parameter modes: put an expression on one operator and the
  others get the same expression.
- **Leaving operators out.** **Except** takes operators out of the link even
  when they match **OPs**.
- **Leaving parameters out.** **Par Except** takes parameters out by name
  pattern. `t? seed` keeps each operator's translate and seed its own, so
  linked noises share their look but not their position or their pattern.
- **Constants only.** With **Constant Only** on, a parameter is linked only
  when it is in constant mode on both sides. An expression on one operator is
  then never overwritten; that operator simply stops following for that
  parameter.
- **Timing.** Changes are collected and written once per frame. When two
  linked operators change the same parameter in the same frame, the last
  change wins.
