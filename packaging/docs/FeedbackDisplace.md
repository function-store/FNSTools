---
package: FeedbackDisplace
summary: 'A feedback loop with a displace stage inside it: opacity, crossfade, filter size, displacement driven by a built-in noise or a second input, a per-pass transform, reset and a dry/wet mix. The alternative for the Feedback TOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Trails with opacity and blur
    anchor: how-to-use-it
    does: 'Each pass is composited over the input with an opacity and a blur, so trails, smears and echoes come straight from the parameters.'
  - name: Noise or image displacement
    anchor: how-to-use-it
    does: 'Warps every pass by a built-in animated noise, or by a displacement map wired into the in_displace input.'
  - name: Zoom, spin and drift each pass
    anchor: how-to-use-it
    does: 'Applies a transform on every pass for drift, zoom and spin, including infinite zooms.'
  - name: Reset the loop
    anchor: how-to-use-it
    does: 'Hold Reset to clear the loop, including the faint ghost an 8-bit loop at a high opacity leaves behind.'
  - name: Mix dry and wet
    anchor: how-to-use-it
    does: 'Dry / Wet Mix blends the whole effect with the input, and Cross fades between the fresh input and the loop.'
  - name: Replace a Feedback TOP
    anchor: how-to-use-it
    does: 'Offered in place of a Feedback TOP created with the alternatives shortcut held, wired into the same spot; also on the OP Create dialog''s FNS tab.'
---

## Why use it

A Feedback TOP on its own gives you the loop, and the rest is always the same
handful of operators around it: a composite with an opacity so old frames fade,
a blur, a displace with an animated noise driving it, a transform for drift,
zoom and spin, a way to reset, and a mix back against the input. That is a
small network to wire up again in every project before the first trail shows.

FeedbackDisplace is that handful in one node. Trails, smears, liquid echoes and
infinite zooms come straight from the parameters, with your chain left as it
is.

## How to use it

1. Create a Feedback TOP with the alternatives shortcut held. FeedbackDisplace
   is offered in its place and lands in that spot, wired the same way. It is
   also on the **FNS** tab of the OP Create dialog.
2. Wire a source into **in1**: a movie, a camera, a particle render. A fresh
   one already has the built-in noise displacing every pass, so the trails
   start to warp straight away.
3. Hold **Reset** to clear the loop. You will want it once after wiring: a
   loop that cooked before its input was connected holds TouchDesigner's
   sample image, and an 8-bit loop at a high opacity never decays all the way
   to zero, so a faint ghost stays until you reset.
4. Set the trail length with **Opacity**: higher values keep more of the
   previous frame each pass. **Operation** picks how each pass is composited
   over the input, and **Filter Size** blurs the loop each pass for smears.
5. Shape the warp. **Displace Amplitude**, **Displace Period** and
   **Displace Speed** set the strength, scale and speed of the built-in noise,
   and **Displace Weight** how far it pushes the image. With **Aspect Correct**
   on, the vertical weight follows the horizontal one, scaled by the image
   aspect, so the push stays square.
6. To warp by something else, wire an image into **in_displace**: it replaces
   the noise. **Source Midpoint** is the value that means no movement; the
   default 0.5 suits a map centred on grey.
7. Add motion per pass. **Scale** a little above 1 zooms the trails outward
   into an infinite zoom, **Rotate** spins them and **T** makes them drift.
8. Blend it in. **Cross** fades between the fresh input and the loop, and
   **Dry / Wet Mix** mixes the whole effect with the input, which is handy to
   automate on a beat.

## Inputs and output

- **in1** (TOP): the image fed into the loop.
- **in_displace** (TOP): optional; a displacement map that replaces the built-in noise.
- **out1** (TOP): the loop's output, mixed with the input by Dry / Wet Mix.
