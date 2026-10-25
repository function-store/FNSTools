---
package: FNS_HotkeyManager
summary: 'Every hotkey in the project in one list: spot clashes, rebind by pressing keys, and keep your bindings across projects and updates.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Reading the Status column
    anchor: reading-the-status-column
  - name: Keeping bindings across projects
    anchor: keeping-bindings-across-projects
  - name: Making your hotkeys show up
    anchor: making-your-hotkeys-show-up
feature_list:
  - name: Find every hotkey in the project
    anchor: how-to-use-it
    does: 'Scans the whole project, toolkit tools and your own components alike, for Keyboard In CHOPs and DATs and shortcut parameters, one row per binding.'
  - name: Rebind by pressing keys
    anchor: how-to-use-it
    does: 'Click a Hotkey cell and press the new keys; a combo already in use asks you to press it again to take it.'
  - name: Reset a binding
    anchor: how-to-use-it
    does: Right-click a Hotkey cell to put that binding back to its default.
  - name: Conflict detection
    anchor: reading-the-status-column
    does: 'Combos bound by more than one tool are flagged CONFLICT, and clicking the flag jumps between the rows that share it.'
  - name: Copies listed once
    anchor: reading-the-status-column
    does: 'A component copied around the project is one row, and rebinding it rewrites every copy.'
  - name: Persist bindings across projects
    anchor: keeping-bindings-across-projects
    does: 'Toolkit hotkeys follow you to other projects and through updates, and any other binding can opt in with a tag or a click.'
  - name: Save, load and defaults
    anchor: keeping-bindings-across-projects
    does: 'Save, reload or put back the default bindings, or force the defaults on every load to get a machine back to a known state.'
  - name: Discovery rules for tool authors
    anchor: making-your-hotkeys-show-up
    does: Where to put a binding so it is found and gets a default that survives renames and moves.
    authors: true
---

## Why use it

Every tool you add brings its own keys, and they live wherever its author put
them: on a parameter, or on a Keyboard In CHOP or DAT a few levels down. Two
tools wanting the same key is easy to do and hard to notice. ResetPLS and
QuickMarks both use `Ctrl+0` out of the box, for example. Finding out who owns
a key and changing it means digging through networks, and a key you changed in
one project is back to the old one in the next.

HotkeyManager scans the whole project, toolkit tools and your own components
alike, and lists every binding in one table. Clashes are flagged, a binding is
changed by pressing the new keys, and your bindings follow you to other
projects and through toolkit updates.

## How to use it

1. Open it from the HotkeyManager tab of [Hub](/docs/fns-hub/) (the **FNS**
   button in the main-menu bar), with **Open hotkey UI** in quick-launch, or
   with **Open Hotkey UI** on the component.
2. Each row is one binding: Tool, Path, Par, Hotkey, Default, Persist and
   Status. Tools are listed by name without the `FNS_` prefix.
3. To rebind, click the Hotkey cell and press the new keys. `Esc` cancels. If
   the combo is already used elsewhere, the hint line says who has it; press
   the same keys again to take it anyway.
4. To undo a rebind, right-click the Hotkey cell. That resets the binding to
   its default.
5. A changed binding reads *unsaved* until you save, with the Save button in
   the UI or **Save Hotkeys** on the component.

Good to know:

- A binding with a macOS variant keeps both when you rebind it: the macOS side
  gets the same combo with `Cmd` in place of `Ctrl`.
- Some tools check their own hotkeys and put the old value back when they
  reject one (Embody does this for duplicates). The hint line then says the
  rebind was refused and what the parameter still holds.
- To leave a whole top-level component out of the scan, add its name to
  **Excluded Roots**. TouchDesigner's own `ui`, `sys` and `local` are left out
  by default.

## Reading the Status column

- **CONFLICT** with a combo: the same keys are bound by more than one tool.
  Click the status to jump to the other row with that combo; click again to
  cycle through them if there are more.
- **shared** with a modifier and a list of tools: bindings that are only
  modifiers, such as `alt` held while dragging, never conflict, because the
  mouse half of the gesture keeps them apart. When several tools hold the same
  modifiers, the row says so and is tinted yellow, so it is visible without
  reading as an error.
- **unsaved**: you changed this binding since the last save.

A component copied around a project, such as a helper inside every copy of a
vendored operator, shows as one row, `Name (xN)`. Rebinding, resetting or
switching Persist on that row writes every copy. A copy you rebind by hand no
longer matches the others and gets its own row.

## Keeping bindings across projects

The Persist column says whether a binding travels:

- **always**: toolkit hotkeys. They always persist; you cannot switch that
  off.
- **yes** or **no**: anything outside the toolkit persists only when declared.
  Click the Persist cell to declare it, which tags the row's Keyboard In or
  COMP `FNS_hotkeys`. You can also add that tag yourself, to the operator or
  to a COMP containing it. A binding declared through a parent's tag has to be
  undeclared at that parent.

Declared bindings are saved to your user palette through
[ConfigRegistry](/docs/fns-configregistry/) and restored when a project loads.
Undeclared ones stay in their project, because the same path means a different
operator in every `.toe`. Saved bindings for components that are not in the
current project ride along untouched, so opening project B never erases
project A's bindings.

To go back to what you saved, press **Load Hotkeys** on the component. To put
every discovered binding back to its default for this session, press **Load
Default**. To get a machine back to a known state, switch on **Force
Default**, and saved bindings are ignored on every load until you switch it
off again.

## Making your hotkeys show up

For tool authors. Discovery looks in every top-level component except the
excluded roots, and finds three shapes:

- a Keyboard In CHOP (its `keys` and `modifiers`),
- a Keyboard In DAT (its `keys` and `shortcuts`),
- a custom parameter on a COMP, of style Str, StrMenu or Menu, whose name
  contains `key`, `shortcut` or `hotkey`. A few names are skipped on purpose,
  such as `Opshortcut` and `Parentshortcut`.

It skips a Keyboard In with something in its Panels parameter, since that only
fires while those panels have focus, and a read-only expression that mirrors a
binding held elsewhere.

The shape that works best is a custom parameter on your COMP holding the combo,
with its default authored on the parameter, and the Keyboard In following it by
a plain expression such as `parent().par.Shortcut`. The binding then shows up
once, the user can find it on your Custom page, and resetting it restores your
default even after the component is renamed or moved. A raw Keyboard In's
factory default is empty, so resetting one would unbind it.

Values are combos joined with `.`, several separated by spaces: `ctrl.k
alt.shift.r`. A parameter is stored when it is a constant, a bind, or an
expression that switches on the operating system; any other expression is
invisible to the manager. The OS switch looks like this:

```python
'ctrl.shift.f' if app.osName == 'Windows' else 'cmd.shift.f'
```
