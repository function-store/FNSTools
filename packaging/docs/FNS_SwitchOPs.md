---
package: FNS_SwitchOPs
summary: Press Ctrl+Tab to jump back and forth between the last two operators you selected.
features:
  - name: SwitchOPs
    anchor: switchops
feature_list:
  - name: Toggle between last two operators
    anchor: switchops
    does: 'Jumps focus back to the operator you were on before this one, and back again on the next press.'
  - name: Jump back across networks
    anchor: switchops
    does: 'Remembers the last two selected operators wherever they are, so after diving into a component you return without retracing the path.'
---

## SwitchOPs

`Ctrl+Tab` (`Alt+Tab` on macOS, since the system owns Cmd+Tab) jumps focus back
to the operator you were on before this one. Press it again and you are back.
It is Alt+Tab for your network.

The pair it remembers is the **last two operators you selected**, so it works
across networks: dive into a component to change something, hit the shortcut,
and you are back where you were without retracing the path.

Configuration is one hotkey and an **Active** toggle. Rebind
the key from its own parameter or from
[HotkeyManager](/docs/fns-hotkeymanager/), like every other shortcut in the
toolkit.
