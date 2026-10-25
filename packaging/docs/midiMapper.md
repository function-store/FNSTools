---
package: midiMapper
summary: Simple MIDI mapping tool by AlphaMoonbase.berlin.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Mapping from the toolbar
    anchor: mapping-from-the-toolbar
    icon: Mapper.png
  - name: Unsticking a device (ResetMIDIPls)
    anchor: unsticking-a-device-resetmidipls
feature_list:
  - name: Drag-and-drop MIDI learn
    anchor: how-to-use-it
    does: 'Drop parameters onto the mapper, switch on Learn and move a fader or knob to assign it.'
  - name: Range per mapping
    anchor: how-to-use-it
    does: 'Each mapping has its own min and max, so a full fader sweep can cover just part of a parameter.'
  - name: Learn from the toolbar
    anchor: mapping-from-the-toolbar
    does: 'Drop a parameter on the toolbar button and move a knob to map it, without opening the mapper.'
  - name: Open the mapper from the toolbar
    anchor: mapping-from-the-toolbar
    does: 'Click the toolbar button to open the MIDI Mapper, or right-click it for the mapper''s settings.'
  - name: Settings across projects
    anchor: how-to-use-it
    does: 'The tool''s settings follow you across projects through ConfigRegistry, while the mappings stay with the project.'
  - name: Reset a stuck MIDI device
    anchor: unsticking-a-device-resetmidipls
    does: 'ResetMIDIPls bypasses and un-bypasses MIDI operators to unstick them, for one device or all of them.'
  - name: Reset all from the toolbar
    anchor: unsticking-a-device-resetmidipls
    does: Middle-click the midiMapper toolbar button to reset all MIDI operators.
  - name: Auto-reset on startup
    anchor: unsticking-a-device-resetmidipls
    does: Can reset all MIDI operators automatically on startup.
---

## Why use it

Putting a MIDI controller on a parameter by hand means a MIDI In CHOP,
finding which channel your fader sends, a Select and a Math CHOP to bring it
into the right range, and an export or expression onto the parameter. Fine
once; slow when you want twenty knobs on twenty parameters during a
rehearsal.

midiMapper, a simple MIDI mapping tool by
[AlphaMoonbase.berlin](https://alphamoonbase.de/), does the learning for you:
drop the parameters you want to control, move the controls, and they are
mapped, each with its own range.

## How to use it

1. Open the **midiMapper** tab in [FNS_Hub](/docs/fns-hub/). Right-click the
   tab to configure the tool.
2. Drag the parameters you want to control onto the mapper. Each one becomes
   a row waiting to learn.
3. Switch on **Learn** and move a fader or knob. While Learn is on, the next
   control you move is assigned to every row still waiting, so drop one
   parameter at a time, or several to put them all on one knob. Switch
   **Learn** off when you are done.
4. Set each mapping's min and max to choose the part of the parameter's range
   the control covers. The controller's 0 to 127 is spread across it.

- **To edit mappings by hand,** **Edit Midimap DAT** opens the table, one row
  per mapping. **Clear** deletes every mapping.
- **To keep mappings somewhere else,** a shared component for instance, point
  **Mappingtable** on the Repositorie page at another table, or press
  **Create** to make one.

The tool's settings persist and follow you across projects through
[ConfigRegistry](/docs/fns-configregistry/), like every other tool; the
`Registry` page on the component controls whether it participates. The
mappings stay with the project.

## Mapping from the toolbar

midiMapper also puts a button on the toolbar, a shortcut into the Galileo
MIDI Mapper, so you can map a parameter without opening anything:

- **Drop a parameter** on the button and move a knob: the parameter is
  learned and mapped.
- **Click** it to open the MIDI Mapper.
- **Right-click** it for the mapper's settings.
- **Middle-click** it to reset all MIDI operators (see below).

For OSC controllers, use [oscMapper](/docs/oscmapper/).

## Unsticking a device (ResetMIDIPls)

A MIDI device sometimes stops responding until its operators are switched
off and on again. ResetMIDIPls, built into midiMapper and requested by
Jacopo, does that for you: it bypasses every MIDI In CHOP, MIDI Out CHOP and
MIDI In DAT in the project, waits a moment, and un-bypasses them.

- In midiMapper, the Reset button resets only the device set in **Device
  ID**.
- Middle-click the midiMapper button on the toolbar, or pulse **Reset All
  Midi**, to reset all of them.
- It can be set to reset all of them automatically on startup.
- If a device needs longer to let go of its port, raise **Reset Delay (Ms)**.
