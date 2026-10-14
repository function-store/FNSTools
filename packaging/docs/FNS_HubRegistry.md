---
package: FNS_HubRegistry
summary: 'The registry behind Hub''s tab bar: tools contribute native panels, viewers or parameter pages as hub tabs. The raw master, promoted to /sys.'
features:
  - name: Hub Registry
    anchor: hub-registry
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Self-healing Hub tabs
    anchor: hub-registry
    does: 'Keeps one entry per Hub tab with label, order and visibility, injects a mirror or viewer for each, and prunes tabs whose tool is gone.'
  - name: Hidden tabs stay hidden
    anchor: for-tool-authors
    does: 'Closing a tab in Hub writes Shown in Hub back to its host, so a hidden tab stays hidden across projects.'
  - name: Contribute a tab through a host
    anchor: for-tool-authors
    does: 'A host copy names the tab: the tool''s own panel, a mirrored panel COMP, or an OP Viewer of a DAT/CHOP/TOP/SOP/POP.'
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
    does: An extension implementing OnHubExposure(exposed) learns when its tab is shown; a palette Web Browser has its Active switched for it.
    authors: true
---

## Hub Registry

The raw registry that decides what [Hub](/docs/fns-hub/) shows: one entry
per tab, with its label, order, visibility and what it renders. The hub itself
draws whatever this registry says, and the registry
injects one mirror or viewer per entry into the hub's tab area, prunes the ones
whose tool is gone, and heals the rest.

It ships as its own core package, promoted to `/sys` (global shortcut
`op.FNS_HUBREGISTRY`), alongside the six surface registries,
[Console](/docs/fns-console/) and [Updater](/docs/fns-updater/). The hub
is its UI.

## For tool authors

A tool that wants a hub tab ships a small **host** copy of this registry and
registers itself on load, the same shape as a toolbar or navbar entry. The
host's Registration page names the tab:

- **Tool COMP**: the contributing tool (defaults to the host's parent).
- **Tab Content**: what to show: empty for the tool itself (it must be a
  panel), a panel COMP inside the tool (mirrored, so it can live anywhere), or a
  DAT/CHOP/TOP/SOP/POP (an OP Viewer).
- **Tab Parameters**: a page scope instead: a Parameter COMP view of the tool
  (`*` for every page).
- **Show in Hub / Shown in Hub / Tab Label / Tab Order / Help URL**: the usual
  publishing controls; *Shown in Hub* is what the hub's close button writes
  back to, so a hidden tab stays hidden across projects.

From Python, `op.FNS_HUBREGISTRY.RegisterTab(comp, 'mytool', content=panel,
label='My Tool', order=50)` does the same; `Tabs()`, `SetTabDisplayed()`,
`Open(tab=)` and `OpenDocs()` are the rest of the API. A component that must
know when its tab is shown (a Web Render, say) implements
`OnHubExposure(exposed)` on its extension; a palette Web Browser has its
*Active* switched for it.
