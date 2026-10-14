---
package: FNS_QuickTime
summary: 'A toolbar clock: resettable, scalable absTime and frame references to drag into your network.'
features:
  - name: QuickTime
    anchor: quicktime
    icon: QuickTime.png
feature_list:
  - name: Drag-and-drop time references
    anchor: quicktime
    does: 'Left-click the icon for a popup of absTime, absFrame, frame and progress (current frame over end frame, for perfect loops) to drag onto parameters.'
  - name: Scalable clock
    anchor: quicktime
    does: 'Multiplier scales absTime and absFrame, 1 for real time and 0.5 for half speed; right-click the icon to reach it.'
  - name: Reset the timers
    anchor: quicktime
    does: 'Sets the internal timers back to zero, the same as pulsing Reset on the component.'
---

## QuickTime

Left-click the icon for a popup of common timing references, ready to drag
onto a parameter:

- **absTime**: like `absTime.seconds`, except it can be reset and scaled.
- **absFrame**: like `absTime.frame`, likewise resettable and scalable.
- **frame**: the current frame.
- **progress**: the fraction `current frame / end frame`, useful for lookups
  and perfect loops.

**Multiplier** scales absTime and absFrame: 1 is real time, 0.5 runs them at
half speed. Right-click the icon to reach it.

**Middle-click** the icon to set the internal timers back to zero, the same
thing as pulsing **Reset** on the component.
