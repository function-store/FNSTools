---
package: FNS_ParRandomizer
summary: 'Randomize an operator''s parameters by click, drag-drop or hotkey.'
features:
  - name: Why use it
    anchor: why-use-it
    icon: Random.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Resetting and saving defaults
    anchor: resetting-and-saving-defaults
feature_list:
  - name: Randomize an operator
    anchor: how-to-use-it
    does: 'A click on the toolbar button, or `Alt+Shift+R`, gives every parameter on the selected operator''s open page a random value within its range.'
  - name: Randomize one parameter
    anchor: how-to-use-it
    does: 'Hover a parameter and press `Alt+R`, or drop it on the button, to randomize just that one.'
  - name: Randomize by drag and drop
    anchor: how-to-use-it
    does: Drop an operator on the button to randomize it without selecting it first.
  - name: Expressions left alone
    anchor: how-to-use-it
    does: Parameters driven by an expression or an export keep their value; only constant and bound ones change.
  - name: Reset parameters
    anchor: resetting-and-saving-defaults
    does: '`Ctrl+Shift+R` puts the hovered parameter back to its default; Ctrl+right-click or `Ctrl+Shift+Alt+R` resets the whole page.'
  - name: Store current values as defaults
    anchor: resetting-and-saving-defaults
    does: Ctrl+Shift+right-click makes the current values of the operator's custom parameters their defaults.
---

## Why use it

Some of the best looks come from settings you would never have dialled in on
purpose. Exploring a Noise TOP, a feedback network or a component full of
custom parameters by hand means nudging one slider at a time, and you tend to
stay close to values you already know.

ParRandomizer rolls the dice for you. One click gives the parameters on an
operator's page random values within their ranges. Keep what you like, undo
what you don't, and reset when you want to start over.

## How to use it

- Select an operator and click the ParRandomizer button on the toolbar, or
  press `Alt+Shift+R` (`Opt+Shift+R` on macOS). Every parameter on the page
  that is open in its parameter dialog gets a random value.
- To randomize only one parameter, hover it and press `Alt+R` (`Opt+R`), or
  drag it onto the button.
- To randomize an operator without selecting it, drag the operator onto the
  button.

Sliders get a value within their slider range, or within their clamp limits
when they have them; toggles and menus get a random state. Parameters on the
About, Info and Common pages are skipped, and so are parameters that are
read-only, disabled, or driven by an expression or an export. Randomizing a
whole operator is one undo step, so a result you don't like is one undo away.

Every action is also in quick-launch: **Randomize pars of op**, **Randomize
rollover par**, **Reset custom pars to defaults** and **Save custom
defaults**. The keys are parameters on the component, so you can rebind them
there, and **Active** or **Toggle ParRandomizer** switches the tool off. If
RayTK is installed and one of its shortcuts uses the same key, ParRandomizer
tells you and offers to open both components' parameters so you can change
one.

## Resetting and saving defaults

- **One parameter:** hover it and press `Ctrl+Shift+R` to put it back to its
  default.
- **The whole page:** Ctrl+right-click the button, or press
  `Ctrl+Shift+Alt+R`, to reset every parameter on the selected operator's
  open page.
- **A result worth keeping:** Ctrl+Shift+right-click the button, or run
  **Save custom defaults**, and the current values of the operator's custom
  parameters become their defaults, expressions and binds included. From then
  on a reset brings them back to this state.
