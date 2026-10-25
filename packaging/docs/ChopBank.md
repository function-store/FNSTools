---
package: ChopBank
summary: 'A bank of channel processors: one block per channel, each with its own range, exponent curve, zero-below, lag and speed mode, built from the input with one Snap Input, with gain before and after and every block promoted as a property. An alternative for the Math CHOP and the Constant CHOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Blocks as properties
    anchor: blocks-as-properties
  - name: Input and output
    anchor: input-and-output
feature_list:
  - name: Shape each channel with its own block
    anchor: how-to-use-it
    does: 'Each block shapes one channel with its own range remap, exponent curve, Zero Below, lag, and a speed mode that turns it into a running total.'
  - name: Build the bank with Snap Input
    anchor: how-to-use-it
    does: 'One press makes a block for every incoming channel, named after it and holding its value; a new block copies the previous block''s settings.'
  - name: Add channels the input lacks
    anchor: how-to-use-it
    does: 'A block with no matching input channel outputs its own Value, so the bank can add channels.'
  - name: Gain before and after
    anchor: how-to-use-it
    does: Master gain on every channel before the blocks and after them.
  - name: Replace a Math or Constant CHOP
    anchor: how-to-use-it
    does: 'Create a Math CHOP or Constant CHOP with the alternatives shortcut held and ChopBank is offered in its place, wired into the same spot.'
  - name: Blocks as properties
    anchor: blocks-as-properties
    does: 'Each block is a property on the node, so Python reads and sets its Value by name.'
    authors: true
---

## Why use it

The faders on a controller rarely want the same treatment. The master fader
wants a gentle curve, a rotation fader wants a wide range and some lag, a
speed knob should keep a value moving. With stock CHOPs, or one
[ChopProcess](/docs/chopprocess/) for the whole controller, that means
splitting the channels apart and building a chain for each one.

ChopBank shapes a whole controller in one node. Every block in the bank is one
channel with its own processing: the ChopProcess chain, set per channel. A bank
of eight faders, each with its own range and feel, is one node.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. Or create a Math
   CHOP or a Constant CHOP with the alternatives shortcut held, pick ChopBank,
   and it lands in that spot with the wiring kept.
2. Wire your controller into it and press **Snap Input**. ChopBank makes one
   block per incoming channel, named after it and holding its current value.
3. Tune each block on the Bank page: **From Range** and **To Range** to remap,
   **Type** to clamp, loop or zigzag outside the range, **Exponent Value** for
   the curve, **Lag** to smooth. **Is Speed** turns a block into a running
   total, for a knob that should keep a value moving.

A new block starts with the settings of the block before it, so a row of
similar faders is quick: tune one, then add blocks after it.

How blocks find their channels:

- A block takes the input channel its **Name** matches. With Name empty, it
  takes the channel at its own position.
- When no input channel matches, the block outputs its own **Value**. That way
  a bank can also add channels that are not in the input, or work with no
  input at all, like a Constant CHOP.

**Gain Pre** and **Gain Post** scale every channel before and after the
blocks, a master level for the whole bank.

## Blocks as properties

With **Promote to Property** on, each block is also a property on the node,
named after the block with its first letter capitalised: the block `fader1`
is `op('chopBank1').Fader1`, and `Fader1_out` reads that block's output.

```python
bank = op('chopBank1')
bank.Fader1 = 0.5            # set the Value of the block named fader1
level = bank.Fader1.eval()   # the property is the Value parameter itself
out = bank.Fader1_out        # the block's output channel
```

- Setting the property sets the block's Value, which is what the block
  outputs while no input channel matches it.
- Setting it does nothing while that Value is driven by an expression or an
  export.
- **Property Prefix** ships empty. If a block's name clashes with something
  already on the COMP, the node shows a script error naming it; a prefix such
  as `C_` turns `Fader1` into `C_Fader1` and clears the clash.

## Input and output

- **in1** (CHOP): the channels to process.
- **out1** (CHOP): one processed channel per block.
