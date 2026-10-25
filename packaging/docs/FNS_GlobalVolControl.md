---
package: FNS_GlobalVolControl
summary: Set the overall volume of TouchDesigner.
features:
  - name: Why use it
    anchor: why-use-it
    icon: GlobalVol.png
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Master volume slider
    anchor: how-to-use-it
    does: 'Sets TouchDesigner''s application-wide output level from the toolbar, leaving the Volume on every Audio Device Out and Audio Play CHOP unchanged.'
  - name: Mute
    anchor: how-to-use-it
    does: 'The speaker button silences output without moving the slider, so unmuting returns to the same level.'
  - name: Set volume or toggle mute from quick-launch
    anchor: how-to-use-it
    does: 'The Set volume command takes a level from 0 to 1, and Toggle mute mutes and unmutes.'
  - name: Restore the level at startup
    anchor: how-to-use-it
    does: The level and the mute state are applied again as the project starts.
---

## Why use it

In a TouchDesigner patch the volume lives in many places: every Audio Device
Out and Audio Play CHOP has its own Volume parameter. When everything needs to
be quieter right now, for a soundcheck or a call in the studio, digging through
a mix you balanced carefully is the last thing you want to do.

GlobalVolControl puts TouchDesigner's master output level on the toolbar, as a
speaker button and a slider, with no dialog to open. It changes the
application-wide level and leaves the Volume parameter on every operator as it
is, so your patch's own mix stays exactly as you built it. That is what makes
it safe to grab mid-set.

## How to use it

- Drag the slider on the toolbar to set the overall level.
- Click the speaker button to mute. The icon lights while the sound is muted.
  The slider stays where it is, so unmuting returns you to the level you were
  at.
- From quick-launch, **Set volume** takes a level from 0 to 1 and **Toggle
  mute** mutes and unmutes.

The tool applies its level and mute state again as the project starts. If a
project opens silent, check the speaker button first.
