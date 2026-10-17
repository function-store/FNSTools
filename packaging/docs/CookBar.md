---
package: CookBar
summary: A bar above every operator in the network you are viewing, showing how long it takes to cook and how much GPU memory it holds, so the expensive parts of a network stand out at a glance.
features:
  - name: Turning it on
    anchor: turning-it-on
  - name: Reading the bars
    anchor: reading-the-bars
  - name: Top List
    anchor: top-list
  - name: Global Hog CHOP
    anchor: global-hog-chop
    icon: HogCHOP.png
  - name: Your network stays as it is
    anchor: your-network-stays-as-it-is
feature_list:
  - name: Toggle from toolbar or command
    anchor: turning-it-on
    does: 'Switch the bars on from the toolbar button, the Toggle cook bar command or Active; they follow you between networks and panes.'
  - name: Bar count budget
    anchor: turning-it-on
    does: 'Max OPs caps how many in-view operators get bars, counted from the middle of the view, 100 by default and up to 250.'
  - name: Cook-time bars
    anchor: reading-the-bars
    does: 'A bar above each operator shows CPU plus GPU cook time, green to red up to 1 ms, growing taller past it and striped while cooking.'
  - name: Cooking-off marker
    anchor: reading-the-bars
    does: 'A COMP whose cooking is switched off gets a grey hatched bar, and Values reads cooking off, so a frozen network explains itself.'
  - name: GPU memory bars
    anchor: reading-the-bars
    does: 'A bar below each operator shows the GPU memory it holds, cyan to blue up to 100 MB, growing taller up to 1 GB.'
  - name: COMP totals
    anchor: reading-the-bars
    does: 'On a COMP, the bars add up the cook time and GPU memory of everything inside it, with stripes moving while anything inside cooks.'
  - name: Numeric values
    anchor: reading-the-bars
    does: 'Values writes each bar''s number beside it, cook time above and GPU memory below, updating ten times a second.'
  - name: Top List of heaviest operators
    anchor: top-list
    does: A corner list names the heaviest operators by cook time or GPU memory; clicking a row selects that operator and zooms to it.
  - name: Shared overlay settings in Hub
    anchor: top-list
    does: Hub's Overlay tab sets list placement for every network-editor overlay tool and can hide the bars or the list without switching Cook Bar off.
  - name: Global Hog CHOP stress test
    anchor: global-hog-chop
    does: Ctrl+right-click the toolbar button to open a global Hog CHOP that eats part of each frame; the button turns red while it is on.
  - name: Leaves the network untouched
    anchor: your-network-stays-as-it-is
    does: 'The bars draw through the shared network overlay, which leaves before every save, so display flags, annotations and operators stay as they were.'
---

It is based on [Anton Heestand's Cook Bar](https://github.com/heestand-xyz/cook_bar).

## Turning it on

Click its toolbar button, run **Toggle cook bar** from quick-launch, or switch
**Active** on. Cook Bar draws over the network in the network editor you are
working in, above the nodes, and follows you as you move between networks and
between panes. The button lights up while the bars are on, whichever way you
switched them. Right-click it to open Cook Bar's parameters, like the other
toolbar tools.

The bars show in one pane at a time: the network editor you are working in.

It needs the timeline playing. While the timeline is paused, **Active** is
greyed out and the bars stop; they come back when you press play.

**Max OPs** sets how many operators get bars at once, starting from the
middle of the view: 100 unless you change it, up to 250. Only operators in
view count. More bars cost GPU time, measured on a 1536x700 pane:

| Max OPs | GPU per frame |
|---|---|
| 50 | about 0.1 ms |
| 100 | about 0.25 ms |
| 250 | about 1.4 ms |

A bigger pane costs more in proportion to its size.

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
it and its stripes move while anything inside is cooking; the bottom bar counts
the GPU memory of everything inside it.

The bars of the current operator and of selected operators sit a little wider,
around their outline.

**Values** writes each bar's number next to it: the cook time above the
operator and the GPU memory below it, dimmer while the operator is not
cooking; a COMP whose cooking is switched off reads cooking off. Operators too small on screen to fit a number get none, so zoom in to
read more of them. The numbers change ten times a second so they stay
readable. Values is off unless you switch it on.

## Top List

While the bars are on, a small list in a corner of the network editor names
the heaviest operators in the network you are viewing.

- The **Cook Time** and **GPU Memory** tabs along its top choose what it
  ranks by. Cook time counts only operators that cooked in the last second,
  so something that cooked once at startup does not stay on top.
- Click a row to select that operator and zoom the view to it.
- The arrow at the right of the tabs folds the list to its tab row (**Top List
  Collapsed** does the same).
- **Top List** switches it on or off, **Rank By** is the same choice as the
  tabs, **List Corner** picks the corner, **List Margin** sets how far it sits
  from the edges of the network editor (12 screen points unless you change
  it), **List Order** sets its place among other tools' lists in the same
  corner (lower sits nearer the corner), and **List Rows** sets how many
  operators it shows, 1 to 12 (8 unless you change it).
- The **Overlay** tab of [FNS_Hub](/docs/fns-hub/) sets the same things for
  every tool that draws on the network editor, and hides the bars or the
  list without switching Cook Bar off.

## Global Hog CHOP

Ctrl+right-click the toolbar button (Ctrl or Cmd on macOS), press **Open Global Hog CHOP** on the
CookBar page, or run **Open Global Hog CHOP** from quick-launch, to open the
parameters of a global **Hog CHOP**. Switch it on,
dial in how much of each frame it eats, and watch how the rest of your patch
copes when it is starved of cook time, with the bars showing where the time
goes. It ships switched off.

While the Hog is on, the toolbar button turns red, so a stress test is never
left running by accident.

## Your network stays as it is

The bars are drawn through the network overlay (FNS_OverlayRegistry, which
installs with Cook Bar), shared with any other tool that draws over the network
editor. Your network keeps its display flags, its annotations and its
operators: the overlay is not one of them, and it leaves before every project
save, so a saved project never holds it.

Earlier versions drew the bars as the network's background, which meant
switching off its TOPs' display flags and fading its annotations while the
bars were on. If a project still holds anything from that, Cook Bar removes it
the next time it starts.
