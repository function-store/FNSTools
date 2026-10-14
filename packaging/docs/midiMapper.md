---
package: midiMapper
summary: Simple MIDI mapping tool by AlphaMoonbase.berlin.
features:
  - name: midiMapper
    anchor: midimapper
  - name: ResetMIDIPls
    anchor: resetmidipls
  - name: Mapper
    anchor: mapper
    icon: Mapper.png
feature_list:
  - name: Drag-and-drop MIDI learn
    anchor: midimapper
    does: 'Drop parameters onto the UI, learn, and move a fader or knob to assign it; each mapping''s min/max range can be changed.'
  - name: Reset a stuck MIDI device
    anchor: resetmidipls
    does: ResetMIDIPls bypasses and un-bypasses MIDI operators to unstick them; a button in midiMapper resets the selected Device ID.
  - name: Reset all from the toolbar
    anchor: resetmidipls
    does: Middle-click the midiMapper toolbar button to reset all MIDI operators.
  - name: Auto-reset on startup
    anchor: resetmidipls
    does: Can reset all MIDI operators automatically on startup.
  - name: Settings across projects
    anchor: resetmidipls
    does: Its settings persist and follow you across projects through ConfigRegistry; the Registry page controls whether it participates.
  - name: Learn by toolbar drop
    anchor: mapper
    does: 'Drop a parameter on the Mapper toolbar button to auto-learn MIDI, or Alt+drop it to auto-learn OSC, then move a knob.'
  - name: Open MIDI or OSC Mapper
    anchor: mapper
    does: 'Left-click the Mapper button for the MIDI Mapper, Alt+left-click for the OSC Mapper, and Alt+right-click for their settings.'
---

## midiMapper

Simple MIDI mapping tool by AlphaMoonbase.berlin. Drag and drop parameters onto the UI, learn, and move a fader/knob to assign. You can also modify the min/max range.
Right click on the folder tab to configure.

## ResetMIDIPls

Bypass and un-bypass MIDI operators to unstick them (requested by Jacopo)  
   - Built into `midiMapper` and its button on the toolbar  
   - 🎛️ In `midiMapper`, a **new button** resets the selected `Device ID`  
   - 🖱️ **Middle-click** the `midiMapper` toolbar button to reset **all**  
   - Can be set to **auto-reset all on startup**  

Its settings persist and follow you across projects through [ConfigRegistry](/docs/fns-configregistry/), like every other tool; the `Registry` page on the component controls whether it participates.

## Mapper

Allows quick MIDI/OSC Mapping by **DragDropping** a **Parameter** onto this button, using Galileo [MIDI](/docs/midimapper/#midimapper)/[OSC](/docs/oscmapper/#oscmapper) Mapper. 

* **LeftClick:** MIDI Mapper
* **Alt(/Cmd)+LeftClick:** OSC Mapper
* **Alt(/Cmd)+RightClick:** (OSC)MIDI Mapper Settings
* **DragDrop par:** auto-learn MIDI
* **Alt(/Cmd)+DragDrop par:** auto-learn OSC

**Move knob to auto-learn.**
