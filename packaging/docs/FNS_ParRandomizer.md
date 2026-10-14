---
package: FNS_ParRandomizer
summary: Randomize an operator's parameters by click, drag-drop or hotkey.
features:
  - name: ParRandomizer
    anchor: parrandomizer
    icon: Random.png
feature_list:
  - name: Randomise the selected operator
    anchor: parrandomizer
    does: A click randomises the selected operator's value sliders; Alt+Shift+R does the same from the keyboard.
  - name: Randomise by drag and drop
    anchor: parrandomizer
    does: 'Drop an operator on the tool to randomise it, or drop a single parameter to randomise just that one.'
  - name: Randomise the hovered parameter
    anchor: parrandomizer
    does: Press Alt+R over a parameter to randomise it.
  - name: Reset parameters
    anchor: parrandomizer
    does: 'Ctrl+right-click resets all parameters, Ctrl+Shift+R resets the hovered one, and Ctrl+Shift+Alt+R resets every parameter on its page.'
  - name: Store current values as defaults
    anchor: parrandomizer
    does: Ctrl+Shift+right-click sets the current parameter values as the defaults.
---

## ParRandomizer

* Click to randomize selected OP value sliders.
* You can also DragDrop an OP to randomize it.
* You can DragDrop a parameter to randomize it.
* **Ctrl+RightClick**-> reset all params
* **Ctrl+Shift+RightClick**-> set current params as default

Hotkeys also available:

* Alt(Opt)+Shift+R to randomize selected OP
* Alt(Opt)+R to randomize hovered param
* Ctrl+Shift+R reset hovered param
* Ctrl+Shift+Alt+R reset all params in hovered param's page
