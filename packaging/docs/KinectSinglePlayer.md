---
package: KinectSinglePlayer
summary: 'Picks one player out of a Kinect skeleton stream: whoever stands inside the bounds you set becomes the active player, and their joints ride out as clean channels until they leave.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Outputs
    anchor: outputs
feature_list:
  - name: Select a player by bounds
    anchor: how-to-use-it
    does: Watches a chosen joint of every tracked player and promotes one whose joint sits inside the box you define to active player.
  - name: Track one player on stable channels
    anchor: why-use-it
    does: 'The active player''s joints come out under a stable name, whichever of the six Kinect slots they occupy.'
  - name: Hand over to the next player
    anchor: why-use-it
    does: 'When the active player walks out of the box, the next player in range takes over.'
  - name: Detect whether a player is active
    anchor: outputs
    does: A separate CHOP output reports whether a player is active right now.
  - name: Read live or recorded data
    anchor: how-to-use-it
    does: 'Reads a Kinect CHOP, or any CHOP with Kinect-style channel names such as a recorded take.'
---

## Why use it

A Kinect CHOP reports every body it sees, spread over six player slots. An
installation usually wants exactly one person: whoever stands on the marked
spot in front of the screen. Which slot that person lands in is out of your
hands, and a passer-by in the background gets a slot too.

KinectSinglePlayer watches a chosen joint of every tracked player and keeps
the players whose joint sits inside a box you define. One of them becomes the
active player, and their joints come out under a stable name, so the rest of
the network never has to know which slot they occupy. When they walk out of
the box, the next player in range takes over.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog.
2. Point **Kinect Data** at your Kinect CHOP. Any CHOP with Kinect-style
   channel names works too, such as a take recorded and played back with
   [FloatDataRecorder](/docs/floatdatarecorder/), so you can set it up without
   the sensor.
3. Choose the **Joint** that decides whether someone counts as in range. The
   default, `spine`, tests the middle of the body; pick `head` or a hand when
   that is what should count.
4. Draw the box with **X Bounds**, **Y Bounds** and **Z Bounds**, in metres
   from the sensor. To pick the person standing on a spot two metres in front
   of the sensor, for example, set Z Bounds to 1.5 and 2.5 and narrow X Bounds
   to the width of the spot.
5. Use the outputs: **OUT_SINGLE_PLAYER** for the active player's joints, and
   **OUT_ACTIVE** to know whether anyone is there at all, for example to fade
   the interactive layer in and out.

## Outputs

- **OUT_ACTIVE** (CHOP): whether a player is active right now.
- **OUT_SINGLE_PLAYER** (CHOP): the active player's joints.
