---
package: FNS_ExprHotStrings
summary: Type a short abbreviation into a parameter's expression and it expands into the full text.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Wrapping a name in op()
    anchor: wrapping-a-name-in-op
  - name: Reaching the parent shortcut
    anchor: reaching-the-parent-shortcut
  - name: Promoting a parameter as you type
    anchor: promoting-a-parameter-as-you-type
video: 'https://www.youtube.com/watch?v=j43gZ0MB2xo'
feature_list:
  - name: Abbreviation table
    anchor: how-to-use-it
    does: 'A table of abbreviations and what they expand to, so `#AT` typed as an expression becomes `absTime.seconds`.'
  - name: Inline expansion
    anchor: how-to-use-it
    does: 'With Replace inline on, abbreviations also expand in the middle of an expression and can be combined, as in `#AT * 0.2`.'
  - name: Externalize the table to a file
    anchor: how-to-use-it
    does: 'With Externalize on, the table is kept in a file, so your abbreviations follow you from project to project.'
  - name: Wrap a name in op()
    anchor: wrapping-a-name-in-op
    does: '`#@noise1.par.amp` becomes `op(''noise1'').par.amp`.'
  - name: Parent shortcut abbreviations
    anchor: reaching-the-parent-shortcut
    does: '`#!` becomes the closest parent shortcut, and `#!!` the same with `.par` after it.'
  - name: Promote a parameter while typing
    anchor: promoting-a-parameter-as-you-type
    does: '`#@!` and `#@~` turn the parameter you are typing in into a custom parameter on its parent, linked by a bind or an expression.'
---

## Why use it

Some expressions you type over and over: `absTime.seconds`, a frame
counter divided by the end frame, the path to a parent's custom parameters.
Each one is a dozen keystrokes and a chance to mistype, every time.

ExprHotStrings gives parameter fields text expansion. Define `#AT` once as
`absTime.seconds`, type `#AT` into any expression, and it is replaced with the
full text. A few built-in abbreviations go further: they wrap an operator name
in `op('...')`, find the nearest parent shortcut, or promote the parameter you
are editing to its parent.

## How to use it

1. Open the abbreviation table: the **ExprHotStrings** tab in
   [FNS_Hub](/docs/fns-hub/), **Edit Table** on the component, or **Open
   hot-strings editor** from quick-launch.
2. Add a row. The first column is what you type, the second is what it
   expands to. Start every abbreviation with a character you would not type
   otherwise, such as `#`, so it never fires by accident.
3. Type the abbreviation into a parameter's expression and press `Enter`
   with the mouse still over the parameter. It expands in place.

The mouse position matters. Because of what the TouchDesigner API makes
available, the mouse has to be over the parameter when you finish typing.
Pressing `Enter` is the easy way; if you click away instead, move the mouse
back over the parameter.

By default an abbreviation expands only when it is the whole expression.
Switch on **Replace inline** and it expands anywhere inside one, so
`#AT * 0.2` works and several abbreviations can share an expression.
Expansion works in bind expressions too.

With **Externalize** on, the table is kept in a file in the toolkit's
folder: the same abbreviations follow you from project to project, and you
can edit the file outside TouchDesigner or keep it in version control.

There is also a [video breakdown](https://www.youtube.com/watch?v=j43gZ0MB2xo)
on YouTube.

## Wrapping a name in op()

`#@` wraps whatever follows it in `op('...')`. `#@noise1.par.amp` becomes
`op('noise1').par.amp`, which saves the quotes and brackets every time you
reach for another operator. It is off by default; switch on **#@op Wrap
Enable** to use it.

## Reaching the parent shortcut

`#!` resolves to the closest parent shortcut above the operator you are
editing, and `#!!` adds `.par` after it. With a component whose shortcut is
`Project` somewhere above:

- `#!.par.Something` becomes `parent.Project.par.Something`
- `#!!Something` becomes `parent.Project.par.Something`

If no component above has a shortcut, you get `parent()`. Both are off by
default; switch on **#! Parent Shortcut Enable** to use them.

It is one more reason to give your components parent shortcuts, which you
can add by `Ctrl+Shift`-clicking the diamond button.

## Promoting a parameter as you type

Two abbreviations turn the parameter you are typing in into a custom
parameter on its parent component, through
[CustomParTools](/docs/fns-custompartools/), and replace themselves with the
shortcut path to it:

- `#@!` promotes it with a **Bind** reference.
- `#@~` promotes it with an **Expression** reference.

Leave off a name and the new parameter takes the name of the one you are
typing in; add one to choose it, as in `#@!MyName`. Both are on by default.
They need CustomParTools installed; without it the text stays as you typed
it.
