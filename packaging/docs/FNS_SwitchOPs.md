---
package: FNS_SwitchOPs
summary: Press Ctrl+Tab to jump back and forth between the last two operators you selected.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
hotkeys:
  - keys: ctrl.tab
    does: Jump back to the operator you selected before this one; press again to return
feature_list:
  - name: Toggle between the last two operators
    anchor: how-to-use-it
    does: 'Jumps focus back to the operator you were on before this one, and back again on the next press.'
  - name: Jump back across networks
    anchor: how-to-use-it
    does: 'Remembers the last two selected operators wherever they are, so after diving into a component you return without retracing the path.'
  - name: Rebind the key
    anchor: how-to-use-it
    does: 'Rebind it on the tool or in HotkeyManager, like every shortcut in the toolkit.'
---

## Why use it

A lot of edits involve two operators: the one you are changing and the one where
you see the result, or a parameter in one component and the expression that
reads it in another. Clicking between them, through the path bar when they sit
in different networks, is most of the work.

SwitchOPs is Alt+Tab for your network. One key takes you back to the operator
you were on before; the same key brings you back.

## How to use it

- Select an operator, then another. Press `Ctrl+Tab` (`Alt+Tab` on macOS, since
  the system owns `Cmd+Tab`) to go back to the first. Press it again and you are
  back.
- The pair it remembers is the last two operators you selected, so it works
  across networks: dive into a component to change something, press the
  shortcut, and you are back where you were without retracing the path.
- To use another key, rebind **Shortcut** or use
  [HotkeyManager](/docs/fns-hotkeymanager/), like every other shortcut in the
  toolkit.
- To keep the key free for something else, switch off **Active** or run
  **Toggle SwitchOPs** from quick-launch.
