---
status: landed
summary: An Overlay tab in FNS_Hub for the network overlay, like the Toolbar and OP menu ones - reorder and show or hide each tool's layer and corner widget, set a widget's corner and margin - with a layer's visibility kept apart from the tool's own on/off.
since: 2026-10-12
verified: 2026-10-12, live - the Layer Active heal on all three overlay tools (old expression moved, Ovdisplayed True), again on a cold boot from the old toxes; POPOverlay on with Displayed off kept running with no layer drawn; from the tab, Show, a reorder (Layer Order 100 and 200 swapped), a corner cycle and a margin landed on the tools' own pars and moved the registry entries, then all reverted; the Overlay and OpMenu tabs both registered. Two cold boots after that: the tab, its rows, all five configurator tabs and every layer displayed; local releases of FNS_OverlayRegistry and FNS_MainMenuRegistry read back scrubbed, Layer Active an expression. Not verified - clicks and drags by hand in the Hub window.
skill: fns-registry
---

# Overlay manager

Owner request, 2026-10-12: "make an overlaymanager similar to toolbar and
else". Owner decisions the same day:

- **Show hides, it never switches a tool off.** "There are DEFINITELY tools
  that should not be deactivated even though their toolbar icon is
  deactivated... same here." The toolbar already works this way:
  `Tbdisplayed` is a constant on the tool, so hiding an icon leaves the tool
  running.
- **Layers and widgets** both get rows in the first version.

Corrected in place as findings land; what landed is below the plan.

## What is wrong today

Every overlay tool's `Ovdisplayed` is an EXPRESSION on its own switch:
`me.par.Active` (CookBar, FNS_POPOverlay), `me.par.Active and
me.par.Showpins` (QuickMarks). Measured 2026-10-12. That expression is how a
layer goes away when its tool is off. It also means a manager that writes
Show through the host's bind flattens the expression to a constant: the
same trap that broke GridShow's toolbar promotion (docs/POPOverlay.md,
Toolbar row). And it leaves no place for "keep the tool on, hide its
layer".

The corner widgets have the same coupling: a tool registers its widget only
while it is on and its list switch is on, and unregisters it otherwise, so
the registry never knows about a hidden widget and a manager could not list
it.

## The plan

### 1. Two flags per layer, one of them the user's

| Flag | Where | Who owns it |
|---|---|---|
| `Displayed` (`Ovdisplayed` on the tool) | host Registration page, bound to the tool's Registry page as today | the user: a constant, written by the manager and by hand |
| `Layeractive` (new, "Layer Active") | host Registration page only, not promoted | the tool: an expression on its own switch, default `Active` when the tool has one |

The registry draws a layer only when both are on. A change to either
re-registers the host, as `Displayed` does now.

Heal on host init (`_ensureLayerActive`, the master AND every stamped host,
per the "master and an init heal" rule): create `Layeractive` when missing;
when the tool's `Ovdisplayed` is still an expression, move it onto
`Layeractive` (`me.par.` becomes `parent().par.`) and set `Ovdisplayed` to a
constant True. Installed tools heal on their next init without a re-stamp.

### 2. Widgets register while the tool exists

`RegisterPanelWidget(panel, canonical, anchor, order, margin, shown=True,
active=True, tool=None, pars=None)`. `pars` names the tool parameters the
manager may write, by role: `show`, `corner`, `margin`, `order`. A tool
registers once it is initialized and re-registers when any of those change;
it unregisters only when it is destroyed. The registry places only widgets
that are shown and active.

| Tool | show | corner | margin | order (new) |
|---|---|---|---|---|
| CookBar | `Toplist` | `Topcorner` | `Topmargin` | `Toporder`, 100 |
| QuickMarks | `Showlist` | `Listcorner` | `Listmargin` | `Listorder`, 150 |

### 3. The tab: `FNS_Hub/OverlayConfigurator`

A copy of OpMenuConfigurator (a Hub tab over a registry that has no bar,
through a small adapter), Hub tab `overlay`, label Overlay, tab order 50.

| Column | Layer row | Widget row |
|---|---|---|
| Name | the canonical (CookBar, QuickMarks, ...) | `<tool> list` |
| Corner | `-` | click to cycle the four corners; writes the tool's corner par |
| Show | `Displayed` | the tool's show par |
| Margin | `-` | right-click to set; writes the tool's margin par |
| Origin | the tool | the tool |

Rows read layers first, bottom layer first, then the widgets by corner and
stacking order; a tool that is off reads dimmed. Dragging reorders within
its kind: layers write `Ovmenuorder`, widgets write their order par,
numbered within their corner. No groups, dividers, built-ins or
drop-to-register. Nothing is owned by the tab, so its `state` table stays
empty: every setting is a parameter of the tool it belongs to, persisted and
roamed with that tool.

Copy recipe (`/fns-registry`): the source's inner hosts and lister clones
get `enablecloning` off and the source `initextonstart` off for the copy,
restored in a `finally`; the copy's DATs lose their file binding before
anything is written to them; PI adopts the new configurator and its
`ConfiguratorExt`; FNS_Hub and the root are saved after it, leaves first.

## Done when

- Each overlay tool on, with its layer hidden from the tab: the tool keeps
  running (CookBar keeps its Top List, POPOverlay its monitor), the layer is
  gone, and the hidden state survives a save and a cold boot.
- A tool switched off removes its layer and widget whatever Show says.
- Reorder and corner/margin edits from the tab land on the tool's pars and
  move the overlay; the tool's own parameter dialog shows the same values.
- Both error surfaces clean on FNS_OverlayRegistry, the three tools and
  FNS_Hub; `test_overlay_registry.py` and a new configurator test pass.
- Docs: NetworkOverlayRegistry.md (two flags, widget spec), HubContract.md
  (tab list), packaging/docs FNS_Hub, CookBar, QuickMarks; release notes.

## What landed, and what it cost

All three parts, as planned. Five findings on the way:

- **A widget spec must stay flat.** The first version stored `pars` as a
  nested dict and the flags as bools; `store()` on the `/sys` global crashed
  TD natively (py-spy: `RegisterPanelWidget` -> `store`, the
  UnhandledExceptionFilter -> fwrite signature of 2026-10-11), and the same
  call ran 90 frames into every boot. The spec now carries
  `'corner=Listcorner margin=Listmargin ...'` and `'1'`/`'0'`;
  `WidgetSpecs()` decodes them.
- **Copying a configurator knocks its source's Hub tab out.** After the copy
  the OpMenu host still read *Registered*, but the hub had no `opmenu`
  entry; a Register pulse put it back. The same thing happened to CookBar's
  toolbar entry when its button host was copied (docs/POPOverlay.md).
- **The tab re-reads a few frames late.** A tool re-registers a frame or
  more after its par changes, a host through the registry's deferred sync,
  so the tab refreshes at once, at 3 frames and at 15. A corner click reads
  the tool's par itself, never the lagging registry copy.

- **Layer Active has to survive two release paths.** Every registry hook
  flattens its Registration page to constants, which froze the expression:
  the overlay hook now skips Layer Active. PI's local Release then
  flattened it again in its own `prerelease_all`, which keeps an expression
  on the released COMP only when it reads `me.`, `op('.`, `app.` and a few
  more; `parent().par.Active` became `me.parent().par.Active`, the same
  operator. Embody's portable export (the bucket rail) kept it either way.
  A constant Layer Active, or the old `parent()` default, heals on init.
- **A roamed settings file brings the old shape back after init.**
  CookBar's config host had saved `Ovdisplayed` as the expression
  `me.par.Active`; ConfigRegistry restored it after the host's init heal
  ran, so CookBar came back hidden after a cold boot. The heal now runs on
  every registration too (the restore re-registers the host), clears the
  dormant expression text it leaves behind, and the next settings save
  writes the constant.

The copy also needed its own `opshortcut` (`OVERLAYCONFIG`) and a
`colDefine` with Corner and Margin columns: the tree lister shows only the
columns that table defines, whatever the entries table carries.

## Nothing cooks for a hidden overlay (2026-10-12)

The registry already drew nothing and ran no frame driver unless some layer
or widget was both displayed and active. The tools did not follow: each
one's frame DAT ran on Active alone. Each now runs on what it would draw,
healed on init: QuickMarks' execute_overlay on Active and (pins shown and
Displayed, or the list on); FNS_POPOverlay's on Active and Displayed;
CookBar's execute_op_info on Active and (Displayed or the Top List), with
the bar pass skipped while only the list shows. Measured live: with
QuickMarks on but its list and pins hidden, or its pins hidden from the
Overlay tab, there was no annotation, no registry frame driver and no
QuickMarks frame work.

v3.2.68 shipped QuickMarks' overlay on: its release hook shipped Mark
List and Pins on and never set Active, so the artifact took the dev
copy's state. The owner's call (2026-10-12): QuickMarks itself ships on,
its overlay off. The hook sets Active on and both switches off, and their
defaults are off.
