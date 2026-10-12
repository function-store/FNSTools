---
package: ParticlesGpuUltimate
summary: 'A GPU particle system driven by images: a thresholded source emits particles, and look, life, turbulence, wind and force fields shape them, each optionally read from its own image, with a feedback pass for trails and one rendered output.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and output
    anchor: inputs-and-output
---

## What it is

ParticlesGpuUltimate turns an image into a particle system and renders it. The source image is thresholded to decide where particles are born and what colour they carry; Look sets their material, size and fades; Life how long they last and how their life maps to size and alpha; Turbulence and Wind push them with fields that read an image's dark and bright sides differently; Forces adds radial, axial, vortex or spiral fields you place; and Post runs the render through a feedback pass for trails, mixed in with Dry / Wet. The whole thing composites over the source or a background colour and comes out as one TOP.

Life, Turbulence and Wind each read their own image when you connect one, so a different picture can decide where particles live longer, swirl or drift than the one that emits them.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and output

1. **in_main** (TOP): the source image.
2. **in_pos_raw** (TOP): optional raw position map that replaces the one derived from the source.
3. **in_col_raw** (TOP): optional raw colour map.
4. **in_optflow_raw** (TOP): optional optical-flow map that moves the particles (Optflow pars on the pGpu page).
5. **in_turb_source** (TOP): optional image the Turb page reads as its effector.
6. **in_wind_source** (TOP): optional image the Wind page reads as its effector.
7. **in_life_source** (TOP): optional image the Life page reads as its effector.

- **bg** (TOP): the rendered particles over the background.
