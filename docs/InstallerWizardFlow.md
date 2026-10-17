---
status: open
summary: The install picker becomes a wizard with one job per screen (start, pick your tools, install); the catalog of tools under its category headings is the home every flow lands on, the selection is a drawer over it and never a destination, compact one-line rows are the default inside TouchDesigner, and Patreon is said once per screen. Sketched 2026-10-16; phases 1 to 4 landed 2026-10-17 with the set as a screen, which the owner rejected the same day; phase 5, the rework to the drawer, landed the same day; the rails rebuild and the clean-TD first-run runs remain, with the release.
since: 2026-10-16
skill: fns-packaging
---

# The installer as a wizard

A clickable prototype, built from the real v3.2.70 catalog at the
installer's window size, is at
https://claude.ai/artifact/TvpZNMbyW9Y3TNiaDiByP4 (private to the owner;
installs simulated). It shows the revised shape below.

**Revision 2026-10-17.** The first sketch made the selection ("Your set")
the home screen and hid the catalog behind an "Add tools" button. Built as
phases 1 to 4 (see Landing plan), it failed the owner's first look: it does
not encourage exploring tools, every flow ended on the set, and after an
install, or in the console's Install and remove tab, the only way to see
the catalog was Start over and Pick my own. The shape is now inverted: the
catalog is the home, every flow lands on it with the picks ticked, and the
set is a drawer over it.

The picker page (`packaging/configurator/index.html`) is one catalog page
with a guided-setup dialog laid over it. The wizard gives it a first screen
of its own, a proper install screen, and a selection you can see at any
time without leaving the tools. The install logic, the entitlement rail,
the plan parsing, the presets and the questionnaire stay as they are; what
changes is where each of them is rendered and what the reader meets first.

## Why

Measured on 2026-10-16 on the served first-run flavor (the flags the
installer injects, the real manifest) at the size of the bootstrap root's
`webBrowser` window, 1040 by 720. The owner's words: intimidating and busy.

| At 1040x720, served first run | |
|---|---|
| Top of the first tool card | 743 px, below the 720 px viewport |
| Hero (eyebrow, headline, three-line paragraph, meta line, step strip) | 337 px |
| Toolbar (search row, then six filter toggles) | 146 px |
| Interactive controls before the first checkbox | 21 |
| Words before the first checkbox | about 150 |
| Items in the sticky bottom bar | 5 |
| Times Patreon is mentioned on the first screen | 4 |

What the numbers mean:

- The first screen contains no tools. Everything above the fold is
  framing: the hero explains the mechanism (the container, verification,
  Pick Tools), the step strip repeats the hero's sentence, the meta line
  names the hash scheme and the TD build.
- Three navigation systems compete: the category rail, the six-toggle
  filter row and the search box all slice the same list, with Guided
  setup as a fourth door. Power-user toggles (Placeable, Compact,
  Selected) sit at the same weight as the primary ones.
- Patreon appears in the segmented filter, in a three-line note box, and
  three times in the sticky bar (Not signed in, Join on Patreon, Sign in
  with Patreon), before a single tool is picked. InstallSurfaceDesign.md
  asked for one understated line.
- The calm view exists and is hidden: Compact mode (title plus checkbox,
  three per row) shows two whole sections in the height where the card
  view shows seven tools. It is the sixth filter toggle, off by default.
- The 2026-09-10 density pass chose "everything open, the raw view" for
  the installer flavor and "everything collapsed" for the site. The raw
  view is the one that reads as intimidating.

## The shape

Two decisions carry the rest.

**The catalog is the home.** Every flow lands on the list of tools under
their category headings: a starting point ticks its tools and drops the
reader on the list with a one-line toast ("16 tools ticked. Browse the
rest; untick anything you do not want"); the questionnaire's "Use this
selection" does the same; the done screen's primary action is "Browse
more tools"; the console's Install and remove tab and Pick Tools on a
project that has tools open the list with the installed tools ticked and
their state on the rows. The owner's rule (2026-10-17): the flow must
keep you exploring, at the end of every branch.

**The set is a drawer, never a screen.** "Your set · 16" in the footer
opens a drawer over the list: what will land in the project, grouped by
category, each row with remove and undo, the Patreon route for locked
picks and the options row at its top. Close it and the list is where you
left it. Nothing is reachable only through the drawer; it is a way to
read and prune the selection, and Review install sits in the footer
beside it, not inside it.

Everything else follows: one toolbar row, no hero, compact rows by
default, Patreon said once per screen in the voice that screen needs
(counts on Start, the route in the drawer, the chip on a row).

## Screens

The step strip that exists today becomes the real navigation: three dots
at the top (Start, Pick tools, Install), Back always available, one
primary action bottom right. Budgets are for the 1040x720 window.

### S0 Start

The welcome dialog, promoted to a screen; there is no catalog behind it
to dismiss into.

- One line: "Welcome to FNSTools." One sentence under it: "Pick a
  starting point. Nothing installs until you review the plan."
- The starting points as cards, the same five plus curated bundles the
  dialog offers today: Set up like last time (served, bare root, record
  present; installs in one go, as now), Answer a few questions,
  Recommended, bundles, Everything, Pick my own.
- One line of counts, the `renderWelcomeAccess()` sentence ("46 tools
  are free, 1 has a free trial, and 24 come with Patreon"), with the
  sign-in link only when the account cannot install something.
- Footer, small: release, TD build, "sha256-verified" and the docs link.
  Nothing else from the hero survives.
- Budget: under 60 words before the cards, no toolbar, no rail.
- Every card lands on S2, the list: Pick my own with nothing ticked, the
  others with their tools ticked and the toast naming the count.

### S1 Find my set

The questionnaire, as its own screen instead of a dialog state: one
question per view, "Question 2 of 5", Back and Next, the result view
with the ticked set and the reasons. Unchanged logic (`quizScore`,
`quizSplit`); "Use this selection" lands on S2 with the set ticked.

### S2 Pick your tools

The home: the catalog, and the one place the reader spends the session.

- Title "Pick your tools" on a first run, "Your toolkit" on re-entry,
  one sentence under it. No hero, no meta line.
- Header row: the search box, a View menu (Cards with full descriptions,
  Free only, Patreon only, Placeable, New). No back button: there is
  nothing to go back to.
- The category rail on the left as today. The list is the tools under
  their category headings, every section open when served (owner,
  2026-10-16: the categories stay, in the list), so the rail jumps and a
  section or all of them can still be folded; the presentation pass
  found the same (open sections plus a rail, since collapsed rows plus a
  rail list the categories twice). The site keeps collapsed by default,
  where the first screen is the overview. A search or a View filter
  opens what matches.
- Compact rows by default: checkbox, title, the Patreon chip (and the
  state chip on re-entry), the description on one line, the format of
  the questionnaire's result, which the owner singled out (2026-10-16:
  "this compactness is great"). The docs link and the surface list ride
  the tooltip; Cards with full descriptions in the View menu brings
  today's cards back for someone who wants to read.
- A ticked row is marked quietly (the checkmark and a slightly stronger
  border), never a full accent outline: sixteen outlined rows read loud.
- Re-entry shows the diff on the rows: "installed", "will install",
  "will be removed" with the row kept visible and undo. On a first run
  no state chips, since every row would say the same thing.
- The row's secondary action stays: "place in this project only" for
  placeable and family packages, and the Patreon prompt on ticking a
  locked tool (the modal stays; it is a decision with three answers).
- Section header: glyph, name, pitch, count. "Select section" and the
  section docs link move behind a small menu at the row's end.
- Banners, not modals, at the top of the list: "N new tools since you
  last looked" with a button that filters the list to them; "A newer
  release is in the store" with Reload. Both exist today as dialogs.
- Footer: the count and download size ("16 tools · 7.2 MB to download",
  or on re-entry "16 tools · 1 to add · 1 to remove") on the left,
  "Your set · N" (secondary, opens the drawer), and "Review install" (or
  "Apply changes" when a removal is in the set) as the primary. With
  nothing ticked the footer says so and the primary is absent.
- Core is not shown. It installs with any selection and S3 names it.

#### The set drawer

Opened from the footer, closed by its button, Escape or a click outside.
Over the list, from the right, under the header.

- Head: "Your set" (or "Your setup" on re-entry), the same count line as
  the footer, Clear, Close.
- At the top, only when they apply: the `plusReality()` sentence counted
  on this set ("2 of these need a Patreon sign-in") with the one action
  beside it (Sign in with Patreon, Check again, or Upgrade), and the
  options row ("Add FNS tab to OP Create" when a family member is in the
  set; the bind mode when the record carried one). Above the rows
  because a set of sixteen scrolls, and the route has to be seen before
  Review.
- The set as compact rows grouped by category: title, chips, one-line
  description, remove; a removed row on re-entry stays visible, struck,
  with undo. A placed-only tool sits in its own group, "In this project
  only".
- Empty: one sentence and "Back to the tools", which closes the drawer.
- The drawer carries no install button; Review install stays in the
  list's footer so the drawer never becomes the place you have to be.

### S3 Install

The plan dialog, the progress narration and the done report, promoted to
one screen with three states. The texts are the installer's own, parsed
as `showPlan()` and `finished()` parse them today.

- Plan: "Install 9 tools and 10 core packages, 14 MB, sha256-verified
  into /project1/FNSTools"; installs, removals and problems as chips;
  "Back to the tools" and the Install button. A refusal (locked source
  root, a gate refusal) keeps its sentence and its next step, per the
  funnel doctrine.
- Progress: the updater's stage line (authorising, fetching, verifying,
  installing) and the counter; Close stops the poll as it does today and
  returns to the list.
- Done: the count, the tool chips linked to their docs, removals and
  failures marked, the two lines of HINTS.done, and three buttons: Close
  (quiet), Open Settings, and "Browse more tools" as the primary, back to
  the list with the installed tools ticked. The end of an install is a
  door back to the tools, not an exit.

## Entry points per flavor

| Flavor | Lands on | Notes |
|---|---|---|
| Served, first run (bare root) | S0 | The bootstrap opens the page by itself, as today |
| Served, re-entry (Pick Tools) | S2 as "Your toolkit" | Installed tools ticked with their state on the rows; Start over in the header reopens S0 |
| Served, paste arrival with Plus picks | S2 | The auto-resume flow runs as today and narrates on S3 |
| Served, locked source root | S2 with a banner | No install; the list stays browsable |
| Served, store refreshing | S0 with the fetch state | The page reloads itself when the catalog lands, as today |
| Embedded in the console | S2 | The console carries identity and tabs; the Install and remove tab is the list, with the drawer |
| Site /get/ | S0 once per browser, then S2 | People come to the site to browse |
| Standalone file | As the site | Keeps the selection.json download beside the paste script on S3 |

On the site and the standalone file S3 has no install: it shows the
paste script (with the Plus note the script dialog carries today) and,
on the file, the selection.json download. The step strip's last label
already changes per flavor; S3's title does the same.

## Where everything goes

The completeness check. Every element the page shows today, and its
home in the wizard.

| Today | New home |
|---|---|
| Hero eyebrow, headline, three-line paragraph | S0 title and one sentence; S2 has a title and one sentence |
| Meta line (count, sha256, release, TD build) | S0 footer; the download size on S3 |
| Step strip | The header of every screen |
| Search box | S2 header |
| Guided setup button | "Start over" in the header |
| Theme toggle | Removed in the served flavor; the site header keeps its own |
| Docs link | S0 footer and the S2 section menu |
| Access filter (All, Free, Patreon) | S2 View menu |
| Selected toggle | Gone; the drawer is the selection |
| Placeable, New toggles | S2 View menu; New also as the S2 banner |
| Compact toggle | The default on S2; the cards view is the menu item |
| Category rail, Expand all, Collapse all | S2, with the sections open under their category headings |
| Plus rail note box | S0 counts line; the drawer's plusReality line; row chips |
| Select all, Clear | S2 section menu (Select section) and the drawer (Clear) |
| Card description, docs link, surfaces, chips | S2 rows carry title, chip and the description on one line; docs link and surfaces in the tooltip; the cards view in the View menu |
| Place in this project only | S2 row action; drawer group |
| Patreon prompt on a locked pick | Unchanged modal |
| Sticky bar count | S2 footer and the drawer head |
| Not signed in, Join on Patreon, Sign in with Patreon | The drawer's plusReality line, only when it applies; the header chip |
| Redeem Gumroad key, Check again | Behind the header chip |
| Add FNS tab to OP Create | The drawer's options row |
| Review install, Apply changes | S2 footer primary |
| "Add tools", "Done, N selected" (phase 1) | Gone; the list is always there |
| Copy install script, Download selection.json | S3 on the site and the file |
| Install plan dialog | S3 plan state |
| Progress and Installed dialogs | S3 progress and done states |
| New since you last looked dialog | S2 banner |
| Catalog reload offer | S2 banner |
| Single-download warning | Unchanged, site only |
| Community pointer line | Removed from the installer; CommunityHighlights.md already moved it to the console |
| Core footnote section | Removed; S3 names the core count |
| Locked source root note | S2 banner |
| Store refreshing note and refusal | S0 state |

## State

One selection, as today: `picked`, `placing`, `familyOn`, `wantBind`.
Every screen derives from it; no screen keeps a copy. `screen` is
navigation state held in the page, carried in the URL hash so the
console frame and a reload land where the reader was (the console
already addresses the page by hash); the drawer is not in the hash, it
is a transient view of the list. Per browser, as now: the fold state,
the cards preference, the theme. Per visit: the welcomed flag. Nothing
new is persisted.

## What does not change

- The server routes and their payloads: `/selection`, `/install`,
  `/status`, `/auth/*`, `/settings`, `/open`, `/recommendations.json`,
  `/manifest.js` and the globals it injects.
- The functions the tests lift from the source: `isPlus`, `entitled`,
  `installable`, `selection`, `installScript`, the auto-resume guard,
  `quizScore`, the preset filter, the search ranking, the catalog check
  and the keep-alive. `tests/test_picker_flavors.py`,
  `test_wizard_presets.py`, `test_wizard_quiz.py`,
  `test_picker_search.py`, `test_picker_catalog_check.py` and
  `test_picker_window_alive.py` pin behavior, not layout.
- The shared base: tokens and components come from `base.css` through
  `sync_base.py`; new screen styles join the page's own block.
- The embedding seams: the page stays one self-contained file, served
  from the Text DAT and baked into /get/ by the site build; the console
  keeps framing it.

## Landing plan

Each phase leaves the page shippable. Phases 1 to 4 built the first
sketch, with the set as a screen; phase 5 is the rework to the shape
above.

1. **Screens and the home.** A `screen` switch over the existing DOM;
   the set built from the selection as a screen; the list with compact
   rows default and the toolbar folded into one row; the sticky bar
   became per-screen footers. Landed 2026-10-17 (uncommitted at the time
   of writing); the record is the section "Wizard phase 1 (2026-10-17)"
   in `InstallSurfaceDesign.md`. The new-tools and catalog-reload
   banners landed with it.
2. **Start and the questionnaire as screens.** S0 and S1 replaced the
   welcome dialog; the dialog markup went. Landed 2026-10-17
   (uncommitted at the time of writing); the record is the section
   "Wizard phases 2 to 4 (2026-10-17)" in `InstallSurfaceDesign.md`.
3. **Install as a screen.** The plan, progress and done dialog states
   became a screen. Landed 2026-10-17, same record.
4. **Flavors and landing.** Entry points, the site and file install
   screen, the embedded mode re-checked, tests updated where an element
   moved, `sync_base.py --write`, `EnsureDevRails()`. Landed 2026-10-17
   up to `EnsureDevRails()`; the rails were rebuilt as 3.2.72 and shipped
   with release v3.2.72 the same day (after phase 5 below), so the wizard
   reaches users from that release on. The FirstRunTestPlan runs on a
   clean TD remain the one open item.
5. **The set becomes a drawer; every flow lands on the list.** Owner,
   2026-10-17, on first use of the built flow: it does not encourage
   exploring tools, every branch ended on the set, and after an install
   (and in the console's Install and remove tab) the catalog was only
   reachable through Start over and Pick my own. The rework: the "set"
   screen's body becomes the drawer over the list (same rows, same
   plusReality line and options row, head with count, Clear and Close);
   the list's footer holds "Your set · N" and Review install; "Add
   tools" and "Done, N selected" go; every preset, the questionnaire's
   result and Pick my own land on the list (with the toast naming the
   count); the done screen gains "Browse more tools" as its primary;
   re-entry and the console frame land on the list with the installed
   tools ticked; the ticked row loses its full accent outline for a
   quiet mark. The hash keeps `catalog` and `install`; `set` is no
   longer a destination (an old `#set` link opens the list with the
   drawer). Landed 2026-10-17 (uncommitted at the time of writing); the
   record is the section "Wizard phase 5 (2026-10-17)" in
   `InstallSurfaceDesign.md`. Phases 1 to 4 had already been committed
   (`842062da`, `ee247d31`), so the set-as-home shape is in the history
   and this phase is the commit on top; no release carries it on its
   own, since the rails are rebuilt only at release time.

## Decisions for the owner

1. **Site entry.** The table above lands /get/ on the list after a
   once-per-browser S0, because site visitors browse. The alternative is
   S0 on every visit, the same as the installer. Recommendation: list
   after one S0.
2. **Compact rows as the default inside TouchDesigner**, with the cards
   as the opt-in. Decided 2026-10-16: yes; the site may keep the cards
   as its default since it has the width.
3. **Re-entry home.** Decided 2026-10-17: the list, with the installed
   tools ticked and the diff on the rows; the set only as the drawer.
4. **The Patreon prompt** on ticking a locked tool stays a modal, since
   it is a three-answer decision. The alternative is an inline row state.
   Recommendation: keep the modal.
5. **Where the family and bind options sit**: the drawer's options row,
   or the S3 plan. Recommendation: the drawer, so the plan is a
   confirmation and never a form.
