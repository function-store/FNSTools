---
status: landed
summary: Owner requests for the overlay widgets after the first QuickMarks pass - outlines of the saved area, a clearer recall, renaming from the list, and collapsing both widgets.
since: 2026-10-11
skill: fns-registry
---

# Overlay widgets backlog (2026-10-11)

Owner feedback on CookBar's Top List and QuickMarks' mark list and pins
(docs/NetworkOverlayRegistry.md). Corrected in place as findings land.

| # | Ask | Plan | State |
|---|---|---|---|
| 1 | QuickMarks should outline the area a mark saved, not pin a point | A mark stores the view centre and zoom; new marks also store the view's size in network units (`w`, `h`). Older marks take the current pane's size at the saved zoom. A GLSL layer draws a rounded outline per mark of the viewed network; the label sits inside its top-left corner. | landed: verified a probe mark's outline matched the saved view, rounded, labelled |
| 2 | Clicking a mark in the list should recall it | Finding: the click already recalls (the status bar read "Jump to 1"), but two of the three dev marks point at networks that no longer exist, and the list showed them like any other. Missing marks now read "missing" and are dimmed; a click on one says so in the status bar. | landed |
| 3 | Rename a mark from the list | Right-click a row: TD's PopDialog (non-blocking) with a text field, prefilled with the name; OK sets it (`SetName`). | landed: OK renames, Cancel leaves it |
| 4 | Collapse either widget | A small toggle at the right of each widget's top row folds it to that row. The state is a parameter of the tool (CookBar: Top List Collapsed; QuickMarks: Mark List Collapsed), so it persists. The registry restacks from the panel's live height. | landed: folded Top List 24 px, mark list moved up to 48 px |
