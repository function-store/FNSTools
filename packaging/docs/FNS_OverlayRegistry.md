---
package: FNS_OverlayRegistry
summary: One overlay over the network editor you are working in, composited from every tool that draws there, shown above the nodes without touching your network.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Arranging the overlay
    anchor: arranging-the-overlay
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Stack every tool's drawing in one overlay
    anchor: why-use-it
    does: 'Stacks every tool''s drawing into one image shown above the nodes of the network editor you work in; with nothing drawing, nothing runs.'
  - name: Follows the view
    anchor: how-to-use-it
    does: 'Pan, zoom or open another network and the overlay follows, keeping everything in place at any zoom and sharp on high DPI screens.'
  - name: Leaves your network untouched
    anchor: how-to-use-it
    does: 'Switches no display flag, dims no annotation, and is taken out before every project save.'
  - name: Corner widgets
    anchor: arranging-the-overlay
    does: Tools can pin small clickable panels to a corner of the network editor that keep their size at any zoom and stack without overlapping.
  - name: Manage layers and widgets in Hub
    anchor: arranging-the-overlay
    does: 'FNS_Hub''s Overlay tab lists every layer and widget: reorder them, hide one without switching its tool off, or move a widget to another corner.'
  - name: Publish a layer
    anchor: for-tool-authors
    does: 'A tool hands over one TOP through a host copy of the registry, or from Python with RegisterWidget(), and the registry composites it with the rest.'
    authors: true
  - name: View data for layers
    anchor: for-tool-authors
    does: 'The View page and View() give the covered network rectangle, render resolution, units per pixel and zoom; NetworkToPixel() converts network positions to pixels.'
    authors: true
  - name: Panel widget API
    anchor: for-tool-authors
    does: RegisterPanelWidget() pins a tool's panel COMP to a corner with an order and margin; UnregisterPanelWidget() takes it away.
    authors: true
---

## Why use it

Some tools draw over the network editor: Cook Bar's bars above every
operator, QuickMarks' outlines, POP Overlay's attribute labels. Drawing there
is awkward in TouchDesigner. Cook Bar's earlier versions showed their image as
the network's background, which meant switching off the display flags of the
network's TOPs and fading its annotations while the bars were on, and putting
it all back afterwards.

The Overlay Registry gives these tools one shared surface. Each tool renders
its own image; the registry stacks them into one, fits it over the network you
are looking at, and shows it above the nodes. Your network is left as it is.

## How to use it

There is nothing to set up. The registry installs with the tools that draw on
the network editor, such as [Cook Bar](/docs/cookbar/) and
[QuickMarks](/docs/quickmarks/), and is promoted to `/sys` (global shortcut
`op.FNS_OVERLAYREGISTRY`) like the toolkit's other registries.

Switch one of those tools on and its drawing appears over the network editor
you work in:

- **It follows you.** Pan, zoom or open another network and the overlay
  follows. Everything stays where it belongs at any zoom, and lines stay sharp
  on high DPI screens.
- **Your network is left alone.** No display flag is switched, no annotation
  is dimmed, and the overlay is not one of your operators. It is taken out
  before every project save, so it never ends up in your file.
- **It costs nothing when idle.** With nothing drawing, there is no overlay at
  all and nothing runs.

## Arranging the overlay

Besides drawing, tools can pin a small panel you can click to a corner of the
network editor, such as Cook Bar's Top List or QuickMarks' mark list. A widget
keeps its size on screen at any zoom and stays in its corner as you pan or
change networks. Widgets in the same corner stack without overlapping.

The **Overlay** tab of [FNS_Hub](/docs/fns-hub/) lists every layer and every
corner widget in one place:

- **To change which drawing sits on top**, reorder the layers.
- **To hide one tool's drawing for a while**, hide it there. The tool keeps
  running; only its layer or widget leaves the screen.
- **To move a corner list out of the way**, give it another corner, or a
  different margin. The margin is how far the widget sits from the edges of
  the network editor, and from the widget before it when several share a
  corner.

The settings stay with each tool, on its own parameters, so they travel with
your other FNSTools settings.

## For tool authors

This section is for people writing their own tools that draw on the network
editor.

### Publishing a layer

A tool hands over one TOP, its layer. The registry composites it with every
other layer and shows the result. What the layer draws is entirely up to the
tool.

To publish a layer, ship a small **host** copy of this registry in the tool.
Its Registration page names the layer TOP (**Layer TOP**), a canonical name,
its stacking order (**Layer Order**: higher draws on top), whether the user
shows it (**Displayed**, a plain switch that never turns the tool off) and
whether the tool is drawing (**Layer Active**, which follows the tool's
**Active** unless you point it at something else). The layer is drawn only
when both are on.

Pick the order by what the layer draws:

| Layer Order | For |
|---|---|
| 0 to 99 | fills and heat maps |
| 100 to 199 | marks on operators (Cook Bar's bars are 100) |
| 200 to 299 | labels and text |
| 300 and up | cursors |

Users can change it per tool with **Layer Order** on the tool's Registry page.

Without a host, the same can be done from Python:

```python
op.FNS_OVERLAYREGISTRY.RegisterWidget(top, 'mytool', order=10)
op.FNS_OVERLAYREGISTRY.UnregisterWidget('mytool')
```

### Drawing in the right place

In return the registry tells the layer where it is drawing. Its **View** page
holds the rectangle the overlay covers in network units (`Viewx0`, `Viewy0`,
`Viewx1`, `Viewy1`), the resolution to render at (`Resolutionw`,
`Resolutionh`), network units per pixel, pixels per screen point, the
editor's zoom and the network being viewed. Bind a shader's uniforms and the
layer's resolution to those parameters and the layer recooks only when the
view moves.

From Python, `View()` returns the same values as a dict, and
`NetworkToPixel(x, y)` turns a network position into layer pixels.
`Cursor()` gives the mouse position over a network editor as
`(network, x, y)` in network units, or `None` when the mouse is over none.

Render the layer premultiplied and transparent wherever it draws nothing. It
sits above the nodes, so leave the node tiles clear.

### Corner widgets

A widget is a panel COMP of your tool, shown at its own size:

```python
op.FNS_OVERLAYREGISTRY.RegisterPanelWidget(panel, 'mytool', anchor='topleft', order=100, margin=12)
op.FNS_OVERLAYREGISTRY.UnregisterPanelWidget('mytool')
```

- **anchor** is the corner: `topleft`, `topright`, `bottomleft` or
  `bottomright`.
- **order** places the widget in its corner's stack, lowest nearest the
  corner, using the same bands as layers.
- **margin** is its distance from the edges and from the widget before it, in
  screen points.

Offer the corner and the margin as parameters of your tool and register again
when they change. The whole panel takes clicks, so keep it small.
