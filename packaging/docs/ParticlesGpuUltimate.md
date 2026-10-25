---
package: ParticlesGpuUltimate
summary: 'A GPU particle system driven by images: a thresholded source emits particles, and look, life, turbulence, wind and force fields shape them, each optionally read from its own image, with a feedback pass for trails and one rendered output.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Steering with images
    anchor: steering-with-images
  - name: Placing forces
    anchor: placing-forces
  - name: Your own maps and optical flow
    anchor: your-own-maps-and-optical-flow
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Emit particles from an image
    anchor: how-to-use-it
    does: The source image is thresholded to decide where particles are born and what colour they carry.
  - name: Material and particle shape
    anchor: how-to-use-it
    does: 'Pick the material, the SOP shape for each particle and the maximum particle size on the Look page.'
  - name: Fade particles over their life
    anchor: how-to-use-it
    does: 'Set how long particles live, fade them in and out at either end of their life, and shrink or dim them as they age.'
  - name: Turbulence and wind
    anchor: steering-with-images
    does: 'Turbulence and wind act differently on the dark and the bright parts of an image, so a picture decides where particles swirl or drift.'
  - name: Steer each effector with its own image
    anchor: steering-with-images
    does: 'Life, turbulence and wind can each read their own image, apart from the one that emits the particles.'
  - name: Force fields you place
    anchor: placing-forces
    does: 'Radial, axial, vortex and spiral fields that you place, each with its own reach and strength.'
  - name: Feedback trails
    anchor: how-to-use-it
    does: 'A feedback pass draws trails behind the particles, mixed in with Dry / Wet, over the source or a background colour.'
  - name: Replace the position and colour maps
    anchor: your-own-maps-and-optical-flow
    does: 'Position and colour maps of your own replace the ones derived from the source image.'
  - name: Optical flow movement
    anchor: your-own-maps-and-optical-flow
    does: 'An optical-flow map pushes the particles, as hard as Optical Flow Magnitude sets.'
---

## Why use it

Getting particles to pour out of a picture, take on its colours and be pushed
around by other pictures is a lot of plumbing around a particle system:
thresholding the image into birth positions, sampling its colour, a lookup
for every force that should follow an image, then a render and a feedback
pass for trails.

ParticlesGpuUltimate is that plumbing, built around particlesGpu, the GPU
particle system from TouchDesigner's palette. An image goes in and the
rendered particles come out as one TOP.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire an image or a movie into **in_main**. Particles are born where its
   pixels pass the threshold on the Source page (**Comparator**, **RGB** and
   **Source Threshold**), and they carry the colour of the pixel they came
   from.
3. The output is the render, at **Render Res** on the pGpu page. The Source
   page decides what sits behind it: raise **Under Opac** to show the source
   image underneath, or switch on **Comp Over Background Color** and pick
   **Bgcolor** for a plain colour.
4. Set the look on the Look page: **Material**, the **SOP** shape for each
   particle and **Particle Size Max**. Avoid the Constant material with the
   Point shape: that pairing raises a texture coordinate error inside the
   operator.
5. Set how long particles live on the Life page with **Life** and
   **Lifevariance**. On the Look page, **Fade In** and **Fade Out** fade them
   at either end of their life, and the Fade to settings shrink or dim them as
   they age.
6. Get them moving: turbulence on the Turb page, wind on the Wind page, and
   forces you place on the Forces page (see below).
7. Trails come from the feedback pass on the Post page. **Opacity** sets how
   long a trail lingers and **Dry / Wet Mix** blends the plain render with the
   trailed one.

If the particles look dim, lower **Drag** on the pGpu page and **Fade In** on
the Look page. **Reset** on the pGpu page starts the system over and **Pause**
freezes it.

## Steering with images

Turbulence and wind read an image and act differently on its dark and bright
parts. Each page has a Dark Side and a Bright Side: give the dark side strong
turbulence and the bright side none, and particles churn in the shadows and
sail through the highlights.

- Life, Turbulence and Wind each read their own image when you connect one:
  **in_life_source**, **in_turb_source** and **in_wind_source**. That way a
  different picture can decide where particles live longer, swirl or drift
  than the one that emits them.
- **InitPos/CurrPos** on the Life, Turb and Wind pages picks where that
  image is read: where the particle was born, or where it is now.
- To let an image set each particle's life, set **Life Type** to Effector.
  **To Range (dark/bright)** sets the life its darkest and brightest parts
  map to.

## Placing forces

The Forces page holds force fields placed in the particle space, one block
each, and a block does nothing until you give it a **Force Amount**. A
negative amount reverses it.

- A **Radial** force pushes particles away from its position, or pulls them in
  with a negative amount.
- An **Axial** force pushes them along its direction.
- A **Vortex** turns them around its direction.
- A **Spiral** turns them around and draws them inward at once, like water
  going down a drain.

**Force Radius** sets how far each one reaches. Add a block for each extra
force.

## Your own maps and optical flow

- **in_pos_raw** and **in_col_raw** take position and colour maps of your own,
  replacing the ones derived from the source image.
- **in_optflow_raw** takes an optical-flow map, and the flow pushes the
  particles. **Optical Flow Magnitude** on the pGpu page sets how hard; it
  ships at 0, so raise it once a flow map is wired. **Optical Flow Size
  Remap** helps the flow map line up with the system's aspect ratio.

## Inputs and output

1. **in_main** (TOP): the source image.
2. **in_pos_raw** (TOP): optional raw position map that replaces the one derived from the source.
3. **in_col_raw** (TOP): optional raw colour map.
4. **in_optflow_raw** (TOP): optional optical-flow map that moves the particles (Optflow pars on the pGpu page).
5. **in_turb_source** (TOP): optional image the Turb page reads as its effector.
6. **in_wind_source** (TOP): optional image the Wind page reads as its effector.
7. **in_life_source** (TOP): optional image the Life page reads as its effector.

- **bg** (TOP): the rendered particles over the background.
