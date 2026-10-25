---
package: ColorGen
summary: 'A colour palette generator: a lookup of any length shaped by a phase step per channel and per channel exponents, with a lookup ramp as a second output.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Palette from a formula
    anchor: why-use-it
    does: 'Red, green and blue follow one curve, offset from each other by a phase step and bent by an exponent each, so a few values give a whole family of gradients.'
  - name: Animate with one Phase
    anchor: how-to-use-it
    does: 'One Phase value scrolls the palette and lands back where it started at 1, so it loops cleanly when you animate it.'
  - name: Palette strip
    anchor: inputs-and-outputs
    does: 'out_col is the palette as a colour strip, as many pixels wide as the palette has colours, ready for a Lookup TOP.'
  - name: Colour an image through the palette
    anchor: how-to-use-it
    does: 'out_lookup colours the input image through the palette; with nothing wired, a built-in 0 to 1 ramp shows the palette.'
---

## Why use it

A palette made from hand-placed keys on a Ramp TOP looks right until you want
it to move. Cycling the colours needs the end of the ramp to meet its start,
and every new colour scheme means placing the keys again.

ColorGen makes the palette by formula. The three channels are the same curve,
offset against each other by a phase step, and an exponent per channel bends
each one, which is enough for most gradients without touching a coefficient
table. Because it is a formula, it loops cleanly and animates with a single
**Phase**. It also colours an image through the palette for you.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. On a bare drop both
   outputs show the palette, because a built-in 0 to 1 ramp stands in for the
   missing input.
2. Spread the colours with **Phase Step per Channel**. At 0 the three channels
   move together and the palette is greys; raising it pulls red, green and
   blue apart. **Exponent Shift** decides where green sits between red and
   blue.
3. Bend a channel with **Exponent R**, **Exponent G** or **Exponent B**. Above
   1 the channel stays dark for longer along the palette, below 1 it brightens
   early.
4. Animate **Phase** to cycle the colours, for example with an expression such
   as `absTime.seconds*0.1` or from an LFO CHOP. 1 is one full cycle and lands
   back where it started; 0.5 mirrors the palette.
5. Colour an image: wire it into the input and take **out_lookup**. A
   greyscale source, such as a Noise TOP or a depth image, maps cleanly: dark
   values take the start of the palette, bright values its end.
6. Set how many colours the palette holds with **Length**, which is also the
   width of **out_col** in pixels. Use out_col to colour something elsewhere in
   your network with a Lookup TOP.

For the full cosine palette coefficients, an RGB and D mode and a blackout
region, see [ColorGenPro](/docs/colorgenpro/).

## Inputs and outputs

- **in1** (TOP): the image to colour through the palette; with nothing wired, a built-in 0 to 1 ramp is used, so both outputs show the palette on a bare drop.
- **out_col** (TOP): the palette strip.
- **out_lookup** (TOP): the input coloured through the palette.
