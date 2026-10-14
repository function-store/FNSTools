---
package: FNS_ColorUI
summary: 'ColorUI: Recolor any TouchDesigner UI element, create presets, import/export, and share!'
features:
  - name: ColorUI
    anchor: colorui
  - name: In the console
    anchor: in-the-console
feature_list:
  - name: Recolour UI elements
    anchor: colorui
    does: Recolour any TouchDesigner UI element by choosing it from a dropdown.
  - name: Operator family colours
    anchor: colorui
    does: 'Recolour whole operator families, POPs included.'
  - name: Local save with auto-load
    anchor: colorui
    does: 'Saving colours locally stores them in the component, from where they can be loaded automatically on startup.'
  - name: JSON export and import
    anchor: colorui
    does: Export colour settings to JSON and import them again; imported settings take precedence over local ones.
  - name: OpColor tab in Hub
    anchor: colorui
    does: 'The colour UI is available as the OpColor tab of Hub, the FNS button in the main-menu bar.'
  - name: Console tab in the browser
    anchor: in-the-console
    does: 'With Expose on, the same colour UI is served in the browser as the ColorUI tab of Console, the toolkit''s web front.'
---

## ColorUI

ColorUI: Recolor any TouchDesigner UI element, create presets, import/export, and share!  
   - Available as the **OpColor** tab of [Hub](/docs/fns-hub/) (the **FNS** button in the main-menu bar)  
   - Includes recoloring **OP Families** (looking at you, POPs)  
   - Or any UI element by choosing from the dropdown  
   - **Saving colors locally** saves them to the component and can be auto-loaded on startup  
   - **Export to JSON**, and **import**; imported settings take precedence over local  

## In the console

ColorUI is also the first tool to contribute a tab to **Console**, the
toolkit's web front: the same colour UI, served in the browser alongside
Settings and Install & remove. Turn it on with **Expose** on ColorUI's
`Registry` page and open the console (`FNS_Console`, tab *ColorUI*). While the
console serves the page, ColorUI's own in-TD web render switches off so it is
not rendering the same page twice.
