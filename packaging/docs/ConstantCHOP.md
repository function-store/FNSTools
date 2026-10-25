---
package: ConstantCHOP
summary: 'A Constant CHOP with typed values: numbers, toggles, tuples, text, paths or operator references, each promoted as a property you can read and set from Python, and a snap from its input. An alternative for the Constant CHOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Constants as properties
    anchor: constants-as-properties
  - name: Input and outputs
    anchor: input-and-outputs
feature_list:
  - name: Typed constants
    anchor: how-to-use-it
    does: 'Every constant can be a float, integer, toggle, four-value tuple, string, file or folder path, or operator reference.'
  - name: Channels plus a table
    anchor: how-to-use-it
    does: 'Numbers, toggles and tuples come out as CHOP channels, and every constant also comes out as a DAT table of names and values.'
  - name: Switch type without losing values
    anchor: how-to-use-it
    does: Changing the type keeps each value wherever it converts.
  - name: Snap from the input
    anchor: how-to-use-it
    does: 'Snap Input turns whatever is wired in into constants, one per channel, named and valued from it.'
  - name: Replace a Constant CHOP
    anchor: how-to-use-it
    does: Create a Constant CHOP with the alternatives shortcut held and ConstantCHOP is offered in its place.
  - name: Constants as properties
    anchor: constants-as-properties
    does: 'Each constant is a property that reads and sets it, a _out property reads the output, and a prefix avoids clashes.'
    authors: true
---

## Why use it

A component's settings are seldom all numbers. Next to a speed and an amount
there is a colour, a file to load, the TOP to show, a label. The numbers go in
a Constant CHOP, the rest ends up spread over custom parameters and a Table
DAT, and reading them back from a script means knowing which is where.

ConstantCHOP holds a list of named values, like the Constant CHOP, and gives
the values a type. Numbers come out as channels, everything comes out as a
table, and with one line of Python you can read or set any of them by name.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. Or create a
   Constant CHOP with the alternatives shortcut held and pick ConstantCHOP.
2. Pick the **Type** first. It applies to every constant on the node: a float,
   an integer, a toggle, a four-value tuple such as XYZW or RGBA, a string, a
   file or folder path, or a reference to an operator. For constants of
   another kind, add a second ConstantCHOP.
3. Add constants with the sequence's **+** button and give each a **Name** and
   a **Value**. A new constant is named `chan1`, `chan2` and so on until you
   rename it.
4. Read them where you need them. Numbers, toggles and tuples come out of out1
   as channels; out2 holds every constant as a table of names and values, and
   it is the only place text, paths and references come out.

Switching Type later keeps each value wherever it converts, so floats switched
to integers keep their values, rounded. A value that does not convert goes
back to the default.

To start from what is already in a CHOP, wire it in and press **Snap Input**:
the constants are replaced with one per channel, named and valued from it.
Snap Input works while Type is Float or Int.

## Constants as properties

With **Promote to Property** on, each constant is also a property on the node,
named after the constant with its first letter capitalised:
`op('ConstantCHOP').Speed` reads and sets the constant named `speed`, and
`Speed_out` reads what the node outputs for it.

```python
consts = op('ConstantCHOP')
consts.Speed = 2.5            # set the constant named speed
speed = consts.Speed.eval()   # the property is the Value parameter itself
out = consts.Speed_out        # a channel for a single number, else its cell in out2
```

- Setting it does nothing while that Value is driven by an expression or an
  export.
- **Property Prefix** ships empty. If a constant's name clashes with
  something already on the COMP, the node shows a script error naming it; a
  prefix such as `C_` turns `Speed` into `C_Speed` and clears the clash.

## Input and outputs

- **in1** (CHOP): optional; the channels Snap Input copies from.
- **out1** (CHOP): the numeric constants as channels.
- **out2** (DAT): every constant as a table of names and values.
