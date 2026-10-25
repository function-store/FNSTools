---
package: FNS_HubRegistry
summary: 'The registry behind Hub''s tab bar: tools contribute native panels, viewers or parameter pages as hub tabs. The raw master, promoted to /sys.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Self-healing Hub tabs
    anchor: why-use-it
    does: 'Keeps one entry per Hub tab with its label, order and visibility, puts a mirror or viewer in the hub for each, and removes tabs whose tool is gone.'
  - name: Arrange tabs
    anchor: how-to-use-it
    does: 'Drag a tab onto another tab to reorder them; the order roams with your settings.'
  - name: Rename a tab
    anchor: how-to-use-it
    does: 'Tab Label on the tool''s Registry page gives its tab a different label.'
  - name: Hide a tab
    anchor: how-to-use-it
    does: 'Hiding a tab is written back to its tool''s Shown in Hub parameter, so it stays hidden across projects until you show it again.'
  - name: Contribute a tab through a host
    anchor: for-tool-authors
    does: 'A host copy names the tab: the tool''s own panel, a panel inside the tool, or an OP Viewer of a DAT, CHOP, TOP, SOP, POP or MAT.'
    authors: true
  - name: Parameter page tabs
    anchor: for-tool-authors
    does: 'Tab Parameters shows a Parameter COMP view of chosen pages of the tool, or every page with `*`, as a Hub tab.'
    authors: true
  - name: Python tab API
    anchor: for-tool-authors
    does: 'RegisterTab(), Tabs(), SetTabDisplayed(), Open(tab=) and OpenDocs() register, list, show and open Hub tabs from Python.'
    authors: true
  - name: Tab exposure callback
    anchor: for-tool-authors
    does: 'An extension implementing OnHubExposure(exposed) learns when its tab is shown; a palette Web Browser has its Active switched for it.'
    authors: true
---

## Why use it

[Hub](/docs/fns-hub/) is one window with a tab per concern: the toolbar,
navbar and main-menu configurators, the console, and the larger UIs of tools
such as [oscMapper](/docs/oscmapper/) and [midiMapper](/docs/midimapper/).
For that to work, the window has to know which tabs exist. If the hub kept its
own list, or searched the project for tools, every new tool would mean
changing the hub, and a removed tool would leave a dead tab behind.

HubRegistry turns that around. Each tool says what its tab shows, and the hub
draws whatever the registry holds: one entry per tab, with its label, order,
visibility and content. The registry puts one mirror or viewer per entry into
the hub's tab area, removes the ones whose tool is gone and repairs the rest,
so the tabs you see are exactly the tools you have installed.

## How to use it

The registry is part of the toolkit's core and installs with it. Everything
you do with it happens in Hub (left-click the **FNS** button at the right end
of the main-menu bar):

- **Reorder:** drag a tab onto another tab.
- **Docs and settings:** right-click a tab. *Parameters* opens the owning
  tool's parameters, which is where the mappers are configured, and
  *Documentation* opens its help page when the tool has one.
- **Hide a tab:** switch off **Shown in Hub** on the tool's **Registry** page.
  The hub writes its own changes back to that same parameter, so a hidden tab
  stays hidden across projects. Bring it back from the FNS button's
  right-click menu, which lists a *Show* entry for every hidden tab.
- **Rename a tab:** set **Tab Label** on the same page.
- **Keep a tool out of the hub entirely:** switch off **Show in Hub**. The tool
  shows nothing in the hub, and its panel stays wherever it lives.

The tool's Registry page settings are listed under
[What it adds to a registered tool](#registry-section). Tab order and the
active tab roam with your settings.

## For tool authors

A tool that wants a hub tab ships a small host copy of this registry and
registers itself on load, the same shape as a toolbar or navbar entry. To get
one:

- Drop the panel COMP on the FNS button, or anywhere on the Hub window, and
  pick **Hub tab**.
- Or stamp it: `op.FNS.op('FNS_HubRegistry').StampHost(tool, canonical_name='mytool')`.
- Or copy the host out of any shipped tool.

The host's Registration page names the tab. **Tool COMP** is the contributing
tool (the host's parent by default), and **Canonical Name** a unique name made
of letters, digits, `_` and `-`. What the tab shows:

| Set on the host | The tab shows |
|---|---|
| **Tab Content** empty | the tool itself, which must be a panel, mirrored through a Select COMP |
| **Tab Content** = a panel COMP inside the tool | that panel, mirrored, so the tool can live anywhere |
| **Tab Content** = a DAT, CHOP, TOP, SOP, POP or MAT | an interactive OP Viewer of it |
| **Tab Parameters** = a page scope, such as `Settings`, or `*` | a Parameter COMP view of the tool's pages |

**Tab Parameters** wins over **Tab Content**. **Help URL** adds the
*Documentation* item to the tab's right-click menu.

A mirror shows a panel at the panel's own size. To make a tool panel fill the
tab area, bind its width and height to `op.FNS.op('FNS_Hub/panel/tabs')`, with
the panel's standalone size as the fallback when there is no hub.

From Python, `op.FNS_HUBREGISTRY.RegisterTab(comp, 'mytool', content=panel,
label='My Tool', order=50)` does the same. The full signature:

```python
op.FNS_HUBREGISTRY.RegisterTab(comp, canonical, content=None, params='', label='',
                               order=50, displayed=True, help_url='', source_registry=None)
```

A registration that cannot work is rejected with a `debug()` line and no
exception: no tool COMP, an empty canonical name or one with other
characters, content that is neither a panel nor a viewable operator, or
content that is gone. `UnregisterTab()`, `Tabs()`, `SetTabDisplayed()`,
`Open(tab=)` and `OpenDocs()` are the rest of the API; `Open(tab='navbar')`
opens the hub on a tab by its canonical name.

**Knowing when your tab is shown.** Only the tab in front is live. When a tab
is shown or hidden, the hub calls `OnHubExposure(exposed)` on the component's
extension if it defines one, which a component holding a Web Render needs.
Without the hook, a component with `Active` and `Address` parameters (a
palette Web Browser) has its `Active` switched for it. A component with a
`Refresh` pulse is pulsed each time its tab is shown.
