---
package: FNS_ParentHierarchy
summary: Hover a parent in the pane-bar path with Alt to see its shortcuts, internal operators and parameters, and click any of them to copy a reference.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Browsing extensions
    anchor: browsing-extensions
feature_list:
  - name: Shortcuts on Alt-hover
    anchor: how-to-use-it
    does: 'Hold `Alt` over a COMP in the pane-bar path to see its parent shortcut, global shortcut and internal operators.'
  - name: Parameter values on Ctrl-hover
    anchor: how-to-use-it
    does: 'Hold `Ctrl` to see where each iop points and every custom parameter with its value; press `Ctrl` again to poll the values.'
  - name: Copy a reference with a click
    anchor: how-to-use-it
    does: 'Clicking any listed item copies a reference to it, ready to paste into an expression or script.'
  - name: Open parameter customisation
    anchor: how-to-use-it
    does: Right-clicking a listed parameter opens the parameter customisation window for it.
  - name: Hover the existing path bar
    anchor: how-to-use-it
    does: 'Works on the path the pane bar already shows, so the bar keeps its buttons and its length.'
  - name: iopBrowser integration
    anchor: how-to-use-it
    does: 'With iopBrowser installed, the same hover also lists the internal operators in its browser.'
  - name: Extension API on hover
    anchor: browsing-extensions
    does: 'Each COMP lists its extensions by Extension Name or class; hovering one expands its promoted methods with signatures, properties and typed attributes.'
    authors: true
  - name: Copy extension calls
    anchor: browsing-extensions
    does: 'Clicking an extension or member copies an ext. reference, such as `ext.TimelineToolsExt.AcceptsDrop(items)`, with the signature intact.'
    authors: true
---

## Why use it

Expressions and scripts in TouchDesigner lean on shortcuts: `parent.Scene`,
`op.Audio`, `iop.Lut`, `parent.Scene.par.Speed`. To write one you need to know
what exists above you: which parent carries which shortcut, which internal
operators it publishes, what its custom parameters are called. Finding out
means clicking up the path bar and opening the parameters of each COMP in turn.

ParentHierarchy answers on the path bar you already have. Hover a COMP in the
path with a modifier held and it lists what that COMP offers; click an entry and
a reference to it is on your clipboard.

## How to use it

- **Shortcuts:** hover an element of the path in the pane bar while holding
  `Alt`. The list shows the **Parent Shortcut** (`P`), **Global Shortcut** (`G`)
  and **Internal Operators** (`iop`) of that COMP only.
- **Parameters:** hold `Ctrl` and the list also shows the relative path of each
  `iop` target, plus every custom parameter with its value. Press `Ctrl` again
  to poll the values.
- **Copy a reference:** click any item to copy a reference to it, then paste it
  into an expression or a script.
- **Customise a parameter:** right-click a parameter in the list to open the
  parameter customisation window for it.

![The ParentHierarchy hover list over a COMP in the path bar](/docs/assets/icons/ParentHierarchy.png)

ParentHierarchy works from the path already shown in the pane bar, so the bar
keeps its existing buttons and stays exactly as long as it was.

With [iopBrowser](/docs/fns-iopbrowser/) installed, the same hover also lists
the internal operators in its browser. Without it the hover works exactly as
described above, it simply does not reach the browser.

The **Navbar** tab of [Hub](/docs/fns-hub/) (the **FNS** button in the
main-menu bar) manages what else lives on the pane bar: reorder items, flip an
item between the left and right side, show or hide it, and drop any panel COMP
on the FNS button to register it as its own self-installing navbar package.

## Browsing extensions

Each COMP in the hover list also shows its extensions, as `E1:`, `E2:` and so
on. The label is the **Extension Name** parameter when one is set, because that
is what `.ext.<Name>` resolves by, and it is often different from the class.
With no name set you get the class name, which is the only thing left to call it
by.

**Hover an extension row and it expands**, listing the API TouchDesigner
promotes to the COMP: methods with their signature, properties, and attributes
with their type. Move off the row and it folds away again.

Capitalized class constants are left out. TouchDesigner promotes those too, but
they are a tool's own bookkeeping, and listing them buries the methods you came
for. The same goes for the accessors CustomParHelper generates for each
parameter: on a tool with forty parameters, those rows would be all you see.

Clicking copies a reference you can paste straight into an expression or a
script: an extension row gives `ext.TimelineToolsExt`, and a member gives
`ext.TimelineToolsExt.AcceptsDrop(items)` with the signature intact.

The `ext.` form works whether or not the COMP sets an Extension Name, because
TouchDesigner registers an extension under that name when there is one and under
its class name when there is not, which is exactly what the row is labelled
with.

Members are read off the class and the instance dictionary, never by fetching
each attribute, so listing an extension cannot trigger a capitalized property and
run somebody else's code as a side effect of hovering.
