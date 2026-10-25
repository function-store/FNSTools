---
package: QuickMarks
summary: Save up to ten spots in your project and jump straight back to them with Ctrl+number.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Seeing your marks
    anchor: seeing-your-marks
feature_list:
  - name: Save a mark
    anchor: how-to-use-it
    does: 'Stores the network you are in, with its pan and zoom, in one of ten numbered slots.'
  - name: Jump to a mark
    anchor: how-to-use-it
    does: Takes you back to a saved mark from anywhere in the project.
  - name: Remove a mark
    anchor: how-to-use-it
    does: Clears a numbered slot.
  - name: Save marks in the project file
    anchor: how-to-use-it
    does: 'Marks live in the project file, so they are waiting the next time you open it.'
  - name: Name and clear marks from quick-launch
    anchor: how-to-use-it
    does: 'Store, jump to, name, list and clear marks from quick-launch, including slots past the first ten.'
  - name: List marks in a corner
    anchor: seeing-your-marks
    does: 'A corner list shows each mark by number and name and highlights the one you are in; click to jump, right-click to rename.'
  - name: Outline what each mark saved
    anchor: seeing-your-marks
    does: 'Outlines the area each mark saved, with its number and name, in the network you are viewing.'
  - name: Toggle the overlay
    anchor: seeing-your-marks
    does: 'Hides or shows the list and the outlines together, while your marks and their keys keep working.'
---

## Why use it

Every project has a handful of places you keep going back to: the output
chain, the component you are debugging, the control panel. Getting there means
clicking up and down the path bar, or zooming out and hunting for the right
box. It is a small thing that adds up over a day.

QuickMarks gives you ten numbered bookmarks. Park one on a network and you are
one keystroke away from it, from anywhere in the project. It is based on
QuickMarks by [Alex Guevara](https://alex-guevara.com).

## How to use it

- **Save** where you are: `Ctrl+Alt+{number}` (`Ctrl+Option+{number}` on
  macOS). The mark remembers the network, the operator you were on, and the pan
  and zoom.
- **Jump** back to it: `Ctrl+{number}`.
- **Remove** it: `Ctrl+Alt+Shift+{number}` (`Option` instead of `Alt` on macOS).

`{number}` is `0` to `9`. A setup that works well: `1` on the output chain,
`2` on whatever you are building right now, `3` on the control panel. After a
day it is muscle memory.

Marks are saved in your project file and are there the next time you open it.
They are per project on purpose: a mark points at a network path, and the same
path means something else in another `.toe`.

The keys overlap shortcuts a lot of people already use. If they get in your
way, switch **Active** off. QuickMarks goes quiet and your marks are kept.

Everything is also in quick-launch: **Store quickmark**, **Go to quickmark**,
**Name quickmark**, **List quickmarks** and **Clear quickmark**. Quick-launch
also reaches slots past the first ten, which have no key.

## Seeing your marks

QuickMarks can draw your marks on the network editor. This starts switched
off: press `Alt+Shift+M` (`Option+Shift+M` on macOS), or switch on **Mark
List** and **Pins**, to see it.

- **The mark list** sits in a corner and shows each mark by number and name,
  with the one for the network you are in highlighted. Click a row to jump
  there, right-click it to rename the mark. A mark whose network no longer
  exists is dimmed and reads *missing*. The arrow on the title row folds the
  list away.
- **Outlines** show what each mark saved: the area that was on screen when you
  stored it, with its number and name, drawn in the network you are viewing.

`Alt+Shift+M`, or **Toggle QuickMarks overlay** in quick-launch, hides and
shows both together. Your marks and `Ctrl+{number}` keep working while they are
hidden.

To move the list to another corner, use the **Overlay** tab of
[FNS_Hub](/docs/fns-hub/), which arranges every tool that draws on the network
editor. If Cook Bar's Top List shares the corner, the mark list sits under it
unless you change the order there.
