---
package: FNS_OpMenuMods
summary: 'Extras for the OP Create dialog: IO filter buttons, your own search words per operator type, and search by initials.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Greg's IO filters
    anchor: gregs-io-filters
  - name: Custom search keywords
    anchor: custom-search-keywords
  - name: Dotsimulate's acronym search
    anchor: dotsimulates-acronym-search
feature_list:
  - name: Filter IO operators
    anchor: gregs-io-filters
    does: 'Buttons at the top right of the OP Create dialog show only IO operators, hide them, or show everything.'
  - name: Custom search keywords
    anchor: custom-search-keywords
    does: 'Give any operator type your own search words, so typing music finds Audio File In and webcam finds Video Device In.'
  - name: Keyword table in Hub
    anchor: custom-search-keywords
    does: 'The keywords live in one table, edited from the SearchWords tab of Hub and synced across project files.'
  - name: Acronym search
    anchor: dotsimulates-acronym-search
    does: 'Type the start of each word of an operator''s name, such as m f o, to find Movie File Out.'
  - name: Remove cleanly, shared with other tools
    anchor: how-to-use-it
    does: 'The mods apply through OpMenuRegistry, so several tools can decorate the dialog together and it returns to stock when they are removed.'
---

## Why use it

The OP Create dialog finds operators by their name. That works once you know
the names, but you have to know that the oscillator you want is a Pattern CHOP,
that a webcam comes in through Video Device In, or that a clamp is a Limit
CHOP. Typing what you mean finds nothing. And with every operator that talks to
the outside world mixed into the list, picking out a processing operator takes
a moment longer than it should.

OpMenuMods adds three things to the dialog: buttons that show or hide the IO
operators, your own search words for any operator type, and search by the
start of each word of a name, so `m f o` finds Movie File Out.

## How to use it

Install it and open the OP Create dialog; all three mods are on.

- Click **IO**, **-IO** or **All** at the top right of the dialog to filter
  the list.
- Type a word you associate with an operator, such as `music`, `webcam` or
  `fft`, and the operator types carrying that word are offered.
- Type the first letters of an operator's name, separated by spaces: `m f o`
  for Movie File Out.
- To add or change search words, open the SearchWords tab of
  [Hub](/docs/fns-hub/) (the **FNS** button in the main-menu bar).

The mods go into the dialog through
[OpMenuRegistry](/docs/fns-opmenuregistry/), so several tools can decorate
the same dialog without fighting over it, and the dialog goes back to stock the
moment you remove them. Other installed tools add their own decorations the
same way: [OpTemplates](/docs/fns-optemplates/) marks every operator type you
have a template for with `>>>`. The OpMenu tab of Hub lists what each tool
contributes, and lets you reorder the contributions or switch one off without
uninstalling its tool.

## Greg's IO filters

This mod by [Greg Hermanovic](https://derivative.ca) adds three filter
buttons to the top right of the OP Create dialog: **IO** shows only IO
operators, **-IO** shows everything except them, and **All**, the default,
shows every operator.

IO operators are the ones that interact with resources outside TouchDesigner,
such as sensors or web interfaces. Switch off **IO Filter Active** to take the
buttons out of the dialog.

## Custom search keywords

Each operator type can carry extra search words. Out of the box, `ramp` or
`cos` finds the Pattern CHOP and the LFO CHOP, `music` finds Audio File In,
`webcam` finds Video Device In, `clamp` finds the Limit TOP and CHOP, and
`donut` finds the Torus SOP.

A keyword counts when you type a single word, and it is matched from the
start of the keyword, so `cam` finds Video Device In through both `cam` and
`camera`.

The words live in one table, edited from the SearchWords tab of Hub, and it is
synced across project files. Each row is an operator type, written the way
TouchDesigner spells it (`patternCHOP`, `audiofileinCHOP`), and its words,
separated by commas. An edit is used the next time the dialog searches.

Other tools can add search words of their own through
[OpMenuRegistry](/docs/fns-opmenuregistry/).

## Dotsimulate's acronym search

Thanks to [Dotsimulate](https://www.patreon.com/dotsimulate/), you can find an
operator by the start of each word of its name. Type the starts in order,
separated by spaces: `m f o` finds Movie File Out, and `a f i` finds Audio File
In. Longer starts work too, such as `mov f o`.
