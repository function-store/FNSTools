---
package: ColorGen
summary: 'A colour palette generator: a lookup of any length shaped by a phase step per channel and per channel exponents, with a lookup ramp as a second output.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Palette by formula
    anchor: what-it-is
    does: 'The three channels share one curve offset by a phase step, an exponent per channel bends each, and Length sets how many colours it holds.'
  - name: Animate with one Phase
    anchor: what-it-is
    does: The palette loops cleanly and animates with a single Phase parameter.
  - name: Palette strip output
    anchor: inputs-and-outputs
    does: 'The palette comes out as a colour strip, ready for a Lookup TOP or a CHOP to Table.'
  - name: Colour an image through it
    anchor: inputs-and-outputs
    does: 'The second output colours the input image through the palette; with nothing wired, a built-in 0 to 1 ramp shows the palette.'
  - name: Place from the FNS tab
    anchor: what-it-is
    does: Pick it from the FNS tab of the OP Create dialog and it lands as one node.
---

## What it is

ColorGen makes a palette by formula, so it loops cleanly and animates with a single Phase. The three channels are the same curve offset against each other by a phase step, and an exponent per channel bends each one, which is enough for most gradients without touching a coefficient table. Length sets how many colours the lookup holds; the palette comes out as a colour strip and as a lookup ramp, ready for a Lookup TOP or a CHOP to Table.

For the full cosine palette coefficients, an RGB and D mode and a blackout region, see ColorGenPro. It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and outputs

- **in1** (TOP): the image to colour through the palette; with nothing wired, a built-in 0 to 1 ramp is used, so both outputs show the palette on a bare drop.
- **out_col** (TOP): the palette strip.
- **out_lookup** (TOP): the input coloured through the palette.
