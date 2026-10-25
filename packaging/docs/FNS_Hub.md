---
package: FNS_Hub
summary: 'The FNS button in the main-menu bar and the one-stop manager window behind it: every surface configurator, the console, and any tab a tool contributes.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Perform Mode
    anchor: perform-mode
  - name: Drop to register
    anchor: drop-to-register
  - name: Scripting the hub
    anchor: scripting-the-hub
  - name: Contributing a tab
    anchor: contributing-a-tab
feature_list:
  - name: Open the hub
    anchor: how-to-use-it
    does: 'Left-click the FNS button in the main-menu bar, or run Open FNS Hub from quick-launch, and the hub opens on the tab you were last on.'
  - name: Jump to any tab from the FNS button
    anchor: how-to-use-it
    does: 'Right-click the FNS button to jump to any tab or console page, bring a hidden tab back, switch Perform Mode, or open the docs.'
  - name: Toolbar configurator
    anchor: how-to-use-it
    does: 'Reorder, group, hide and show the widgets on TouchDesigner''s bookmark bar, and add dividers between them.'
  - name: Navbar configurator
    anchor: how-to-use-it
    does: 'Reorder pane-bar items, flip them between the left and right side, and show, hide or group them.'
  - name: Main menu configurator
    anchor: how-to-use-it
    does: 'Arrange the main-menu bar with TouchDesigner''s own items included, so your entries can sit between them.'
  - name: Reorder OP Create contributions
    anchor: how-to-use-it
    does: 'Reorder what tools add to the OP Create dialog, or switch a contribution off without uninstalling its tool.'
  - name: Network overlay layout
    anchor: how-to-use-it
    does: 'Reorder, show and hide what tools draw on the network editor, and move each corner list to another corner.'
  - name: Console tab
    anchor: how-to-use-it
    does: 'The toolkit''s web console renders inside the hub, and its browser runs only while the tab is shown.'
  - name: Commands tab
    anchor: how-to-use-it
    does: 'Lists every command the command registry serves, hidden and built-in ones included, to star or hide.'
  - name: Tool tabs
    anchor: how-to-use-it
    does: 'The larger tool UIs, such as the OSC and MIDI mappers, sit in the same window, exactly the ones you have installed.'
  - name: Arrange and hide tabs
    anchor: how-to-use-it
    does: 'Drag tabs into your order, hide one from its tool''s Shown in Hub parameter, and pick a wrapping or single-row tab bar; the layout roams with your settings.'
  - name: Perform Mode
    anchor: perform-mode
    does: 'Stops the tools that only serve the network editor for a show, turns the FNS button red, and brings everything back as it was. Follows TouchDesigner''s Perform Mode by default.'
  - name: Drop to register
    anchor: drop-to-register
    does: 'Drop a panel COMP on the FNS button, pick a surface, and it gets a self-registering host and appears there at once.'
  - name: Open a tab from Python
    anchor: scripting-the-hub
    does: '`op.FNS_HUBREGISTRY.Open(tab=''navbar'')` opens the hub on a tab by its canonical name, contributed tabs included.'
    authors: true
  - name: Contribute a tab
    anchor: contributing-a-tab
    does: 'A tool carrying a stamped FNS_HubRegistry host gets a tab showing itself, an inner panel, an operator in an OP Viewer, or a parameter page.'
    authors: true
---

## Why use it

FNSTools reaches into many corners of TouchDesigner: buttons on the toolbar
and the pane bars, entries in the main menu and the OP Create dialog, lists
and outlines on the network editor. Each of those places needs arranging, and
some tools have a bigger interface of their own, like the OSC and MIDI
mappers. Spread over components and floating windows, that is a lot to keep
track of.

Hub gathers it in one window behind an **FNS** button at the right end of the
main-menu bar: a configurator for each bar, the console with every tool's
settings, and the tabs tools contribute. The per-bar gear buttons of older
versions moved here. Hub is a core package: a root that has the registries
has the hub.

## How to use it

1. Left-click the **FNS** button in the main-menu bar. The hub opens on the
   tab you were last on. From quick-launch, **Open FNS Hub** does the same and
   **Open main-menu configurator** opens it on the MainMenu tab.
2. Right-click the button for a menu: every tab, then the console's
   *Settings* and *Install & remove* pages, a *Show …* entry for each hidden
   tab, the **FNSTools Perform Mode** toggle (checked while it is on), *Toolbar
   tool docs…* (the toolbar's tools that have a docs page, in bar order), and
   *Documentation*, *Website* and *Support FNSTools on Patreon*.
3. Pick a tab:
   - **Console**: the toolkit's [web console](/docs/fns-console/) (settings,
     install and remove, updates, and the tabs tools contribute there),
     rendered inside the hub. Its browser only runs while this tab is shown.
   - **Toolbar**: the widgets on TouchDesigner's bookmark bar. Drag rows to
     reorder, group them, hide or show them, add dividers between them, and
     right-click a name for its docs.
   - **Navbar**: the pane bars. Reorder, flip an item between the left and
     right side, show, hide, group.
   - **MainMenu**: the main-menu bar, TouchDesigner's own items included, so
     your entries can sit between them. The *TD* button restores TD's
     original order.
   - **OpMenu**: what tools add to the OP Create dialog (search words, row
     decorations, right-click items, filters). Reorder them, or switch a
     contribution off without uninstalling its tool.
   - **Overlay**: everything tools draw on the network editor
     ([OverlayRegistry](/docs/fns-overlayregistry/)). Layers, such as Cook
     Bar's bars and QuickMarks' outlines, come first, bottom layer first; then
     the corner lists, corner by corner. Drag rows to reorder, click **Show**
     to hide or show one (hiding never switches its tool off), **Corner** to
     move a list to the next corner and **Margin** to set its distance from
     the edges. A tool that is off reads *(off)* and draws nothing whatever
     Show says. Every change lands on the tool's own parameters.
   - **Commands**: every command the command registry serves, hidden ones and
     TouchDesigner's built-ins included, with its tool and context. Star and
     hide from here; your choice beats the tool's default. Contributed by
     [CommandPalette](/docs/fns-commandpalette/).
   - **Tool tabs**: the larger tool UIs that used to live in the `Fx` tools
     panel, such as oscMapper, midiMapper, ExprHotStrings, GlobalOutSelect,
     SearchWords (OpMenu's keyword table) and OpColor (ColorUI's palette
     editor). Exactly the ones you have installed.

To make the hub yours:

- **Reorder tabs:** drag a tab onto another tab.
- **Configure a tool:** hover a tab to see what it is, and right-click it for
  the owning tool's parameters (that is where the mappers are configured) and
  its documentation when it has a page.
- **Hide a tab:** switch off **Shown in Hub** on the contributing tool's
  Registry page. There is no close button; bring a hidden tab back from the
  FNS button's right-click menu.
- **Change the tab bar:** **Tab Bar** on the hub's Hub page picks **Rows**,
  fixed-width tabs that wrap into as many rows as needed, or **Strip**,
  TouchDesigner's single-row folder tabs with scroll arrows and a dropdown.
  Dragging works in both.

Tab order, the active tab, the bar style and the three bar configurators'
layouts roam with your settings through [ConfigRegistry](/docs/fns-configregistry/).

## Perform Mode

Many FNS tools exist for building: they draw on the network editor, watch the
mouse and the panes, and keep themselves ready while you work. During a show
none of that helps, and some of it costs frame time even when nothing on
screen shows it. Perform Mode switches all of it off at once.

Switch it from any of these:

- the FNS button's right-click menu, **FNSTools Perform Mode**
- quick-launch, **Toggle FNSTools perform mode**
- **Perform Mode** on the FNSTools page of the `/FNSTools` root

While it is on, the FNS button turns red and its tooltip says how to switch it
off, so a project that opens performing explains itself.

**What stops:** Cook Bar, QuickMarks' pins and list, POP Overlay and the
network overlay that shows them; the Radial Menu, which does not open; the
scene changers' *Cook While Editing*, so only the show's scenes cook;
Autosave, while its *Skip In Perform Mode* is on; HydroHomie's reminders; the
operator family's update checks; and the small watchers behind hovering,
dragging and the window title. The toolkit's log waits and catches up when you
switch back, errors included.

**What keeps running:** everything a show uses, such as BeatMod, the scene
changers' switching, Remote, Output, the family operators you placed, and the
MIDI and OSC mappers.

No tool setting changes. Each tool keeps its own on/off and display settings,
so switching Perform Mode off brings back exactly what was on.

**Follow TD Perform Mode**, next to it on the root (on by default), turns
Perform Mode on when you enter TouchDesigner's Perform Mode (`F1`) and puts it
back to what it was when you leave. Switch it off to keep the two separate.
Both settings are saved with the project and never carried to other projects,
so a show file can open ready to perform. The guide
[Working with FNSTools in your project](/docs/guides/working-in-your-project/#performing-a-show)
covers it from the show side.

## Drop to register

To put one of your own panel COMPs on a bar or in the hub, drop it on the FNS
button, or anywhere on the hub window. The hub offers every surface that can
take it in a small menu: Toolbar, Navbar and MainMenu, plus *Hub tab*, and
*Palette tab* when the [Palette registry](/docs/fns-paletteregistry/) is
installed.
Pick one and the COMP receives a self-registering host of that surface's
registry and appears immediately; on a bar it lands after the last entry. A
COMP that should live on two surfaces is dropped twice. The COMP stays where it
is and publishes into the registry, exactly like every shipped tool.

## Scripting the hub

```python
op.FNS_HUBREGISTRY.Open()                # the hub, on the last active tab
op.FNS_HUBREGISTRY.Open(tab='navbar')    # a tab by canonical name
```

The built-in tabs are `console`, `toolbar`, `navbar`, `mainmenu`, `opmenu`
and `overlay`; a contributed tab goes by its own canonical name, and a hidden
one is shown again before it opens. On the hub itself,
`op.FNS.op('FNS_Hub')`, `ShowTab(name, displayed=True)` shows or hides a
tab, `HiddenTabs()` lists the hidden ones, `Close()` closes the window and
`TogglePerform()` switches Perform Mode.

## Contributing a tab

A tool that wants a tab carries a stamped `FNS_HubRegistry` host. A panel
COMP can be dropped on the FNS button with *Hub tab* picked; any tool can be
stamped from the registry master:

```python
op.FNS.op('FNS_HubRegistry').StampHost(tool, canonical_name='mytool')
```

The host's Registration page names what the tab shows:

- **Tab Content** empty: the tool itself, which must be a panel. It is
  mirrored into the hub, so the tool can live anywhere in the project.
- **Tab Content** set to a panel COMP inside the tool: that panel, mirrored.
- **Tab Content** set to a DAT, CHOP, TOP, SOP or POP: an OP Viewer of it.
- **Tab Parameters** set to a page scope (`*` for every page): a parameter
  view of the tool. It wins over Tab Content.

**Tab Label** and **Tab Order** place it on the bar. The console sits at 0
and the configurators at 10 to 50; contributions default to 50 and sort by
label within an order. **Help URL** adds *Documentation* to the tab's
right-click menu.

The host registers itself when it initializes, so a tool added while the hub
is open simply appears, and it re-registers on every project open. From
Python without a host:

```python
op.FNS_HUBREGISTRY.RegisterTab(comp, 'mytool', content=panel,
                               label='My Tool', order=50)
```

`Tabs()`, `SetTabDisplayed()`, `Open(tab=)` and `OpenDocs()` are the rest of
the registry's API; [HubRegistry](/docs/fns-hubregistry/) has the details.

What the hub does for your tab:

- Only the shown tab is live, and every tab goes quiet when the window
  closes. A component that must know (a Web Render, say) implements
  `OnHubExposure(exposed)` on its extension; a palette Web Browser has its
  *Active* switched for it.
- A component with a *Refresh* pulse parameter is pulsed every time its tab is
  shown.
- A mirrored panel at the root of a tool has no panel parent, so give it a
  fixed size. The shipped tool tabs bind theirs to the hub's tab area, with
  their standalone size as the fallback.
