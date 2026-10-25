---
package: EaseInterpolator
summary: 'Crossfades between two CHOPs through an easing curve: thirty classic easings from sine to bounce, or a custom curve from a third input, all driven by one Select value.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Easing several values at once
    anchor: easing-several-values-at-once
  - name: Drawing your own curve
    anchor: drawing-your-own-curve
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Crossfade two CHOPs along a curve
    anchor: how-to-use-it
    does: 'Moves from the first input to the second as Select runs from 0 to 1, along an easing curve.'
  - name: Easing curves from sine to bounce
    anchor: how-to-use-it
    does: 'Linear, or sine, quad, cubic, quart, quint, expo, circ, back, elastic and bounce curves in In, Out and In-Out forms.'
  - name: Drive the move from one value
    anchor: how-to-use-it
    does: 'Select runs the whole transition, so a timer, an LFO or a slider can drive it.'
  - name: Custom ease from a CHOP
    anchor: drawing-your-own-curve
    does: 'Reads the curve from an optional third input, so any shape drawn in a CHOP becomes the transition.'
---

## Why use it

Moving from one value to another, a camera from one framing to the next or a
look from one preset to another, is a crossfade: a Cross CHOP and a value
running from 0 to 1. A plain crossfade moves in a straight line, though, and a
move with character needs that value shaped first, through a Lookup CHOP or an
expression, for every curve you want to try.

EaseInterpolator crossfades between two CHOPs along an easing curve you pick
from a menu. Drive it from a timer, a slider or an LFO and two presets become
a move with character: a camera that settles, a value that overshoots and
springs back.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire the start value into **in1** and the end value into **in2**, for
   example two Constant CHOPs.
3. Move **Select**. At 0 the output is the first input, at 1 the second, and
   in between it follows the curve.
4. Pick a curve in **Easing**:
   - In curves start slowly and speed up; Out curves start fast and settle,
     the natural choice for a camera arriving somewhere; In-Out curves do
     both.
   - Back overshoots a little, Elastic springs, Bounce bounces.
   - Linear is a plain crossfade.
5. Drive **Select** from something that runs 0 to 1: a Timer CHOP for a timed
   move, an LFO for a move back and forth, a slider for hand control.

The output is worked out when Select changes. A change to the inputs or to
Easing shows up the next time Select moves.

The curves are the standard set from [easings.net](https://easings.net), which
shows each one moving.

## Easing several values at once

EaseInterpolator eases the first channel of in1 toward the first channel of
in2, sample by sample, and outputs the result as one channel, `chan1`. Further
channels on the inputs are left out.

To move several values together, a camera's position and rotation say, hold
them as samples of one channel: a Shuffle CHOP set to swap channels and
samples does that before each input, and a second one after out1 turns the
samples back into channels. A Rename CHOP then gives them their names back.

## Drawing your own curve

Set **Easing** to CustomEase and the curve comes from **in_custom_ease**.

- Its first channel is the curve, read across its samples: the first sample
  is where the move starts (Select 0), the last where it ends (Select 1).
- A value of 0 on the curve means the first input and 1 the second. Values
  outside 0 to 1 push past either end, for an overshoot of your own.
- The lookup takes the nearest sample without blending between samples, so a
  curve with few samples moves in steps. Give it enough samples for a smooth
  move.

A Pattern CHOP is a quick way to make one; any CHOP that holds the curve as
samples works.

## Inputs and output

- **in1** (CHOP): the channels at Select 0.
- **in2** (CHOP): the channels at Select 1.
- **in_custom_ease** (CHOP): optional; the curve used when Easing is Custom Ease.
- **out1** (CHOP): the eased blend of the two inputs.
