---
package: FNS_SwapOps
summary: 'Swap the selected operators in place, positions and wiring together.'
features:
  - name: Why use it
    anchor: why-use-it
    icon: SwapOPs.png
  - name: How to use it
    anchor: how-to-use-it
hotkeys:
  - keys: alt.shift.s
    does: Swap the two selected operators in place
feature_list:
  - name: Swap two operators
    anchor: how-to-use-it
    does: 'Two selected operators trade places and connections, from the hotkey, the toolbar button or quick-launch.'
  - name: Wires stay on their inputs
    anchor: how-to-use-it
    does: 'Connections keep their input and output numbers, so a Merge or Composite keeps its input order, and COMPs keep their top and bottom connections.'
  - name: Mirror a row
    anchor: how-to-use-it
    does: 'With more than two operators selected, the row is mirrored end to end.'
  - name: Keep extra inputs in place
    anchor: how-to-use-it
    does: 'When one operator takes fewer inputs than the other, the inputs it cannot hold stay where they were.'
  - name: Undo the whole swap in one step
    anchor: how-to-use-it
    does: A single undo puts everything back.
---

## Why use it

You put the Blur before the Level and want them the other way round. By hand
that is: cut the wires, move both nodes, wire them up again, and remember which
input of the Composite downstream each one fed.

SwapOps trades the places and the wiring of the selected operators on one key.

## How to use it

1. Select two operators in the same network.
2. Press `Alt+Shift+S` (`Option+Shift+S` on macOS), click the SwapOps button on
   the toolbar, or run **Swap selected ops** from quick-launch.

The two trade positions and connections. Each wire lands on the same input or
output number it used before, so a Merge or a Composite keeps the order of its
inputs, and two COMPs swap their top and bottom connections as well.

- **A row of operators:** select more than two and the row is mirrored end to
  end. Reading the selection left to right, the first swaps with the last, the
  second with the one before last, and so on.
- **Different input counts:** when a Merge with two inputs swaps with the Null
  it feeds, only the input both can hold changes hands. The second input stays
  on the Merge, so no wire is lost.
- **Undo:** the whole swap is one undo step.

If a connection still cannot be rebuilt, the status bar says how many were
lost, so you know to check the wiring.

**Active** switches the tool off while keeping it installed, and the key can be
rebound from **Shortcuts**.
