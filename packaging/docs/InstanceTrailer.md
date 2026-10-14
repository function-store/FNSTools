---
package: InstanceTrailer
summary: 'Turns one moving image into a trail of its recent frames: a cache of the last N frames laid out in a row or column, with the spacing shaped by an exponent, ready to drive instancing.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Trail of recent frames
    anchor: what-it-is
    does: 'Caches incoming frames while an input is wired and lays the latest Depth frames side by side, oldest at one end, newest at the other.'
  - name: Shaped sample spacing
    anchor: what-it-is
    does: 'Direction and Expval shape how samples spread through the cache, so the trail bunches near the present or fans out into the past.'
  - name: CHOP output for instancing
    anchor: inputs-and-outputs
    does: 'A second output carries the trail as a CHOP in the same layout as the texture, for instanced geometry or CHOP-side use.'
  - name: Place from the FNS tab
    anchor: what-it-is
    does: Pick it from the FNS tab of the OP Create dialog and it lands as one node.
---

## What it is

InstanceTrailer caches the incoming frames and lays the most recent ones out side by side, oldest at one end and newest at the other. Depth says how many, Direction and Expval shape how the samples are spread through the cache, so the trail can bunch up near the present or fan out into the past. The layout is a texture and the sample positions ride out as a CHOP, which is what an instanced geometry needs to draw the trail in 3D.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and outputs

- **in1** (TOP): the frames to trail. The cache records only while something is wired in.
- **out1** (TOP): the laid out trail.
- **out2** (CHOP): the trail as pixel data (one sample per pixel of a second, identical layout, r g b a channels), for instancing or CHOP-side use; the first block is the newest copy and the last block the oldest, matching out1 top to bottom.
