---
status: in-force
summary: FNS_OverlayRegistry, the twelfth registry -- every tool hands over one layer TOP, the registry composites them, shows the result above the nodes through one utility annotation, and tells each layer where it draws; tools can also pin small interactive panels (widgets) to a corner. CookBar is the first client of both.
since: 2026-10-11
verified: 2026-10-11, pilot layers and CookBar live: composite, stacking by Menuorder, teardown on Displayed off and on deletion, pre-save removal, clone-master skip, bar positions equal NetworkToPixel; the viewed network's display flags, annotation alphas and children unchanged. Widgets: cold boot, corner stacking measured (margin 30, gap 20: second widget 30 + 170 + 20 points down), margin change and package save, Top List rows, tabs and click framing. Non-Commercial (2026-10-15, under app.addNonCommercialLimit): View pars equal the drawn size, 1280x602. Not verified: macOS.
skill: fns-registry
---

# Network overlay registry

## The contract

**The client renders, the registry composites.** A tool tells the registry
"here is my output TOP, composite it with the rest", and in return the
registry gives it everything it needs to render: where the view sits in the
network, the scale, the resolution and which network it is. What a layer
draws, and how, is entirely the client's business (owner, 2026-10-11).

The registry owns the rest, once for everyone:

- **following the network editor you work in** (the current pane, else the
  network editor followed last while another pane type is current);
- **the composite**: one Composite TOP (`over`), the shown layers top first
  (higher `Menuorder` on top, verified), ending in `null_overlay`;
- **showing it**: ONE utility Annotate COMP in the viewed network,
  `layerzone = abovenodes`, transparent, `enable` off, fitted over the view
  plus a 15% margin every frame the view moves (TDCollab's partner overlay,
  `CollabPaneSyncHandler._drawOverlay`, RemoteTD, generalised).

## What a client gets

The global's **View** page, written only when the view changes, so anything
bound to it recooks only then:

| Par | Means |
|---|---|
| `Viewx0 Viewy0 Viewx1 Viewy1` | the rectangle the overlay covers, network units |
| `Resolutionw Resolutionh` | the resolution to render at, pixels (monitor DPI, capped at 4096; longest side 1280 under a Non-Commercial licence, so this is also the size TD draws) |
| `Unitsperpixel` | network units per layer pixel |
| `Pixelsperpoint` | layer pixels per screen point (keeps a line one width on screen at any zoom) |
| `Zoom` | the network editor's zoom |
| `Network` | the network being viewed, empty when there is none |

`View()` returns the same as a dict (`x0 y0 x1 y1 width height
unitsPerPixel pixelsPerPoint zoom network shown`), and `NetworkToPixel(x, y)`
turns a network position into layer pixels (origin bottom left).

**Parameters, not a `tdu.Dependency`.** A dependency lives on the extension
instance and is rebuilt on every reinit, leaving every subscribed client
expression stale; parameters live on the COMP and survive it, and an
expression reading one is already a dependency. The registry polls the pane
each frame (TD has no pan/zoom callback; CookBar did the same) only while a
layer is shown.

## What a client does

Stamp a host (`op.FNS_OVERLAYREGISTRY` master's `StampHost`, then
`Promotepars` on) into the tool:

| Host par | Means |
|---|---|
| `Layer` | the layer TOP (a TOP par; `Comp` stays the base's COMP par, the tool) |
| `Menuorder` | stacking order, higher on top |
| `Displayed` | the user's show switch, a constant on the tool's Registry page (`Ovdisplayed`); the Overlay tab in FNS_Hub writes it |
| `Layeractive` | the tool's own half, an expression on its switch (`Active` by default), kept on the host; the layer draws only with both (see "Two flags per layer") |

### Stacking: bands, not arbitrary numbers

A tool sets its own depth, by what it draws (owner, 2026-10-11). Stacking
only matters where layers cover the same pixels, and there the right order
is semantic (a cursor above an outline, an outline above a fill), which the
tool knows. `Menuorder` falls in a band:

| Band | For |
|---|---|
| 0-99 | fills and heat maps: broad, translucent |
| 100-199 | per-operator marks: CookBar's bars (100), outlines |
| 200-299 | labels and text |
| 300+ | cursors and other transient pointers |

Within a band pick a slot; a tie is broken by canonical name. The user
overrides per tool with **Layer Order** (`Ovmenuorder`) on the tool's
Registry page, which roams through the config file like every other surface
order, and the shipped value comes from packaging/surface_defaults.json. A
Hub tab to rearrange layers (as the toolbar and navbar have) waits until
there are about three clients; `ConfiguratorBase` makes it cheap then.

Render the layer at the View's resolution over the View's rectangle,
premultiplied, transparent where it draws nothing, keeping the node tiles
clear (it sits above the nodes).

## Rules the registry keeps

- **Idle is free.** No shown layer: no annotation, no layer selects, the
  frame driver (`execute_frame`) off. The composite always has two inputs
  (the clear layer fills the second slot): a Composite TOP with one source
  errors "Not enough sources specified".
- **A deleted tool cleans up.** TD calls no `onDestroyTD` for a host dying
  inside its parent's subtree, so every sync and the 15-frame heal tick drop
  entries whose layer no longer exists, and the frame driver turns itself
  off when nothing is shown.
- **Saves never hold it.** `execute_save` (`projectpresave`) removes the
  annotation; the next frame draws it again. `pre_release_common` strips any
  tagged annotation from artifacts, and the global sweeps the whole toolkit
  once at boot.
- **Never in a clone master.** A child added to a COMP others clone
  replicates into every clone: drawn in the registry master's own network,
  the annotation appeared, path broken, in each host. Networks found by
  `_isClonedByOthers` get no overlay; the answer is cached per network.

## Packaging

A package, not core (owner, 2026-10-11): tools that draw overlays require it,
through `requires` derived from the host (`build_manifest.REGISTRY_OWNER`),
and the installer resolves that like any dependency. This is the one
registry outside `CORE`; CREATING.md's "tools depend only on core" names
the norm, this is the exception. The shipped layout of a layer
(`Ovmenuorder`) comes from packaging/surface_defaults.json like every other
surface (docs/ShippedSurfaceDefaults.md).

## CookBar on it

`glsl_cook_bar` renders into `null_cook_bar_layer` at the View's resolution;
its `zoom` uniform is `1 / Unitsperpixel`; the shader outputs premultiplied
bars with their fade as alpha and transparency elsewhere. `execute_op_info`
measures operators in layer pixels from `View()`. Gone: the Select TOP and
suicide DAT it planted in the viewed network, the display-flag switching, the
annotation dimming, the pane tracking (`execute_pane_info`, the window-size
tscript) and the save hooks (`execute_save`, `putBack`/`reapply`).
`retireBackdrop` removes, once at init, anything the backdrop method left in
a project. `Annotationalpha` is now unused (left in place for now). The Top
List is a widget (see "CookBar's Top List" below).

## Widgets: what the spike showed (2026-10-11)

Interactive panels cannot go through the composite: it is one TOP, and an OP
viewer only passes clicks to the operator it shows. Annotations can show a
panel interactively (Annotate COMP docs: **OP Viewer Interactive**,
`Opviewerinteractive`, with **Enable Interaction**, `enable`, on), so a
widget is its OWN small utility annotation showing the tool's panel COMP.
A throwaway spike (a slider and a button pinned to the view's top-right
corner at a constant 220x64 points) measured:

| Question | Result |
|---|---|
| Interaction | works: the owner dragged the slider (0.414 to 0.384) and pressed the button (2 presses counted) |
| Clicks through to the network | **no**: the widget's whole rectangle takes clicks, so widgets must stay small |
| Zoom and pan | stays pinned at the same on-screen size (size and offset divided by zoom, refitted when the view moves) |
| The annotation's own resize handles | usable by the user; the next view change re-pinned it. The spike compared against its last written rectangle; a real version compares against the live geometry and re-pins at once |
| Cost | none measurable (12.5 ms a frame against a 13.3 ms baseline) |
| Placement | the top-right corner sat under TD's floating parameter window: widgets need anchor options |

Two traps found:

- **`op()` never finds a utility operator**, which is what utility is for.
  The spike looked its annotation up by path, missed it, and made a new one
  every frame: 163 in a few seconds and 21 fps before it was stopped. Keep
  the OP itself (storage holds operator references), and guard against more
  than one.
- A fresh annotation carries the provisional-name Component warning until
  its `annotation/back` is cooked once more (TDCollab's heal, needed here
  too).

## Widgets: the contract

A tool registers a panel COMP and a corner; the registry owns everything
else: the annotation, the pinning, the layout, the pre-save removal.

```python
reg = getattr(op, 'FNS_OVERLAYREGISTRY', None)
if reg is not None and hasattr(reg, 'RegisterPanelWidget'):
    reg.RegisterPanelWidget(panel, 'MyTool', anchor='topleft', order=100, margin=12,
                            shown=bool(c.par.Showlist), active=bool(c.par.Active), tool=c,
                            pars={'show': 'Showlist', 'corner': 'Listcorner',
                                  'margin': 'Listmargin', 'order': 'Listorder'})
```

- **Register for as long as the tool exists**, and say whether the widget
  shows: `shown` is the user's switch, `active` the tool's own on/off. Only
  a widget with both is placed. Unregister only when the panel goes away;
  a hidden widget stays listed in the Overlay tab of FNS_Hub (since
  2026-10-12, docs/OverlayManager.md).
- **`tool` and `pars`** name the tool parameters behind show, corner,
  margin and order, so the Overlay tab writes a change where it lives and
  the tool re-registers from it.

- **`anchor`** is `topleft`, `topright`, `bottomleft` or `bottomright`;
  the tool usually offers it as a parameter (the floating parameter window
  covers the top right for some users).
- **`order`** is the widget's place in its corner's stack, lowest nearest
  the corner, ties by name. Use the layer bands' numbers (100 for marks,
  as CookBar does).
- **`margin`** is the tool's, in screen points (12 by default): the widget
  sits that far from the editor's edges, and that far from the widget
  before it when several share a corner. Offer it as a parameter of the
  tool, beside the corner (CookBar: List Corner, List Margin). The stacking
  is the registry's, so two tools in one corner never overlap.
- **The panel's own size is its size on screen.** Size and offsets are
  divided by the zoom and compared with the live geometry every frame, so a
  drag or resize by the user is undone at once.
- **Registrations live in the global's storage** (`widgets`, strings and
  numbers only: a spec holding a nested dict and bools crashed TD natively
  inside `store()`, 2026-10-12, so `pars` travels as
  `'corner=Listcorner margin=Listmargin ...'` and the flags as `'1'`/`'0'`;
  `WidgetSpecs()` hands them back decoded) and the annotations are held as
  OP references; the presave hook, the
  extension teardown and the boot sweep (tag `fns_network_overlay_widget`)
  remove them, and `pre_release_common` strips the tag from artifacts.
- **Keep it small.** The whole rectangle takes clicks.

## Two flags per layer (2026-10-12)

A layer is drawn when **Displayed** (the user's, bound to the tool's
`Ovdisplayed` and a constant) AND **Layer Active** (the tool's, on the
host's Registration page, never promoted) are on. Layer Active is an
expression on the tool's own switch, `Active` by default; QuickMarks' reads
`me.parent().par.Active and me.parent().par.Showpins`. Before this the tool's
switch lived in `Ovdisplayed` itself, so hiding a layer meant switching the
tool off and a manager writing Show through the bind flattened the
expression. `_ensureLayerActive` moves an old expression across on every
host's init. Reasoning and the Overlay tab that writes these:
[OverlayManager.md](OverlayManager.md).

### The master keeps Enable Cloning off

The package is the COMP every host clones from; it clones nothing. It
shipped with **Enable Cloning** on and an empty Clone par, and in that
state any custom-par write on it crashed TouchDesigner natively: seconds
later, at the next save, or on every boot once a page of pars was in its
tox (seven crashes, 2026-10-11). Switching only that flag off, the same
writes and saves survived and a cold boot was clean; the Toolbar, Timeline
and Config masters have it off. `_ensureMasterNotCloning` heals it on init.

That page was a package-wide **Widgets** page (Margin, Gap), and it lasted
one day: the owner wanted the margin per tool, beside the tool's corner,
where Layer Order already lives. `_retireWidgetLayoutPage` removes it where
it was saved.

### CookBar's Top List

The first widget: the viewed network's heaviest operators, ranked by cook
time (only what cooked within the last second: `cookTime` keeps the last
cook's duration forever) or GPU memory. Tabs along the top switch the rank
(`Toprank`), a row click makes the operator the only selection and frames
it (`homeSelected(zoom=True)`), and the widget's own annotation is
deselected first, since framing it would zoom out further on every click.

## QuickMarks on it

The second client, and the first with both parts. The **mark list** is a
widget (order 150, so it stacks under the Top List in a shared corner): the
stored marks by number and name, the one for the viewed network
highlighted, a row click running `RetrieveQuickmark` like Ctrl+number. The
**outlines** are a layer (`null_pins_layer`, order 200, the labels band): a
GLSL TOP draws the rounded outline of each mark's saved area (centre `x`,
`y`, and since 2026-10-11 the area's size `w`, `h` in network units; older
marks take the current pane's size at the saved zoom), and a Text TOP
labels each in its top-left corner, positioned through the View like
CookBar's bars. A list row's right-click renames its mark (TD's
non-blocking PopDialog), a mark whose network is gone reads *missing*, and
both widgets fold to their top row from an arrow there (Mark List
Collapsed, Top List Collapsed); the registry restacks from the live
height. `execute_overlay` checks every frame and rewrites the
list or the pins only when what they show has changed. Mark List, List
Corner, List Margin and Pins sit on QuickMarks' Custom page; the host's
Layer Active follows `Active and Showpins` (Displayed until 2026-10-12).

Its release hook now empties every mark slot: the author's own marks had
shipped in the tox, and the list would have shown them on a fresh install.

## Later

- A shared marks layer: partner_overlay's shader (rounded outlines,
  cursors, name tags) as a component any tool feeds with rectangles.
- TDCollab as a client when the toolkit is present (its own project).
  Done: TDXCollab registers one layer and two widgets (see below).

## Never rebuild the global by accident (2026-10-12)

Toolbar buttons that switch a layer (CookBar, POPOverlay) needed a re-hover
before the next click. Every toggle rebuilt the `/sys` extension: TD builds
it by evaluating `ext0object`, and every operator read during that
evaluation becomes a dependency of the expression. `_ensureOverlayOps` and
`_syncSurface` read `execute_frame` (its text and Active) during
construction, and creating a layer Select TOP inside the global
re-evaluated the lookup too. A toggle flipped `execute_frame`, the next
access (QuickMarks' frame callback, every frame) rebuilt the extension, and
the new instance swept and redrew the overlay and widgets in the viewed
network in the middle of the click, on a frame of up to 244 ms.

The rules that keep it from coming back:

- **No operator reads during construction.** `postInit` only schedules
  `_globalSetup` a frame later; `_syncSurface` returns while `_inInit` is set.
- **No children created on a toggle.** Layers go through a fixed pool,
  `layer_0` .. `layer_5`, made by `_ensureOverlayOps` and re-pointed by
  `_syncSurface`.
- **No annotation created or destroyed on a toggle.** A widget whose tool
  switches off is parked (viewer off, not clickable, no size) and reused on
  its next show; widgets are destroyed only when nothing is shown at all,
  the network changes, or the project saves.

Measured after: no rebuild on any toggle; the click frame went from 244 ms
to 29 ms (POPOverlay on) and from 174 ms to 38 ms (CookBar off). The other
`/sys` registries cooked their extension DAT once in the same session.

## Shared with TDXCollab (0.2.x, 2026-10-15)

TDXCollab embeds a host of this registry and ships the registry unchanged:
one version, built from this master, serves both toolkits. Whichever loads
first is the global and the other's copy ties and stays out. TDXCollab
never edits or re-versions it, so its findings land here and both take the
next release. It draws one layer (partner cursors, view rectangles,
selection boxes from one GLSL TOP reading the View pars) and two widgets
through `RegisterPanelWidget`.

What 0.2.0 settled, from their reports:

- **Non-Commercial is 1280 on the longest side, aspect kept.** Measured
  here under `app.addNonCommercialLimit(password=...)`: 2000x1000 drew
  1280x640, 1280x1000 and 1000x1280 were untouched, 2000x2000 drew
  1280x1280, 4000x2 was untouched. Detection reads
  `licenses.isNonCommercial`; `licenses.type` says
  `TouchDesigner Non-Commercial` (and `TouchDesigner Educational` on the
  dev machine), so the old `== 'Non-Commercial'` never matched. TD then drew
  the composite smaller than the View pars said, and TDXCollab's cursors
  landed outside the image on a Non-Commercial Mac.
- **Widgets survive a takeover.** Layers ride the base's entry table;
  widgets live in their own `widgets` storage, which the takeover did not
  merge, so a newer global started without them until each tool registered
  again. `_merge_pane_registry_from` now carries them, and
  `_dropParallelTable` clears the master's copy afterwards.
- **A host that comes up before the global retries** (every 30 frames, 20
  times) instead of reporting Registered while its registration was
  ignored.
- **The annotations enclose no operators** (`encloseops = False`).
- **0.2.1: no self-dependency on reinit.** The master's widget cleanup ran
  in `postInit` with `fetch('widgets')`, and a fetch during construction
  made the COMP depend on its own storage: a cook dependency loop warning
  naming only the COMP after every reinit (TDXCollab saw it on their host).
  It reads `storage.get` now; reinit leaves no warning on master or host.

What a client can rely on, and must keep:

- **Layer Active stays an expression.** Every registration re-asserts the
  default expression over a constant (`_ensureLayerActive`), so a tool that
  wants its own condition writes it as an expression (TDXCollab reads COMP
  storage, QuickMarks `Active and Showpins`).
- **The tags are stable**: `fns_network_overlay` on the layer annotation,
  `fns_network_overlay_widget` on each widget annotation. Both are utility
  operators that `COMP.saveByteArray` carries, so a tool that serialises a
  network strips them by tag.
- **Pane following**: the current network editor, else the one followed
  last while another pane type is current. A change to this rule is a
  change to the contract.
- **The covered rectangle includes the pane's path bar.** `bottomLeft` and
  `topRight` include the roughly 24 point bar, while `pane.x`/`pane.y` is
  the centre of the network below it. Network-space positions (the View
  pars, `NetworkToPixel`) are self-consistent; anything placed in screen
  points from the pane centre is off by about 12 points.
