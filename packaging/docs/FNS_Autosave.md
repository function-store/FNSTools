---
package: FNS_Autosave
summary: Save the project on a timer, without touching the timeline or interrupting a show
features:
  - name: Saving on an interval
    anchor: saving-on-an-interval
  - name: Staying out of the way
    anchor: staying-out-of-the-way
  - name: The main menu button
    anchor: the-main-menu-button
feature_list:
  - name: Timed saves
    anchor: saving-on-an-interval
    does: 'A Timer CHOP saves the project at your interval, independent of the timeline, so it works whether or not the project is playing.'
  - name: TD save mode
    anchor: saving-on-an-interval
    does: 'TD mode uses TouchDesigner''s own Save, honouring your Increment Filename and Copy to Backup Folder preferences.'
  - name: Overwrite mode
    anchor: saving-on-an-interval
    does: 'Overwrite holds the increment preference off during the save, so every save lands in the file you already have open.'
  - name: Skip unchanged projects
    anchor: staying-out-of-the-way
    does: 'Only if modified skips the save when nothing has changed, so an idle project is not rewritten.'
  - name: Skip while performing
    anchor: staying-out-of-the-way
    does: Skip while performing suppresses saves in Perform Mode.
  - name: Wait for mouse rest
    anchor: staying-out-of-the-way
    does: 'Wait For Mouse Rest holds a due save until the mouse has been still for a few seconds, so the save never interrupts a drag.'
  - name: Save status
    anchor: staying-out-of-the-way
    does: A status line shows when the last save happened and when the next one is due.
  - name: Main menu toggle
    anchor: the-main-menu-button
    does: 'A button after the project name in the main menu shows whether autosave is on, toggles it on click and opens its parameters on right-click.'
---

## Saving on an interval

Set an interval and leave it on. The save is driven by a Timer CHOP, independent of the timeline, so it does not depend on the project playing
and does not move anything you are working with.

Two modes, because people mean different things by "save":

- **TD** uses TouchDesigner's own Save, honouring your *Increment
  Filename when Saving* and *Copy to Backup Folder* preferences, so if
  you like numbered saves, you keep getting them.
- **Overwrite** holds that increment preference off for the duration of
  the save, so every save lands back in the file you already have open,
  however the preference is set.

## Staying out of the way

**Only if modified** skips the save when nothing has changed, so an idle
project is not rewritten every few minutes. **Skip while performing**
suppresses saves in Perform Mode, because the middle of a show is the
worst possible moment for a disk write.

A save stalls TouchDesigner for as long as the file takes to write, which
is easy to feel in the middle of a drag. **Wait For Mouse Rest** holds a
save that is due until the mouse has not moved, clicked or scrolled for
**Mouse Rest** seconds (5 by default), then saves. While it waits the
status line says so. Between saves it costs nothing: the mouse is only
watched while a save is waiting, a few times a second.

Nothing is saved until you turn it on: it arrives inactive, and the
status line tells you when the last save happened and when the next one
is due.

## The main menu button

A small button sits in TouchDesigner's main menu, right after the project
name. It looks like the toolbar's buttons: lit, with circling arrows, while
autosave is on, and dark, with crossed-out arrows, while it is off. Click
it to switch; right-click opens Autosave's parameters. Like any main menu
entry it can be moved or hidden from the Hub's Main Menu tab.
