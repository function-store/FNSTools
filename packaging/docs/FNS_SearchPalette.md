---
package: FNS_SearchPalette
summary: Search field for TouchDesigner's palette browser, installed into the palette on startup.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: The search hotkey
    anchor: the-search-hotkey
  - name: Writing a search
    anchor: writing-a-search
feature_list:
  - name: Find components in the palette browser
    anchor: how-to-use-it
    does: 'A search field in TouchDesigner''s palette browser lists the matching components from every folder; it is put in every time a project opens, or added and removed on demand.'
  - name: Focus the field by hotkey
    anchor: the-search-hotkey
    does: '`Ctrl+Shift+F` brings TouchDesigner''s own palette tab to the front and puts the cursor in an empty search field; the key is rebindable in HotkeyManager.'
  - name: Ranked substring search
    anchor: writing-a-search
    does: 'Finds a word anywhere in a name, combines several words, and lists exact, prefix and word-start matches first.'
  - name: Wildcard patterns
    anchor: writing-a-search
    does: 'Words with `*` or `?` match as patterns from the front of a name, so a wildcard can only widen the search.'
  - name: Exclude matches with a minus
    anchor: writing-a-search
    does: 'A word starting with `-` takes its matches out of the results.'
  - name: Fuzzy fallback for typos and spellings
    anchor: writing-a-search
    does: 'When nothing matches as typed, it tries the other side''s spelling, initials, a typo, and finally letters in order.'
  - name: Folder search
    anchor: writing-a-search
    does: 'A word containing / matches the palette folder, so tools/ on its own lists a whole folder.'
  - name: Latest version only
    anchor: writing-a-search
    does: 'Numbered or duplicate copies of one component collapse to the most recently modified file.'
  - name: Jump by word in the field
    anchor: how-to-use-it
    does: 'The field edits like TouchDesigner''s own text fields, including `Ctrl+Left` and `Ctrl+Right` to jump by word.'
---

## Why use it

TouchDesigner's palette browser is a folder tree. To use a component you have
to remember which folder it is in and scroll to it, and the more components
you collect, the longer that takes.

SearchPalette adds a search field to the palette browser. Type part of a name
and the list shows the matching components from every folder, best match
first. It is based on
[Yea Chen's TD-SearchPalette](https://github.com/yeataro/TD-SearchPalette),
with a search that goes well past the original's prefix match.

## How to use it

1. Install it. The search field is put into the palette browser every time a
   project opens while **Auto Install at startup** is on. That choice roams
   with your config, so it holds across projects. **Install** and
   **Uninstall** add or remove the field right away.
2. Open the palette browser and type into the field. The list follows as you
   type.
3. To get back to browsing, click a folder in the tree. That clears the search,
   and the list shows the folder's own contents again. The **X** button next
   to the field clears the search without changing folder.

The field is a Text COMP, so it edits the way TouchDesigner's own text fields
do, including `Ctrl+Left` and `Ctrl+Right` to jump by word. It replaced the
legacy Field COMP, which TouchDesigner deprecated in 2022.24200 and which had
no word navigation.

Two settings worth knowing:

- If a very large palette makes typing feel heavy, switch off **Live Search**:
  the list then waits until you stop typing.
- To have the palette browser close itself when you are not using it, switch
  on **Hide Palette When Idle** and set **Hide After (Minutes)**. Unused means
  the mouse is outside the palette and nothing is being typed into the field.

Earlier releases shipped this package as TDX_SearchPalette. It is
FNS_SearchPalette now. A copy installed under the old name keeps working but is
no longer offered updates, so reinstall it under the new name.

## The search hotkey

With the palette browser open, `Ctrl+Shift+F` (`Cmd+Shift+F` on macOS) brings
TouchDesigner's own palette tab to the front, clears the search field and puts
the cursor in it, ready to type.

It works on the palette where it already is. It leaves
`ui.openPaletteBrowser()` uncalled on purpose, because that pops the palette
out into a floating window. So if the browser is closed, the hotkey does
nothing and your workspace stays as it is.

The tab step matters because the search field lives inside the stock palette
list, and any contributed palette tab hides that list. The hotkey asks
whichever palette-tab owner is installed to show TouchDesigner's own tab again
([PaletteRegistry](/docs/fns-paletteregistry/) and TDXLU's own injector are
both detected, neither is required), then takes focus one frame later, because
a tab switched back this frame is still hidden.

The combo is this package's own **Search Hotkey** parameter. Change it there,
or in [HotkeyManager](/docs/fns-hotkeymanager/), which lists it under
SearchPalette; resetting it to its default brings back `Ctrl+Shift+F`. It used
to live in MY_HOTKEYS. Keeping it with the tool that owns the field means
uninstalling this package takes its hotkey with it.

## Writing a search

What you can type, from plain words to patterns:

- **Anywhere in the name, any case.** `blur` finds `hsvBlur`, `radialBlur` and
  `barrel_blur`, as well as names that start with it.
- **Several words narrow it down.** Every word has to match: `audio an` finds
  `audioAnalysis`.
- **Best matches first.** An exact match comes first, then names starting with
  the query, then names where it starts a word (`blur` puts `hsvBlur` and
  `barrel_blur` above `unblurred`), then the rest, alphabetical within each
  group.
- **Wildcards.** A word carrying `*` or `?` is matched as a pattern, anchored
  at the front only, so a wildcard can only widen the search: `audio*` is
  still a classic prefix search, `*fee` finds `feedbackGen` just like plain
  `fee` does, and `web*ser` finds `webBrowser`.
- **Leave things out with `-`.** A word starting with a minus removes its
  matches: `blur -barrel` finds every blur except the `barrel_blur` pair.
- **When nothing matches.** Each word is then read more loosely, best reading
  first: a spelling from the other side of the Atlantic (`randomise` finds
  `randomize`, `colour` finds `color`), initials (`mfo` finds
  `movieFileOut`), a typo of a word or its start (`nosie` finds `noise`,
  `kinnect` finds `kinectAzure`; one slip for words of four to seven letters,
  two from eight), and last the letters in order, so `fbg` finds
  `feedbackGen` and `wbrsr` finds `webBrowser`. These only appear when the
  strict search came up empty, and they never reorder it.
- **Search a folder.** A word containing `/` matches the palette folder, so
  `gen/ noise` finds `noise` in the Generators folder, and `tools/` alone lists
  a whole folder. **Folder Search (token/)** switches this off.
- **One copy per component.** Numbered copies of one component (`tool`,
  `tool1`, `tool2`, or the same name in two folders) collapse to the most
  recently modified file. **Latest Version Only** switches this off.

The list stops at 200 rows, so a one-letter query shows the 200 best-ranked
components only.
