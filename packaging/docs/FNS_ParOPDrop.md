---
package: FNS_ParOPDrop
summary: Use this tool to create Param(Exec) CHOP/DATs inside of COMPs from their Custom Pars.
features:
  - name: Why use it
    anchor: why-use-it
    icon: ParOpDrop.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Execute DATs from a drop
    anchor: execute-dats-from-a-drop
feature_list:
  - name: Parameter CHOP, DAT or Execute DAT by drop
    anchor: how-to-use-it
    does: 'Inside a COMP, drop one of its custom parameters on the toolbar button with modifiers held for a Parameter CHOP, Parameter DAT or Parameter Execute DAT already pointed at it.'
  - name: Hotkeys over parameters
    anchor: how-to-use-it
    does: 'Hover a parameter and press `P` with the same modifiers, no dragging needed.'
  - name: Collect several parameters in one operator
    anchor: how-to-use-it
    does: 'While the operator it made is current, the next parameter you add with the same modifiers joins it.'
  - name: Execute DATs from operator drops
    anchor: execute-dats-from-a-drop
    does: 'Drop a CHOP, one channel or a DAT on the button for a CHOP Execute or DAT Execute DAT already watching it.'
---

## Why use it

A component's own custom parameters are usually what drives the network
inside it: a Parameter CHOP to feed a slider into a chain, a Parameter DAT to
read a menu or a string, a Parameter Execute DAT to run code when a value
changes. Each one means creating the operator, pointing it at the component
and typing the parameter names in.

ParOPDrop does that in one gesture. Drop a custom parameter on its toolbar
button, or press a key over it, and the operator appears inside the
component, already set up for that parameter.

## How to use it

Go inside the COMP whose parameters you want, open its parameters, and drag
one of its custom parameters onto the ParOPDrop button on the toolbar:

* **Ctrl+Alt(Opt)+DragDrop a param:** create Par CHOP in child
* **Ctrl+Shift+DragDrop a param:** create Par DAT
* **Alt(Opt)+Shift+DragDrop:** create ParExec DAT

The same three are on the keyboard. Hover the parameter and press:

* **Ctrl+Alt(Opt)+P over a param:** create Par CHOP in child
* **Ctrl+Shift+P over a param:** create Par DAT
* **Alt(Opt)+Shift+P over a param:** create ParExec DAT

The new operator lands where you are looking in the network, with its viewer
on, and becomes the current operator.

- **To collect several parameters in one operator,** add the next one while
  the operator ParOPDrop just made is still current: the parameter is added to
  it. An existing Parameter CHOP or DAT that already points at the component
  works the same way once you make it current.
- **Hovering one field of a row** such as Translate adds the whole row.
- **To use another letter,** change **Key**.
- **If the modifiers clash with something else,** switch ParOPDrop off with
  **Active** or **Toggle ParOPDrop** in quick-launch.

## Execute DATs from a drop

You can also drop an **operator** on the same button to get its Execute DAT:

* **Drop a CHOP:** creates a CHOP Execute DAT watching every channel (`*`)
* **Drop a single channel:** creates a CHOP Execute DAT watching just that channel
* **Drop a DAT:** creates a DAT Execute DAT watching it

No modifier is needed here. Modifiers on a parameter drop choose between
three possible results; an operator drop has only one, and what you dropped
decides which channel to watch. The new DAT is created in the network you are
looking at, already pointed at its source and with an event turned on (Value
Change for a CHOP, Table Change for a DAT) so it can fire immediately.
