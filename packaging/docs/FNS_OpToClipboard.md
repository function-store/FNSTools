---
package: FNS_OpToClipboard
summary: 'Pressing Ctrl(Cmd)+Shift+C will copy the currently selected OP name to the clipboard, so you can easily paste OP references to expressions.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Copying a parameter reference
    anchor: copying-a-parameter-reference
feature_list:
  - name: Copy an operator reference
    anchor: how-to-use-it
    does: '`Ctrl+Shift+C` copies a reference to the selected operator, ready to paste into an expression.'
  - name: Resolve the right path wherever you paste
    anchor: how-to-use-it
    does: 'The pasted reference resolves to the right relative or shortcut path for the operator you paste it into.'
  - name: Copy a parameter reference
    anchor: copying-a-parameter-reference
    does: 'Over a parameter the same shortcut copies that parameter, or the whole group when over the name of a row with several fields.'
  - name: Toggle the tool from quick-launch
    anchor: how-to-use-it
    does: 'Toggle OpToClipboard switches the tool on and off, and Copy op to clipboard does the same as the key.'
---

## Why use it

Referencing another operator in an expression means working out its path
from where the expression lives: `op('../geo1')`, `op('base1/null3')`, or a
parent shortcut. Get one level wrong and the parameter turns red, and the
further apart the two operators sit, the easier that is.

OpToClipboard copies a reference to the selected operator with one key.
Paste it into any expression and it becomes the correct relative or shortcut
path for that spot.

## How to use it

1. Select the operator you want to reference and press `Ctrl+Shift+C`
   (`Cmd+Shift+C` on macOS).
2. Click into the expression of the parameter that needs it, paste, and keep
   typing.

The pasted text has an `@` after it. TouchDesigner does not tell a tool where
you are going to paste, so the final path cannot be written at copy time. The
`@` marks the spot, and it resolves to the full relative or shortcut path to
the copied operator. The mechanism is the same one
[ExprHotStrings](/docs/fns-exprhotstrings/) uses. In practice: ignore the `@`
and keep typing your expression; it resolves in the end.

**Copy op to clipboard** in quick-launch does the same as the key. If the
shortcut gets in the way, change it with **Shortcut**, or switch the tool off
with **Active** or **Toggle OpToClipboard**.

## Copying a parameter reference

Press the same shortcut while the mouse is over a parameter and you copy a
reference to that parameter. Over a single field,
such as `tx`, you get `op('geo1')@.par.tx`. Over the name of a parameter row
with several fields, such as Translate, you get the whole group:
`op('geo1')@.parGroup.t`.

The `@` resolves the same way as for an operator, and the `.par` or
`.parGroup` part stays behind it, so the finished expression reads
`op('geo1').par.tx` (with the path adjusted to wherever the expression
lives).
