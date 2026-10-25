---
package: ComplexMix
summary: 'A GLSL TOP that combines two UV fields as complex numbers: add, subtract, multiply, divide or raise one to the other, optionally weighted, then samples an image through the result.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Combine two UV fields as complex numbers
    anchor: how-to-use-it
    does: 'Treats each pixel pair of two UV fields as complex numbers and adds, subtracts, multiplies, divides or raises one to the other.'
  - name: Weighting between the operands
    anchor: how-to-use-it
    does: 'Fn Weight balances the two operands before they combine, so with Add one warp can morph into the other.'
  - name: Sample an image through the result
    anchor: how-to-use-it
    does: 'Samples the in1 image through the combined coordinates, so two ComplexOp warps become their sum, product or quotient.'
  - name: Transform the combined coordinates
    anchor: how-to-use-it
    does: 'Moves, rotates and scales the combined coordinates, with Aspect keeping rotation and scale round on a non-square output.'
  - name: Blend the effect in
    anchor: how-to-use-it
    does: Blend fades from the plain image to the full combination; animate it to bring the warp in on a cue.
  - name: Chain the combined UV field
    anchor: inputs-and-outputs
    does: out2 outputs the combined UV field for chaining into another sampler.
---

## Why use it

[ComplexOp](/docs/complexop/) warps an image through one complex function. To
get the sum of two such warps, their product, or one divided by the other, the
arithmetic has to happen on the coordinates themselves, per pixel and as
complex numbers, before the image is looked up. Compositing the two warped
images does something else, so this takes a shader of its own.

ComplexMix is that step. Feed it the UV outputs of two ComplexOps, choose the
operation, and the picture comes out warped by the combination. The combined
coordinates also leave as a UV field, so you can keep chaining. The complex
arithmetic is taken from
[Ricky Reusser's Shadertoy implementation](https://www.shadertoy.com/view/tlcGzf),
credited in the shader source.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire the image you want to see warped into **in1**.
3. Make the two operands: two ComplexOps with different functions, their
   second outputs (the UV fields) wired into **in2** (Op1) and **in3** (Op2).
   The ComplexOps need no image of their own; with nothing wired in they work
   on a built-in UV map. Keep them on a float **Pixel Format**, or the
   coordinates are quantised.
4. Choose the **Operation**. Op1 and Op2 pass one operand through on its own,
   which is the quickest way to check each warp. Add, Subtract, Multiply and
   Divide combine them, and the two power entries raise Op1 to Op2 or the
   other way round.
5. To favour one operand, switch on **Weighting** and set **Fn Weight**: 0 is
   all Op1, 1 is all Op2. It is one value for the whole image. With Add,
   animating it morphs one warp into the other.
6. Move the result with **Trans**, **Rot**, **Scale** and **Pivot**, in the
   order **Transform Order** sets. Switch on **Aspect** to keep rotation and
   scale round on a non-square output.
7. Choose what shows where the coordinates leave the image with **Extend**:
   hold the edge, zero, repeat or mirror.
8. Fade the effect with **Blend**: 0 is the plain image, 1 the full
   combination. Animate it to bring the warp in on a cue.

To keep going, take **out2**, the combined UV field, into another ComplexMix,
a ComplexOp with **Operand/Map** off, or a Remap TOP.

## Inputs and outputs

- **in1** (TOP): the image that is sampled through the combined coordinates.
- **in2** (TOP): the first complex operand (Op1), a UV map such as ComplexOp's second output.
- **in3** (TOP): the second complex operand (Op2).
- **out1** (TOP): the combined image.
- **out2** (TOP): the combined UV field, for chaining into another sampler.
