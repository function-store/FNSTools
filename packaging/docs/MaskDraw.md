---
package: MaskDraw
summary: 'Draw a mask with the mouse straight onto the image: a panel you paint in, with the mask and the masked image as outputs, a lock, a reset, and debug and display toggles.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Keeping the mask
    anchor: keeping-the-mask
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Paint and erase on the image
    anchor: how-to-use-it
    does: 'Paint on the input image with the left button and erase with the right; the panel follows the input''s aspect.'
  - name: Output the mask and the masked image
    anchor: inputs-and-outputs
    does: 'Outputs the drawn mask and the input inside the painted area, to key a composite, drive a Level or mark a projection surface.'
  - name: Reset the mask
    anchor: how-to-use-it
    does: 'Middle-click in the panel clears the mask, and so does Reset, which keeps it clear while it is on.'
  - name: Show or hide the button bar
    anchor: how-to-use-it
    does: 'Ctrl and middle-click shows or hides the button bar, and Show Input, Show Mask and Show Brush choose what the panel draws.'
  - name: Lock a finished mask
    anchor: how-to-use-it
    does: Lock keeps a finished mask from being changed by a stray click or reset.
  - name: Pause drawing
    anchor: how-to-use-it
    does: 'Switching Active off hides the brush and ignores the mouse, and the mask stays as it is.'
  - name: Save the mask with the project
    anchor: keeping-the-mask
    does: 'Optionally bakes the mask into the component on every save, so it is back when the project reopens.'
---

## Why use it

Some masks are quicker to draw than to build: the part of a wall your
projector should hit, the region of a camera image you want to key, a shape
around a performer that no threshold will find. Drawing one usually means
leaving TouchDesigner for an image editor, exporting a file and loading it back
in, and doing it all again when the stage moves.

MaskDraw lets you paint the mask straight onto the image inside your network.
The strokes accumulate into a mask, which comes out on its own and applied to
the input.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire the image you want to mask into it: a camera, a movie, a still of the
   projection surface.
3. Open MaskDraw's panel. The input image is your canvas, and the panel
   follows the input's aspect.
4. Paint with the left button and erase with the right. **Radius** sets the
   brush size, relative to the mask. Drawing works while **Active** is on;
   switch it off and the brush hides and the mouse is ignored, with the mask
   kept.
5. To start over, middle-click in the panel. **Reset** does the same: the
   mask stays clear for as long as it is on.
6. `Ctrl` and middle-click shows or hides the button bar in the panel, the
   same as **Display UI**. **Show Input**, **Show Mask** and **Show Brush**
   change what the panel draws while you paint: the input behind the mask, the
   mask in white, and the brush outline in red.
7. When the mask is right, switch on **Lock**. New strokes, erasing and Reset
   are ignored until you turn it off, so a stray click during a show cannot
   change it.
8. Use the outputs: **out_mask** is the mask itself, and **out_masked** is the
   input inside the painted area. Key a composite with it, drive a Level, or
   mark a projection surface.

## Keeping the mask

By default the mask lives in the running session and nothing is written into
the file, so it is gone when you reopen the project. Turn on **Save Mask With
Project** and the mask is baked into the component on every project save, or
right away with **Bake Mask Now**, and restored when the project is reopened.
The baked texture is the size of the panel, so the file grows by a few
megabytes.

## Inputs and outputs

- **in1** (TOP): the image to draw over.
- **out_mask** (TOP): the drawn mask.
- **out_masked** (TOP): the input inside the painted area.
