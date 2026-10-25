---
package: FNS_ColorUI
summary: 'Recolour any part of TouchDesigner''s interface or a whole operator family, keep the result with your settings, and share it as a JSON file.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Finding what to change
    anchor: finding-what-to-change
  - name: Sharing a palette
    anchor: sharing-a-palette
  - name: In the console
    anchor: in-the-console
feature_list:
  - name: Recolour UI elements
    anchor: how-to-use-it
    does: 'Every colour in TouchDesigner''s interface in one list, each with its default and a reset.'
  - name: Operator family colours
    anchor: how-to-use-it
    does: 'Recolour whole operator families, POPs included.'
  - name: Save and reapply your colours
    anchor: how-to-use-it
    does: 'Your colours are stored in the component, applied as the project opens, and follow you to other projects and through updates.'
  - name: Filter the list
    anchor: finding-what-to-change
    does: 'Narrow the list by name with wildcards, to changed colours only, or to colours close to a reference colour.'
  - name: Change many at once
    anchor: finding-what-to-change
    does: 'Give one colour to everything listed, or to a whole group, and reset a group in one go.'
  - name: Randomize and undo
    anchor: finding-what-to-change
    does: 'Throw random colours at the whole interface, then put your own colours back with one click.'
  - name: Share your colours as JSON
    anchor: sharing-a-palette
    does: 'Export writes only the colours you changed to a JSON file, to keep with a project, commit or send to someone.'
  - name: Import a JSON palette
    anchor: sharing-a-palette
    does: 'Import applies such a file; its colours take precedence over the ones stored locally, and elements this build does not know are skipped.'
  - name: Open from Hub or quick-launch
    anchor: how-to-use-it
    does: 'The colour editor opens from the OpColor tab of Hub (the FNS button in the main-menu bar), Open color UI in quick-launch, or Open UI on the component.'
  - name: Console tab in the browser
    anchor: in-the-console
    does: 'With Expose to Console on, the same editor is served in the browser as the ColorUI tab of Console, the toolkit''s web front.'
---

## Why use it

Every colour in TouchDesigner's interface is a named entry in its UI colour
table, the operator family colours included. You might want the families
easier to tell apart at a glance (POPs especially), or the whole interface
darker for a dim venue. Changing those by hand means finding the right entries
by name and setting them one by one from Python.

ColorUI is an editor for that table. Every element is listed with its colour
and its default, grouped and searchable, with the operator families on their
own row. Change one colour, a group or everything you have filtered; your
colours are applied again when the project opens and follow you to your other
projects.

## How to use it

1. Open it from the OpColor tab of [Hub](/docs/fns-hub/) (the **FNS** button
   in the main-menu bar), with **Open color UI** in quick-launch, or with
   **Open UI** on the component. When Console serves it, these open the
   console's ColorUI tab in your browser; see
   [In the console](#in-the-console).
2. The Families row at the top holds the operator family colours: COMP, TOP,
   CHOP, SOP, DAT, MAT, POP and CUSTOM. Click one to pick its colour.
3. Below it, every other element of the interface, in groups. Click a row to
   pick its colour. Each row also shows the default colour and a reset button.
4. Changes apply as you make them and are stored in the component. Only
   colours that differ from TouchDesigner's default are kept, so setting one
   back to its default simply drops it.

With **Auto-Load Colors** on, the stored colours are applied every time a
project opens. They are also saved with your toolkit settings through
[ConfigRegistry](/docs/fns-configregistry/), so they follow you to other
projects and survive toolkit updates.

## Finding what to change

The list is long, and the tools at the top are there to cut it down:

- **The filter field** matches element names. Several words must all match,
  and `*` is a wildcard.
- **changed only** lists the colours you have changed.
- **near** lists the elements whose colour is close to a reference colour,
  closest first. Click the swatch beside it to pick the reference, and set
  how close in the number field.
- **group by** sorts the list by the start of each element's name (prefix) or
  by what the element is used for (role). **expand all** and **collapse all**
  open and close every group.

Once the list shows what you want, change it all at once. **Set shown…**
gives one colour to every element listed. Each group header has its own
**set…** for that group, and a **reset** that puts the group's changed colours
back to default after a second click to confirm.

For example, to lift every element that uses one particular dark grey: switch
on **near**, pick that grey as the reference, check the list, then use **Set
shown…** to give them all the new colour.

**Randomize** gives every element a random colour, for fun or to find out
which element is which. **Undo** puts back TouchDesigner's defaults with your
own colours on top. **Reset all** returns everything to TouchDesigner's
defaults and clears your stored colours, after a second click to confirm.

## Sharing a palette

- **Export** writes the colours you changed to a JSON file, one entry per
  element. Only changed colours go in. Keep the file with a project, commit it,
  or send it to someone.
- **Import** reads such a file and applies it. Imported colours take
  precedence over the ones stored locally: they become your stored colours.
  Elements this build of TouchDesigner does not know are skipped, and the
  editor says how many.

The buttons in the editor ask for a file each time. The **Import** and
**Export** pulses on the component use the file in **File (.json)**, so a
project can keep its palette next to it.

## In the console

ColorUI is also the first tool to contribute a tab to
[Console](/docs/fns-console/), the toolkit's web front: the same colour
editor, served in the browser alongside Settings and Install & remove.

It is switched on by **Expose to Console** on ColorUI's Registry page. The
toolkit's installer turns it on when it installs ColorUI; a ColorUI dragged
into a project by hand starts with it off and works on its own. While the
console serves the page, opening ColorUI goes to the console's ColorUI tab,
and ColorUI's own web render inside TouchDesigner switches off so the same page
is not rendered twice.
