---
package: FNS_BorderlessTD
summary: 'Hide the window''s title bar and the timeline for a cleaner TouchDesigner, on a key each.'
features:
  - name: BorderlessTD
    anchor: borderlesstd
hotkeys:
  - keys: F7
    does: Show or hide the window's title bar (Windows only)
  - keys: alt.F7
    does: Show or hide the timeline
# Bound on the tool's keyboardin through a list expression, which
# HotkeyManager cannot discover; see the "fixed key" sentence below.
fixed_keys:
  - Shift+Esc
feature_list:
  - name: Hide the title bar
    anchor: borderlesstd
    does: Shows and hides TouchDesigner's window title bar.
    platform: Windows only
  - name: Hide the timeline
    anchor: borderlesstd
    does: Shows and hides the timeline.
  - name: Escape key for the title bar
    anchor: borderlesstd
    does: Shift+Esc puts the title bar back; the Use Shift-Esc to undo toggle turns this fixed key off once you no longer need it.
  - name: Borderless on start
    anchor: borderlesstd
    does: 'On Start goes borderless as the project opens with no key press, and State on Startup decides whether the timeline starts hidden.'
  - name: Full screen control
    anchor: borderlesstd
    does: Fix Fullscreen On Start re-asserts full screen after opening; turning off Force Full Screen lets TouchDesigner run borderless in a smaller window.
  - name: Hide menu buttons
    anchor: borderlesstd
    does: 'Removes the Wiki, Forum and Tutorials links from the main-menu bar.'
  - name: Project name in the menu bar
    anchor: borderlesstd
    does: 'Shows the project file''s name in the main-menu bar, where the hidden title bar would normally carry it.'
  - name: Pause indicator
    anchor: borderlesstd
    does: 'While playback is paused, recolours a chosen TouchDesigner UI colour element to Pause State Color, standing in for the hidden timeline''s indicator.'
---

## BorderlessTD

For a cleaner TouchDesigner look. More screen space is better!

- `F7` shows and hides the window's **title bar** (**Windows only**).
- `Alt+F7` (`Opt+F7` on macOS) shows and hides the **timeline**.
- `Shift+Esc` puts the title bar back. It is a fixed key, and the **Use Shift-Esc to undo** toggle turns it off once
  you no longer need the escape hatch.

The two features have an **Enable** toggle each; both ship switched on. With
one off, its shortcut does nothing and TouchDesigner's window or timeline is
left exactly as it was.

What happens when a project opens is set on the component too: **On Start**
goes borderless immediately, with no key press needed, and the
timeline's **State on Startup** decides whether it starts hidden.

- **Fix Fullscreen On Start** re-asserts full screen shortly after the project
  opens, because TouchDesigner does not reliably come back full screen on
  its own. Ships on.
- **Force Full Screen (always)** keeps the window full screen whenever it is
  borderless. Ships on; turn it off to run TouchDesigner borderless inside a
  smaller window, in a fancy zone for example.
- **Hide Menu Buttons** removes the Wiki, Forum and Tutorials links from the
  main-menu bar.
- **Show Project Name** displays the project file's name in the menu bar,
  handy once the title bar that normally carries it is gone. It is what
  BorderlessTD contributes to the main menu.

With the timeline hidden you lose its pause indicator, so the tool provides a
substitute: **Pause Indicator** names a TouchDesigner UI colour element that is
recoloured to **Pause State Color** while playback is paused, and restored on
play.
