---
package: CircularDistortionTOP
summary: 'A circular distortion for images: rings of displacement around a centre you place, with phase, frequency, amplitude and a mode blend, and a choice of how the input extends past its edge.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Ring distortion around a centre you place
    anchor: how-to-use-it
    does: 'Pushes the image in rings around any point: the middle of the frame, a face, a logo.'
  - name: Animate the rings with Phase
    anchor: how-to-use-it
    does: 'Animating Phase sends the rings outward or inward; a step of 1 moves them by one ring.'
  - name: Round on any aspect
    anchor: how-to-use-it
    does: The rings stay circular on a 16:9 frame or any other non-square image.
  - name: Blend between two distortion modes
    anchor: how-to-use-it
    does: 'Mode blends between a push that grows with the distance from the centre and one that is the same strength everywhere.'
  - name: Edge handling
    anchor: how-to-use-it
    does: 'Choose what shows where the rings pull in pixels from past the image edge: hold, zero, repeat or mirror.'
---

## Why use it

A ripple running out from one point is a move you reach for again and again: a
shockwave on a kick, a drop hitting the surface of a clip, a pulse around a
logo. With stock operators it is a Displace TOP fed by a radial sine pattern
you build yourself, and getting the rings centred where you want them and round
on a widescreen frame takes some fiddling.

CircularDistortionTOP is that ripple in one node. Place the centre, set how
many rings and how far they push, and animate one value to make them travel.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire an image or a movie into it. Fine detail and straight lines make the
   rings easiest to see.
3. Put **Center** where the rings should come from, in UV: 0.5, 0.5 is the
   middle of the frame. Move it onto a face or a logo to make that the source
   of the ripple.
4. Set the rings: **Frequency** packs more of them across the image, and
   **Amplitude** sets how far they displace it. At 0 the image is untouched.
5. Make them travel by animating **Phase**. One full step, 0 to 1, moves the
   rings by one ring, so a steadily rising value keeps them moving and counting
   down reverses them. Drive it from a CHOP for a ripple that follows your
   music or a trigger.
6. Change the character with **Mode**. At 0 the image is scaled radially
   around the centre, so the push grows with the distance from it and the
   middle stays calm. At 1 every pixel is pushed along its direction from the
   centre by the same amount. Values in between mix the two.
7. Pick what fills the frame edge with **Input Extend Mode Uv**. Where the
   rings pull in pixels from outside the image, they can hold the edge colour,
   go to zero, repeat the image or mirror it.

## Inputs and output

- **in1** (TOP): the image to distort.
- **out1** (TOP): the distorted image.
