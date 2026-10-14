---
package: FNS_TimelineRegistry
summary: 'Publish a widget into TouchDesigner''s timeline bar: transport controls beside the stock ones, an entry on the time-properties block, or a full-width strip in the frame-ruler band that gets its own row.'
features:
  - name: Timeline Registry
    anchor: timeline-registry
  - name: The three zones
    anchor: the-three-zones
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Stock bar when unused
    anchor: timeline-registry
    does: 'With nothing contributed the timeline bar stays stock, and it returns to its stock height when the last widget goes.'
  - name: Background zone adds a row
    anchor: the-three-zones
    does: 'The background zone makes the bar taller by its own height, recomputed from the base each time so the bar never creeps taller.'
  - name: Publish widgets to the timeline bar
    anchor: timeline-registry
    does: 'A tool publishes a panel COMP and it appears in the timeline bar, shown through mirrors so the stock blocks stay as they are.'
    authors: true
  - name: Three placement zones
    anchor: the-three-zones
    does: 'A widget sits beside the play controls, with the time-properties block, or as a full-width strip under the frame-ruler numbers.'
    authors: true
  - name: Registration host
    anchor: for-tool-authors
    does: 'A tool ships a small host copy whose Registration page names the COMP, canonical name, zone, order and whether it is displayed.'
    authors: true
  - name: Python registration API
    anchor: for-tool-authors
    does: 'RegisterWidget, UnregisterWidget and SetWidgetZone on op.FNS_TIMELINEREGISTRY add, remove and move widgets from Python; the zone settles a frame later.'
    authors: true
---

## Timeline Registry

TouchDesigner's timeline bar is a fixed piece of chrome. This registry makes it
extensible: a tool publishes a panel COMP and it appears in the bar, in a zone it
picks, without that tool knowing anything about the dialog's layout.

The stock blocks stay where they are, as they are. Contributions are shown through Select
COMP mirrors anchored to TD's own blocks, and `/ui` is never saved with a
project, so the whole surface is rebuilt on every load; the registry
re-registers each time.

It ships as its own core package, promoted to `/sys` (global shortcut
`op.FNS_TIMELINEREGISTRY`), alongside the other surface registries.

**With nothing contributed, the bar stays stock.** The surface appears with
the first registration and disappears with the last, and the bar returns to its
stock height.

## The three zones

- **transport**: beside TD's own play controls, in the existing row.
- **properties**: with the time-properties block at the left.
- **background**: a full-width strip in the frame-ruler band, drawn underneath
  the ruler numbers (TD's own ruler background is transparent, so it shows
  through).

`background` is a **grow** zone: it makes the bar taller by its own height and
the bar's fixed-height blocks follow, so the transport row keeps its full height
and its controls stay unclipped. The dialog height is always
recomputed as base plus growth and never incremented; the bar's height is saved in
the `.toe` while `/sys` is not, so an increment-and-restore scheme would creep
taller every session.

## For tool authors

A tool that wants a timeline widget ships a small **host** copy of this registry,
the same shape as a toolbar or navbar entry. The host's Registration page names
the contribution: the tool COMP, a canonical name, the zone, order, and whether
it is displayed.

From Python, `op.FNS_TIMELINEREGISTRY.RegisterWidget(comp, 'mytool',
zone='transport', order=20)` does the same, with `UnregisterWidget()` and
`SetWidgetZone()` as the rest of the API.

Registration takes a frame: the entry is stored first and its zone
arrives with the host's parameter a frame later, so anything that depends on the
final zone settles a frame later.

[TimelineTools](/docs/fns-timelinetools/) is the reference consumer; it uses
`transport` for its own controls and `background` for the media strip.
