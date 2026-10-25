---
package: FNS_AutoCombine
summary: Hold Alt while placing a generator TOP to set its combine, operation and format defaults.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Only the operator you dropped
    anchor: only-the-operator-you-dropped
feature_list:
  - name: Composite as you place
    anchor: how-to-use-it
    does: 'Hold `Alt` while placing a generator TOP such as a Noise, Circle or Rectangle onto a chain, and it comes in set to combine with its input.'
  - name: Blend and format defaults
    anchor: how-to-use-it
    does: 'The Combine with Input mode, the Operation, the Pixel Format and the Noise TOP''s RGB mode all come from your settings on AutoCombine.'
  - name: Alt or another modifier key
    anchor: how-to-use-it
    does: 'Pick the key that arms the gesture; the default chooses the right one per platform.'
  - name: Skip reloads and large batches
    anchor: only-the-operator-you-dropped
    does: 'Acts only on the operator that just appeared in the network you are looking at; operators surfacing deeper down and large batches are left alone.'
  - name: Toggle from quick-launch
    anchor: how-to-use-it
    does: 'The Toggle AutoCombine command switches it off and on without opening its parameters.'
---

## Why use it

Generator TOPs can combine with the image wired into them. A Noise TOP set to
multiply over its input does the job of a Noise plus a Composite, in one node.
Getting there means setting Combine with Input on every new generator, then the
Operation, and on a Noise TOP the RGB mode too. You set them the same way every
time.

AutoCombine sets them as you place the TOP. Hold `Alt` while you add a generator
to a chain and it arrives already compositing over its input, with the blend you
picked.

## How to use it

1. Create a generator TOP so that it arrives wired to the TOP you want to
   cover, for example from that TOP's output connector, and hold `Alt`
   (`Option` on macOS) as you place it.
2. It lands with **Combine with Input**, **Operation**, **Pixel Format** and, on
   a Noise TOP, **RGB** set to AutoCombine's values.

AutoCombine only changes a TOP that has an input once it is placed. A generator
you place on its own is left as TouchDesigner made it; that case belongs to
[AutoRes](/docs/fns-autores/), which listens for the same `Alt`.

To change what new generators get, set those four parameters on AutoCombine
itself. To arm the gesture with another modifier, change **Keys**. To take
AutoCombine out of the way without removing it, switch off **Active** or run
**Toggle AutoCombine** from quick-launch.

## Only the operator you dropped

AutoCombine acts on the operator that just appeared in the network you are
looking at, and on nothing else. Operators that surface deeper down (a package
reloading, a replicator, a component loading its contents) are not drops and are
left alone, and a batch too large to be a drop is skipped with a note in the
Textport. Earlier versions could catch up on such a backlog at your next
Alt-drop and rewrite every TOP with inputs in it.
