---
package: TDXMap
summary: 'MIDI controller mapping with a live web UI: multiple devices, banks, Smart Learn, button actions, 14-bit controls. Its own product with its own licence, a 14-day trial then Base or Pro, installable from the picker.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Updates and licensing
    anchor: updates-and-licensing
feature_list:
  - name: MIDI mapping by drag and drop
    anchor: why-use-it
    does: 'Drag a parameter onto a knob, fader or button in a web UI served from inside your project to map that MIDI control to it.'
  - name: Controller banks per device
    anchor: why-use-it
    does: Switch banks independently on each MIDI device you map.
  - name: Learn controls with Smart Learn
    anchor: why-use-it
    does: Smart Learn works out what the hardware sends.
  - name: Button actions
    anchor: why-use-it
    does: Maps buttons to actions as well as continuous controls.
  - name: Read 14-bit controls
    anchor: why-use-it
    does: 'Reads 14-bit controls, for controllers that send them.'
  - name: Install from the toolkit picker
    anchor: how-to-use-it
    does: 'Lands at the network root, where `op.TDXMap` resolves from anywhere, and keeps working with the toolkit removed.'
  - name: Update in place
    anchor: updates-and-licensing
    does: 'Checks for updates from its own preferences footer and reloads the new build in place.'
  - name: Smoothing, pickup and easing in Pro
    anchor: updates-and-licensing
    does: 'Pro adds smoothing, pickup mode, easing curves, slot and modify modes.'
  - name: Mappings outlive the trial
    anchor: updates-and-licensing
    does: 'Without a licence, live MIDI to parameters keeps working and your mappings are kept.'
---

## Why use it

Driving TouchDesigner from a MIDI controller usually means a MIDI In CHOP,
picking out the channels you need, and an export or expression on every
parameter you want to move. That holds up for a fixed setup. It gets tedious
the moment you change your mind about which knob does what, or plug in a
second controller.

TDXMap maps MIDI controllers to TouchDesigner parameters through a web UI
served from inside your project: drag a parameter onto a knob, fader or
button, switch banks per device, and let Smart Learn work out what the
hardware sends. It handles several devices at once, maps buttons to actions
as well as continuous controls, and reads 14-bit controls. The full manual,
guides and changelog live on its own site:
[tdxmap.functionstore.xyz](https://tdxmap.functionstore.xyz).

TDXMap is a **family product** with its own releases. The toolkit mirrors its
released build so you can install it from the same picker as everything else.
The tool itself, its updates and its licensing are its own.

## How to use it

1. Tick **TDXMap** in the installer picker. Select all and the presets leave
   it out, so it only arrives when you pick it. Its card also offers *place in
   this project only*, which installs it here without making it part of the
   setup your next project starts from.
2. It lands at your network root, beside the toolkit container, so
   `op.TDXMap` resolves from anywhere in the project, the address its own
   documentation assumes.
3. From there, TDXMap's [documentation](https://tdxmap.functionstore.xyz/docs/)
   takes you through mapping your first control.

Once installed, it does not depend on any toolkit registry and works with the
toolkit removed. It needs TouchDesigner 2023.12120 or later.

## Updates and licensing

TDXMap keeps itself current. The toolkit's Updates view lists it as
**updates itself** and never touches it: check for updates from the TDXMap
preferences footer, which downloads the new build and reloads it in place.

TDXMap is not free. A 14-day trial of Pro runs once
per computer; after it the mapping editor needs a Function Store Patreon
membership at the Base or Pro tier, or a Gumroad lifetime key. Live MIDI to
parameters keeps working without one, and your mappings are kept. Pro adds
smoothing, pickup mode, easing curves, slot and modify modes. See
[licensing](https://tdxmap.functionstore.xyz/license/) on the product site.
