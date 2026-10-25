---
package: FNS_TimelineRegistry
summary: 'Publish a widget into TouchDesigner''s timeline bar: controls in the transport row, a full-width strip in the frame-ruler band that gets its own row, or controls in the Animation editor''s graph heading.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: The three zones
    anchor: the-three-zones
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Stock bar when unused
    anchor: why-use-it
    does: 'With nothing contributed the timeline bar stays stock, and it returns to its stock height when the last widget goes.'
  - name: Background zone adds a row
    anchor: the-three-zones
    does: 'The background zone makes the bar taller by its own height, recomputed from the stock height each time so the bar never creeps taller.'
  - name: Publish widgets to the timeline bar
    anchor: why-use-it
    does: 'A tool publishes a panel COMP and it appears in the timeline bar, shown through mirrors so the stock blocks stay as they are.'
    authors: true
  - name: Transport, ruler and graph-heading zones
    anchor: the-three-zones
    does: 'A widget sits at the right end of the transport row, as a full-width strip under the frame-ruler numbers, or in the Animation editor''s graph heading.'
    authors: true
  - name: Register through a host copy
    anchor: for-tool-authors
    does: 'A tool ships a small host copy whose Registration page names the COMP, canonical name, zone, order and whether it is displayed.'
    authors: true
  - name: Python registration API
    anchor: for-tool-authors
    does: 'RegisterWidget, UnregisterWidget and SetWidgetZone on op.FNS_TIMELINEREGISTRY add, remove and move widgets from Python; the zone settles a frame later.'
    authors: true
---

## Why use it

TouchDesigner's timeline bar is a fixed piece of chrome: the play controls,
the frame ruler and the time settings, laid out exactly as TouchDesigner
draws them. A tool that wants to add to it, say transport buttons for your
media or a filmstrip behind the ruler, would have to copy its panel into the
bar on every launch (TouchDesigner's UI is never saved with a project), find a
spot that does not cover the stock controls, and grow the bar for anything
that needs its own row, then shrink it back exactly when it leaves. Two tools
doing that on their own would trip over each other's sizes.

TimelineRegistry makes the bar extensible. A tool publishes a panel COMP and
it appears in the bar, in a zone it picks, without the tool knowing anything
about the bar's layout. The stock blocks stay where they are, as they are:
contributions are shown through Select COMP mirrors anchored to
TouchDesigner's own blocks, and the registry rebuilds them on every open.

**With nothing contributed, the bar stays stock.** The surface appears with
the first registration and disappears with the last, and the bar returns to
its stock height.

## How to use it

The registry is part of the toolkit's core and installs with it, and there is
nothing to arrange in it directly. You see it through the tools that publish
into the timeline. [TimelineTools](/docs/fns-timelinetools/) is the reference
consumer: its media controls sit in the transport row, its filmstrip and
waveform run in a strip behind the frame ruler, and its controls in the
Animation editor arrive through the graph heading zone.

To show or hide what a tool puts there, use that tool's own settings, such as
TimelineTools' **Show In Timeline Strip** or **Controls In Animation Editor**.

## The three zones

- **transport**: in TouchDesigner's transport row, packed against its right
  end, clear of the stock play controls.
- **background**: a full-width strip in the frame-ruler band, drawn underneath
  the ruler numbers. TouchDesigner's own ruler background is transparent, so
  the strip shows through.
- **graphheading**: in the graph heading of the Animation editor,
  right-aligned.

`background` is a **grow** zone. It makes the bar taller by its own height and
the bar's fixed-height blocks follow, so the transport row keeps its full
height and its controls stay unclipped; the playhead is stretched to span the
taller bar. The bar's height is always recomputed as TouchDesigner's stock
height plus the growth, never added to the height it already has. The
timeline's height is saved in the `.toe` while the registry is not, so
adding to it would make the bar creep taller every session.

There is no zone for the time-properties block on the left. TouchDesigner
stacks three panels there and draws only one of them, so anything placed in
that block would be covered.

## For tool authors

A tool that wants a timeline widget ships a small host copy of this registry,
the same shape as a toolbar or navbar entry. The host's Registration page names
the contribution: the **Widget COMP** (the host's parent by default), a
**Canonical Name**, the **Timeline Zone**, its **Timeline Order** and whether
it is **Displayed**. **Auto-register** keeps it published.

Size the widget for its zone. **Bar Height** at 0 uses the zone's own row
height. The registry sizes your source panel to it, because a mirror shows
the widget at the widget's own size: an oversized source shows only its
top-left corner in the slot. **Bar Width** at 0 follows the widget.

From Python, guarded:

```python
reg = getattr(op, 'FNS_TIMELINEREGISTRY', None)
if reg is not None:
	reg.RegisterWidget(comp, 'mytool', zone='transport', order=20)
```

`UnregisterWidget()` and `SetWidgetZone()` are the rest of the API, and
`RegisterWidget()` also takes `width` and `height`. A zone name the registry
does not know falls back to `transport`. `/sys` is rebuilt on every open, so a
script registration has to run again each time; a host does that for you.

Registration takes a frame: the entry is stored first and its zone arrives
with the host's parameter a frame later, so anything that depends on the
final zone settles a frame later.
