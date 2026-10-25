---
package: Particles2D_POP
summary: 'A 2D particle simulation as a POP loop: a source image emits particles, curl noise and wind effectors steer them with lookup ranges, trails stretch them, and the loop rides out as points for your own render.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Steering with images
    anchor: steering-with-images
  - name: The simulation loop
    anchor: the-simulation-loop
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Emit from a source image
    anchor: how-to-use-it
    does: 'Particles are born from the image on in_source and carry its colours, each with its own life, mass and drag.'
  - name: Curl noise field
    anchor: how-to-use-it
    does: 'A moving curl noise field swirls the particles, with its strength set per axis and its speed on the Curl page.'
  - name: Wind with variance
    anchor: how-to-use-it
    does: 'A wind blows the particles along a direction you set, with random variance on top; it starts at zero.'
  - name: Steer forces with images
    anchor: steering-with-images
    does: 'Each force reads an image through its own lookup, so a picture or a mask decides where it is strong and where it is off.'
  - name: Motion trails
    anchor: how-to-use-it
    does: Trails stretch the points along their motion.
  - name: Points out for your own render
    anchor: inputs-and-output
    does: 'The simulated points come out of out_loopout, ready for a Render TOP with your own material or any POP that takes points.'
  - name: Insert your own POPs into the loop
    anchor: the-simulation-loop
    does: 'out_loopout and in_loopin are the two ends of the simulation loop, so POPs of your own can sit inside it.'
---

## Why use it

A 2D particle look on POPs (particles pouring out of an image, swirling in
curl noise, drifting in a wind, dragging trails behind them) takes a fair
network to build: a Particle POP in a feedback loop, the image turned into
birth points, a noise field and a texture lookup for every force, and a trail
at the end. Getting the lookups and the loop right takes a while before you
see a single particle move.

Particles2D_POP is that simulation in one node. It runs on the GPU and hands
you points.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire an image or a movie into **in_source**. Particles are born from its
   pixels and carry their colour; fully transparent areas emit nothing.
   **Maximum Particles** follows the source's resolution, one particle per
   pixel, so with nothing connected there is room for only one.
3. **Start Pulse** starts the simulation and **Reset Pulse** clears it. When
   the source's aspect ratio changes, the simulation restarts by itself.
4. Set how dense it is with **Birthrate**, **Life** and **Life Variance**.
5. The curl noise is on from the start. **Curl** sets its strength on each
   axis and **Speed** on the Curl page how fast the field moves.
6. The wind starts at zero. Set a **Wind** direction on the Wind page, and
   **Variance** for random variation on top.
7. Watch it in the node's viewer, which shows the simulated points.

Particles2D_POP is a Geometry COMP, and the geometry it renders is the
particles with their trails; **Length** under Trails stretches them into
streaks. out_loopout carries the simulated points without the trails, for a
render of your own or any POP that takes points.

For more control over the noise itself, **Open Curl Noise** and **Open
Variance** open the noise generators inside.

## Steering with images

Each force reads an image at every particle, and the value it reads scales
that force there. With the lookup's ranges left as they are, the force is off
wherever the image is black.

- With nothing wired into **in_effector_curl** or **in_effector_wind**, the
  source image itself is the effector, so its bright parts swirl and blow
  harder than its dark parts.
- Wire a different picture into either input to decide separately where
  particles swirl and where they drift: a gradient, a text mask, a second
  movie.
- The Lookup section on each page shapes what is read: the channel (**Rgb**
  on the Curl page, **RGB** on the Wind page), **Normalize**, a remap from one
  range to another, and an exponent to bend it.

Every particle reads the effector images where it is born. With **Update** on,
it reads them again every frame where it is now, so a force fades as particles
move into the dark parts of the image. Update ships on for the curl and off
for the wind.

## The simulation loop

out_loopout and in_loopin are the two ends of the loop the simulation runs
in. With nothing wired into in_loopin, the loop closes inside the operator.
Wire out_loopout through POPs of your own and back into in_loopin, and those
POPs run inside the loop on every step.

in_loopin expects the simulation's own particle data. Plain points from a
Grid POP raise errors there.

## Inputs and output

- **in_loopin** (POP): optional; points to carry into the loop.
- **in_source** (TOP): the image particles are born from.
- **in_effector_curl** (TOP), **in_effector_wind** (TOP): optional images that steer the curl and wind effectors through their lookups.
- **out_loopout** (POP): the simulated points.
