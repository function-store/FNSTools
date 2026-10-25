---
package: FloatDataRecorder
summary: 'Records a float texture such as a depth point cloud, a colour texture and a CHOP to files in sync, then plays the three back together against the timeline with a frame offset.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Record a point cloud, colour and CHOP together
    anchor: how-to-use-it
    does: 'Rec writes a float texture such as a depth point cloud, a colour texture and a CHOP such as skeleton data to files at once.'
  - name: Play back in step with the timeline
    anchor: how-to-use-it
    does: 'Plays the three files back in step with the timeline, with a frame offset to line them up, as textures and channels.'
  - name: Live pass-through
    anchor: how-to-use-it
    does: 'With Play off, and always while recording, the outputs carry the live inputs, so nothing downstream has to be rewired.'
  - name: Timeline fitted to the take
    anchor: how-to-use-it
    does: Sets the timeline's end to the length of the recording in one pulse.
  - name: Reload a new take
    anchor: how-to-use-it
    does: 'Reload picks up a take recorded over the same files and looks again for a missing CHOP file; until that file exists the CHOP player stays off, so a fresh node shows no error.'
---

## Why use it

An installation built around a depth camera means standing in front of the
sensor every time you want to test a change, with the sensor plugged into the
machine you are working on. Recording a take solves that only if the depth
point cloud, the colour image and the skeleton data come back in step. The
point cloud is a float texture, and the three streams are three different
kinds of data.

FloatDataRecorder records all three together: a float texture such as a
Kinect or depth camera point cloud, a colour texture, and a CHOP such as
skeleton data. Later it plays them back in step with the timeline, as if the
sensor were still there, so you can build and test the whole installation
without the hardware plugged in.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. Wire the float
   texture into the first input, the channels into the second and the colour
   texture into the third.
2. Under Record, set the two texture files and the **CHOP File** to where the
   take should go. A CHOP file name with no extension gets `.bclip`.
3. Turn **Rec** on, perform the take, and turn it off. All three streams write
   while it is on, and turning it off saves the channels to the CHOP file.
4. Under Play, open the three recorded files and switch on **Play**. With Play
   off, and always while recording, the outputs pass the live inputs through,
   so the rest of the network stays wired the same way for live and recorded
   data.
5. Line the take up. **Play Offset Frames** shifts playback against the
   timeline, and **Sync Timeline** makes the timeline as long as the recording.
6. After recording a new take over the same files, pulse **Reload**. It also
   looks again for a CHOP file that was missing.

The CHOP player stays off until its file exists, so a fresh node shows no
error before you have recorded anything.

The played-back channels keep their names, so a skeleton take can stand in for
the live Kinect CHOP, for example as the input of
[KinectSinglePlayer](/docs/kinectsingleplayer/).

## Inputs and outputs

- **in1** (TOP): the float texture to record, such as a point cloud.
- **in2** (CHOP): the channels to record.
- **in3** (TOP): the colour texture to record.
- **out_pointcloud** (TOP), **out_color** (TOP): the played-back textures.
- **out2** (CHOP): the played-back channels.
