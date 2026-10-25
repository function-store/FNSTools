---
package: FNS_SwitchTools
summary: 'A companion for any Switch, Cross or multi-input operator: index by slider, menu or bind, loop or clamp, colour the live input, cook only the inputs in use and unload the rest, plus reorder, reverse, randomize and align.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Cooking only what is on screen
    anchor: cooking-only-what-is-on-screen
  - name: Rewiring the inputs
    anchor: rewiring-the-inputs
  - name: Callbacks
    anchor: callbacks
feature_list:
  - name: Drive the switch index
    anchor: how-to-use-it
    does: 'Binds the switch''s index to its own Index, so a slider, a menu of input names, a CHOP or a bound parameter drives it.'
  - name: 'Loop, clamp or zigzag'
    anchor: how-to-use-it
    does: 'Decides what happens when the index runs past the last input: clamp at the ends, loop round to the first, or zigzag back.'
  - name: Crossfade between inputs
    anchor: how-to-use-it
    does: 'With Blend on, index values between two inputs crossfade between them.'
  - name: Colour the live input
    anchor: how-to-use-it
    does: Colours the input on screen in the network editor and the rest in a second colour.
  - name: Cook only what is on screen
    anchor: cooking-only-what-is-on-screen
    does: Input components the switch is not showing stop cooking until they are selected again.
  - name: Release unused memory
    anchor: cooking-only-what-is-on-screen
    does: 'Frees the CPU and GPU memory of inputs that went off screen, spread over several frames so the switch does not hitch.'
  - name: Reverse or shuffle the inputs
    anchor: rewiring-the-inputs
    does: 'Flips or shuffles the input order in one click, and Restore Original goes back to the saved wiring.'
  - name: Reorder inputs to match the layout
    anchor: rewiring-the-inputs
    does: 'Rewires the switch so the top node is the first input, or moves the nodes to match the wiring.'
  - name: Align and rename input nodes
    anchor: rewiring-the-inputs
    does: Lines the input nodes up beside the switch and renames them so their digits match their index.
  - name: Callbacks on cook and selection changes
    anchor: callbacks
    does: 'Run your own Python when inputs start or stop cooking, or are selected and unselected.'
---

## Why use it

A scene setup in TouchDesigner often ends in a Switch TOP with a dozen inputs,
each scene in its own component. As the project grows, so does the cost of the
scenes you are not showing: their textures stay in GPU memory, and whatever
inside them keeps cooking still takes frame time. Driving the switch is a small
network of its own as well: a slider or a CHOP for the index, logic for what
happens at the ends, and some way to see which input is live.

SwitchTools sits next to the switch and takes care of both. It drives the
index, lets only the inputs in use cook and can release the memory of the
rest. It also colours the live input in the network editor and rewires the
inputs for you: reversed, shuffled or in the order they sit on screen.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog, under COMP. It lands
   in the network you are working in.
2. Point **Switch OP** at your Switch TOP, Switch CHOP, Cross CHOP, Switch POP
   or other multi-input operator, or dock the tool to it. SwitchTools docks to
   the switch, moves just above it, and binds the switch's index (Cross, on a
   Cross CHOP) to its own **Index**. It also saves the current wiring as the
   original, so you can always go back to it.
3. Drive the switch from **Index**: drag it, bind it to a slider, or export a
   CHOP to it. **Select** picks an input by name. With **Blend** on, values
   between two inputs crossfade between them.
4. Choose what happens when Index runs past the last input with **Loop Type**:
   clamp at the ends, loop round to the first, or zigzag back.
5. To see which input is live, switch on **Colorize**. The live input takes
   **On Color** and the others **Off Color**.

To take the tool out of the picture without deleting it, switch off
**Active**: the switch is unbound and left as it is.

## Cooking only what is on screen

This works on inputs that are components. Wire each scene's Out TOP (or Out
CHOP) into the switch, and SwitchTools works with the component around it.

- **Control Cook (COMPs)** lets only the component on screen cook; the others
  stop cooking until they are selected. While Blend crossfades between two
  inputs, both cook.
- **Unload GPU** also releases an input's CPU and GPU memory a few frames after
  it goes off screen. If you switch back before then, the unload is cancelled.
  With **Unload Method** on Progressive, the release is spread over several
  frames, at most **Unload Budget (ms/frame)** milliseconds each, so a heavy
  scene does not hitch the frame it leaves, and POPs are covered too. Locked
  operators keep their data. Immediate unloads every unlocked TOP in one frame.

## Rewiring the inputs

The Inputs page rewires the switch for you. Reversing, shuffling, reordering,
aligning, renaming and disconnecting are each one undo step.

- **Trying another order:** **Reverse Inputs** flips the order and
  **Randomize Inputs** shuffles it. **Restore Original** goes back to the
  wiring saved when you set Switch OP, or the one you last saved with **Save as
  Original**.
- **Keeping the layout and the order in step:** **NodeY to Order (reconnect)**
  rewires the switch so the top node is the first input. **Order to NodeY
  (swap)** does the opposite and moves the nodes to match the wiring. The
  toggle beside NodeY to Order rewires every time you move an input node.
- **Tidying up:** **Align Inputs (retoggle)** lines the input nodes up beside
  the switch, top, centre or bottom by **Alignment Mode**. **Re-Digitize Inputs
  (rename)** renames them so their digits match their index, `scene0`,
  `scene1` and so on, or from 1 with the toggle beside it.
- **Closing a loop:** **First == Last** wires the first input again as the
  last, so a loop closes cleanly. The reorder actions leave that repeat out.
- **Starting over:** **Disconnect All Inputs** clears the switch.

## Callbacks

Pulse **Create Callbacks** on the Callbacks page. It makes a DAT beside the
tool and points **Callbacks** at it. The DAT has two functions:

- `onCookingChange(cooked_comps, uncooked_comps)`: the input components that
  started and stopped cooking, with Control Cook (COMPs) on.
- `onSelectionChange(selected_ops, unselected_ops)`: the inputs that were
  selected and unselected.

Both arguments arrive as sets. For example, to restart a timer inside each
scene whenever it comes back on screen:

```python
def onCookingChange(cooked_comps, uncooked_comps):
	for comp in cooked_comps:
		timer = comp.op('timer1')
		if timer is not None:
			timer.par.start.pulse()
	return

def onSelectionChange(selected_ops, unselected_ops):
	return
```
