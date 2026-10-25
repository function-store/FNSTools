---
package: FNS_AutoRes
summary: Hold Alt while placing a generator TOP and its resolution follows the project, or the panel it sits in.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Only the operator you dropped
    anchor: only-the-operator-you-dropped
feature_list:
  - name: Resolution that follows the project
    anchor: how-to-use-it
    does: 'A generator TOP placed with `Alt` held gets a resolution expression that follows the `parent.Project` shortcut.'
  - name: Panel size inside panels
    anchor: how-to-use-it
    does: 'Inside a panel component, such as a Container COMP, the new TOP is set to Parent Panel Size.'
  - name: Fallback size without a Project shortcut
    anchor: how-to-use-it
    does: 'Where no `parent.Project` is found, the TOP uses the resolution you set on AutoRes.'
  - name: Default colour format
    anchor: how-to-use-it
    does: 'Sets the RGB mode and the Pixel Format of the new TOP too, where it has them.'
  - name: Skip reloads and large batches
    anchor: only-the-operator-you-dropped
    does: 'Leaves operators from package reloads, replicators or loading components alone, and skips a batch too large to be a drop with a Textport note.'
---

## Why use it

Generator TOPs come in at 1280x720. In a 1920x1080 project, or one built for an
LED wall, every Noise, Ramp or Constant you place needs its resolution changed,
and the one you forget sends a 1280x720 layer into your 1080p composite.

AutoRes sets the resolution as you place the TOP. Hold `Alt` while you drop a
generator and it comes in following the project's size.

## How to use it

Hold `Alt` (`Option` on macOS) while you place a generator TOP with nothing
wired into it. What it gets depends on where it lands:

- **Inside a panel component**, such as a Container COMP, its Output Resolution
  is set to Parent Panel Size.
- **Anywhere else**, its Output Resolution is set to Custom Resolution, and the
  width and height get an expression:

  ```python
  tdu.tryExcept(lambda: parent.Project.width, op.AUTO_RES.par.Resolutionw)
  ```

  with the same for the height. If `parent.Project.width` is defined, the TOP
  follows it. If not, it takes the size from AutoRes's own **Resolution**.

Where the TOP has them, its RGB mode and Pixel Format are set to AutoRes's
**RGB** and **Pixel Format** as well.

A generator placed onto a chain, with an input, is left to
[AutoCombine](/docs/fns-autocombine/), which listens for the same `Alt`.

To arm the gesture with another modifier, change **Keys**. To take AutoRes out
of the way without removing it, switch off **Active** or run **Toggle AutoRes**
from quick-launch.

## Only the operator you dropped

AutoRes acts on the operator that just appeared in the network you are looking
at, and on nothing else. Operators that surface deeper down (a package
reloading, a replicator, a component loading its contents) are not drops and are
left alone, and a batch too large to be a drop is skipped with a note in the
Textport. Earlier versions could catch up on such a backlog at your next
Alt-drop and rewrite every generator TOP in it.
