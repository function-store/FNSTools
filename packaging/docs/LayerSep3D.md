---
package: LayerSep3D
summary: 'Slices an image into depth layers by a channel threshold and instances them as a stack in 3D: per layer threshold, softness, mix, colour, position, scale and rotation, each driven by a curve or a CHOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Shaping the stack
    anchor: shaping-the-stack
  - name: Driving layers from CHOPs
    anchor: driving-layers-from-chops
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Slice an image into layers
    anchor: how-to-use-it
    does: 'Each layer takes the part of the image that passes its threshold on the channel you pick, with a soft edge to its neighbours.'
  - name: Instance the layers as a 3D stack
    anchor: how-to-use-it
    does: 'The layers are instanced as planes along Z in one Geometry COMP, so a camera pointed at it sees a flat picture with depth.'
  - name: Shape each value with a curve
    anchor: shaping-the-stack
    does: 'Threshold, softness, mix, depth, scale and rotation each follow a curve over the layers, set by offset, amplitude, power and phase.'
  - name: Shuffle the layer order
    anchor: shaping-the-stack
    does: 'Reverse, repeat, phase-shift or randomise which layer each plane shows, or show one layer on every plane.'
  - name: Drive layers from CHOPs
    anchor: driving-layers-from-chops
    does: 'CHOPs with one sample per layer take over the threshold, softness or mix curves.'
  - name: Instancing overrides
    anchor: driving-layers-from-chops
    does: 'Per-layer Z, scale and rotation can also be overridden in the instancing.'
  - name: Colour the layers from another image
    anchor: inputs-and-outputs
    does: 'Slice one image and draw another on the layers, such as a depth map cutting up the camera feed it came from.'
  - name: Output the layers as a texture
    anchor: inputs-and-outputs
    does: out_layers gives the layer stack as a 2D texture array or 3D texture for your own instancing.
---

## Why use it

Pulling a flat picture apart by brightness into planes at different depths is
a classic 2.5D look, and a moving camera turns it into parallax. Built by
hand, it is one Threshold TOP per band, a Texture 3D TOP to stack them, and
instancing to space the planes, and changing the number of layers means
rebuilding the chain.

LayerSep3D is that stack in one Geometry COMP. Set how many layers you want
and how they spread, and every value that changes from layer to layer is a
curve you shape with a few parameters, or a CHOP you wire in.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. It lands as one
   Geometry COMP.
2. Wire the image to slice into **in_mask**, and wire the same image into
   **in_color** to see it on the layers. With in_color empty the layers show
   an internal colour noise.
3. Add a Camera COMP and a Render TOP beside it. The Render TOP draws
   LayerSep3D like any other Geometry COMP. Move the camera off to the side to
   see the planes come apart.
4. Set **Layers** to the number of planes, and **Mode** to the value that
   sorts a pixel into a layer: Luminance for brightness, Alpha for a cut-out,
   or a single channel.
5. Fit the slicing to your image with **Threshold Range**: the range of mask
   values the layers are spread across. An image that only uses the middle of
   the range puts most of itself on a few planes until you narrow it.
6. Spread the stack in depth with **Z Amplitude** on the Transform page.
7. Soften the cut between layers with **Softness Offset**.

To check what a single layer holds, switch on **Single Layer** and step
through the layers with **Select Layer**.

## Shaping the stack

Every value that changes from layer to layer (threshold, softness, mix, depth,
scale and rotation) is a ramp from the first layer to the last, set by four
parameters:

- **Offset** adds the same amount to every layer.
- **Amplitude** sets how much the value changes from the first layer to the
  last.
- **Power** bends the ramp, so the change bunches toward one end.
- **Phase** rotates the ramp across the layers, so it wraps around. Rotation
  has **Rotation Invert** in its place, which runs the ramp backwards.

A few looks to start from:

- **Cut paper or a solid block.** With the mix at 0 each layer holds only its
  own band, like sheets of cut paper. Raising **Mix Offset** toward 1 keeps
  everything from that layer upward in each slice, so the planes overlap into
  something closer to a solid.
- **A fan or a tunnel.** **Rotation Amplitude** turns each layer a little
  further than the one before, and **Scale Amplitude** grows them.
- **Uneven depth.** **Z Power** bunches the planes toward the front or the
  back.

The Texture Index section changes which layer each plane shows, without
changing how the image is sliced: **Invert Texture Index** runs the order
backwards, **Texture Index Period** repeats the sequence, and **Randomize
Seed** shuffles it. **Reverse Layer Order** flips the slices themselves, so
layer 0 becomes the brightest band.

## Driving layers from CHOPs

Threshold, softness and mix can each come from a CHOP with one sample per
layer: wire it into **in_threshold**, **in_softness** or **in_mix**, or point
**Threshold CHOP (override)**, **Softness CHOP (override)** or **Mix CHOP
(override)** at it. The CHOP replaces that parameter curve.

- Thresholds should rise from layer to layer. A threshold CHOP that does not
  (a sine across the layers, say) puts nearly the whole image on one plane.
- The edge between layers j-1 and j uses softness j-1.

Per-layer Z, scale and rotation can also be overridden in the instancing.

## Inputs and outputs

- **in_mask** (TOP): the image that is sliced.
- **in_color** (TOP): the colour drawn on the layers, when different from the mask.
- **in_threshold**, **in_softness**, **in_mix** (CHOP): optional per layer curves that override the parameter curves.
- **out_layers** (TOP): the layer stack as a 2D texture array or 3D texture, for your own instancing.
