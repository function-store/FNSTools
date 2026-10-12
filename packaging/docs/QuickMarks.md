---
package: QuickMarks
summary: Save up to ten spots in your project and jump straight back to them with Ctrl+number.
features:
  - name: QuickMarks
    anchor: quickmarks
  - name: On the network editor
    anchor: on-the-network-editor
---

## QuickMarks

Ten numbered bookmarks for places in your project. Park one on the network you
keep coming back to and you are one keystroke away from it, from anywhere.
It is based on QuickMarks by [Alex Guevara](https://alex-guevara.com).

- **Save** a mark: `Ctrl+Alt+{number}` (`Ctrl+Option+{number}` on macOS)
- **Recall** it: `Ctrl+{number}`
- **Remove** it: `Ctrl+Alt+Shift+{number}` (`Option` instead of `Alt` on macOS)

`{number}` is `0` through `9`, so there are ten slots.

> **The overlay starts off.** QuickMarks itself is on, so the keys work from the
> start, but nothing is drawn on the network editor until you switch on **Mark
> List** or **Pins**, or press `Alt+Shift+M` for both. The shortcuts overlap keys
> a lot of people already use; switch **Active** off if they get in your way.

The marks are stored on the component itself, which means they are saved **in
your project file** and are waiting for you the next time you open it. They are
per-project by design: a mark points at a network path, and the same path means
something different in a different `.toe`. Turning **Active** off later hides the
shortcuts and keeps the marks; nothing is thrown away.

## On the network editor

Switch it on and your marks show on the network editor itself.

- **The mark list** sits in a corner: each mark by number and name, with the
  one for the network you are in highlighted. Click a row to jump to that mark,
  the same as `Ctrl+{number}`, and right-click it to rename the mark. A mark
  whose network no longer exists reads *missing* and is dimmed. The arrow at
  the right of the title row folds the list to that row (**Mark List
  Collapsed** does the same). **Mark List** switches it on or off, **List
  Corner** picks the corner (top left unless you change it), **List Margin**
  sets how far it sits from the edges, in screen points, and **List Order**
  its place among other tools' lists in that corner. With Cook Bar's Top List
  in the same corner, the mark list sits under it unless you change the order.
  The **Overlay** tab of [FNS_Hub](/docs/fns-hub/) sets these too.
- **Outlines** show what each mark saved: the area that was on screen when you
  stored it, with its number and name in the corner, in the network you are
  viewing. **Pins** switches them on or off. Marks stored before outlines
  existed use the size of your network editor.

To hide both at once, press `Alt+Shift+M` (`Option+Shift+M` on macOS) or run
**Toggle QuickMarks overlay** from quick-launch; do it again to bring them
back. Your marks and `Ctrl+{number}` keep working while they are hidden. The
hotkey is the **Overlay Hotkey** parameter; change it there or in the Hotkey
Manager.
