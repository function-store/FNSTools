---
package: FNS_SearchFix
summary: The network editor's find bar finds what you mean. Any part of a name, case-insensitive, with wildcards, optionally fuzzy and inside child networks, with the bar's arrows and Home toggle kept.
features:
  - name: Searching
    anchor: searching
  - name: The find bar
    anchor: the-find-bar
feature_list:
  - name: Match any part of a name
    anchor: searching
    does: Finds operators by any part of their name in any case; typed spaces become underscores and a split text needs every part to match.
  - name: Wildcard patterns
    anchor: searching
    does: 'Patterns like `noise*`, `*out?` and `[ab]lur*` match whole names as in TouchDesigner''s pattern fields, and a leading `^` inverts the match.'
  - name: Fuzzy matching
    anchor: searching
    does: 'When switched on, also finds word initials, a typo or two, or the letters in order, listed after every plain hit.'
  - name: Best results first
    anchor: searching
    does: 'Exact names rank first, then names starting with the text, then word matches, then anywhere, with shallower operators before deeper ones.'
  - name: Step through results
    anchor: the-find-bar
    does: 'The bar''s arrows step through results, the first is picked as you type, and with Home on the pane centres on the picked operator.'
  - name: Deep search into child networks
    anchor: the-find-bar
    does: A per-pane Deep checkbox and depth field search networks inside the current one; picking a hit takes the pane into its network.
  - name: Legacy search toggle
    anchor: the-find-bar
    does: A Legacy checkbox in the find bar brings back TouchDesigner's own search for every pane.
  - name: Close the bar from inside it
    anchor: the-find-bar
    does: 'With Shortcut Closes Find Bar on, Ctrl+F also closes the find bar while you are typing in it.'
  - name: Quick-launch commands
    anchor: the-find-bar
    does: 'Toggle SearchFix, Toggle fuzzy find and Toggle legacy find switch the parameters, and Repatch find bars reapplies the search to every bar.'
---

## Searching

TouchDesigner's find bar only finds names that start with exactly what you
typed, in the network you are looking at. SearchFix replaces that search in
every pane's find bar:

- **Any part of a name, any case.** `SimpleScene` finds
  `FNS_SimpleSceneChanger`; `scene` finds it too.
- **Spaces become underscores** as you type, since operator names have
  none. A text that does not match as typed is tried as its parts:
  `scene_chang` finds `FNS_SimpleSceneChanger`, and every part has to hit.
- **Wildcards** work like TouchDesigner's own pattern fields (a Select OP's,
  for example), in any case: `noise*`, `*out?`, `[ab]lur*`. A pattern has to
  match the whole name, and `^` turns it around: `^FNS_*` finds everything
  that does not start with FNS_.
- **Fuzzy**, when you switch it on, also finds the first letters of words
  (`sschg`), a typo or two (`nosie`), or the letters in order. Those hits come
  after every plain one.
- **Best first.** An exact name comes before one that starts with your text,
  then a word inside the name, then anywhere in it, and shallower operators
  before deeper ones.

## The find bar

Open a pane's find bar as usual. The back and forward arrows step through
the results, and the first result is picked as you type, like before. A
picked operator becomes current and selected; with **Home** on, the pane
centres on it. When a **Deep** search finds something inside a child network,
picking it takes the pane into that network, and the arrows keep stepping
through the same results.

Beside Home sit three checkboxes, drawn like Home's own. **Legacy** brings TouchDesigner's own search
back and **Fuzzy** turns loose matching on; they are the tool's parameters,
so every pane's find bar shares them. **Deep** belongs to that pane's bar:
off searches the network you are in, like TouchDesigner; on, a number field
appears beside it and sets how deep the search goes: 1 is the network you
are in, 2 adds the networks inside it, and so on. The field starts at the
tool's Deep Depth, and each pane keeps its own Deep and depth for the
session.

TouchDesigner opens and closes a pane's find bar on Ctrl+F (Cmd+F on macOS)
while you work in the network, but once you are typing in the bar the
shortcut does nothing. With **Shortcut Closes Find Bar** on, it closes the
bar from there too.

Switching SearchFix off leaves every find bar exactly as TouchDesigner made
it.

From quick-launch: **Toggle SearchFix**, **Toggle fuzzy find** and **Toggle
legacy find** switch the same parameters and show whether each is on, and
**Repatch find bars** applies the search to every find bar again.
