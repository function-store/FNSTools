---
package: InstanceTrailer
summary: 'Turns one moving image into a trail of its recent frames: a cache of the last N frames laid out in a row or column, with the spacing shaped by an exponent, ready to drive instancing.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Trail of recent frames
    anchor: why-use-it
    does: 'Caches incoming frames while an input is wired and lays the latest copies side by side, oldest at one end, newest at the other.'
  - name: Reach and copy count
    anchor: how-to-use-it
    does: 'Set how many copies the trail holds and how many frames back the oldest one reaches.'
  - name: Shape the time spacing
    anchor: how-to-use-it
    does: 'An exponent spaces the delays, so the copies bunch up near the present or fan out evenly into the past.'
  - name: Row or column layout
    anchor: how-to-use-it
    does: 'Lays the copies out left to right, right to left, top to bottom or bottom to top.'
  - name: CHOP output for instancing
    anchor: inputs-and-outputs
    does: 'A second output carries the trail as a CHOP in the same layout as the texture, for instanced geometry or CHOP-side use.'
---

## Why use it

To show where something has been, a dancer's silhouette, a hand, a moving
logo, you keep its last frames around and draw several of them at once. By hand
that is a Cache TOP, a Cache Select TOP per copy with its own offset, and a
Layout TOP to put them side by side. Changing the number of copies or how far
back they reach means editing every select.

InstanceTrailer builds and maintains that chain. It caches the incoming frames
and lays the most recent ones out side by side, oldest at one end and newest
at the other. You set how many copies, how far back they reach and how they are
spaced in time. The layout is a texture, and the same layout rides out as a
CHOP, which is what an instanced geometry needs to draw the trail in 3D.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire a moving image into it: a movie, a camera, a keyed silhouette. The
   cache records only while something is wired in, so the older copies fill
   in once it has recorded that far back.
3. Set **Depth**, the number of copies in the trail, the live frame included.
   After changing it by a large amount, pulse **Recreate All Operators** to
   rebuild the copies.
4. Set how far back the trail reaches with **Cache Size**. It is clamped to
   **Max Cache Size**, the number of frames the cache holds; raising that
   allows longer trails and uses more GPU memory.
5. Shape the spacing with **Exponent Value**. At 1 the copies are spread
   evenly through the cache, higher values bunch them near the live frame, and
   0 puts every copy on the same frame. **Direction** sets the sign and
   strength of the offset: positive values delay the copies into the past,
   negative values reverse their order.
6. Choose the layout with **Align**: left to right, right to left, top to
   bottom or bottom to top.
7. For 3D, take **out2**: the same trail as pixel data in a CHOP, ready for a
   Geometry COMP's instancing or anything else on the CHOP side.

## Inputs and outputs

- **in1** (TOP): the frames to trail. The cache records only while something is wired in.
- **out1** (TOP): the laid out trail.
- **out2** (CHOP): the trail as pixel data (one sample per pixel of a second, identical layout, r g b a channels), for instancing or CHOP-side use; the first block is the newest copy and the last block the oldest, matching out1 top to bottom.
