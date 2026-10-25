---
package: FNS_AltSelect
summary: Hold Alt and drag a selected operator to leave a Select in its place.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Drag out a Select with Alt
    anchor: how-to-use-it
    does: 'Alt-drag a selected operator and it stays where it was, while a Select pointed at it appears where you let go.'
  - name: Match the operator family
    anchor: how-to-use-it
    does: 'Works for TOPs, CHOPs, SOPs, DATs, POPs and panel COMPs, each getting the matching Select.'
  - name: Ready to use
    anchor: how-to-use-it
    does: 'The new Select arrives selected and current, with its viewer on and a tint that marks it as a reference.'
  - name: Undo in one step
    anchor: how-to-use-it
    does: A single undo takes the Select away again.
  - name: Find them later by tag
    anchor: how-to-use-it
    does: 'Every Select it makes is tagged `FNS_AltSelect`, so a Find or a `findChildren(tags=...)` sweep can list them.'
---

## Why use it

To use an operator in another part of a network, you either pull a long wire
across everything in between, or create a Select, point it at the source and
move it into place. Both are fine once. Over an evening of patching, the wires
cross the whole network and every Select is another round of create, point and
move.

AltSelect makes it one gesture: hold `Alt` and drag the operator to where you
want the reference. The original stays where it was.

## How to use it

1. Select an operator.
2. Hold `Alt` (`Option` on macOS) and drag it away from where it sits.
3. Let go. The operator snaps back to its original position, along with
   anything docked to it, and a Select of the same family appears where you
   dropped it, already pointed at the original.

The new Select is selected and made current, so your next action lands on it.
Its viewer is on, and it is tinted so a reference is easy to tell from the real
thing at a glance. Panel COMPs also get Match Size switched on, which is almost
always what you want. The whole thing is a single undo step.

Non-panel COMPs are left alone: TouchDesigner's Select COMP only handles panels,
so there is nothing to create for them and the drag moves the COMP as usual.

Every operator AltSelect creates is tagged `FNS_AltSelect`, so you can find them
all later with a Find or a `findChildren(tags=...)` sweep.

To stop it catching drags while keeping it installed, switch off **Active**, or
run **Toggle AltSelect** from quick-launch.
