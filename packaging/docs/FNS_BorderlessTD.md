---
package: FNS_BorderlessTD
summary: 'Hide the window''s title bar and the timeline for a cleaner TouchDesigner, on a key each.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Making it yours
    anchor: making-it-yours
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
    anchor: how-to-use-it
    does: Shows and hides TouchDesigner's window title bar on one key.
    platform: Windows only
  - name: Hide the timeline
    anchor: how-to-use-it
    does: Shows and hides the timeline on one key.
  - name: Escape back to the title bar
    anchor: how-to-use-it
    does: '`Shift+Esc` always brings the title bar back, until you switch that safety net off.'
  - name: Start borderless
    anchor: making-it-yours
    does: 'The project can open borderless, with the timeline already hidden.'
  - name: Full screen or windowed
    anchor: making-it-yours
    does: 'Keeps a borderless window full screen, or lets it sit in a smaller window or a window zone.'
  - name: Pause indicator
    anchor: making-it-yours
    does: 'While playback is paused, a part of TouchDesigner''s UI changes colour, standing in for the hidden timeline''s pause cue.'
  - name: Hide the menu bar links
    anchor: making-it-yours
    does: 'Hide Menu Buttons removes the Wiki, Forum and Tutorials links from the menu bar.'
  - name: Show the project name in the menu bar
    anchor: making-it-yours
    does: 'Show Project Name puts the project''s file name in the menu bar, where the hidden title bar used to show it.'
---

## Why use it

Between the operating system's title bar at the top and the timeline at the
bottom, a fair slice of the screen goes to things you rarely look at. On a
laptop that is space the network editor could use, and on a performance
machine it is clutter the audience might see.

BorderlessTD puts both on a key. Hide them while you work, bring them back the
moment you need them.

## How to use it

- Press `F7` to hide or show the window's title bar (Windows only).
- Press `Alt+F7` (`Opt+F7` on macOS) to hide or show the timeline.
- If a borderless window leaves you stuck, `Shift+Esc` brings the title bar
  back. It is a fixed key. Once you are comfortable without it, switch off
  **Use Shift-Esc to undo**.

Both features ship switched on, and each has its own **Enable** toggle. With
one switched off, its key does nothing and the window or timeline stays exactly
as TouchDesigner drew it.

## Making it yours

- **Always borderless:** switch on **On Start** and the window goes borderless
  as the project opens, no key press needed. **State on Startup** on the
  HideTimeline page does the same for the timeline.
- **Borderless in a window:** a borderless window is kept full screen unless you
  switch off **Force Full Screen (always)**. Turn it off to run TouchDesigner in
  a FancyZones layout or any window size you like. BorderlessTD also re-applies
  full screen shortly after the project opens, because TouchDesigner does not
  always come back full screen on its own.
- **Seeing that playback is paused:** the timeline is where you would normally
  notice a pause. With it hidden, BorderlessTD recolours one element of
  TouchDesigner's UI while playback is paused and restores it on play. Choose
  the element with **Pause Indicator** and the colour with **Pause State
  Color**.
- **A tidier menu bar:** **Hide Menu Buttons** removes the Wiki, Forum and
  Tutorials links, and **Show Project Name** puts the project's file name in the
  menu bar, which helps once the title bar that normally shows it is gone.
