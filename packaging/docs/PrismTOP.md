---
package: PrismTOP
summary: 'A kaleidoscopic prism: the input rendered through instanced, rotating polygon facets in up to three ring patterns, with softness, a chromatic distortion pass, fit and transform, and a dry/wet mix. An alternative for the Tile TOP and the Mirror TOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Kaleidoscope prism facets
    anchor: how-to-use-it
    does: 'Maps the input onto polygon facets set in rings around the centre, so the image is repeated, mirrored and rotated at once.'
  - name: Stack up to three ring patterns
    anchor: how-to-use-it
    does: 'Up to three rings stack, each with its own facet count, radius, size, rotation and opacity.'
  - name: Soften the facet edges
    anchor: how-to-use-it
    does: Softness blurs the seams where the facets meet.
  - name: Animate the rotation
    anchor: how-to-use-it
    does: 'Phase turns each ring around the centre, and the whole prism can swing back and forth on a sine.'
  - name: Chromatic distortion
    anchor: how-to-use-it
    does: A chromatic pass splits the colours apart the way real glass does.
  - name: Mix with the original
    anchor: how-to-use-it
    does: 'The original image can sit underneath the facets, and Dry/Wet blends the whole result with the input.'
  - name: Replace a Tile or Mirror TOP
    anchor: how-to-use-it
    does: 'Offered in place of a Tile TOP or Mirror TOP when you create one with the alternatives shortcut held.'
---

## Why use it

A Tile TOP repeats an image and a Mirror TOP flips it. For the look of an
image seen through a cut-glass prism you need both at once, plus rotation and
some colour fringing, and building that yourself means a small render network:
geometry for the facets, instancing to lay them out in rings, a camera, a
Render TOP and a composite on top. That is a lot of setup when you just want to
try the look on a clip.

PrismTOP is that network in one node. Feed it an image and it comes out as a
prism, ready to tweak and animate.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. Or create a Tile TOP
   or a Mirror TOP with the alternatives shortcut held, pick PrismTOP, and it
   lands in that spot with the wiring kept.
2. Wire an image or a movie into it. Footage with detail and some colour
   variation shows off the facets best; a flat gradient stays a flat gradient.
3. Shape the first ring on the Patterns page. **Instances** sets how many
   facets go around the ring and **Radius** how far from the centre they sit.
   **Sides** on the Custom page sets the facet shape, six for hexagons.
4. Add a second ring with a different count and radius for a denser,
   layered prism, and a third if you want more.
5. Animate it. **Phase** turns a ring around the centre, so rings turning at
   different speeds give the classic kaleidoscope motion. For a pendulum swing,
   raise **Rot Sin Amp**: **Rot Sin Phase** already runs on time, and its
   expression is where you set how fast it swings.
6. On the Chroma page, raise **Chromatic** to split the colours apart at the
   facet edges. **Distortion** bends the image as it splits.
7. Blend to taste. **Softness** blurs the seams between facets, **Orig Opac**
   lets the original show underneath, and **Dry/Wet** mixes the whole thing
   back with the input, which is handy to automate on a beat.

## Inputs and output

- **in1** (TOP): the image to refract.
- **out1** (TOP): the prism, mixed with the input by Dry/Wet.
