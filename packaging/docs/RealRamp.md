---
package: RealRamp
summary: 'A ramp with a true phase and period and its colour keys as parameters: vertical, horizontal, radial or circular, holding, zeroing, repeating or mirroring past its ends. An alternative for the Ramp TOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Colour keys as parameters
    anchor: why-use-it
    does: 'Each key''s position and colour is a parameter on the operator, so it can take an expression, an export or a CHOP like any other.'
  - name: Phase and period ramp
    anchor: how-to-use-it
    does: 'Computes the gradient in a shader from a phase and a period, so driving Phase from a CHOP cycles the ramp smoothly forever.'
  - name: Radial, circular, vertical or horizontal ramps
    anchor: how-to-use-it
    does: 'Draws the ramp vertical, horizontal, radial or circular, with Radial starting at 3 o''clock like the Ramp TOP.'
  - name: Repeat or mirror past the ends
    anchor: how-to-use-it
    does: 'Holds the end colours, goes to zero, repeats or mirrors past the ends of the ramp.'
  - name: Interpolate between keys like the Ramp TOP
    anchor: how-to-use-it
    does: 'Step, Linear, Ease In Ease Out and Hermite blending between keys, matched against the stock Ramp TOP.'
  - name: Banding-free output
    anchor: how-to-use-it
    does: 'Outputs 32-bit float by default, so a slow gradient shows no steps.'
  - name: Resolution from an input
    anchor: how-to-use-it
    does: 'With an input connected the ramp takes its resolution, and the image itself is never sampled; without one, Resolution sets the size.'
  - name: Replace a Ramp TOP
    anchor: how-to-use-it
    does: 'Offered in place of a Ramp TOP created with the alternatives shortcut held, wired into the same spot.'
---

## Why use it

The Ramp TOP keeps its colour keys in a table DAT. That suits a gradient you
design once and leave alone. It gets awkward when you want to drive one: a key
colour that follows a CHOP, a second key that tracks another operator's
parameter, a palette you animate from a control panel.

RealRamp keeps its keys as parameters on the operator, so each key's position
and colour takes an expression, an export or a CHOP like any other parameter.
The gradient is computed in a shader from a phase and a period, so a driven
phase cycles the ramp smoothly forever, and the output is 32-bit float by
default. Its types, extend modes and interpolation were measured against the
stock Ramp TOP and match it closely.

## How to use it

1. Create a Ramp TOP with the alternatives shortcut held. RealRamp is offered
   in its place and lands in that spot, wired the same way. A fresh one is
   horizontal, black to white, repeating, with linear blending.
2. Set the colours on the Keys page. Add or remove keys with + and -, and give
   each a **Position** along the ramp and a **Color** with alpha. Keys can be
   in any order; they are sorted by position.
3. Pick the geometry with **Type**. Radial runs round the centre starting at
   3 o'clock, like the Ramp TOP; Circular grows outward from the centre.
4. Make it move by driving **Phase** with an expression or a CHOP, for example
   `absTime.seconds*0.2`, to scroll the ramp. **Period** sets the length of
   one cycle; smaller values repeat the ramp more often.
5. Choose what happens past the ends with **Extend**. Repeat starts over, which
   keeps a scrolling ramp cycling; Mirror runs back; Hold keeps the end
   colours; Zero goes transparent black.
6. Change the blend between keys with **Interpolate**: Step holds each key,
   Linear blends straight, Ease In Ease Out slows at each key and Hermite
   curves through them, with **Curve Tension** to bend that curve.
7. Size it with **Resolution** when nothing is wired in. With an input
   connected, the ramp takes the input's resolution; the image itself is
   never sampled. **Pixel Format** is 32-bit float out of the box, which keeps
   the ramp free of banding; 16-bit float is usually enough, and 8-bit shows
   visible steps.

Like the Ramp TOP, the output is premultiplied: each colour is multiplied by
its alpha. RealRamp has no Anti-Alias parameter, so hard edges on radial and
circular ramps (Step keys, the seams of Repeat and Zero) stay hard where the
Ramp TOP would smooth them.

## Inputs and output

- **in1** (TOP): optional; sets the output resolution when connected.
- **out1** (TOP): the ramp.
