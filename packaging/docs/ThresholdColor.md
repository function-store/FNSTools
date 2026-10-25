---
package: ThresholdColor
summary: 'A Threshold TOP that keeps the colour: the pixels that pass the test come through in their original colour, with a soft edge.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Colour-keeping threshold
    anchor: why-use-it
    does: Pixels the Comparator removes go black while every other pixel keeps its exact RGB.
  - name: Test luminance, a channel or RGB
    anchor: how-to-use-it
    does: 'Tests luminance, one channel, or the average or maximum of RGB or RGBA against the threshold.'
  - name: Soften the edge
    anchor: how-to-use-it
    does: Soften feathers the boundary between kept and removed pixels.
  - name: Alpha cut-outs for compositing
    anchor: how-to-use-it
    does: 'Removed pixels can also turn transparent, ready to composite over something else.'
  - name: Replace a Threshold TOP
    anchor: how-to-use-it
    does: 'Create a Threshold TOP with the alternatives shortcut held and ThresholdColor is offered in its place, wired into the same spot.'
---

## Why use it

To pull the bright part out of a picture, say the lights in a night shot to
feed a glow, the Threshold TOP gets you halfway. It answers a yes or no
question per pixel and paints the answer white on black, so you multiply that
matte back onto the source to get the colours back.

ThresholdColor asks the same question and keeps the pixel's own colour: the
pixels the test removes go black, every other pixel keeps its exact RGB, and
the edge between them can be soft. It is the usual first step for isolating
the bright or dark part of a picture without losing its colour.

## How to use it

1. Create a Threshold TOP with the alternatives shortcut held. ThresholdColor
   is offered in its place and lands in that spot, wired the same way.
2. Set the test. The **Comparator** names the pixels that are removed, with the
   same meaning as on the Threshold TOP: with Less, every pixel whose value is
   below **Threshold** goes black and the rest keep their colour. Move
   Threshold to decide how much survives.
3. To keep the dark part of the picture, switch the Comparator to Greater.
4. Choose what is tested with **RGB**: luminance, a single channel, the RGB or
   RGBA average, or the RGB or RGBA maximum.
5. Raise **Soften** to feather the cut. Pixels near the threshold then fade
   between their colour and black; 0 is a hard cut.
6. Set **Alpha** for compositing. Same as RGB makes removed pixels
   transparent, so the result sits cleanly over another layer; One keeps the
   input's alpha untouched.

## Inputs and output

- **in1** (TOP): the image to threshold.
- **out1** (TOP): the image with only the passing pixels, in colour.
