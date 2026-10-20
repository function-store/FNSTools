---
package: FNS_Hub
summary: 'The FNS button in the main-menu bar and the one-stop manager window behind it: every surface configurator, the console, and any tab a tool contributes.'
features:
  - name: The FNS button
    anchor: the-fns-button
  - name: The tabs
    anchor: the-tabs
  - name: Perform Mode
    anchor: perform-mode
  - name: Drop to register
    anchor: drop-to-register
  - name: Contributing a tab
    anchor: contributing-a-tab
feature_list:
  - name: Open the hub
    anchor: the-fns-button
    does: Left-clicking the FNS button in the main-menu bar opens the hub on the tab you were last on; quick-launch offers Open FNS Hub too.
  - name: FNS button menu
    anchor: the-fns-button
    does: 'Right-clicking the FNS button lists every tab, the console''s Settings and Install & remove pages, Show entries that bring hidden tabs back, the Perform Mode toggle, and links to the docs, the website and the Patreon page.'
  - name: Perform Mode
    anchor: perform-mode
    does: 'One switch for a show: the tools that only serve the network editor stop, the FNS button turns red, and switching back brings everything back as it was. Follows TouchDesigner''s Perform Mode (F1) by default.'
  - name: Toolbar configurator
    anchor: the-tabs
    does: 'Reorders, groups, hides and shows the widgets on TouchDesigner''s bookmark bar and adds dividers between them; right-click a name for its docs.'
  - name: Navbar configurator
    anchor: the-tabs
    does: 'Reorders pane-bar items, flips them between the left and right side, and shows, hides or groups them.'
  - name: Main menu configurator
    anchor: the-tabs
    does: 'Arranges the main-menu bar including TouchDesigner''s own items, so your entries can sit between them; the TD button restores TD''s original order.'
  - name: OP Create contributions
    anchor: the-tabs
    does: 'Reorders what tools add to the OP Create dialog (search words, row decorations, right-click items, filters) and switches any off without uninstalling its tool.'
  - name: Network overlay layout
    anchor: the-tabs
    does: 'Reorders, shows and hides everything tools draw on the network editor, and moves each corner list to another corner with its own margin.'
  - name: Console tab
    anchor: the-tabs
    does: 'Renders the toolkit''s web console (settings, install and remove, contributed tabs) inside the hub, running its browser only while the tab is shown.'
  - name: Commands tab
    anchor: the-tabs
    does: 'Lists every command the command registry serves, hidden and built-in ones included, with tool and context, to star or hide; contributed by CommandPalette.'
  - name: Tool tabs
    anchor: the-tabs
    does: 'Shows the larger UIs of installed tools, such as oscMapper, ExprHotStrings, GlobalOutSelect, SearchWords, midiMapper and OpColor, as hub tabs.'
  - name: Arrange and hide tabs
    anchor: the-tabs
    does: 'Drag a tab onto another to reorder, right-click it for the owning tool''s parameters, and hide it with that tool''s Shown in Hub parameter.'
  - name: Two tab bar styles
    anchor: the-tabs
    does: 'Tab Bar picks Rows, which wraps fixed-width tabs, or Strip, TouchDesigner''s single-row folder tabs with scroll arrows and a dropdown.'
  - name: Roaming hub layout
    anchor: the-tabs
    does: 'Tab order, the active tab and the three configurators'' layouts roam with your settings through ConfigRegistry.'
  - name: Drop to register
    anchor: drop-to-register
    does: 'Dropping a panel COMP on the FNS button or hub window offers Toolbar, Navbar or Main Menu and gives it a self-registering host, so it appears immediately.'
  - name: Open a tab from Python
    anchor: the-fns-button
    does: '`op.FNS_HUBREGISTRY.Open(tab=''navbar'')` opens the hub on a tab by its canonical name, contributed tabs included.'
    authors: true
  - name: Contribute a tab
    anchor: contributing-a-tab
    does: 'A tool carrying a stamped FNS_HubRegistry host gets a tab showing itself, an inner panel, an operator through an OP Viewer, or a parameter page.'
    authors: true
---

Hub is the one place to manage the toolkit from inside TouchDesigner. It
puts an **FNS** button at the right end of the main-menu bar and, behind it, a
window with a tab per concern: the Toolbar, Navbar and Main Menu configurators
(the per-bar gear buttons are gone; this is where they went), the web
console, and whatever else a tool decides to show. It is a core package: a
root that has the registries has the hub.

## The FNS button

| Gesture | What happens |
|---|---|
| **Left-click** | opens the hub on the tab you were last on |
| **Right-click** | a menu: every tab, then the console's *Settings* and *Install & remove* pages, the **FNSTools Perform Mode** toggle (checked while it is on; see [Perform Mode](#perform-mode)), then *Toolbar tool docs…*, *Documentation*, *Website* and *Support FNSTools on Patreon* |
| **Drop a panel COMP on it** | registers it into a surface; see [Drop to register](#drop-to-register) |

From Python, `op.FNS_HUBREGISTRY.Open()` opens the hub; `Open(tab='navbar')`
lands on a tab by its canonical name (`toolbar`, `navbar`, `mainmenu`,
`console`, or a contributed one). The quick-launch palette offers *Open FNS
Hub*, *Open main-menu configurator* and *Toggle FNSTools perform mode*.

## The tabs

- **Toolbar**: reorder, group, hide/show and add dividers between the
  widgets on TD's bookmark bar; drag rows, right-click a name for its docs.
- **Navbar**: the pane bars: reorder, flip an item between the left and
  right side, show/hide, group.
- **MainMenu**: the main-menu bar, TD's own items included, so your entries
  can sit between them; the *TD* button restores TD's original order.
- **OpMenu**: what the tools contribute to TD's OP Create dialog (search
  words, row decorations, right-click items, filters): reorder them, switch
  a contribution off without uninstalling its tool.
- **Overlay**: everything tools draw on the network editor
  ([OverlayRegistry](/docs/fns-overlayregistry/)). Layers, such as Cook Bar's
  bars and QuickMarks' outlines, come first, bottom layer first; then the
  corner lists, corner by corner. Drag rows to reorder, click **Show** to hide
  or show one (hiding never switches its tool off), click **Corner** to move
  a list to the next corner and **Margin** to set its distance from the edges.
  A tool that is off reads *(off)* and draws nothing whatever Show says. Every
  change lands on the tool's own parameters.
- **Console**: the toolkit's web front (settings, install & remove, tabs
  tools contribute) rendered inside the hub; its browser only runs while
  this tab is shown.
- **Commands**: every command the command registry serves, hidden ones and
  TouchDesigner's built-ins included, with its tool and context; star and
  hide from here, and your choice beats the tool's default. Contributed by
  [CommandPalette](/docs/fns-commandpalette/).
- **Tool tabs**: the larger tool UIs that used to live in the `Fx`
  tools panel: oscMapper, ExprHotStrings, GlobalOutSelect, SearchWords
  (OpMenu's keyword table), midiMapper and OpColor (ColorUI's palette
  editor). Exactly the ones you have installed.

**Right-click a tab** to open the owning tool's parameters; that is where
the mappers are configured. The bar comes in two styles (*Tab Bar* on the
hub's Hub page, roams with your settings): **Rows** wraps fixed-width tabs
into as many rows as needed; **Strip** is TouchDesigner's single-row folder
tabs with scroll arrows and a dropdown. Drag a tab onto another tab to reorder
in either style. Neither style has a close button. Hide a tab from the contributing tool's *Shown in Hub*
parameter on its Registry page, and bring any hidden tab back from the FNS
button's right-click menu ("Show …"). Tab order and the active tab roam with
your settings through [ConfigRegistry](/docs/fns-configregistry/), as do
the three configurators' layouts. A tool carrying a *Refresh* pulse is
refreshed every time its tab is shown.

## Perform Mode

Many FNS tools exist for building: they draw on the network editor, watch
the mouse and the panes, and keep themselves ready while you work. During a
show none of that helps, and some of it costs frame time even when nothing
on screen shows it. **Perform Mode** switches all of it off at once.

Switch it from any of these:

- the FNS button's right-click menu, **FNSTools Perform Mode**
- the quick-launch palette, *Toggle FNSTools perform mode*
- **Perform Mode** on the FNSTools page of the `/FNSTools` root

While it is on, the FNS button turns red and its tooltip says how to switch
it off, so a project that opens performing explains itself.

**What stops:** Cook Bar, QuickMarks' pins and list, POP Overlay and the
network overlay that shows them; the Radial Menu, which does not open; the
scene changers' *Cook While Editing*, so only the show's scenes cook;
Autosave, while its *Skip In Perform Mode* is on; HydroHomie's reminders;
the operator family's update checks; and the small watchers behind
hovering, dragging and the window title. The toolkit's log waits and
catches up when you switch back, errors included.

**What keeps running:** everything a show uses, such as BeatMod, the scene
changers' switching, Remote, Output, the family operators you placed, and
the MIDI and OSC mappers.

No tool setting changes. Each tool keeps its own on/off and display
settings, so switching Perform Mode off brings back exactly what was on.

**Follow TD Perform Mode**, next to it on the root (on by default), turns
Perform Mode on when you enter TouchDesigner's Perform Mode (F1) and puts
it back to what it was when you leave. Switch following off if you want the
two to stay separate. Both settings are saved with the project and never
carried to other projects, so a show file can open ready to perform. The
guide [Working with FNSTools in your project](/docs/guides/working-in-your-project/#performing-a-show)
covers it from the show side.

## Drop to register

Drop any panel COMP on the FNS button (or anywhere on the hub window). The hub
offers every surface that can take it (Toolbar, Navbar, Main Menu) in a
small menu; pick one and the COMP receives a self-registering host of that
surface's registry, placed after the bar's last entry, and appears on the bar
immediately. A COMP that should live on two surfaces is dropped twice. The
COMP stays where it is and publishes into the registry, exactly like every
shipped tool.

## Contributing a tab

A tool that wants a tab in the hub carries a stamped `FNS_HubRegistry` host
(drop the tool on nothing; stamp it from the registry master with
`op.FNS.op('FNS_HubRegistry').StampHost(tool, canonical_name='mytool')`, or copy
the host out of any shipped tool). Its Registration page names what the tab
shows: the tool itself or any panel inside it (mirrored into the hub, so the
tool can live anywhere), a DAT/CHOP/TOP/SOP/POP (shown through an OP Viewer),
or a parameter page of the tool. The host registers itself when it
initializes, so a tool added while the hub is open
simply appears. The developer-facing contract is
[docs/HubContract.md](https://github.com/function-store/FunctionStore_tools/blob/main/docs/HubContract.md).
