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

## Only a user's changes roam (2026-10-14)

Layout used to roam like any parameter, so a settings file carried the
layout of whatever release last saved it and replayed it over every later
release's defaults. After the v3.2.70 update the owner's project got new
tools at the new numbers and the old tools back at the file's numbers
(three tied pairs, HydroHomie hidden, the pre-10-10 dev group in the
toolbar table), and that project's save spread the result to every other
project through the shared file.

- **Release:** `Apply` also sets each layout par's `default` to the shipped
  value and tags its owner `fns_layoutdefaults`; each configurator gets a
  `state_default` table holding the shipped rows.
- **Save (FNS_ConfigRegistry):** a layout par of a tagged owner is saved
  with its default beside its value (`pars` and `surfaces` alike). An
  untagged owner (a tool from an earlier release, the dev masters) saves no
  default, since a factory default would make every shipped number look
  like a change.
- **Load:** a layout value applies only when it differs from the default
  saved beside it: a position the user chose. Otherwise the tool's own
  shipped value stands, which is how a new release's layout arrives.
- **Hub tables:** `config_callbacks` saves a configurator table only when
  it differs from `state_default`, as schema 2; schema 1 tables are
  ignored on load.

**...and written only when the user changed it.** The rule above decides
whether a value applies; this one decides whether it is written. A project
that loaded with some other layout (its own `.toe`, a load that did not
land) and is saved without a rearrange would otherwise spread it. So each
surface's `/sys` global carries a flag, set only by the user's own edits
(the Hub configurators' drag, show/hide, side, width, groups, dividers,
Restore TD order, drop-to-register; the bar's group eye; the Hub's tab
show/hide) and never by a boot, a restore or a heal. On SaveAll an
untouched surface's layout records, and its Hub table, are carried over
from the file unchanged; the flags clear once the file is written. An
explicit settings export (UiExport) still writes the live layout. The Hub's
tab drag order (`Tabuserorder`) is a plain Hub parameter and roams as
before.

**Cost, accepted by the owner:** values and tables written before this
rule carry no default and are ignored once, so a user who had arranged
their bars starts from the shipped layout after the update that brings it.

## Not in scope

- The dev checkout's own arrangement and its `.dev.json`: untouched.
- Users who already arranged their surfaces: their changes live in their
  config file and win over the shipped defaults at load (next section).
- TD's built-in buttons ship visible, as the configurator table had them;
  the author's own bar hides the layout buttons, which stays local.

## Automatic passes never renumber (2026-10-17)

The rule above decides what is written to the settings file. This one
decides what is written to the tools' own parameters, and by whom.

An installed project (SculptReveal) updated in-session from v3.2.70 to
v3.2.71 came out with a bar the dist artifacts did not explain: the registry
held a dense 1..N numbering with packages replaced later in the pass
re-registered at their shipped slots among it (two tools tied at 40), and
the FNSTools and Project groups were gone. Two causes:

- `SetWidgetSequence`, the registry primitive behind the Hub's drag,
  reassigns 1..N over the whole sequence and writes every number back to
  its host. The Hub's boot passes called it too, to interleave group
  brackets and adopted built-ins into the order. Run while hosts were
  missing (every package replaced in an update unregisters and registers
  again), that wrote dense numbers over the shipped slot of every tool after
  a gap; FNS_ConfigRegistry then saved them as the user's choices (value
  differs from default), and they roamed.
- The group-bracket restore retried six times a second apart, against an
  apply that replaces packages for minutes. Its budget ran out while
  members were mid-replacement, so a group with no member present was
  dropped and the others were bracketed around whoever was there.

Now there are two primitives on every bar registry (Toolbar, Navbar,
MainMenu, Timeline):

- `SetWidgetSequence` is the user's edit only (the paths that call
  `_markChanged`): it renumbers 1..N and writes back, which is right for a
  drag.
- `PlaceWidgetSequence` is what the automatic passes call (the Hub's boot
  adoption, its stored-order apply, the group-bracket restore, the main
  menu's first adoption): a published entry keeps its host's number; group
  brackets, dividers and adopted built-ins take the whole numbers between
  the tools, and where there is none they borrow the number of the tool
  that follows with a negative `menu_sub` (the resolver sorts by order,
  sub-order, name). No host is written, so a host at its stamped default
  stays there and the settings file keeps reading it as unchanged. A
  published entry an automatic pass would move relative to its peers is
  placed the same way, store-only, and logged as a warning: an automatic
  pass has no business reordering tools.

Bar positions come from the resolved sequence either way (`_barOrder`), so
nothing visible depends on dense numbers; the sub-order lives only in the
/sys store and disappears on the user's next drag, which renumbers.

The group-bracket restore spends an attempt only on a look at a SETTLED
registry: the same tools as the look before, and FNS_Updater not applying
(`IsApplying`). Looks during churn are free, up to fifteen minutes; a group
none of whose members is present is retried like any other. The Hub side
needs nothing from the updater for this: an apply replaces a package every
few frames, so the set of registered tools changes between looks until it
is done. FNS_Updater adds two things on top: `IsApplying`, which the
restore reads, and a call to each configurator's `RepublishOwned` when an
apply finishes, so a bracket placed around a partial group closes around
the whole one without waiting for the next settled look.

`tests/test_toolbar_update_replay.py` replays the update on a fixture and
holds the four registries to one placement block.

Installs that saved the dense numbers before this (SculptReveal, SandPit)
still carry them, in their `.toe` and in the shared settings file, and
nothing can tell those from an arrangement the user made. So the heal is
the user's call: **Reset toolbar**, a pulse on the Hub's Toolbar
configurator (`Resettoolbar`, page Toolbar), asks first and then puts every
tool whose owner carries `fns_layoutdefaults` back to its stamped default,
the configurator's table back to `state_default` where a release wrote
one, and once the tools have re-registered re-places the brackets and
saves the settings file, whose records then read value equals default and
never apply again. It counts as the user's edit, stores nothing, and is
harmless to press twice. An untagged tool (an older release, the dev
masters) is never touched. The user's own arrangement of the bar is lost,
which is why it asks.
