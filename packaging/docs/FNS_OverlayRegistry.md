---
package: FNS_OverlayRegistry
summary: One overlay over the network editor you are working in, composited from every tool that draws there, shown above the nodes without touching your network.
features:
  - name: Overlay Registry
    anchor: overlay-registry
  - name: Widgets
    anchor: widgets
  - name: Managing the overlay
    anchor: managing-the-overlay
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: One shared overlay
    anchor: overlay-registry
    does: 'Stacks every tool''s layer into one image shown above the nodes of the network editor you work in; with nothing drawing, nothing runs.'
  - name: Follows the network editor view
    anchor: overlay-registry
    does: 'The overlay follows pan, zoom and network changes, keeps everything in place at any zoom and stays sharp on high DPI screens.'
  - name: Leaves your network untouched
    anchor: overlay-registry
    does: 'Switches no display flag, dims no annotation, is not one of your operators and is taken out before every project save.'
  - name: Corner widgets
    anchor: widgets
    does: Tools can pin small clickable panels to a corner of the network editor that keep their size at any zoom and stack without overlapping.
  - name: Manage layers in Hub
    anchor: managing-the-overlay
    does: 'FNS_Hub''s Overlay tab lists every layer and widget: reorder them, hide one without switching its tool off, or move a widget''s corner or margin.'
  - name: Publish a layer
    anchor: for-tool-authors
    does: 'A tool ships a host copy naming its layer TOP, stacking order and Displayed and Layer Active switches, or calls RegisterWidget() from Python.'
    authors: true
  - name: View data for layers
    anchor: for-tool-authors
    does: 'The host''s View page and View() give the covered network rectangle, render resolution, units per pixel and zoom; NetworkToPixel() converts network positions to pixels.'
    authors: true
  - name: Panel widget API
    anchor: for-tool-authors
    does: RegisterPanelWidget() pins a tool's panel COMP to a corner with an order and margin; UnregisterPanelWidget() takes it away.
    authors: true
---

## Overlay Registry

Some tools draw over the network editor: bars above every operator, outlines,
markers. This registry gives them one shared surface. Each tool renders its
own image; the registry stacks them into one, fits it over the network you
are looking at, and shows it above the nodes.

It follows the network editor you work in. Pan, zoom or open another network
and the overlay follows. Everything stays where it belongs at any zoom, and
lines stay sharp on high DPI screens.

Your network is left as it is: no display flag is switched, no annotation is
dimmed, and the overlay is not one of your operators. It is taken out before
every project save, so it never ends up in your file.

**With nothing drawing, there is no overlay at all and nothing runs.**

Tools that draw overlays install it with them. It is promoted to `/sys`
(global shortcut `op.FNS_OVERLAYREGISTRY`), like the toolkit's other
registries.

## Widgets

Tools can also pin a small panel you can click to a corner of the network
editor, such as Cook Bar's Top List. A widget keeps its size on screen at any
zoom and stays in its corner as you pan or change networks. Widgets in the
same corner stack instead of overlapping.

Each tool sets its widget's corner and margin among its own parameters: the
margin is how far the widget sits from the edges of the network editor, and
from the widget before it when several share a corner.

## Managing the overlay

The **Overlay** tab of [FNS_Hub](/docs/fns-hub/) lists every layer and every
corner widget. Reorder them, hide one without switching its tool off, and
move a widget to another corner or margin there. The settings stay with each
tool, on its own parameters, so they travel with your other FNSTools
settings.

## For tool authors

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

Pick the order by what the layer draws: 0 to 99 for fills and heat maps, 100
to 199 for marks on operators (Cook Bar's bars are 100), 200 to 299 for labels
and text, 300 and up for cursors. Users can change it per tool with **Layer
Order** on the tool's Registry page. From Python,
`op.FNS_OVERLAYREGISTRY.RegisterWidget(top, 'mytool', order=10)` does the
same, with `UnregisterWidget('mytool')` to take it out.

In return the registry tells the layer where it is drawing. Its **View** page
holds the rectangle the overlay covers in network units (`Viewx0`, `Viewy0`,
`Viewx1`, `Viewy1`), the resolution to render at (`Resolutionw`,
`Resolutionh`), network units per pixel, pixels per screen point, the
editor's zoom and the network being viewed. Bind a shader's uniforms and the
layer's resolution to those parameters and the layer recooks only when the
view moves. From Python, `View()` returns the same values as a dict, and
`NetworkToPixel(x, y)` turns a network position into layer pixels.

Render the layer premultiplied and transparent wherever it draws nothing. It
sits above the nodes, so leave the node tiles clear.

A widget is a panel COMP of your tool, shown at its own size:
`op.FNS_OVERLAYREGISTRY.RegisterPanelWidget(panel, 'mytool', anchor='topleft', order=100, margin=12)`
pins it to a corner (`topleft`, `topright`, `bottomleft` or `bottomright`),
and `UnregisterPanelWidget('mytool')` takes it away. **order** places it in
its corner's stack, lowest nearest the corner, using the same bands as
layers. **margin** is its distance from the edges and from the widget before
it, in screen points. Offer the corner and the margin as parameters of your
tool and register again when they change. The whole panel takes clicks, so
keep it small.
