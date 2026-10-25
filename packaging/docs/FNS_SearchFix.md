---
package: FNS_SearchFix
summary: 'The network editor''s find bar finds what you mean. Any part of a name, case-insensitive, with wildcards, optionally fuzzy and inside child networks, with the bar''s arrows and Home toggle kept.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: What a search matches
    anchor: what-a-search-matches
feature_list:
  - name: Find any part of a name
    anchor: what-a-search-matches
    does: 'Finds operators by any part of their name in any case; typed spaces become underscores, and a text split into parts needs every part to match.'
  - name: Wildcard patterns
    anchor: what-a-search-matches
    does: 'Patterns like `noise*`, `*out?` and `[ab]lur*` match whole names as in TouchDesigner''s pattern fields, and a leading `^` inverts the match.'
  - name: Fuzzy matching
    anchor: what-a-search-matches
    does: 'When switched on, also finds word initials, a typo or two, or the letters in order, listed after every plain hit.'
  - name: Rank the best results first
    anchor: what-a-search-matches
    does: 'Exact names rank first, then names starting with the text, then word matches, then anywhere, with shallower operators before deeper ones.'
  - name: Step through results
    anchor: how-to-use-it
    does: 'The arrows step through results, the first is picked as you type, and with Home on the pane centres on the picked operator.'
  - name: Deep search into child networks
    anchor: how-to-use-it
    does: A Deep checkbox and depth field in each pane's bar search the networks inside the current one; picking a hit takes the pane into its network.
  - name: Restore TouchDesigner's own search
    anchor: how-to-use-it
    does: 'A Legacy checkbox in the find bar brings back TouchDesigner''s own search for every pane, and switching SearchFix off restores every bar as it was.'
  - name: Close the bar from inside it
    anchor: how-to-use-it
    does: The find bar shortcut also closes the bar while you are typing in it.
---

## Why use it

TouchDesigner's find bar only finds names that start with exactly what you
typed, with the same capitals, in the network you are looking at. Type
`scene` looking for `FNS_SimpleSceneChanger` and you get nothing; type
`simplescene` and you still get nothing. In a big project you end up
scrolling around for the operator, or remembering exactly how you spelled it.

SearchFix replaces that search in every pane's find bar. It finds any part of
a name in any case, understands wildcards, can match loosely, and can look
inside the networks below the one you are in. The bar itself works as before:
same arrows, same Home toggle.

## How to use it

1. Open a pane's find bar as usual, with `Ctrl+F` (`Cmd+F` on macOS).
2. Type any part of the name you are after. The first result is picked as you
   type: it becomes the current and selected operator, and with **Home** on
   the pane centres on it.
3. Use the back and forward arrows to step through the other results.

Beside Home sit three checkboxes, drawn like Home's own:

- **To find operators in child networks**, tick **Deep**. A number field
  appears beside it and sets how deep the search goes: 1 is the network you
  are in, 2 adds the networks inside it, and so on. Picking a hit inside a
  child network takes the pane into that network, and the arrows keep
  stepping through the same results. Deep belongs to that pane's bar: each
  pane keeps its own Deep and depth for the session, and the field starts at
  the tool's **Deep Depth**.
- **To find something you only half remember**, tick **Fuzzy**. It also
  matches the first letters of words, a typo or two, or the letters in
  order.
- **To get TouchDesigner's own search back**, tick **Legacy**.

Fuzzy and Legacy are the tool's parameters, so every pane's find bar shares
them.

A few more things you can do:

- **Close the bar without reaching for the mouse.** TouchDesigner opens and
  closes a pane's find bar on `Ctrl+F` while you work in the network, but
  once you are typing in the bar the shortcut does nothing. With **Shortcut
  Closes Find Bar** on, it closes the bar from there too.
- **Switch it all off.** With **Active** off, every find bar is exactly as
  TouchDesigner made it.
- **From quick-launch**, **Toggle SearchFix**, **Toggle fuzzy find** and
  **Toggle legacy find** switch the same settings and show whether each is
  on. If a find bar stops searching the SearchFix way, for example after
  TouchDesigner rebuilt it, **Repatch find bars** applies the search to every
  bar again.

## What a search matches

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
  (`sschg`), a typo or two (`nosie`), or the letters in order. Those hits
  come after every plain one.
- **Best first.** An exact name comes before one that starts with your text,
  then a word inside the name, then anywhere in it, and shallower operators
  before deeper ones.
