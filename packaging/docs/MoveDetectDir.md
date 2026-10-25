---
package: MoveDetectDir
summary: 'Reads which way things move in a camera or any image with optical flow and turns it into left/right and down/up channels, with thresholds, inversion and filtering, for swipe and gesture triggers.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and output
    anchor: inputs-and-output
feature_list:
  - name: Optical flow direction
    anchor: why-use-it
    does: 'Runs optical flow on the input image and measures how much of the flow points left, right, down and up.'
  - name: Direction channels
    anchor: inputs-and-output
    does: 'Outputs LR and DU channels that swing toward the direction of movement once it passes a threshold, for swipe and gesture triggers.'
  - name: Filter out noise and small motion
    anchor: how-to-use-it
    does: 'Blur on the input, a flow threshold and a movement threshold per axis keep camera noise and small motion from firing it.'
  - name: Invert a direction for mirrored cameras
    anchor: how-to-use-it
    does: Flips either direction for a mirrored camera.
  - name: Smooth the channels
    anchor: how-to-use-it
    does: Smooths the direction channels over a time you set.
---

## Why use it

A swipe in front of a camera is an easy gesture for an audience to learn, and
a fiddly one to read in TouchDesigner. A frame difference tells you that
something moved, but not which way. For the direction you need optical flow,
then a way to boil the flow field down to left, right, down and up, then
thresholds and smoothing so that a twitch or camera noise does not count as a
swipe.

MoveDetectDir is that chain in one node. It runs optical flow on the input,
measures how much of the flow points left, right, down and up, and once the
movement passes a threshold it comes out as two channels: one for left and
right, one for down and up. Wave a hand across the camera and the channel
swings to the side you swiped to.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Wire a camera into it, for example a Video Device In TOP for a webcam. Any
   image works.
3. Swipe in front of the camera and watch **LR** and **DU**. If a swipe to the
   left reads as right, as it does with a mirrored camera, switch on **Inverse
   X**; **Inverse Y** does the same for down and up.
4. Tune it to the room:
   - If it fires on noise or on small movements in the background, raise
     **Input Filter Size** to blur away fine detail, or **OptFlow Threshold**
     to ignore weak flow.
   - If a deliberate swipe does not register, lower **Move Threshold X** or
     **Move Threshold Y**.
   - If the channels feel jumpy or slow, change **Filter Width**: a shorter
     time reacts faster, a longer one is steadier.
5. Use the channels for anything that should react to the direction of motion
   as well as its amount: paging through a
   [SlideShow](/docs/slideshow/) with a gesture, or steering a scene from a
   crowd.

## Inputs and output

- **in1** (TOP): the image to watch, usually a camera.
- **out1** (CHOP): two channels, **LR** for left and right movement and **DU** for down and up.
