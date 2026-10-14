---
package: PrismTOP
summary: 'A kaleidoscopic prism: the input rendered through instanced, rotating polygon facets in up to three ring patterns, with softness, a chromatic distortion pass, fit and transform, and a dry/wet mix. An alternative for the Tile TOP and the Mirror TOP.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Instanced prism facets
    anchor: what-it-is
    does: 'Maps the input onto polygon facets instanced in rings around the centre, so the image is repeated, mirrored and rotated at once.'
  - name: Three stacking ring patterns
    anchor: what-it-is
    does: 'Up to three ring patterns stack, each with its own instance count, radius, scale, phase and alpha.'
  - name: Soft edges and swinging rotation
    anchor: what-it-is
    does: 'Facets meet with soft edges, and the rotation can swing on a sine.'
  - name: Chromatic distortion
    anchor: what-it-is
    does: A chromatic distortion pass splits the colours the way a real prism does.
  - name: Original underlay and Dry/Wet
    anchor: what-it-is
    does: 'The original image sits underneath at its own opacity and scale, and Dry/Wet mixes the whole result against the input.'
  - name: Tile and Mirror TOP alternative
    anchor: what-it-is
    does: 'Create a Tile TOP or Mirror TOP with the alternatives shortcut held and PrismTOP is offered in its place, wired into the same spot.'
---

## What it is

A Tile TOP repeats, a Mirror TOP flips; a prism does both through glass. PrismTOP maps the input onto polygon facets, instances them in rings around the centre and renders the result, so the picture is repeated, mirrored and rotated at once, with soft edges between facets, a rotation that can swing on a sine, and a chromatic distortion pass that splits the colours the way a real prism does. Up to three ring patterns stack, each with its own instance count, radius, scale, phase and alpha, and the original sits underneath at its own opacity and scale. Dry / Wet mixes the whole thing against the input.

It is the alternative for the Tile TOP and the Mirror TOP: create either with the alternatives shortcut held and PrismTOP is offered in its place, wired into the same spot. It is also a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and output

- **in1** (TOP): the image to refract.
- **out1** (TOP): the prism, mixed with the input by Dry/Wet.
