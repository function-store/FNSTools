---
package: FNS_ExprHotStrings
summary: YouTube breakdown
features:
  - name: ExprHotStrings
    anchor: exprhotstrings
video: 'https://www.youtube.com/watch?v=j43gZ0MB2xo'
feature_list:
  - name: Abbreviation table
    anchor: exprhotstrings
    does: 'Abbreviations in the first column expand to the Expands column''s string when used as a parameter expression, for example `#AT` to `absTime.seconds`.'
  - name: Inline expansion
    anchor: exprhotstrings
    does: 'With Replace inline on (off by default), abbreviations expand inside a longer expression and can be combined, as in `#AT * 0.2`.'
  - name: Wrap a path in op()
    anchor: exprhotstrings
    does: '`#@` wraps what follows in `op(''...'')`, so `#@noise1.par.amp` becomes `op(''noise1'').par.amp`; it has its own enable toggle.'
  - name: Parent shortcut abbreviations
    anchor: exprhotstrings
    does: '`#!` resolves to the closest parent shortcut and `#!!` adds `.par` after it, both behind their own enable toggle.'
  - name: Promote a parameter while typing
    anchor: exprhotstrings
    does: '`#@!` (Bind) and `#@~` (Expression) promote the parameter you are typing in to its parent via CustomParTools, using its own name or one you supply.'
---

## ExprHotStrings

[YouTube breakdown](https://www.youtube.com/watch?v=j43gZ0MB2xo)

Define `Abbreviations` in the first column that when used in a parameter expression will expand to the string defined in the `Expands` column.
Type `#AT` for `absTime.seconds`! With `Replace inline` enabled on the component (off by default; without it an abbreviation only expands when it is the *entire* expression) the abbreviations work in-line too, meaning you can type `#AT * 0.2` or even combine them!

> Most of the behaviors below live behind their own toggle on the component, and only `CustomPar Promote Enable` is on by default: `#@op Wrap Enable` gates `#@`, `#! Parent Shortcut Enable` gates `#!`/`#!!`.

There is a special reserved abbreviation, `#@` which will wrap anything valid after it in `op('...')`. So `#@noise1.par.amp` becomes `op('noise1').par.amp` saving you some heavy keystrokes!

Another special abbreviation `#!` will resolve to the closest parent shortcut, as well as `#!!` will also add a .par after it!

   - #!.par.Something -> parent.Project.par.Something (for example)
   - #!!Something -> parent.Project.par.Something (for example)
   - Encouraging even more to use parent shortcuts (which you can easily add by `ctrl+shift-clicking` on the diamond button

Two more abbreviations promote the parameter you're typing in straight to its parent (via [CustomParTools](/docs/fns-custompartools/#custompar-tools), if installed) and replace themselves with the resulting shortcut path:
   - `#@!` promotes with a **Bind** reference
   - `#@~` promotes with an **Expression** reference
   - Leave off a name to reuse the parameter's own name, or supply one, e.g. `#@!MyName`

> **IMPORTANT**: due to what's available through the TD API, you need to have your mouse over the parameter box when finishing typing (either by clicking away, in which case you need to move the mouse over to the parameter again, or my suggested way of hitting `Enter`).
