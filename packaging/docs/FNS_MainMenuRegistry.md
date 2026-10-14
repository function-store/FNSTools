---
package: FNS_MainMenuRegistry
summary: 'TD main-menu surface registry, including project-name display. The raw master, promoted to /sys.'
features:
  - name: Main Menu Registry
    anchor: main-menu-registry
feature_list:
  - name: 'Order, hide and place entries'
    anchor: main-menu-registry
    does: 'Holds the order, visibility and left/right placement of every main-menu entry, TD''s own built-in items and tool-published ones alike.'
  - name: Edit from the Hub MainMenu tab
    anchor: main-menu-registry
    does: 'The MainMenu tab of Hub, opened from the FNS button in the bar, reorders, hides or groups entries, TD''s own items included.'
  - name: Publish an entry from a tool
    anchor: main-menu-registry
    does: 'A tool ships a small host copy of the registry beside its widget to get a main-menu entry, reachable globally as op.FNS_MAINMENUREGISTRY.'
    authors: true
---

## Main Menu Registry

The raw registry that manages TouchDesigner's main-menu bar as a single surface: order, visibility and left/right placement of every entry, both TD's own built-in items (wiki, forum, tutorials, fps, etc.) and the ones tools publish, live here in one place.

It ships as its own core package, promoted to `/sys` (global shortcut `op.FNS_MAINMENUREGISTRY`), one of the toolkit's six surface registries, which together with [Console](/docs/fns-console/), [Hub](/docs/fns-hub/) and [Updater](/docs/fns-updater/) make up the always-installed core. A tool that wants a main-menu entry, for example [BorderlessTD](/docs/fns-borderlesstd/)'s project-name display or the hub's own **FNS** button, ships a small host copy of this registry alongside its widget. Open the **MainMenu** tab of [Hub](/docs/fns-hub/#the-tabs) (the FNS button in the bar) to reorder, hide or group entries, TD's own items included.
