---
status: in-force
summary: The install-surface makeover — one shared UI base (base.css, marker-synced) under two shells (web storefront picker, in-TD console manager), the always-available guided setup, the understated Plus rail, and the console's Updates tab over new /api/updates* routes fronting FNS_Updater. Records why the framed picker stayed a frame and became invisible instead.
since: 2026-08-30
skill: fns-packaging
---

# The install surfaces: one base, two shells

Before this work the toolkit had three token families across its web
surfaces: the website/picker look (`#0a0a0a`, amber, marketing density),
the console look (`#191b1e`, `#e8a33d`, TD-panel density), and ColorUI's
own near-copy of the console's. The most visible cost was the console's
Install & remove tab: family-B chrome wrapping a family-A page in an
iframe — a website inside a box. The least visible cost was the worst
one: **updates had a complete backend and no surface at all.**
`FNS_Updater` has carried `CheckUpdates()` / `Compare()` /
`UpdateProject()` from the start; nothing served them to a page.

## The shape

**One base.** `packaging/configurator/base.css` is the single source for
the family's tokens and shared components (buttons, chips, cards, grid,
category headings, dialogs, steps, presets, toast — plus a `body.app`
density switch). Both shells must stay single self-contained files (one
is embedded into the installer and served from a Text DAT; one doubles
as a double-clickable standalone), so the base is **inlined by
generation, not linked**: `python packaging/configurator/sync_base.py
--write` pushes the block between `/* FNS:UIBASE:START */` markers into

- `packaging/configurator/index.html` — the web storefront shell
- `FNSTools/FNS_Console/console_page.html` — the in-TD manager shell

and `tests/test_ui_base_sync.py` (a bare `sync_base.py` run) fails the
suite on drift. This is the mechanized version of the "token-for-token
with website/docs.css" hand-contract the picker already carried — which
still holds one level up: **token VALUES stay in lockstep with
docs.css**, because the /get/ flavor loads both and the inline block
wins the cascade. Change a value in both places or in neither.

**Shell 1 — the storefront** (`index.html`, still built into /get/, the
standalone, and the installer's served page by the untouched build
seams). Gains: a category quick-nav (`#catnav` jump chips built from
`category_meta`), the Plus rail (`#plusrail` — one understated line:
the free tools are the toolkit, N extras are a thank-you for
supporters; the per-tool state stays on the cards' chips), **Guided
setup as a permanent mode** (the first-run welcome + step strip,
re-enterable from the bar in every flavor; step 3 names the flavor's
real finish — Review & install where the page can install, Copy the
install script where it cannot), and an **embedded mode**: framed
inside the console (`window.self !== window.top`), it drops the hero,
sets `body.app` density, and hides the theme toggle, so the framed
picker reads as a native panel.

**Shell 2 — the manager** (`console_page.html`). The console is the
in-app home for everything after the first install: Settings (config
registry views, restyled; scope/export/import moved from the top bar
into the Settings view's own toolbar), Install & remove (the framed
picker, now seamless), contributed tabs — and the new **Updates tab**:
a count badge on the tab (painted from the store manifest already on
disk, no network), per-package rows (installed → available, state
chip, the release's `whatsnew` prose), Check for updates, update one
or all with a confirm dialog, and live narration of the pass (the
updater's own Status par, so a wedge names its hop). Failure keeps its
sentence and a next step, per the funnel doctrine.

**Routes.** The console server grew `/api/updates` (GET — `Compare()`
rows joined with `whatsnew`, plus `checking`/`applying`/`detail`),
`/api/updates/check` (POST — deferred `CheckUpdates()`),
`/api/updates/apply` (POST `{names}` — deferred `UpdateProject()`), and
`/api/updates/status` (GET — the live job's stage/results/failed), all
implemented as `Ui*` methods on `ConsoleRegistryExt`. Job kicks are
deferred out of the web-server callback with `run(..., delayFrames=1,
delayRef=op.TDResources)` — the same marshaling cure
`InstallerExt._refreshStore` applies, for the same measured reason.
`PICKER_URIS` now also forwards `/auth/*` and `/settings`, so the
framed picker's account rail (sign in / recheck / redeem / the done
step's Open Settings) answers when the console serves it; before this
those posts 404ed in the frame while the same page served by the
installer answered. The frozen paths (`/api/state`, `/api/set` —
TDXLPP reads them) are untouched.

## Why the framed picker stayed a frame

The chosen direction was "shared base, two shells, no iframe" — and the
iframe survives **as plumbing only**, deliberately. The picker's install
logic (selection/plan/install polling, the entitlement rail, gated-pick
splitting, auto-resume) is the most behavior-pinned code in the project
(`tests/test_picker_flavors.py` lifts its real source lines), and every
one of those behaviors exists once, in one file, served by one
`ServeRequest`. Re-implementing it natively in the console page would
have reintroduced exactly the two-answers drift the single-source
design exists to prevent. With the shared base + embedded mode the
frame is visually indistinguishable from native — same tokens, same
density, `--bg` on both sides of the seam — which is what the "no
iframe" choice was actually buying. If a future need genuinely requires
the catalog UI outside a frame, the extraction path is a shared
`base.js` catalog module, not a rewrite.

## The guided setup's preset bundles

The wizard's first step offers starting points. Four are fixed behavior
(*Set up like last time* / *Recommended* / *Everything* / *Pick my own*);
anything beyond them is **curation, not code**: `catalog.json` may carry

```json
"presets": [
  {"name": "VJ essentials",
   "blurb": "the live-set core: resolution, timeline, media.",
   "packages": ["AutoRes", "FNS_TimelineTools"]}
]
```

`build_manifest._presets()` validates each bundle against the very
package list that manifest ships — an unknown name is dropped and
reported (`preset_problems` on `Build()`'s return), a bundle emptied by
the filter is dropped whole, and a catalog with no curation emits no
key, so older manifests stay byte-identical. The page filters again on
boot (the same discipline as `starter`) and renders surviving bundles
between Recommended and Everything; a bundle pick routes through the
same `choose()` as every fixed preset, so a Plus item in a bundle
composes with the wanted/locked machinery for free.
`tests/test_wizard_presets.py` pins the page's filter from its real
source lines and mirrors the build guard against `catalog.json` (the
build-side guard runs only in TD, so the test is what CI sees).

**Authoring home, deliberately deferred:** presets are content (curation,
no entitlement), so per the CMS split they belong in `cms.mjs` — but
that file is mid-flight in the parameter-reference-rail session, so the
CMS field lands through or after that work, not beside it. Until then
`catalog.json` is hand-edited; the validators above make a typo loud
rather than shipped. The wizard's *flow* (steps, guards, flavor labels)
stays in the page on purpose — it is behavior, pinned by tests, and a
CMS-authored flow would be a second place the funnel is defined.

## Density pass (2026-09-10): overview first

Owner finding: /get is hard to get an overview of. Fifty-nine packages
in eight always-open sections, each card carrying a description, a
byline, three link-outs and up to five chips, under a hero, a meta
line, a chip row, a five-line core note and the Plus rail. Too much at
first glance; /get is the funnel and has to be friendly, the installer
surface may stay raw. Desktop first: this page is not a phone surface,
so a side menu is fair game.

The list, corrected in place as it lands:

1. **Collapsible category sections.** Each category renders as a
   section with a header row (glyph, name, pitch, "N tools, k
   selected", chevron). Header click toggles; open state persists per
   browser (`fns.fold`). Default on the site and the standalone:
   everything collapsed, so the first screen is the eight category rows
   and their pitches, which is the overview. Default when the installer
   serves the page (served or framed): everything open, the raw view.
   A filter query force-opens every section with a match; a preset from
   the guided setup opens the sections it selected into.
   *Landed.*
2. **Core folds away.** The core section collapses by default
   everywhere with a one-line header ("13 packages, always installed")
   and the long persistence note moves inside it. Nothing actionable
   was on the first screen there.
   *Landed.*
3. **A side rail on wide screens.** At 1000px and up the category
   quick-nav becomes a sticky left rail: glyph, name, count, selected
   count, plus Expand all / Collapse all. Clicking a rail entry opens
   that section and jumps to it. Below 1000px it stays the chip row
   above the list (the framed installer picker is narrow).
   *Landed.*
4. **Quieter cards.** Surface chips ("Toolbar button", "Pane bar
   button") leave the card; the surfaces stay searchable and ride the
   card's tooltip. Descriptions clamp to two lines (the full text is the
   tooltip). Plus, placement and integration chips stay: those change
   what happens on install. Doc links stay; site and changelog links
   render only for foreign packages, as before.
   *Landed.*
5. **Shorter hero.** Two sentences and a trimmed meta line. The steps
   strip and the guided setup are unchanged.
   *Landed.*

6. **Core is de-prioritized, same as on the website.** Owner: people do
   not need to know about it. The picker now honours the catalog's
   `deprioritized` flag: Core renders last as a quiet dashed footnote
   ("10 packages, installed with any selection"), never opens by
   default in any flavor, is off the rail, and is gone from the meta
   line; its note is one sentence. Item 2 above is superseded by this.
   *Landed.*

7. **Plus, filterable and said plainly where it surprises.** Owner
   (2026-09-11): people need a Plus-only view, and a reminder of what
   Plus is at the moments they would otherwise learn it at install
   time. A "Plus only" toggle sits in the bar (and as a link on the
   Plus rail); it narrows the list like a search, opening every section
   with a Plus tool. One sentence, `plusReality()`, says what happens to
   a Plus pick in the current flavor (sign in inside TouchDesigner /
   sign in / covered by the membership or waiting for an upgrade), and
   it appears on the rail, on the questionnaire's result (with the count
   of Plus tools in the set and a "Leave Plus out" button), and in the
   paste-script dialog (the script installs the free picks and opens the
   picker for the Plus ones). The count on the result is of what is not
   installable here, so an entitled account's own tools raise no flag.
   *Landed.*

Not in this pass: card art or per-tool screenshots (no assets), a
search-first landing (search is one keystroke away and the overview is
the point), and any change to the install/entitlement logic, which the
flavor pins keep untouched.

## The questionnaire: "Find my set"

The guided setup's first card runs a short questionnaire and ends in a
recommended selection. Questions and their options' tags live in
`catalog.json` under `quiz`; each package carries `fits`, the tags it
answers. The score is a count: how many chosen tags a tool fits, a tag
chosen by two answers counting twice. Every tool with a score is
recommended, best first, each with the answers that brought it as the
reason. The set is what several answers pointed at (score two or more,
ticked); a single-answer match is offered below it unticked under "Also
fits", so six generous answers do not turn most of the catalog into the
selection, and a thin result keeps its single matches in the set. The
reader edits the list before "Use this selection", which routes through
the same `choose()` as every preset. `build_manifest._quiz()` validates the block (an option tag no
shipped package fits is reported; a question with no options is
dropped) and emits `quiz` only when authored, so an unauthored catalog
stays byte-identical; `fits` rides each package entry presence-style.
`tests/test_wizard_quiz.py` lifts `quizScore` from the page and mirrors
the tag validation against the catalog.

Tags over direct option-to-package lists on purpose: a direct list rots
the day a tool is added and nobody remembers the four answers it belongs
to; a tag is declared once on the package and every question asking for
it picks it up. The first `fits` draft (2026-09-10) came from
descriptions, categories and surfaces and is the owner's to review in
the CMS; the questionnaire is content, so its authoring home is the
`cms.mjs` side with presets. Reachable only from Guided setup for now;
a bigger door on the site waits on seeing whether people use it.

## Classification pass (2026-09-11): categories and fits from the content

Owner: re-evaluate the installer categories and the questionnaire's
fits from the actual content, not from memory. Three readers read every
non-core package's doc, its parameters with tooltips, its manifest
surfaces and, where the doc was thin, its extension source; 46 packages,
35 with changes, applied with these judgment calls on top.

**Category moves (5, one withdrawn).** FNS_CommandKit Core to Developer (an SDK piece
you adopt while writing an extension; it was also invisible in the
picker, see below). FNS_HydroHomie Media & Output to Workflow (a water
reminder; nothing to do with media). FNS_OpToClipboard Network to
Parameters (its whole payoff is an operator reference in a parameter
expression). FNS_SetSmoothness Control to Parameters (bulk-sets one
built-in parameter; no hardware anywhere). FNS_PreviewPanel Network to
Surfaces (a pane type you look at, not a way to build or navigate).
FNS_ParentHierarchy Network to Developer was proposed (copies paste-ready
references and lists extension APIs; it reads the path bar, it does not
navigate) and withdrawn the same day: the owner disagreed, and the
counter-argument already stood here, that it lives on the pane bar
beside iopBrowser and the pair is what people meet. It stays in Network;
its `dev` fit stays, so the questionnaire still surfaces it for
component authors.

**Fits.** Twenty-four packages had tags added or removed to match the
doc; the largest corrections were FNS_AutoRes (its tags were an output
tool's; it is an Alt-placement hook), FNS_QuickTime (a toolbar clock of
time references for parameters, nothing about media or the timeline)
and FNS_TimelineTools (media, audio, keyframing and markers; the doc
says nothing about performing live). One rule was set and recorded in
the catalog comment: `visual` means the working surface is something you
look at or work in, not that a button exists; the readers had added it
to nearly every tool with a toolbar button, which would have made the
"Visual" answer match most of the catalog and inflate every set.
FNS_HydroHomie stays untagged on purpose.

**The Core gap.** FNS_CommandRegistry, FNS_PaletteRegistry and
FNS_TimelineRegistry were catalog category Core but manifest kind
tool, because `build_manifest.CORE` was never extended when they were
added. The picker draws Core by kind and skips the Core category, so
these three were never rendered and installed only as a dependency.
They are now in CORE; the change lands at the next `Build()`.

**Descriptions corrected (6)**, where the catalog contradicted the doc:
AutoRes, QuickTime, SwitchOPs, PasteFromClipboard (images only, Windows
only), Output (NDI and Spout/Syphon are half the tool), OpMenuMods
("script injection" was an implementation detail; acronym search is the
feature).

**Found, not fixed here** (content work for the docs and CMS side):
docs whose frontmatter summary is literally "YouTube breakdown"
(ResetPLS, ExprHotStrings, VSCodeTools) or a truncated sentence
(HotkeyManager, AutoRes); stub docs under 20 lines (AutoCombine,
AutoRes, SwapOps, oscMapper, GlobalOutSelect); parameters.json entries
missing or stale (FNS_Misc and FNS_CommandKit have none, ConfigHost
stops at Register while the doc lists five more, BackupCleaner has
empty help on every parameter, PreviewPanel exposes two author-side
"Stub T3D" pulses with no help); BorderlessTD doc says its features ship
on while the parameter defaults are off; ExprHotStrings doc and
parameters disagree on the promote abbreviation (#@~ vs #!~);
SetSmoothness filter-menu labels look shifted by one; ParOPDrop's Key
help describes the reverse of the doc; SearchPalette registers no
surface although it injects UI into the palette; QuickMarks ships
inactive (the questionnaire cannot promise it works out of the box).

## Presentation pass (2026-10-16): the installer shows tools first

Owner finding: the installer interface is intimidating and busy. Measured
on the served first run at the bootstrap window's real size (1040x720,
the `webBrowser` beside `FNS_Installer`): the first tool card began at
document y 743, below the viewport, behind 21 interactive controls and
about 150 words (hero 337 px: eyebrow, headline, three-line paragraph,
meta line, step strip; toolbar 146 px: search row plus six filter
toggles); Patreon was named four times before a tool was picked (the
access filter, the note box, "Not signed in", two sticky-bar buttons);
and the calm view already existed as the Compact toggle, sixth in the
filter row and off by default. The brief is
`briefs/2026-10-16-installer-presentation-pass.md` (gitignored; this
section is its record).

What changed, all in `index.html` (no base.css change, so the console
page and ColorUI are untouched; `tests/test_ui_base_sync.py` green):

1. **One hero line when served.** `html[data-served]` (set in `fnsBoot`
   when `FNS_SERVED` or `FNS_REFRESHING` and not framed) shrinks the hero
   to a 22 px headline and one sentence and hides the eyebrow. The first
   run says "Welcome to FNSTools. Tick the tools you want, then Review
   install"; a root that already holds tools (Pick Tools) gets its own copy
   ("Your toolkit. Tick to install, untick to remove, then review the
   changes below") instead of the site's Textport sentence, which was
   wrong inside TD. The site and the standalone keep the headline and one
   sentence. The meta line (count, sha256, release, TD build) is gone from
   every flavor; release, TD build and the verification promise now sit in
   the Install plan hint (served) and the script hint (site), where the
   download question is actually asked. The `#sub` element stays for the
   store-refresh status and hides when empty. **The step strip is removed
   everywhere** (`setStep` and its eight call sites): with the hero at one
   line there is no row for it, and the primary button names the next
   step. Density pass item 5 is superseded by this.
2. **One toolbar row.** The `bar-filters` row (access segment, Selected,
   Placeable, New, Compact; plus Expand/Collapse all when framed) is a
   popover under a **View** button beside the search, anchored to the
   button's right edge, closed by Escape or an outside click. The button
   carries a count while any filter narrows the list, and the results line
   keeps its removable pills, so a hidden filter can never read as a lost
   catalog. The access segment moved with the others: the Plus-only view
   the owner asked for (2026-09-11) is one click deeper and still one
   click to clear; pull it back beside the search if that proves wrong.
3. **A one-line list by default when served.** `compactOn` defaults to
   on when `FNS_SERVED` and nothing is stored under `fns.compact`; a
   stored choice wins; the site and the standalone stay card-first. The
   dense view itself changed the same day: the title-only tiles the
   Compact toggle drew (owner, 2026-10-03) said nothing to a newcomer
   (owner, 2026-10-16: "just listing their names is not enough"), so a
   dense card is now a row -- the name in a 180 px column, the description
   clamped to one line beside it (the full text still rides the tooltip),
   the state chips at the row's end, the docs link on hover; the byline,
   hint and where-chips stay hidden. Measured at 1040x720: 34 px per row,
   22 rows in the first screen, about 450 px of description per row
   (388 px in the 760 px console frame). Two traps paid for on the way: a
   bare `1fr` grid column is `minmax(auto, 1fr)`, and the one-line
   description's min-content width is the whole sentence, so the list
   blew out to 2700 px until the column became `minmax(0, 1fr)`; and the
   pin in `tests/test_picker_search.py` that lifted the old "Compact hides
   the description" selector moved to the new behavior (description kept
   on one line; byline, hints, where-chips hidden), with
   `configurator-standalone.html` regenerated from the page the way
   `build_manifest.py` does, because that test reads both shells. The
   served flavor also takes `body.app` (the manager's density), keeping
   the category pitch, which the window has the width for. Sections stay
   open when served, as before: the rail is the overview, and one-line
   rows keep open sections short, so collapsed rows plus a rail would have
   listed the categories twice.
4. **Patreon said once.** Served (in TD or framed) the rail runs
   `compactPatreonLine`: one sentence, only while something needs doing,
   with the action that fixes it; the account controls that the sticky
   bar carried (`acct`, Sign in, Check again, Join, Redeem) follow onto
   that line, each wrapped so a hidden one takes its separator with it,
   and Join stays hidden while signed out (the Patreon dialog and the docs
   link cover it, as in the console). The sticky bar keeps the count and
   Review install. The site rail lost its preamble ("the free tools are
   the full toolkit...") and is one sentence: the count, "listed last in
   each section", `plusReality()`, the link. Section headers show "Select
   section" and "docs" only on hover or focus. The theme toggle is hidden
   when served.

Measured after, same window and flags: hero 75 px, toolbar 58 px, first
tool card at document y 303 with 22 list rows inside the first screen; 16
controls before the first card, 6 of them the rail's category links; the
sticky bar holds two items. Framed at 760 px the page still fits (no
horizontal scroll), the View menu holds Expand/Collapse all, and the
embedded chrome is unchanged. The test pins the pass had to keep:
`tests/test_picker_search.py` lifts the `bar-row bar-filters` div and the
Compact button's `aria-pressed="false"` markup, `COMPACT_KEY` and its
storage line; `tests/test_picker_flavors.py` requires the four remedy
controls hidden in markup and every unhide behind the `hasAuthRail`
guard. Both hold because the markup moved into the popover rather than
being rewritten.

Not in this pass: card content, the guided setup's presets and
questionnaire, the console chrome, the rails rebuild. The page reaches the
dev installer only through `EnsureDevRails()` and users only with the next
rails release (see Landing notes).

## Wizard phase 1 (2026-10-17): the set is the home screen

`docs/InstallerWizardFlow.md` (status open) sketched the picker as a
wizard: the selection is the home screen, the catalog a sub-screen entered
to add tools, one job per screen. This is the first phase of its landing
plan, built on the presentation pass above; the welcome dialog and the
install dialog stay where they were, so the page is shippable at this
step. The prototype the owner approved is the artifact linked from that
doc; the owner's explicit ask, that the categories stay in the list with
every section open when served, holds.

What changed, all in `index.html` (no base.css change;
`tests/test_ui_base_sync.py` green):

1. **Two screens over the existing DOM.** `<main>` holds `#screen-set`
   (S2) and `#screen-catalog` (S3: the presentation pass's hero, toolbar,
   rail and list). `setScreen()` toggles them and writes the screen to the
   hash with `replaceState` (`#set`, `#catalog`; the rail's `#cat-<slug>`
   jumps and the access deep links mean the catalog), so a reload and the
   console frame land where the reader was, and `hashchange` follows a
   hash set from outside. Landing: the hash wins; else a re-entry
   (`FNS_INSTALLED` or `FNS_PLACED` non-empty) and the console frame land
   on the set, a first run and the site on the catalog. The first-run
   welcome opens over the catalog as before; a starting point lands on the
   set, Pick my own (and Esc) on the catalog, since an empty set answers
   nothing. The site's once-per-browser welcome follows the same rule, so
   the site lands on the catalog with the set one click away on the
   count.
2. **S2, "Your set" on a first run and "Your setup" on a re-entry.**
   `renderSet()` runs at the end of every `render()`: the picks as rows
   grouped by category (glyph heading; title, chips, the description on
   one line, the docs link on hover, a remove control). A row the project
   loses stays visible, struck, "will be removed", with undo; placed-only
   tools sit in their own group. State chips (installed, will install,
   will be removed) appear only on a re-entry (`reentry`), where they
   carry a difference; the catalog's cards follow the same rule, so a
   first run no longer says "will install" on every card. Above the list,
   only when they apply: the Patreon line (`renderPlusLine`, counted on
   this set, with the one action that fixes it: sign in, I just pledged,
   or upgrade; the site gets `plusReality()`) and the options row (the FNS
   tab switch, which left the sticky bar). Two dialogs became banners:
   "N new tools since you last looked" (See them opens the catalog
   filtered to New; Not now and Stop announcing record them as shown; the
   `newtools` dialog markup and `showNewTools` are gone) and the catalog
   reload offer (`offer()` appends to `#banners`, which `setScreen` carries
   to whichever screen is up). The footer: the count with the adds,
   removals and download size (`downloadSize()`, from the manifest's
   artifact bytes, core included on a first install), Clear, Add tools,
   and the page's own primary (`#save`: Review install, Apply changes, or
   the source lock; `#script` on the site). Served, the set fills the
   window so the footer sits at its bottom. Empty state: one sentence and
   Add tools. The account is one chip in the header (`#acctchip`); the
   status line and the sign-in, recheck, join and redeem controls the
   account block fills sit in a menu behind it, so the catalog's Patreon
   rail line is gone when served (the tiles carry the chip) and
   `compactPatreonLine` with it. Guided setup is the header's button.
3. **S3, "Add tools".** The presentation pass's catalog body with a
   "Your set" control at the start of the toolbar row; every section open
   when served, the rail and the fold controls, one-line rows by default
   in TouchDesigner, all unchanged; a sticky footer "Done, N selected"
   returns to the set (in the console frame it moves into the toolbar's
   right end, the spot the presentation pass used for the count, and the
   catalog's footer goes; the set keeps its own). Core is not shown
   (`coreCard`, the core section and the core note went; the plan dialog
   already names the core count). The Selected filter went with the tray:
   the set is the selection. No install from this screen.

Measured at 1040x720 on the simulated served flavors (the installer's
globals prepended to the real manifest). First run, after Recommended: the
set shows 16 rows in 5 groups (35 px per row, 20 px headings with the
manager's density; the list has 586 px between the header and the stuck
footer, so about 13 rows in three groups fit without scrolling and this
set runs to 838 px); the catalog is as the presentation pass left it, with
the search focused on entry. Re-entry: "Your setup", installed chips, the
new-tools banner; unticking an installed tool and ticking a new one in the
catalog gives a struck row with undo, a "will install" row, and a footer
of "9 tools, 1 to add, 1 to remove, 16 KB to download, Apply changes".
Framed at 745 px the set has no horizontal scroll and its footer sits at
the frame's bottom; the catalog's Done sits in the toolbar. Live in
TouchDesigner (`EnsureDevRails()`, then Pick Tools on the dev root): the
console frames the set as "Your setup" with the 84 installed tools, the
account chip "supporter, 40 unlocked" with its menu, the FNS tab row, the
catalog with its 12 sections open and Done in the toolbar; both error
surfaces clean, no browser console errors. The dev root is the toolkit's
source checkout, so its primary reads "Locked (source checkout)" and the
plan dialog could not be exercised there; the Review install handler is
untouched, and in the simulated page the click opens the dialog titled
"Install plan" (which then names the missing server).

Test pins moved, each because an element moved: `tests/test_new_tools.py`
(the dialog's auto-open, ids and cancel handler became the banner's
builder, its `seen()` and its ids) and `tests/test_family_optional.py`
(the switch's home is the set's options row, not the embedded toolbar).
The seven picker tests the flow doc names held unchanged.
`configurator-standalone.html` was regenerated from the page the way
`build_manifest.py` does.

Not in this phase: S0 and S1 as screens (the welcome dialog stays), S4
(the plan, progress and done dialog states stay), the per-flavor landing
table beyond the rule above, the bind-mode option (no control exists
today), the rails rebuild (the page reaches the dev installer through
`EnsureDevRails()` and users only with the next rails release, see Landing
notes).

## Wizard phases 2 to 4 (2026-10-17): every screen, the landing per flavor

The rest of `docs/InstallerWizardFlow.md`, on top of phase 1 above. The
welcome dialog is gone: a first run opens on a Start screen; the
questionnaire is its own screen; the plan, the progress narration and the
done report are three states of one install screen; the step strip is
back, as the header of every screen, and it is the navigation.

What changed, all in `index.html` (no base.css change;
`tests/test_ui_base_sync.py` green):

1. **The header (`#wizhead`).** The three steps (Start, Your set, Install;
   the last reads "Install script" off-machine), the account chip and
   Start over. `setScreen` moves it to the top of whichever screen is up
   and lights the step the screen belongs to (the catalog is a sub-screen
   of the set, the questionnaire of Start). The steps are buttons: Start
   reopens the starting points, Your set the home screen, Install presses
   the set's primary; the Install step is disabled while the primary is.
   Start over and the chip step aside on Start and in the questionnaire.
2. **S0 Start (`#screen-start`).** The welcome's cards, filled by
   `showStart()` from the manifest and the machine's record on every show
   (Set up like last time, Answer a few questions, Recommended, the
   curated bundles, Everything, Pick my own; the bundle lines the preset
   test pins are unchanged), one lead sentence, the counts sentence with
   the sign-in link only when the account cannot install something
   (`renderWelcomeAccess`, unchanged), and a line of facts that was the
   hero's meta line: release, TD build, "every download sha256-verified",
   the docs link. A choice marks the visit welcomed (the auto-resume guard
   reads it) and lands on the set; Pick my own lands on the catalog. The
   title reads "Welcome to FNSTools." on a first run or a first visit and
   "Choose a starting point." from Start over. The store-refresh state
   renders its note on this screen, the cards hidden until the catalog
   lands; the pinned refusal lines are unchanged.
3. **S1 Find my set (`#screen-quiz`).** The questionnaire's markup moved
   out of the dialog into a screen with a sticky footer (Back, Next, Use
   this selection); `quizShow` switches screens, `quizRender`, `quizScore`
   and `quizSplit` are unchanged. Back on the first question returns to
   Start; Use this selection lands on the set.
4. **S4 Install (`#screen-install`).** `showInstall(state, text, hint)`
   renders one screen in five states: plan (the installer's plan parsed
   by `showPlan` into chips, the Install button only when the plan was
   accepted; a refusal keeps its sentence and no button), progress (the
   updater's narration from `installOrPoll`; Close stops the poll and
   returns to the set), done (`finished`: the count, the tool chips
   linked to their docs, removals and failures marked, the done hint, Open
   Settings and Close), failed (what stopped, with Install again) and,
   off-machine, script (the paste script with Copy and, on the
   double-clicked file, Download selection.json beside it; the website has
   no download, owner 2026-09-27). Set up like last time plans and installs
   through the same screen. The transient dialog (`showDialog`, signature
   unchanged for the reconnect test) keeps the sign-in waits, the recheck
   and redeem answers, a refusal in the auto-resume flow and a server that
   is gone; it carries no install controls any more.
5. **Landing per flavor** (the flow doc's table): the hash wins (`#start`,
   `#set`, `#catalog`, `#install`; a reload mid-questionnaire lands on
   Start and mid-install on the set); the console frame lands on the set;
   served, a first run lands on Start and a re-entry on the set; the
   website and the file land on Start once per browser and on the catalog
   after, with the set one click away on the count. A locked source root
   lands on the set with one banner saying why, the primary reading
   "Locked (source checkout)" as before and the catalog still browsable;
   the flow doc's one-screen notice became this banner, since the set
   already carries everything else the reader needs.

Measured at 1040x720 on the simulated flavors (the installer's globals
prepended to the real manifest). Served first run: Start with four cards,
the counts line and the facts line fits without scrolling; Answer a few
questions walks six questions and a result of 58 rows with the Patreon
box and lands on a set of 19; Review install opens the install screen on
"Planning" and, with no server behind the simulation, the dialog names
the missing server over it; Back, the Start step and Pick my own land
where the doc says. A machine with a record shows Set up like last time
first. Re-entry lands on "Your setup"; Start over reads "Choose a
starting point."; the Your set and Install steps navigate. The locked
root shows the banner and the disabled primary. The store-refresh state
shows its note on Start with the header in place. The website's first
visit lands on Start, Recommended on the set with "Install script" as the
primary, which opens "Paste this into the Textport" with the script and
Copy; the second visit lands on the catalog with the picks kept. The file
adds Download selection.json beside Copy. The console frame at 745 px
lands on the set, Start over reaches Start inside the frame and
Recommended returns to the set. Live in TouchDesigner
(`EnsureDevRails()`, Pick Tools on the dev root): the console frames the
set with the installed tools and the header; the dev root is the source
checkout, so the plan screen could not be exercised there.

Test pins: none moved in this pass; the welcome's pinned lines live in
`renderWelcomeAccess` and the bundle code, which moved whole, and
`showDialog` kept its signature. `configurator-standalone.html` was
regenerated from the page the way `build_manifest.py` does.

Not in this pass: the rails rebuild and the FirstRunTestPlan runs on a
clean TD (the flow doc's phase 4 names both; they are the release motion,
`packaging/RELEASING.md`), and the bind-mode option on the set (no control
exists today). The flow doc stays open until those land.

## Wizard phase 5 (2026-10-17): the catalog is the home, the set a drawer

The owner used the wizard of phases 1 to 4 and rejected its shape the same
day: with the set as the home screen the catalog sat behind an "Add
tools" button, every flow ended on the set, and after an install, or in
the console's Install and remove tab, the only way to see all the tools
was Start over and Pick my own. "The flow should bring you to explore
other tools still." `docs/InstallerWizardFlow.md` was revised (its
revision note, "The shape", "S2 Pick your tools" with "The set drawer",
Landing plan item 5) and the prototype linked from it shows the target.
This phase lands that revision on top of phases 1 to 4 (commits
`842062da`, `ee247d31`).

What changed, all in `index.html` (no base.css change;
`tests/test_ui_base_sync.py` green):

1. **The set is a drawer, not a screen.** `#screen-set` keeps its ids
   and `renderSet()` keeps filling it, but it is a fixed panel on the
   right edge (560 px, 92 vw at most, its own scroll) under a scrim
   (`#drawerscrim`), opened from the catalog footer's count button
   (`#catdone`, now "Your set · N" or "Your setup · N"), closed by its
   Close button, the empty state's "Back to the tools", Escape, or a
   click on the scrim. Its head is sticky and carries the title, the
   one-line hint, Clear and Close; the Patreon line and the options row
   sit at its top as before. It carries no install button: the drawer
   is for reading and pruning the selection, never the place you have
   to be. `setDrawer()` owns it; it is not in the hash. `SCREENS` lost
   `set`; `setScreen('set')` (and an old `#set` link) opens the catalog
   with the drawer.
2. **The catalog is the home.** Its footer (`#catfoot`) took the count
   line (`#cnt`, `#cntlabel`, `#cntmore`, `#deps`), the drawer's button
   and the page's primary (`#save` served, `#script` off-machine); the
   set's footer went, and with it "Add tools" (both of them) and "Done,
   N selected"; the "‹ Your set" back control left the toolbar. Served,
   the hero reads "Pick your tools." on a first run and "Your toolkit."
   on a re-entry (`heroServed`, from `FNS_INSTALLED`/`FNS_PLACED`); the
   site keeps "Build your install." with a sentence that names the
   footer. The banners live in `#catbanners` for good (the new-tools
   banner, the catalog reload offer and the locked-root banner all show
   on the list); the slot-moving code in `setScreen` and the banner's
   screen check went. The step strip reads Start, Pick tools, Install;
   the second step opens the catalog.
3. **Every flow lands on the list.** `choose()` (every starting point
   and the questionnaire's Use this selection) calls `landOnCatalog()`:
   the catalog, the picks ticked, and a toast ("16 tools ticked. Browse
   the rest; untick anything you do not want.") from the base's `.toast`
   class, which had styles and no caller; with nothing picked the search
   takes focus instead. The install screen's Back reads "Back to the
   tools" and returns to the catalog, Close on the progress and done
   states returns to the catalog, and the done state gained "Browse more
   tools" as its primary (`#instbrowse`; Open Settings became the
   secondary). Landing: the console frame and a served re-entry land on
   the catalog; a served first run still lands on Start; the site and the
   file land on Start once per browser and on the catalog after;
   `#install` in the hash lands on the catalog.
4. **In the console frame** the toolbar's right end (`.bar-act`) takes
   the count, `#deps`, the drawer's button and the primary, and the
   footer goes, the place the presentation pass gave the count and the
   install button.
5. **A ticked row is marked quietly**: the checkmark and a firmer border
   (`--border-strong`, `--bg-2`), no accent outline and no gradient;
   sixteen outlined rows read loud at 1040x720.

Measured at 1040x720 on the simulated served flavors (the installer's
globals prepended to the real manifest). First run: Start, then
Recommended lands on "Pick your tools." with 16 rows ticked, the toast,
and a footer of "16 tools · 7.3 MB to download · Your set · 16 · Review
install"; the drawer opens at 560 px with 16 rows under its head, a row
removed there drops the count to 15, Escape closes it; Review install
opens the install screen on "Install plan" (the simulation has no server,
so the dialog names it) with Back reading "Back to the tools" and Browse
more tools hidden until done. Re-entry: "Your toolkit.", 16 installed
chips, a footer of "16 tools · Your setup · 16 · Review install";
unticking an installed card gives "15 tools · 1 to remove · Apply
changes" and a struck row with undo in the drawer; the scrim closes it;
with two unseen free tools the new-tools banner sits at the top of the
list and See them filters it to those two. Framed at 730 px: the toolbar
holds "16 tools · Your setup · 16 · Review install", no footer, no
horizontal scroll, the drawer opens at 560 px. Live in TouchDesigner
(`EnsureDevRails()`, then Pick Tools on the dev root): the served page
lands on the catalog as "Your toolkit." with 68 ticked, the lock banner
on the list, the footer "68 tools · Your setup · 68 · Locked (source
checkout)", the account chip "supporter"; the drawer opens with 68 rows
in 12 groups, the Patreon line and the FNS tab row at its top, and
closes; no browser console errors. The dev root is the source checkout,
so the plan itself is not reachable there.

Test pins: none moved. The nine page tests (`test_picker_flavors`,
`test_wizard_presets`, `test_wizard_quiz`, `test_picker_search`,
`test_picker_catalog_check`, `test_picker_window_alive`,
`test_family_optional`, `test_new_tools`, `test_ui_base_sync`) pass as
scripts. `configurator-standalone.html` was regenerated from the page
the way `build_manifest.py` does.

Not in this phase: the "Review install" label on a re-entry with nothing
changed (the primary stays enabled and the plan answers "nothing to do",
as before). Shipped the same day: the rails were rebuilt as 3.2.72 (the
bootstrap carrying updater 3.2.28) and published with release v3.2.72;
the staged bootstrap was expanded offline and carries the drawer page,
and two of its artifacts installed clean into a cooking-disabled trial.
The FirstRunTestPlan runs on a clean TD remain. The root tox carries the
refreshed dev picker page (saved by a later PI save that day).

## What update announcing deliberately is NOT

- The web/get flavor has no updates surface — updates are meaningless
  off-machine, and the shell split is what makes that free.
- The Updates tab never invents a decision: `Compare()` is the single
  decision point (update / current / locked / incompatible /
  unversioned / missing), and the tab renders its states verbatim,
  release notes attached.
- Install and update stay separate motions (the plan dialog may say an
  update exists; applying it lives here).

## Landing notes

- `index.html` is an embedded snapshot in the installer rails: after
  landing, run `EnsureDevRails()` and rebuild the rails per
  `packaging/RELEASING.md`, or the live picker keeps serving the old
  page (Phase-3 errata in `EntitlementFunnelPlan.md` documents this
  trap).
- `console_page.html`, `ConsoleRegistryExt.py` and
  `console_server_callbacks.py` are externalized with `syncfile` — they
  hot-reload on landing; the /sys console global runs a COPY of the ext
  DAT, so push + reinit (or re-promote) before testing, per
  `/fns-registry`.
- ~~ColorUI's `webui.html` still carries the third token family~~ DONE
  (2026-08-30): ColorUI inlines the synced base with its legacy var names
  mapped onto the tokens, and the console serves `/base.css` (sliced from
  the page's own synced block) so future contributed tabs link it instead
  of re-declaring a palette — the styling section of
  `docs/ConsoleTabContract.md` is now the contract. The three token
  families are one.
