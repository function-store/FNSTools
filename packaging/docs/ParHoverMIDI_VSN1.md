---
package: ParHoverMIDI_VSN1
summary: 'Adjust any parameter by hovering over it and turning an endless MIDI encoder, built for the Intech Studio VSN1 with screen and LED feedback: slots and banks, ParGroup control, step sizes, shortcuts, and network zoom when nothing is under the mouse.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Before you install
    anchor: before-you-install
  - name: Updates
    anchor: updates
feature_list:
  - name: Hover and turn to adjust
    anchor: how-to-use-it
    does: 'Hover the mouse over any parameter and turn an endless relative MIDI encoder to change it; any such encoder works for this, the VSN1 included.'
  - name: Screen and LED feedback
    anchor: why-use-it
    does: The VSN1's screen shows the parameter under the mouse and its LEDs show state.
  - name: Step size switching
    anchor: how-to-use-it
    does: The buttons under the VSN1 screen switch the step size the encoders use.
  - name: Save a parameter to a slot
    anchor: how-to-use-it
    does: Long-press a primary button to save the hovered parameter to a slot.
  - name: Recall slots across banks
    anchor: how-to-use-it
    does: 'Saved parameters come back instantly across banks, without hunting for them again; long-press the step buttons to switch banks.'
  - name: 'Reset, default and clamp shortcuts'
    anchor: how-to-use-it
    does: 'Device buttons run shortcuts for reset, default and clamp on the hovered parameter.'
  - name: ParGroup control
    anchor: how-to-use-it
    does: Parameter groups such as RGB or XYZ turn as one; this needs TouchDesigner 2025.
  - name: Zoom and pan the network
    anchor: how-to-use-it
    does: 'With no parameter under the mouse, the encoders zoom and pan the network editor.'
  - name: Show custom parameter help
    anchor: how-to-use-it
    does: Holding Alt over any custom parameter of the component shows its help.
  - name: Update in place from GitHub
    anchor: updates
    does: 'Checks its GitHub releases from its About page and updates in place, keeping your slot data when you externalize the component first.'
---

## Why use it

Fine-tuning a parameter with the mouse means dragging a slider and watching
the value jump further than you meant. A MIDI controller fixes that for the
parameters you mapped to it, but every mapping is set up by hand, and the
moment you want to nudge something else you are back on the mouse.

ParHoverMIDI_VSN1 works the other way round: hover the mouse over a
parameter, turn an encoder, and the parameter follows. There is no
per-parameter mapping to set up. It is a hardware integration for the Intech
Studio VSN1: the device's screen shows the parameter under the mouse, its LEDs
show state, and its buttons switch step size, recall saved parameters and run
reset, default and clamp. Any endless relative MIDI encoder works for the
hovering itself; the screen and LED feedback are VSN1 features.

## How to use it

Read [Before you install](#before-you-install) first: it needs the hardware
and a few things set up outside TouchDesigner.

1. Tick ParHoverMIDI_VSN1 in the installer picker. Its card also offers
   *place in this project only*, which installs it here without making it
   part of the setup your next project starts from.
2. Install the `TouchDesigner Par Hover Control` package in Grid Editor
   (Package Manager on recent versions) and import its configuration to the
   VSN1.
3. In TouchDesigner's MIDI Device Mapper, set the VSN1 (Intech Grid MIDI
   Device) as input and output, and note the Grid device ID.
4. Enter that ID on the component's VSN1 / UI parameter page.
5. Hover a parameter and turn an encoder.

Once that works, the rest is on the device:

- The buttons under the screen switch the step size the encoders use.
- Long-press a primary button to save the hovered parameter to a slot, for
  instant recall across banks without hunting for it again. Long-press the
  step buttons to switch banks.
- The device buttons also run reset, default and clamp on the hovered
  parameter.
- Parameter groups such as RGB or XYZ turn as one. This needs TouchDesigner
  2025.
- With no parameter under the mouse, the encoders zoom and pan the network
  editor.
- Hold `Alt` (`Option` on macOS) over any custom parameter of the component
  to see its help.

The full documentation, including other controllers and the recovery system,
is on [the component's own site](https://function-store.github.io/TD_ParHoverMIDI_VSN1/).

## Before you install

- It lands at the network root, one instance per project, and only one
  project at a time can have it open, because the Grid connection is
  exclusive.
- It is never part of Select all, the Everything preset or a recommended set.
  Pick it yourself when you have the hardware.
- Requirements: TouchDesigner 2023.12120 or later (2025 for ParGroup control),
  a USB MIDI connection, and for the VSN1 the Grid Editor open with exclusive
  access to port 9642.

## Updates

ParHoverMIDI_VSN1 is a foreign package: its releases come from its own
repository, and its built-in updater keeps it current from there. The store
places it; the component governs itself afterwards.

The component's About page checks GitHub releases and updates itself in
place. Press Externalize Component there before updating to keep your slot
data across the update. The FNS updater reports it as self-managed and does
not replace it. Release notes are on
[GitHub](https://github.com/function-store/TD_ParHoverMIDI_VSN1/releases).
