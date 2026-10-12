---
status: landed
summary: Update never fetched family operators, the installer never re-fetched a recorded one whose file was missing, and nothing told a user that a release added tools. Backlog for fixing all three, the first-install rules the new-tools notice must keep, and (2026-10-12) store-only updates, the gated state and the sidecar rule.
since: 2026-09-25
---

# New tools, and family operators that stay current

Field report, 2026-09-25 (owner, on a second project): after pressing
Update, the FNS tab showed nothing new, although every family operator was
ticked in the picker. Uninstalling and reinstalling the family did not bring
them all back. And the question behind it: how does anyone learn that a
release added tools?

## What was wrong

1. **Update never fetched a family operator.** An FNS family member is
   installed as a record only (placement `none`): nothing is placed, the
   tox waits in the store and the family folder mirrors it. `Compare()`
   reported every such member as `component` and never as an update, so an
   update pass never downloaded its new version. The family folder mirrors
   what the store holds, so members stayed at whatever version first
   landed, and ones that never reached the store never appeared.
2. **The installer never re-fetched a recorded member whose file was
   missing.** `ResolvePlan` treats a `none` package as present when the
   install record names it, and `to_fetch` only took steps that were
   neither on disk nor present. A member recorded on this machine but
   absent from the store (a store cleaned, another machine's record) was
   planned as present and never downloaded.
3. **Nothing announced new tools.** Update checks installed packages only.
   Release `notices` are hand-written and rare, and the picker's New filter
   shows only to someone who goes looking.

## The backlog

- [x] **A. The installer fetches a recorded family member with no file.**
      `to_fetch` includes a `none` step whose artifact is not in the store,
      present or not.
- [x] **B. Update keeps family members current in the store.** `Compare()`
      reports a recorded `none` member as an update when its store copy is
      missing or its bytes differ from the manifest. The update pass
      fetches it, the apply step records it (nothing to replace), and the
      family sync that already ends every pass mirrors it into the folder.
      Gated members follow the existing gated-skip rule.
- [x] **C. The picker announces tools this machine has not been shown.**
      - "Shown" is machine-wide, in `<palette>/FNSTools/config/seen_packages.json`
        (served picker; the installer reads and writes it), and in the
        browser's `localStorage` on the site and the standalone.
      - Opening the picker with unseen tools shows a dismissable "New
        since you last looked" dialog: the tools as small cards with their
        release note and a tick, "Add the ticked ones" and "Not now". Either
        button marks them shown.
      - Unseen tools keep a New badge on their card until the next release.
- [x] **D. The console's Install & remove tab carries the count,** the way
      the Updates tab already carries its count.

## First installs (owner: "watch out for first installs")

A new user must never be greeted with eighty "new" tools. The rules:

- **A bootstrap's first run** (`FNS_FIRSTRUN`) and **a first visit to the
  site** mark every current tool as shown and show no dialog. The guided
  setup is their introduction.
- **A first install that never opened this picker** (TDX Launcher Ultra,
  the paste rail, any headless `Install` with a selection file) counts as
  a first run too: whatever picked its tools was the introduction.
  `Install()` asks the picker's own question (`_isFirstRun`, no tool in the
  target yet) *before* installing, and afterwards `RecordFirstInstall`
  marks every current non-preview tool as shown, only while the machine
  has no seen file. Asking afterwards is too late: the root then holds
  tools and reads as an existing install with no record (field report
  2026-10-06, a fresh machine installing through TDXLU was greeted with
  the release line's new tools).
- **An existing install with no seen file yet** (everyone on the release
  that introduces it) starts from what they already know: every tool is
  shown except the ones the release line introduced (`whatsnew` starts
  "new package") that they have not installed. So an upgrading user sees
  the genuinely new tools once, and nobody sees the whole catalog.
- The dialog never opens during the guided setup, over another dialog, or
  inside a project that is locked as a source checkout.
- **A Patreon tool the viewer cannot get is never news** (owner,
  2026-09-25: "don't pester them"). Signed out, or without the tier, the
  dialog leaves it out and opens only if something free or owned remains;
  the console's count leaves it out too. It is not marked shown, so it is
  announced once the account holds it; its card keeps the New badge.
- **A tool you already have is not news** (field report 2026-10-07:
  CookBar picked on /get, installed by the paste, and the picker inside
  TouchDesigner still opened on it, ticked and greyed out as "already
  picked"; the owner called that "a non-state"). The page and the installer
  keep separate records, so both now apply the rule. On the page, a new
  tool already in the selection is recorded as shown and left out of the
  dialog, which then opens only if something is left to decide. In the
  installer, `UnseenTools` records an installed tool as shown instead of
  returning it, and `/newtools.json` leaves installed tools out of the
  console's count (it stays read-only).
- **It is a preference** (owner, 2026-09-25). The window carries "Show
  this window when tools are added"; unticked, it never opens by itself
  (the record's `announce: false` when served, `fns.announce` in the
  browser elsewhere). The New filter still lists the tools, and with it
  on the results line shows the setting, so the way back is findable.

## Verified (2026-09-25)

- **B**: `Compare()` on a scratch root recording ComplexMix and
  FNS_RandomCHOP reported both as updates with the family note (the store
  held neither the one nor the current bytes of the other).
- **C and D**: `/newtools.json` and `/manifest.js` answered through the
  dev installer's request handler, and the machine record was written from
  what the project holds. Rendered headless: a first site visit opened the
  guided setup, not the dialog, and recorded all 82 tools as shown; a
  returning visitor with no record saw the 17 tools this release line
  introduced; the served dialog listed the installer's unseen tools.
- **A** is pinned in tests/test_new_tools.py; the live path needs a real
  install on a machine whose store lacks a recorded member.

## Verified (2026-10-06): a headless first install

The patched `InstallerExt` ran in TD against the live store manifest (68
pickable tools, 14 previews), with `InstallPlan` stubbed to create the
picked tool's COMP and the seen file redirected to a scratch folder:

- **Empty target, no seen file:** first run before the install, not after
  (the field bug's condition). The install wrote a record of all 68 tools,
  no previews, and `UnseenTools` then returned nothing.
- **Target already holding a tool, no seen file:** the install wrote no
  record, and `UnseenTools` returned the release line's 10 introduced
  tools, as before.

## The store copy is the update (2026-10-12)

Owner, 2026-10-12: updates of FNS family operators and of the op menu's
store alternatives are about the store, never about operators already
placed. Three gaps closed together.

- **Store-only updates.** `Compare()` lists a store-served tool (a family
  member while the family is installed here, or a package with
  `alternatives_for`) as an update when the project does not hold the
  package itself, the store holds a copy, and that copy is not the
  manifest's bytes. The row carries `store_only`; the plan passes it to the
  apply step, which verifies the new store copy and replaces nothing.
  A tool never fetched on this machine is an install, not an update, so it
  is not listed. The project's install record is refreshed only for a
  package it already recorded: an update never turns into an install.
- **`gated`.** A newer build of a Patreon tool this account does not hold
  (signed out, tier lapsed) is reported as `gated` with `MissingFor`'s
  sentence and is not counted. Before, it counted as an update, the pass
  skipped it, and it never cleared. The console labels it "needs your
  account".
- **The sidecar matches its tox.** A check or the picker refreshes the
  manifest without fetching bytes, and the family sync then wrote the new
  row's version beside the old tox. The sync now takes a member only from a
  store copy that matches its row; a stale one keeps the pair the last
  sync wrote, or stays out until it is fetched. A folder that already held
  a mismatched pair corrects itself on the next fetch.

Verified live against a scratch store, family folder and toolkit root
(instance overrides on the updater, the real store untouched): with one
current and four stale copies, `Compare()` listed the free family member
and the free alternative as store-only updates and the two Patreon ones as
`gated`; the family sync left the stale member's old sidecar (`0.0.1`) and
wrote the current one's (`1.0.1`). An update pass from `packaging/publish`
fetched both, reported "refreshed in the store", wrote no install record,
re-mirrored the member at `1.0.1`, and a second `Compare()` listed nothing.
Pinned in tests/test_new_tools.py.
