---
package: ComplexOp
summary: 'A GLSL TOP that treats the image plane as the complex plane and applies a complex function to it: square, root, exp, log, inverse, the trigonometric and hyperbolic families and their inverses, with iteration, a pre and post transform and a choice of edge handling.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Chaining functions
    anchor: chaining-functions
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Warp an image through a complex function
    anchor: why-use-it
    does: 'Reads each pixel''s UV as a complex number, runs it through the chosen function and samples the input image at the result.'
  - name: 'Function menu: square, root, exp, log, sin and more'
    anchor: how-to-use-it
    does: 'Offers square, root, exp, log, inverse, power, and the trigonometric and hyperbolic families with their inverses.'
  - name: Iteration
    anchor: how-to-use-it
    does: 'Applies the function up to 64 times in a row, with an escape radius that can stop it early.'
  - name: Transform before and after the function
    anchor: how-to-use-it
    does: A transform before and after the function moves the point of interest to where the function does something worth seeing.
  - name: Edge handling
    anchor: how-to-use-it
    does: 'Extend picks what fills the frame where the warped coordinates leave the image: hold the edge, zero, repeat or mirror.'
  - name: Border mask output
    anchor: how-to-use-it
    does: 'The borders output keeps the mapped image only near the edges of each repeated tile, with Borders setting where that soft edge starts.'
  - name: Chain functions through the UV output
    anchor: chaining-functions
    does: 'A second output carries the mapped UV field, for a second ComplexOp, ComplexMix or a Remap TOP.'
---

## Why use it

Warping an image through a complex function is a GLSL job: the complex
arithmetic, a mapping from pixels to the plane, transforms around it, and a
rule for what happens past the image edge. ComplexOp has all of it behind a
menu.

It reads the UV of every pixel as a complex number, runs it through the
function you pick, and samples the input image at the result. A square folds
the plane once around the origin; a log turns rings into stripes; the
trigonometric functions tile and warp the picture in ways a plain Transform TOP
cannot reach. The complex math is taken from
[Ricky Reusser's Shadertoy implementation](https://www.shadertoy.com/view/tlcGzf),
credited in the shader source.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire an image into it. A photo with clear shapes, or a grid, makes the warp
   easy to read. With nothing wired in, it works on a built-in UV map at
   **Resolution**.
3. Pick a function from **Op**: csqr, csqrt, cexp, clog, cinv, csin and the
   rest of the trigonometric and hyperbolic families, their inverses, cpow and
   more. None passes the plane through, so only the transforms and Extend act.
4. Switch on **Center UV** to put the origin of the plane in the middle of the
   image. Off, z runs 0 to 1 from the bottom-left corner, so you only see the
   quarter of the plane above and to the right of the origin. Switch on
   **Aspect** as well to keep circles round on a non-square image.
5. Move the point of interest with the pre transform: **Trans**, **Rot**,
   **Scale** and **Pivot** act on the plane before the function, in the order
   **Transform Order** sets. Animate them to get motion out of a still
   image. **Post Trans**, **Post Rot**, **Post Scale** and
   **Post Pivot** act on the result.
6. Fold further with **Op Iter**, which applies the function again on its own
   result, up to 64 times. **Boundary** stops the iteration once the value
   passes that radius; 0 switches the test off.
7. Two functions take a value: **Power** is the exponent for cpow and the
   base of the logarithm for clog, and **Const** is what cconst returns.
8. Choose what fills the frame where the warped coordinates leave the image
   with **Extend**: hold the edge, zero, repeat or mirror. The **borders**
   output keeps the mapped image only near the edges of each repeated tile,
   with **Borders** setting where that soft edge starts.
9. Fade the effect in and out with **Blend**: 0 is the unwarped image, 1 the
   full warp.

## Chaining functions

The second output, **out2**, is the mapped coordinates as a UV field in red and
green. Two things use it:

- **A second function after the first.** Wire out2 into another ComplexOp and
  switch its **Operand/Map** off. It then reads its input's red and green as
  the complex numbers to work on, so its out2 is both functions in a row.
  Center UV and Aspect apply in map mode only.
- **Sampling an image.** Look up your image through the field with a Remap TOP,
  or with [ComplexMix](/docs/complexmix/), which also combines two fields by
  adding, multiplying, dividing or raising one to the other.

Keep a float **Pixel Format** wherever the UV output feeds another Complex
tool or a Remap TOP, or the coordinates are quantised.

## Inputs and outputs

- **in1** (TOP): the image to warp.
- **out1** (TOP): the warped image.
- **out2** (TOP): the mapped UV field, for feeding another sampler.
- **borders** (TOP): the border mask, where the mapped UV left the image.
