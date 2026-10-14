---
package: LayerSep3D
summary: 'Slices an image into depth layers by a channel threshold and instances them as a stack in 3D: per layer threshold, softness, mix, colour, position, scale and rotation, each driven by a curve or a CHOP.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and outputs
    anchor: inputs-and-outputs
  - name: Layer edges
    anchor: layer-edges
feature_list:
  - name: Slice an image into layers
    anchor: what-it-is
    does: 'Each layer takes the parts of the input passing a threshold on the channel you pick, with a soft edge between neighbouring layers.'
  - name: Instanced 3D stack
    anchor: what-it-is
    does: 'Instances the layers as planes along Z, so pointing a camera at it gives a flat picture depth.'
  - name: Per-layer curves
    anchor: what-it-is
    does: 'Threshold, softness, mix, offset, scale and rotation each follow a curve over the layer index with offset, amplitude, power and phase.'
  - name: CHOP-driven layers
    anchor: inputs-and-outputs
    does: 'Optional CHOPs wired into in_threshold, in_softness and in_mix override the parameter curves per layer.'
  - name: Separate colour source
    anchor: inputs-and-outputs
    does: in_color supplies the colour drawn on the layers when it differs from the mask image that is sliced.
  - name: Layer texture output
    anchor: inputs-and-outputs
    does: out_layers gives the layer stack as a 2D texture array or 3D texture for your own instancing.
  - name: Instancing overrides
    anchor: layer-edges
    does: 'Per-layer Z, scale and rotation can also be overridden in the instancing.'
---

## What it is

LayerSep3D is a Geometry COMP that turns one image into a stack of planes. Each of the Layers slices the input by a threshold on the channel you pick, so the bright parts land on one plane and the dark parts on another, with a soft edge between. The planes are instanced along Z, and every per layer value (threshold, softness, mix, offset, scale, rotation) is a curve over the layer index with an offset, amplitude, power and phase, or a CHOP you wire in. Point a camera at it and a flat picture gets depth.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and outputs

- **in_mask** (TOP): the image that is sliced.
- **in_color** (TOP): the colour drawn on the layers, when different from the mask.
- **in_threshold**, **in_softness**, **in_mix** (CHOP): optional per layer curves that override the parameter curves.
- **out_layers** (TOP): the layer stack as a 2D texture array or 3D texture, for your own instancing.

## Layer edges

The edge between layers j-1 and j uses softness j-1. Per-layer Z, scale and rotation can also be overridden in the instancing.
