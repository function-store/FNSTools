---
package: ComplexOp
summary: 'A GLSL TOP that treats the image plane as the complex plane and applies a complex function to it: square, root, exp, log, inverse, the trigonometric and hyperbolic families and their inverses, with iteration, a pre and post transform and a choice of edge handling.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Complex-plane warp
    anchor: what-it-is
    does: 'Reads each pixel''s UV as a complex number, runs it through the chosen function and samples the input image at the result.'
  - name: Complex function set
    anchor: what-it-is
    does: 'Offers square, root, exp, log, inverse, and the trigonometric and hyperbolic families with their inverses.'
  - name: Iteration
    anchor: what-it-is
    does: Applies the function several times in a row.
  - name: Pre and post transform
    anchor: what-it-is
    does: A transform before and after the function moves the point of interest to where the function does something worth seeing.
  - name: Mapped UV output
    anchor: inputs-and-outputs
    does: 'A second output carries the mapped UV field, for feeding another sampler.'
  - name: Edge handling and border mask
    anchor: inputs-and-outputs
    does: 'Offers a choice of edge handling, and a borders output masks where the mapped UV left the image.'
---

## What it is

ComplexOp reads the UV of every pixel as a complex number, runs it through the complex function you pick, and samples the input image at the result. A square folds the plane once around the origin; a log turns rings into stripes; the trigonometric functions tile and warp the picture in ways a plain Transform TOP cannot reach. The function can be applied several times in a row, and a transform before and after it moves the point of interest to where the function does something worth seeing.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and outputs

- **in1** (TOP): the image to warp.
- **out1** (TOP): the warped image.
- **out2** (TOP): the mapped UV field, for feeding another sampler.
- **borders** (TOP): the border mask, where the mapped UV left the image.
