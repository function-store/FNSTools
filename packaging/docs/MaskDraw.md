---
package: MaskDraw
summary: 'Draw a mask with the mouse straight onto the image: a panel you paint in, with the mask and the masked image as outputs, a lock, a reset, and debug and display toggles.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Paint and erase on the image
    anchor: what-it-is
    does: 'Open the panel and paint on the input image with the left button, erase with the right; the panel follows the input''s aspect.'
  - name: Mask and masked image outputs
    anchor: inputs-and-outputs
    does: 'Outputs the drawn mask and the input inside the painted area, to key a composite, drive a Level or mark a projection surface.'
  - name: Reset and button bar gestures
    anchor: what-it-is
    does: Middle-click resets the mask; Ctrl and middle-click toggles the button bar.
  - name: Lock a finished mask
    anchor: what-it-is
    does: Lock keeps a finished mask from being changed by a stray click or reset.
  - name: Save the mask with the project
    anchor: what-it-is
    does: 'Save Mask With Project bakes the mask into the component on every save, or now with Bake Mask Now, and restores it on reopen.'
  - name: Place from the FNS tab
    anchor: what-it-is
    does: Pick it from the FNS tab of the OP Create dialog and it lands as one node.
---

## What it is

MaskDraw is a panel. Open it, and the input image is your canvas: paint with the left button, erase with the right, and the strokes accumulate into a mask. The mask comes out on its own and applied to the input (the input inside the painted area), so it can key a composite, drive a Level, or mark a projection surface. The panel follows the input's aspect. Middle-click resets the mask; Ctrl and middle-click toggles the button bar. Lock keeps a finished mask from being touched by a stray click or reset.

By default the mask lives in the running session and nothing is written into the file. Turn on Save Mask With Project and the mask is baked into the component on every project save (or right away with Bake Mask Now), and restored when the project is reopened. The baked texture is the size of the panel, so the file grows by a few megabytes.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Inputs and outputs

- **in1** (TOP): the image to draw over.
- **out_mask** (TOP): the drawn mask.
- **out_masked** (TOP): the input inside the painted area.
