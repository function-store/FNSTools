---
package: FNS_SwitchTools
summary: 'A companion for any Switch, Cross or multi-input operator: index by slider, menu or bind, loop or clamp, colour the live input, cook only the inputs in use and unload the rest, plus reorder, reverse, randomize and align.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Callbacks
    anchor: callbacks
feature_list:
  - name: Drive the switch index
    anchor: what-it-is
    does: 'Binds the target operator''s index to its own Index, driven by a slider, menu, CHOP or bound parameter, looping or clamping at the ends.'
  - name: Cook only the live input
    anchor: what-it-is
    does: 'Every input the switch is not showing stops cooking and, optionally, unloads from the GPU, so only what is on screen costs.'
  - name: Colour the live input
    anchor: what-it-is
    does: Colours the live input in the network editor.
  - name: Reorder inputs in one click
    anchor: what-it-is
    does: 'Reorders, reverses, shuffles or aligns the operator''s inputs in one click.'
  - name: Cooking and selection callbacks
    anchor: callbacks
    does: 'Create Callbacks makes a DAT with onCookingChange and onSelectionChange, reporting which inputs started or stopped cooking and which were selected.'
---

## What it is

Drop SwitchTools next to a Switch TOP, Switch CHOP, Cross CHOP, Switch POP or any multi-input operator and point Switch Op at it (or dock it): the tool binds the operator's index to its own Index, so a slider, a menu, a CHOP or a bound parameter drives the switch, looping or clamping at the ends. Every input the switch is not showing stops cooking and, if you ask, unloads from the GPU, so a scene wall of heavy inputs costs only what is on screen. The live input is coloured in the network, and the inputs can be reordered, reversed, randomized or aligned in one click.

## Callbacks

Create Callbacks makes a DAT beside the tool with onCookingChange (which inputs started and stopped cooking) and onSelectionChange (which inputs were selected and unselected); the Callbacks parameter points at it.
