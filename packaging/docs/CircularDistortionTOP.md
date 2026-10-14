---
package: CircularDistortionTOP
summary: 'A circular distortion for images: rings of displacement around a centre you place, with phase, frequency, amplitude and a mode blend, and a choice of how the input extends past its edge.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Ring distortion around a centre
    anchor: what-it-is
    does: Pushes the image in rings around a centre you place; Frequency sets how many rings and Amplitude how far pixels move.
  - name: Animated Phase
    anchor: what-it-is
    does: 'Animating Phase spins the rings outward or inward, for example driven from a CHOP for a ripple.'
  - name: Mode blend
    anchor: what-it-is
    does: Mode blends between the distortion's two characters.
  - name: Edge extend choice
    does: Choose how the input extends past its edge.
  - name: Place from the FNS tab
    anchor: what-it-is
    does: Pick it from the FNS tab of the OP Create dialog and it lands as one node.
---

## What it is

CircularDistortionTOP pushes the image in rings around a point. Frequency sets how many rings, Amplitude how far the pixels move, Phase spins the rings outward or inward when animated, and Mode blends between the distortion's two characters. Put the centre on a face, a logo or the middle of the frame and drive Phase from a CHOP for a ripple; crank Amplitude for a lens that breathes.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and output

- **in1** (TOP): the image to distort.
- **out1** (TOP): the distorted image.
