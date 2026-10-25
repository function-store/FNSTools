---
package: CookBar
summary: A bar above every operator in the network you are viewing, showing how long it takes to cook and how much GPU memory it holds, so the expensive parts of a network stand out at a glance.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Reading the bars
    anchor: reading-the-bars
  - name: Finding the heaviest operators
    anchor: finding-the-heaviest-operators
  - name: Bars in a big network
    anchor: bars-in-a-big-network
  - name: Global Hog CHOP
    anchor: global-hog-chop
    icon: HogCHOP.png
  - name: Your network stays as it is
    anchor: your-network-stays-as-it-is
feature_list:
  - name: Toggle from the toolbar or quick-launch
    anchor: how-to-use-it
    does: 'Click the toolbar button, run Toggle cook bar from quick-launch or switch Active on; the button lights up while the bars are on.'
  - name: Cook time at a glance
    anchor: reading-the-bars
    does: 'A bar above each operator shows its CPU plus GPU cook time, green to red up to 1 ms and growing taller past it, with stripes while it cooks.'
  - name: GPU memory at a glance
    anchor: reading-the-bars
    does: 'A bar below each operator shows the GPU memory it holds, cyan to blue up to 100 MB and growing taller up to 1 GB.'
  - name: COMP totals
    anchor: reading-the-bars
    does: 'On a COMP, the bars add up the cook time and GPU memory of everything inside it, so you can find the heavy part from the top of a project down.'
  - name: Cooking-off marker
    anchor: reading-the-bars
    does: A COMP whose cooking is switched off gets a grey hatched bar, so a frozen network explains itself.
  - name: Numeric values beside the bars
    anchor: reading-the-bars
    does: 'Each bar can write its number beside it, cook time above the operator and GPU memory below.'
  - name: Top List of the heaviest operators
    anchor: finding-the-heaviest-operators
    does: 'A corner list names the heaviest operators by cook time or GPU memory; click a row to select that operator and zoom to it.'
  - name: Stress test with a Hog CHOP
    anchor: global-hog-chop
    does: 'A global Hog CHOP eats part of every frame on purpose, so you can watch how the network copes; the toolbar button turns red while it runs.'
  - name: Overlay that leaves the network untouched
    anchor: your-network-stays-as-it-is
    does: 'The bars draw on the shared network overlay, which leaves before every save, so display flags, annotations and operators stay as they were.'
---

## Why use it

When a project starts dropping frames, the first question is which operator
is responsible. You can middle-click nodes one by one to read their cook
times, or open the Performance Monitor and work through a list of paths, but
neither shows you where in the network the cost sits. In a busy network that
hunt takes a while, and GPU memory is even harder to see.

Cook Bar draws the answer onto the network itself. Every operator in view
gets a bar above it for its cook time and one below it for the GPU memory it
holds, so a heavy blur, an oversized feedback buffer or a COMP full of
expensive work stands out the moment you open the network. A list in the
corner names the worst offenders and takes you to one with a click.

It is based on [Anton Heestand's Cook Bar](https://github.com/heestand-xyz/cook_bar).

## How to use it

1. Click Cook Bar's toolbar button, run **Toggle cook bar** from quick-launch,
   or switch **Active** on. The button lights up while the bars are on,
   whichever way you switched them. Right-click it to open Cook Bar's
   parameters, like the other toolbar tools.
2. Keep the timeline playing. While it is paused, **Active** is greyed out
   and the bars stop; they come back when you press play.
3. Open the network you want to check. The bars are drawn over the network
   editor you are working in, above the nodes, and follow you as you move
   between networks and between panes. They show in one pane at a time.
4. Look for the reddest, tallest bars, or read the Top List in the corner.
   Click a row there to jump straight to that operator.

From there:

- To read exact figures, switch on **Values**. Each bar writes its number
  beside it.
- To see where the time goes in a whole project, start at the top and follow
  the heaviest COMP down: a COMP's bars add up everything inside it.
- To check how much headroom a patch has, open the
  [Global Hog CHOP](#global-hog-chop) and let it eat part of every frame.

## Reading the bars

Each operator can get two bars: cook time above it and GPU memory below it.

**The top bar is cook time**, CPU and GPU together.

| What you see | What it means |
|---|---|
| The bar fills across the operator | Cook time from 0 to 1 ms: full width at 1 ms |
| The fill goes from green through yellow to red | Green up to 0.5 ms, red at 1 ms |
| A faint strip after the fill | The rest of the bar, up to 1 ms |
| The bar grows taller and fades toward its top | Past 1 ms, up to ten times its height at 10 ms |
| Diagonal stripes moving along it | The operator cooked this frame or the last one |
| A dim bar that stands still | It is not cooking now; the bar shows its last cook |
| A grey hatched bar on a COMP | Its cooking is switched off, by hand or by a tool such as a scene changer's Control Cook; nothing inside it cooks until it is switched back on |

**The bottom bar is GPU memory.** Operators that hold none have no bottom bar.

| What you see | What it means |
|---|---|
| The bar fills across the operator | GPU memory from 0 to 100 MB: full width at 100 MB, about three 4K RGBA textures |
| The fill goes from cyan to blue | Blue past 50 MB |
| The bar grows taller and fades downward | Past 100 MB, up to ten times its height at 1 GB |

The memory bar has no stripes.

**On a COMP**, the top bar adds the COMP's own cook time to everything inside
it, and its stripes move while anything inside is cooking. The bottom bar
counts the GPU memory of everything inside it.

The bars of the current operator and of selected operators sit a little
wider, around their outline.

**Values** writes each bar's number next to it: the cook time above the
operator and the GPU memory below it, dimmer while the operator is not
cooking. A COMP whose cooking is switched off reads cooking off. Operators too
small on screen to fit a number get none, so zoom in to read more of them.
The numbers change ten times a second so they stay readable. Values is off
unless you switch it on.

## Finding the heaviest operators

While the bars are on, a small list in a corner of the network editor, the
Top List, names the heaviest operators in the network you are viewing. It is
the quickest way from "this network is slow" to the operator responsible.

- **To go to an operator**, click its row. The operator is selected and the
  view zooms to it.
- **To rank by memory**, click the **GPU Memory** tab along the top of the
  list; **Cook Time** switches back. Cook time counts only operators that
  cooked in the last second, so something that cooked once at startup does
  not stay on top.
- **To see more or fewer operators**, set **List Rows**.
- **To keep the list but free the corner**, click the arrow at the right of
  the tabs. The list folds to its tab row.
- **To move it to another corner**, or further from the edges, use the
  **Overlay** tab of [FNS_Hub](/docs/fns-hub/), which arranges every tool that
  draws on the network editor. **List Corner** and **List Margin** on Cook
  Bar hold the same settings. When another tool's list shares the corner,
  **List Order** decides which sits nearer the corner: lower is nearer.
- **To hide the list**, switch off **Top List**. The Overlay tab in FNS_Hub
  can also hide the list or the bars without switching Cook Bar off.

## Bars in a big network

**Max OPs** sets how many operators get bars at once, counted from the middle
of the view: 100 unless you change it, up to 250. Only operators in view
count, so in a large network you can also zoom in on the part you care about.

More bars cost GPU time, measured on a 1536x700 pane:

| Max OPs | GPU per frame |
|---|---|
| 50 | about 0.1 ms |
| 100 | about 0.25 ms |
| 250 | about 1.4 ms |

A bigger pane costs more in proportion to its size.

## Global Hog CHOP

Before a show it helps to know how much headroom a patch has. Ctrl+right-click
the toolbar button (`Ctrl` or `Cmd` on macOS), press **Open Global Hog CHOP**
on the CookBar page, or run **Open Global Hog CHOP** from quick-launch, to
open the parameters of a global **Hog CHOP**. Switch it on, dial in how much
of each frame it eats, and watch how the rest of your patch copes when it is
starved of cook time, with the bars showing where the time goes. It ships
switched off.

While the Hog is on, the toolbar button turns red, so a stress test is never
left running by accident.

## Your network stays as it is

The bars are drawn through the network overlay
([FNS_OverlayRegistry](/docs/fns-overlayregistry/), which installs with Cook
Bar), shared with any other tool that draws over the network editor. Your
network keeps its display flags, its annotations and its operators: the
overlay is not one of them, and it leaves before every project save, so a
saved project never holds it.

Earlier versions drew the bars as the network's background, which meant
switching off its TOPs' display flags and fading its annotations while the
bars were on. If a project still holds anything from that, Cook Bar removes it
the next time it starts.
