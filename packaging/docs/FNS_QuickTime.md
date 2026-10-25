---
package: FNS_QuickTime
summary: 'A toolbar clock: resettable, scalable absTime and frame references to drag into your network.'
features:
  - name: Why use it
    anchor: why-use-it
    icon: QuickTime.png
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Drag-and-drop time references
    anchor: how-to-use-it
    does: 'Click the toolbar icon for absTime, absFrame, frame and progress, ready to drag onto a parameter.'
  - name: Reset the clock
    anchor: how-to-use-it
    does: 'Middle-click the icon, or run Reset timer, to send QuickTime''s absTime and absFrame back to zero.'
  - name: Scale the clock speed
    anchor: how-to-use-it
    does: 'Multiplier scales absTime and absFrame: 1 is real time, 0.5 is half speed.'
  - name: Progress for perfect loops
    anchor: how-to-use-it
    does: 'The current frame divided by the end frame, for lookups and loops that close exactly.'
---

## Why use it

Driving a parameter with time is one of the first expressions anyone writes:
`absTime.seconds` for a slow drift, a multiplier on it for speed, the current
frame over the end frame for something that loops with the timeline. Typing
them out gets old, and a run-through often wants every timed thing to start
from zero together.

QuickTime keeps a clock on the toolbar. Click it and drag the time reference
you need onto a parameter; reset or scale the clock when you need to.

## How to use it

1. Click the QuickTime icon on the toolbar. A popup lists four time
   references.
2. Drag one onto a parameter:
   - **absTime**: like `absTime.seconds`, except it can be reset and scaled.
   - **absFrame**: like `absTime.frame`, likewise resettable and scalable.
   - **frame**: the current frame.
   - **progress**: the fraction `current frame / end frame`, useful for
     lookups and perfect loops.

- **To slow everything down or speed it up,** right-click the icon to open
  the parameters and change **Multiplier**: 1 is real time, 0.5 runs absTime
  and absFrame at half speed.
- **To start the clock from zero,** middle-click the icon, pulse **Reset**,
  or run **Reset timer** from quick-launch.
