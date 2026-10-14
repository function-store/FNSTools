---
package: FNS_GlobalVolControl
summary: Set the overall volume of TouchDesigner.
features:
  - name: Mute and Volume
    anchor: mute-and-volume
    icon: GlobalVol.png
feature_list:
  - name: Master volume slider
    anchor: mute-and-volume
    does: 'Sets TouchDesigner''s application-wide output level from the toolbar, leaving the Volume on every Audio Device Out and Audio Play CHOP unchanged.'
  - name: Mute
    anchor: mute-and-volume
    does: 'The speaker button silences output without moving the slider, so unmuting returns to the same level.'
---

## Mute and Volume

A speaker button and a slider on the toolbar for TouchDesigner's **application-wide**
output level, the same thing the Audio Device Out settings control, without
opening a dialog.

This is the master level: it leaves the Volume parameter on every Audio Device
Out and Audio Play CHOP as it is, so turning it down leaves
your patch's own mix exactly as you built it. That is what makes it safe to grab
mid-set.

**Mute** silences output without disturbing the slider, so unmuting returns you to
the level you were at.
