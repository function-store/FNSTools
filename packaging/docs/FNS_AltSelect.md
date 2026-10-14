---
package: FNS_AltSelect
summary: Hold Alt and drag a selected operator to leave a Select in its place.
features:
  - name: Alt-drag to Select
    anchor: alt-drag-to-select
feature_list:
  - name: Alt-drag to create a Select
    anchor: alt-drag-to-select
    does: 'Alt-dragging a selected TOP, CHOP, SOP, DAT, POP or panel COMP snaps it back and leaves a Select pointed at it where you drop.'
  - name: Ready-to-use Select
    anchor: alt-drag-to-select
    does: 'The new Select is wired, selected and current, viewer on and tinted, with Match Size on for panels, all as a single undo step.'
  - name: Tagged for later sweeps
    anchor: alt-drag-to-select
    does: 'Every operator it creates is tagged FNS_AltSelect, so a Find or `findChildren(tags=...)` sweep can locate them later.'
---

## Alt-drag to Select

Hold `Alt` and drag a selected operator away from where it sits. The operator
snaps back to its original position and a **Select** of the same family
appears where you dropped it, already pointed at the original.

It is the fastest way to reference an operator somewhere else in the network
without touching the original chain: grab it, pull a copy out, keep working.

The new Select arrives ready to use: wired to the source, selected and made
current so your next action lands on it, viewer on, and tinted so a
referencing node is distinguishable from the real thing at a glance. Panel
COMPs also get **Match Size** turned on, which is almost always what you want.
The whole thing is a single undo step.

Works for TOPs, CHOPs, SOPs, DATs, POPs and panel COMPs. Non-panel COMPs are
left alone: TouchDesigner's Select COMP only handles panels, so there is
nothing to create for them and the drag behaves normally.

Every operator it creates is tagged `FNS_AltSelect`, so you can find them
later with a Find or a `findChildren(tags=...)` sweep.

Turn the **Active** parameter off to stop it intercepting drags; the component
can stay installed.
