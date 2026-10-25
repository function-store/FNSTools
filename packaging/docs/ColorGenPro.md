---
package: ColorGenPro
summary: 'A cosine palette generator in GLSL: the full coefficient set per channel, an RGB and D mode, a blackout region with a soft edge, and a lookup ramp as a second output.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Palette behavior
    anchor: palette-behavior
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Cosine palette with every coefficient
    anchor: how-to-use-it
    does: 'Offset, amplitude, period, phase and exponent for red, green and blue, for smooth gradients that loop cleanly.'
  - name: RGB and D mode
    anchor: how-to-use-it
    does: 'Drives the three phases from one Offset, Amplitude and Exponent, so a single value scrolls the whole palette.'
  - name: Blackout region
    anchor: how-to-use-it
    does: 'Keeps the start of the palette black, added to the length or taken from the colours, with a soft edge you shape.'
  - name: Palette strip output
    anchor: inputs-and-outputs
    does: 'out_col is the palette as a colour strip, and Length sets how many colours it holds.'
  - name: Colour an image through the palette
    anchor: how-to-use-it
    does: out_lookup colours the input image through the palette; with nothing wired a built-in 0 to 1 ramp shows the palette.
  - name: Reset to the shipped coefficients
    anchor: how-to-use-it
    does: Default restores the shipped coefficients and leaves any parameter driven by an expression alone.
---

## Why use it

The cosine palette, `pow(a + b*cos(2PI*(c*t+d)), e)` per channel, gives smooth
gradients that loop cleanly and animate with a single phase. Using it in a
project means writing a GLSL TOP, wiring fifteen values into its uniforms, and
adding a Lookup TOP to put the result on an image.

ColorGenPro has the formula with every coefficient open, an RGB and D mode
that collapses them to one offset, amplitude and exponent when you want fewer
knobs, and a blackout region that keeps the start of the palette black. The
palette comes out as a colour strip and colours your image through a lookup in
the same node.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. On a bare drop both
   outputs show the palette, because a built-in 0 to 1 ramp stands in for the
   missing input.
2. Shape the palette with the coefficients under the formula header, each set
   for red, green and blue. **a (Offset)** is the base brightness,
   **b (Amplitude)** how far each channel swings around it, and
   **c (Period)** how many colour cycles fit along the palette. The hues come
   from **d (Phase)**: offsetting the three channels from each other is what
   makes colour. **e (Exponent)** deepens a channel above 1 and lifts it
   below 1.
3. For fewer knobs, switch on **RGBD Mode**. The three d values then follow
   **Offset**, **Amplitude** and **Exponent**: Offset sets the phase of red,
   and green and blue follow from it, so animating Offset alone scrolls the
   whole palette. Amplitude at 0 puts all three channels in phase, which gives
   greys. Switching RGBD Mode on restores the shipped coefficients first, so
   note any values you want to keep.
4. Colour an image: wire it into the input and take **out_lookup**. A
   greyscale source, such as a Noise TOP or a depth image, maps cleanly: dark
   values take the start of the palette, bright values its end. **Input
   Smoothness** on Nearest picks exact palette entries, which with a short
   **Length** gives distinct bands; Linear blends between neighbours.
5. To keep the darkest values black, raise **Blackout**. That share at the
   start of the palette fades to black. **Reductive** at 0 adds the black on
   top of **Length**, at 1 it takes it from the colours. **Soften Black**,
   **Soften Exponent** and **Soften Extend** shape the fade into the palette.
6. To start over, pulse **Default**. It restores the shipped coefficients and
   the RGBD values, and leaves any parameter driven by an expression as it is.

ColorGenPro is the Pro sibling of [ColorGen](/docs/colorgen/), which shapes its
palette with a phase step and exponents.

## Palette behavior

Each channel is clamped at zero before the exponent is applied, so no pixel
goes invalid. When **b (Amplitude)** is larger than **a (Offset)**, the troughs
of that channel's swing therefore clip to black. Keep a at or above b and
nothing clips.

## Inputs and outputs

- **in1** (TOP): the image to colour through the palette; with nothing wired, a built-in 0 to 1 ramp is used, so both outputs show the palette on a bare drop.
- **out_col** (TOP): the palette strip.
- **out_lookup** (TOP): the input coloured through the palette.
