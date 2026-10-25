---
package: FNS_SetSmoothness
summary: Set Input and Viewer Smoothness on TOPs from the toolbar, without opening the Common page.
features:
  - name: Why use it
    anchor: why-use-it
    icon: Set Smoothness.png
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Set smoothness on selected TOPs
    anchor: how-to-use-it
    does: 'Click the toolbar button, pick a filtering mode, and it is written to the Input and Viewer Smoothness of the selected TOPs.'
  - name: Apply to every TOP in the network
    anchor: how-to-use-it
    does: Hold `Alt` while picking to write it to every TOP in the current network.
  - name: Change input and viewer smoothness separately
    anchor: how-to-use-it
    does: 'Set the two values separately on the component and apply them with a pulse or a quick-launch command.'
  - name: Components with their own smoothness
    anchor: how-to-use-it
    does: 'Components that carry their own Input or Viewer Smoothness parameters, such as RealRamp, are set along with the TOPs.'
  - name: Run from quick-launch
    anchor: how-to-use-it
    does: 'Smoothness -> selected and Smoothness -> all apply the settings with no toolbar button needed.'
---

## Why use it

Pixel art, LED maps and anything on a low-resolution grid need
nearest-neighbour filtering, and TouchDesigner defaults to linear. Switching
a dozen TOPs by hand means opening each one's Common page and changing two
menus, again for every TOP you add.

SetSmoothness puts both settings behind one toolbar menu and writes them to
the TOPs you have selected, or to every TOP in the network.

## How to use it

1. Select the TOPs you want to change.
2. Click the SetSmoothness button on the toolbar and pick a filtering mode.
   It is written to both Input Smoothness and Viewer Smoothness on the Common
   page of every selected TOP.
3. To change every TOP in the network you are in, hold `Alt` while you pick.
   The button's own tooltip says so: *"Press ALT to set all in a Comp."*

All the changes from one pick are a single undo step.

The two settings do different jobs. Input Smoothness is how a texture is
sampled as it comes into an operator; Viewer Smoothness is how it is filtered
when drawn on screen. The toolbar menu sets both to the same mode. To give
them different values, set **Input Smoothness** and **Viewer Smoothness** on
the SetSmoothness component, then pulse **Selected** or **All**.

Both actions are also quick-launch commands, **Smoothness -> selected** and
**Smoothness -> all**, so they can be fired from
[CommandKit](/docs/fns-commandkit/) with no toolbar button at all. They use the
two values set on the component.

Components that carry their own Input Smoothness or Viewer Smoothness
parameters, such as [RealRamp](/docs/realramp/) and
[ComplexMix](/docs/complexmix/), are set along with the TOPs.
