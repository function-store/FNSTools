# The registries

A registry is a service every tool can publish into instead of a surface
hardcoding its contents. Each registry package in the toolkit root is a
master; while the toolkit runs, one copy of each is promoted into
`/sys/FNS_Registries` and that copy is the global, reached by its shortcut.
The shortcut is the address: the promoted copy may be replaced by a newer
version at any time, so a path into `/sys` is never stable while the shortcut
always is. The registry packages are core and always installed, except
`FNS_OverlayRegistry`, which a package that draws an overlay requires.

| Registry | Global | Owns | A tool joins with |
|---|---|---|---|
| `FNS_ConfigRegistry` | `op.FNS_CONFIGREGISTRY` | The aggregated settings file: one section per registered tool, persisted globally in `<user palette>/FNSTools/config/FNStools_config.json` or inside the `.toe` under project scope | `RegisterTool(comp, canonical_name, callback=None, autoload=True, persist_pars=True, exclude_pars='', exclude_pages='', source_registry=None)` |
| `FNS_ToolbarRegistry` | `op.FNS_TOOLBARREGISTRY` | The toolbar: widgets mirrored into TouchDesigner's bookmark bar, their order, width and visibility, dividers | `RegisterWidget(widget_op, canonical_name, order=None, display=True, callback=None, source_registry=None, width=None, help_url=None)` |
| `FNS_NavbarRegistry` | `op.FNS_NAVBARREGISTRY` | The pane bars: an item stamped into every network editor pane's bar, left or right | `RegisterWidget(widget_op, canonical_name, order=None, side=None, kind=None, display=True, callback=None, source_registry=None, width=None, help_url=None)` |
| `FNS_MainMenuRegistry` | `op.FNS_MAINMENUREGISTRY` | TouchDesigner's main-menu bar: ordered entries, left or right, anchored to a stock item | `RegisterWidget(widget_op, canonical_name, order=None, side=None, display=True, callback=None, source_registry=None, width=None, help_url=None, anchor=None)` |
| `FNS_OpMenuRegistry` | `op.FNS_OPMENUREGISTRY` | The OP Create dialog: search words, row decorations, right-click items, filter stages and the op alternatives | `RegisterContributor(comp, canonical_name, callback=None, order=None, display=True, source_registry=None, help_url=None, panel=None, panel_anchor=None)` |
| `FNS_PaneTypeRegistry` | `op.FNS_PANETYPEREGISTRY` | The pane-type menu of every pane bar: named entries any COMP can appear as, recalled with owner, type and flags | `RegisterPanel(panel_op, canonical_name, pane_type=None, action=None, set_owner=None, change_type=None, maximize=False, tear_away=False, float_pane=False, open_parameters=False, callback=None, source_registry=None, menu_order=None)` |
| `FNS_Console` | `op.FNS_CONSOLE` | The toolkit's web front, served from inside the project: the settings page, the install picker and any tab a tool contributes | `RegisterTab(comp, canonical, page=None, api_dat=None, label='', order=50, displayed=True, source_registry=None)` |
| `FNS_HubRegistry` | `op.FNS_HUBREGISTRY` | The Hub's tab bar: native panels, viewers and parameter pages shown as tabs of the manager window | `RegisterTab(comp, canonical, content=None, params='', label='', order=50, displayed=True, help_url='', source_registry=None)` |
| `FNS_PaletteRegistry` | `op.FNS_PALETTEREGISTRY` | TouchDesigner's Palette Browser: a native panel COMP shown as a tab beside the stock Palette tab | `RegisterTab(comp, canonical, panel=None, label='', order=50, displayed=True, callback=None, source_registry=None)` |
| `FNS_TimelineRegistry` | `op.FNS_TIMELINEREGISTRY` | TouchDesigner's timeline dialog: tool-owned panels in two zones beside the stock transport | `RegisterWidget(widget_op, canonical_name, order=None, display=True, callback=None, source_registry=None, width=None, height=None, help_url=None, zone=None)` |
| `FNS_PaneSearchRegistry` | `op.FNS_PANESEARCHREGISTRY` | The find bar of every network editor pane: a control beside the bar's own Home toggle, one copy per pane | `RegisterWidget(widget_op, canonical_name, order=None, display=True, callback=None, source_registry=None)` |
| `FNS_OverlayRegistry` | `op.FNS_OVERLAYREGISTRY` | One overlay composited over the network editor the user works in, from a layer TOP per tool, plus small panels pinned to a corner | `RegisterWidget(widget_op, canonical_name, order=None, display=True, callback=None, source_registry=None, active=True)` for a layer, `RegisterPanelWidget(panel, canonical, anchor='topleft', order=None, margin=None, shown=True, active=True, tool=None, pars=None)` for a pinned panel |
| `FNS_CommandRegistry` | `op.FNS_COMMANDREGISTRY` | The quick-launch commands every tool declares, served to the command palette and the TDX launcher | `Register(owner, commands=None)`, normally through the `FNSCommand.announce(comp)` call in the tool's extension |

Every method above is a promoted method of the global; `references/<Registry>.md`
lists each registry's full promoted API with the first line of every
docstring, and its parameters.

## What a consumer reads

- A registry is the authority for its surface. A consumer reads the surface
  through the registry's promoted methods and registers through them; it
  does not write into the registry's tables, the stamped mirrors in
  TouchDesigner's UI, or the settings file.
- The manager side of each surface registry is the same on all of them:
  `Groups()`, `CreateGroup`, `RenameGroup`, `RemoveGroup`, `SetGroupVisible`
  and `ToggleGroup` manage named groups of entries; `SetWidgetDisplay`,
  `SetWidgetOrder`, `SetWidgetWidth` and `SetTabDisplayed` change one entry;
  `Widgets` or `Tabs()` is the live snapshot of the entries. The Hub's
  configurator tabs are the UI over these calls.
- `op.FNS_COMMANDREGISTRY.Commands()` is the live command list and
  `Run(key)` runs one; `references/commands.md` is the same list as built.
- `op.FNS_CONFIGREGISTRY.SaveAll()` and `LoadAll()` snapshot and re-apply
  every registered tool's settings; `SetConfigScope('global' | 'project',
  prompt=False)` moves them between the machine file and the project.
- `op.FNS_OPMENUREGISTRY.Alternatives` is the merged map of op alternatives
  and `PlaceAlternative(orig_op, alternative)` places one.

## How a tool carries its registration

A tool that publishes into a registry carries a host: a child COMP named
after the registry (a tool with a toolbar button has a child
`FNS_ToolbarRegistry`), stamped from the master. The host registers the tool
with the global when the project opens. The tool's own parameter dialog has
a page named `Registry` with one section per registry it publishes into, each
parameter carrying a two-letter prefix for its registry (`Cf` for the config
registry, `Tb` for the toolbar, `Hb` for the Hub, ...). The section's
parameters are the registration itself: `Autoregister` (register when the
project opens), the `Register` and `Unregister` pulses, `Regstatus`
(read-only), and the surface's own settings, such as `Displayed`,
`Menuorder`, `Align`, `Tablabel` or `Taborder`. Those parameters are
persisted by the config registry like any other, so a user's arrangement of
the surfaces follows them between projects.

A package page's `surfaces` line (Toolbar button, Pane bar button, Main menu
entry, OP Create menu entry, Custom pane type, Hub tab, Console tab, Timeline
panel, Find bar control, Network editor overlay) is the list of registries
the package hosts; `Requires` names the registry packages it needs installed.
