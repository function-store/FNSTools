---
package: FNS_PaletteRegistry
summary: 'Contribute tabs to TouchDesigner''s Palette Browser: a tool publishes a native panel COMP and it appears beside the stock Palette tab, sized to the slot and notified on every tab change.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: For tool authors
    anchor: for-tool-authors
  - name: Several tabs from one tool
    anchor: several-tabs-from-one-tool
feature_list:
  - name: Tabs in the Palette Browser
    anchor: why-use-it
    does: 'Adds a tab strip above the Palette Browser''s list, with TouchDesigner''s own Palette tab first and one tab per contributed panel.'
  - name: Stock palette left intact
    anchor: why-use-it
    does: 'With nothing contributed the palette stays as TouchDesigner ships it; the strip appears with the first registration and goes with the last.'
  - name: Switch back to the Palette tab
    anchor: how-to-use-it
    does: 'SearchPalette''s `Ctrl+Shift+F` switches to the stock Palette tab before focusing its search field; other tools can call ShowTab(''palette'') the same way.'
  - name: Register a tab from a host
    anchor: for-tool-authors
    does: 'A tool ships a small host copy whose Registration page sets the tab''s tool, canonical name, panel, label, order and visibility.'
    authors: true
  - name: Tab API from Python
    anchor: for-tool-authors
    does: 'RegisterTab(), Tabs(), SetTabDisplayed(), ShowTab(), CurrentTab() and UnregisterTab() on op.FNS_PALETTEREGISTRY manage tabs from code.'
    authors: true
  - name: Tab change callback
    anchor: for-tool-authors
    does: 'An optional Callbacks DAT gets onPaletteTab(canonical, previous) on every tab change.'
    authors: true
  - name: Panels fitted to the slot
    anchor: for-tool-authors
    does: 'A registered panel is resized to the slot, restored when the tab goes away, and keeps its state across tab switches, Web Render included.'
    authors: true
  - name: Extra tabs from one tool
    anchor: several-tabs-from-one-tool
    does: 'The Extra Tabs sequence adds one tab per block, and a block without its own panel reuses the first tab''s panel.'
    authors: true
---

## Why use it

The Palette Browser is a natural home for a tool that wants a column of its
own beside the network. TouchDesigner even leaves a 32 pixel strip free above
the component list, exactly the height of a row of folder tabs. But it is one
dialog, and any tool that injects its own tab row there claims the same strip
and the same slot as every other tool doing it, so two of them end up stacked
on top of each other.

PaletteRegistry owns that strip. It puts one row of tabs there:
TouchDesigner's own *Palette* first, then one tab per contribution, each
showing a panel from the tool that published it. The stock palette stays where
it is, as it is: the registry loads TouchDesigner's own `folderTabs` widget
into the free row and shows each contributed panel through a Select COMP
mirror. The stock panels only have their display flag switched off while a
contributed tab is in front.

**With nothing contributed, the palette stays exactly as TouchDesigner ships
it.** The strip and its mirrors appear with the first registration and
disappear with the last.

## How to use it

The registry is part of the toolkit's core and installs with it. Once a tool
contributes a tab, the strip appears above the palette list:

- Click a tab to show that tool's panel, and **Palette** to get the stock list
  back.
- [SearchPalette](/docs/fns-searchpalette/)'s `Ctrl+Shift+F` switches to the
  Palette tab before it focuses the palette's search field, because that field
  lives in the stock list a contributed tab hides.
- To hide a tab, switch off **Shown in Palette** on the contributing tool's
  **Registry** page. The registry writes its own changes back there too, so a
  hidden tab stays hidden with the tool. **Tab Order** and **Tab Label** on the
  same page move and rename it.

TouchDesigner's UI is never saved with a project, so the strip is rebuilt on
every open from whatever is registered.

## For tool authors

A tool that wants a palette tab ships a small host copy of this registry, the
same shape as a toolbar or navbar entry. Drop the panel COMP on the FNS button
and pick **Palette tab**, or copy a host out of a shipped tool.

The host's Registration page names the tab. It belongs to the **Tool COMP**
(the host's parent by default) and shows the **Tab Panel** (the tool itself
by default). Its unique name is **Canonical Name**, or the tool's name when
that is empty; `palette` is TouchDesigner's own tab and is rejected. To react
to tab changes, point **Callbacks DAT** at a DAT with
`onPaletteTab(canonical, previous)`. **Expose in Palette** publishes the tab
while the tool exists, and **Shown in Palette**, **Tab Label** and **Tab
Order** are the usual publishing controls.

From Python, guarded, since no registry is guaranteed to exist:

```python
reg = getattr(op, 'FNS_PALETTEREGISTRY', None)
if reg is not None:
	reg.RegisterTab(comp, 'mytool', panel=panel, label='My Tool', order=20)
```

`Tabs()`, `SetTabDisplayed()`, `ShowTab()`, `CurrentTab()` and
`UnregisterTab()` are the rest of the API. Any tool whose UI is hidden by a
contributed tab can call `ShowTab('palette')` the way SearchPalette does.

The callback fires on every tab change for every registered tab, so check the
name before you act. It is raise-contained:

```python
def onPaletteTab(canonical, previous):
	# canonical: the tab now in front ('palette' is TouchDesigner's own)
	# previous: the tab that was in front before
	if canonical == 'mytool':
		...
```

**Your panel is resized while it is registered.** A Select COMP cannot push
its size into its source, so the registry rewrites the panel's width and
height to slot expressions and restores the originals when the tab goes away.
Leave those two parameters alone while it is registered.

The panel keeps its state across tab switches, a Web Render's browser process
included, because the mirrors are views of the same panel.

## Several tabs from one tool

The Registration parameters define the first tab; the **Extra Tabs** sequence
on the same page adds one more per block:

- A block's **Canonical Name** left empty means no tab, which is how a block
  stays inert (TouchDesigner always keeps at least one block in a sequence).
- A block's **Tab Panel** left empty reuses the first tab's panel. That is how
  one panel serves several tabs: register them all, then route on
  `onPaletteTab`.
- A block's **Tab Label**, **Tab Order** and **Shown in Palette** work as
  above.

A block with a bad or duplicate name is reported in **Registration Status**
and skipped; it never costs the tool its first tab.
