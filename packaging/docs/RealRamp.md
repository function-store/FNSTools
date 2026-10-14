---
package: RealRamp
summary: 'A GLSL ramp with a true phase and period: vertical, horizontal, radial or circular, repeating or mirroring, so an animated phase never drifts or snaps the way a keyed Ramp TOP can.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Phase and period ramp
    anchor: what-it-is
    does: 'Computes the gradient in a shader from a phase and a period, so driving Phase from a CHOP cycles the ramp smoothly forever.'
  - name: Four geometries
    anchor: what-it-is
    does: 'Draws the ramp vertical, horizontal, radial or circular.'
  - name: Repeat or mirror
    anchor: what-it-is
    does: Extends the gradient past one period by repeating or mirroring it.
  - name: Resolution from input
    anchor: inputs-and-output
    does: An optional TOP input sets the output resolution when connected.
---

## What it is

The Ramp TOP is a keyframed gradient, which is the right tool for a designed palette and the wrong one for a driven gradient: a phase that runs past the last key snaps, and a period is a matter of stacking keys. RealRamp computes the gradient in a shader from a phase and a period, in four geometries, and extends it by repeating or mirroring. Drive Phase from a CHOP and the ramp cycles smoothly forever.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and output

- **in1** (TOP): optional; sets the output resolution when connected.
- **out1** (TOP): the ramp.
