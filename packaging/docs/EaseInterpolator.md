---
package: EaseInterpolator
summary: 'Crossfades between two CHOPs through an easing curve: thirty classic easings from sine to bounce, or a custom curve from a third input, all driven by one Select value.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Eased crossfade
    anchor: what-it-is
    does: 'Blends each channel of the first input into the matching channel of the second as Select runs from 0 to 1, along an easing curve.'
  - name: Classic easing curves
    anchor: what-it-is
    does: 'Linear, or sine, quad, cubic, quart, quint, expo, circ, back, elastic and bounce curves in In, Out and In-Out forms.'
  - name: Custom ease from a CHOP
    anchor: what-it-is
    does: 'Custom Ease reads the curve from the optional third input, so any shape drawn in a CHOP becomes the transition.'
  - name: Place from the FNS tab
    anchor: what-it-is
    does: Placed as one node from the FNS tab of the OP Create dialog.
---

## What it is

EaseInterpolator blends every channel of one CHOP into the matching channel of another, and the blend follows an easing curve. Select runs from 0, all of the first input, to 1, all of the second. Pick Linear for a plain crossfade, or one of the sine, quad, cubic, quart, quint, expo, circ, back, elastic and bounce curves in their In, Out and In-Out forms. Custom Ease reads the curve from a third input, so any shape you can draw in a CHOP becomes the transition.

Drive Select from a timer, a slider or an LFO and two presets become a move with character: a camera that settles, a value that overshoots and springs back.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and output

- **in1** (CHOP): the channels at Select 0.
- **in2** (CHOP): the channels at Select 1.
- **in_custom_ease** (CHOP): optional; the curve used when Easing is Custom Ease.
- **out1** (CHOP): the eased blend of the two inputs.
