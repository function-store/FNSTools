---
status: in-force
summary: Shipped surface layout (toolbar, navbar, main menu, op menu, pane types, hub tabs) comes from packaging/surface_defaults.json, applied at export; the author's live arrangement reaches it only through a snapshot.
since: 2026-10-10
verified: 2026-10-10 — real exports of FNS_GlobalVolControl and FNS_Hub read back from disk carried marker values from the file while the live project kept its own; tests/test_surface_defaults.py
---

# Shipped surface defaults

## The rule

What a new user sees on the toolbar, navbar, main menu, op menu, pane-type
menu and hub tabs is `packaging/surface_defaults.json`. Every export applies
it to the staged copy of the package (`pre_release_common.py`, last
section), so the live project is never touched and the author keeps any
arrangement they like.

To make the current arrangement the release default, take a snapshot in
TouchDesigner, then commit the file:

```python
sd = {}
exec(open('packaging/surface_defaults.py').read(), sd)
sd['WriteSnapshot'](op('/FNSTools'))
```

`WriteSnapshot` refuses to write a file with problems (two entries sharing
an order, a group with one bracket) and says which. Edit the JSON by hand
for small changes; `python tests/test_surface_defaults.py` checks it.

## Why

The author arranges those surfaces in the dev checkout like any user does,
and every drag or hide wrote straight into what ships:

- `SetWidgetSequence` (the configurators' drag) writes each entry's order
  back to its host (`_writeBackHostPar`), and the host's layout par is
  bound to the tool's own surface par. Measured 2026-10-10:

  | Surface | Tool pars | Tools |
  |---|---|---|
  | Toolbar | `Tbmenuorder`, `Tbdisplayed`, `Tbbarwidth` | 19 |
  | Navbar | `Nbmenuorder`, `Nbdisplayed`, `Nbalign` | 5 |
  | Main menu | `Mm*` (order, displayed, align, anchor, width) | 1 |
  | Op menu | `Ommenuorder`, `Omdisplayed` | 3 |
  | Pane types | `Ptmenuorder` | 2 |
  | Hub tabs | `Hbtaborder`, `Hbdisplayed`, `Hbtablabel` | 12 |

- The Hub's four configurators (Toolbar, Navbar, MainMenu, OpMenu) keep a
  `state` table of TD's built-ins, dividers and groups, saved into
  `FNS_Hub.tox`.

v3.2.67 shipped the author's "FNSTools" toolbar group anchored on Perform
and HydroHomie, neither in the starter set (a starter-only install got no
group), two toolbar tools tied at one order, and two pairs of hub tabs
tied (MediaBrowser/BackupCleaner, HotkeyManager/ExprHotStrings; split to
71 and 115 without changing what shows).

The author is also a user of the toolkit. The settings files were already
split (the dev checkout roams `FNStools_config.dev.json`, every other
project the shared file, see ConfigScope.md); the tox was the one place the
dev arrangement leaked into what everyone gets.

## What is captured

- **Surface pars**: for every registry host in a package, the tool par its
  layout par (`Menuorder`, `Displayed`, `Barwidth`, `Align`, `Anchor`,
  `Taborder`, `Tablabel`) is bound to, when that tool par is a constant.
  Registration switches (`Autoregister`, `Register`, ...) are behaviour,
  not place, and stay as authored.
- **Configurator tables** verbatim, with one change: each group's start
  bracket stores the group's whole membership (`Mute|Volume|...`).

## Other dev values: `shipped_values`

Layout is not the only dev state that rode into releases: VSCodeTools
shipped the author's workspace file name and TimelineTools a `test.csv`
export target. The same file has a third key, `shipped_values`
(`{package: {relative path: {par: value}}}`), written by hand, applied by
the same export step, and carried over unchanged by `WriteSnapshot`. Add a
par there when its dev value must not ship; give it the value a new user
should start with (usually the par's default).

## Groups survive missing tools

A bracket used to hang on one named tool, and the whole group vanished on
an install without it. ConfiguratorBase now reads an anchor cell as the
group's members in order (`ANCHOR_SEP = '|'`; a single name still works):
the start bracket opens before the first member present, the end bracket
closes after the last, and while members are missing the brackets are
re-placed on the usual retries. The writer stores the whole membership too,
so groups a user builds behave the same.

## Not in scope

- The dev checkout's own arrangement and its `.dev.json`: untouched.
- Users who already arranged their surfaces: their order lives in their
  config file and wins over the shipped defaults at load, as before.
- TD's built-in buttons ship visible, as the configurator table had them;
  the author's own bar hides the layout buttons, which stays local.
