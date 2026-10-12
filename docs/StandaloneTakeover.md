---
status: landed
summary: The updater finds standalone copies of global tools (non-core packages that land inside FNSTools) by a release-stamped <FNS:GLOBAL> tag and FNS_About.Pkgname, the console offers Take over (move the copy in, or delete it when the toolkit has its own), the picker refuses to install a second copy, and every global tool carries a guard that releases its Global OP Shortcut beside a toolkit copy. A removed tag is the opt-out for a kept fork. Notices for people and agents: a site guide, /llms.txt, the toolkit README and a one-line comment. Built and verified live 2026-10-09; reaches users with the next release and rails rebuild.
since: 2026-10-09
verified: 2026-10-09
skill: fns-packaging
---

# Taking over standalone copies of global tools

Free tools can be downloaded as single `.tox` files from the website
(2026-10-08). A user who drops one into a project and later installs the
toolkit got a second copy: the updater looked only inside its own container
(`ExtUpdater.Compare` read `root.children`, plus the doorstep for `pane`/`root`
placements), and nothing anywhere asked "is this tool already here".
`docs/LauncherToolkitBoundary.md` records the same gap.

A global tool is meant to exist once per project, so a second copy is broken:

- **Global OP Shortcut.** Measured on TD 2025.33070: with two holders,
  `op.<Shortcut>` keeps returning the FIRST holder (creation order, not name),
  and both get a "Multiply defined Global OP Shortcut" script error, which
  shows in `scriptErrors()`, never `errors()`. Clearing the first holder's
  shortcut hands it to the other at once. So a standalone copy that was in the
  project before the toolkit captures every `op.<Shortcut>` call, the
  toolkit's own included.
- **Hotkeys and registrations.** Both copies bind their hotkeys and register
  into the same `/sys` registry globals, so actions fire twice and tabs or
  buttons appear twice.

## Which tools this covers

A **global tool** is a package that is not replicable: in the catalog, one
that lands inside FNSTools (`placement: toolkit`). Replicable packages land
elsewhere: FNS family operators go to the family folder and are placed by the
user as often as they like, and OpTemplates entries are chains the user
pastes. Measured on the v3.2.67 manifest:

| Lands in | Family | Packages | Covered |
|---|---|---|---|
| `toolkit` (FNSTools) | no | 62 | 48 (the 14 core ones excluded) |
| `none` (placed by the user) | yes | 33 | never |
| `none` | no | 2 | never (RealRamp, ThresholdColor) |
| `root` (beside the toolkit) | no | 2 | never (TDXMap, ParHoverMIDI_VSN1) |

A shortcut is not part of the rule: 15 of the 48 have none.

Two exclusions:

- **Core packages** (`kind: core`: the updater, the registries, ...) are never
  taken over. Developers may embed them in their own tools, and the registries
  already settle duplicates themselves (newest wins, `/fns-registry`). A
  takeover that deleted a registry from inside a third-party tool would break
  that tool.
- **A copy nested inside another package** is never a candidate, core or not.
  It belongs to the tool that carries it.

```
global = (placement or 'toolkit') == 'toolkit' and not family and kind != 'core'
```

The rule lives in `packaging/package_identity.IsGlobal` and, for the updater
running in a user's project, `ExtUpdater._isGlobal`; the test keeps them equal.

## Identity, stamped onto every artifact

The COMP name was the only identity, and it changes more often than it looks,
most of all for standalone downloads: a browser names a second download
`CustomParTools (1).tox`, and TouchDesigner renames a drop into a network that
already holds one to `CustomParTools1`. The updater had the same blind spot
for installed tools: `Compare` matched `child.name` only, so a renamed toolkit
tool was invisible to updates and its install record read `missing`.

The release step (`build_manifest.ScrubArtifact`, through
`packaging/package_identity.Stamp`) stamps every exported artifact copy:

| Stamp | On | Means |
|---|---|---|
| `Pkgname` | the top-level `FNS_About`, Identity page, read-only | the catalog name, `FNS_` included |
| `<FNS:GLOBAL>` | the root COMP of a global tool | find me |
| `fns_standalone_guard` | an Execute DAT in a global tool's root | the step-aside (below) |

- **Internal.** `Pkgname` sits on its own Identity page, never `To Deploy`, so
  FNS_About's Deploy pulse never mirrors it onto the tool's About page.
- **Top level only.** Registry hosts nested in a tool carry their own
  FNS_About; the stamp touches `comp.op('FNS_About')` only.
- **Artifact, not master.** The design first had the release bump write
  `Pkgname` onto the 48+ masters. Every copy that needs it, standalone or
  managed, comes from an artifact, so the stamp goes where the licence notice
  already goes (`docs/LicenseNotices.md`): no master edits, no PI saves. The
  cost: the dev project's own tools carry no `Pkgname`, and every reader falls
  back to the COMP name, as it must for installs that predate the stamp anyway.
- **A non-global package** gets `Pkgname` only; a stray tag or guard on it is
  removed.

### The tag form is TDFam's

Owner, 2026-10-09: adopt it. TDFam tags its operators with an uppercase key in
angle brackets, bare or with a value: `<FAM>` on a family COMP, `<MANIFEST>`,
`<FAM:FNS>` and `<TYPE:complexmix>` on each member's `FamManifest` (measured
live). The brackets keep these apart from ordinary tags (`TDExtension`,
`pi_suspect`), and `FNS` as our key keeps ours apart from TDFam's, which
already sit inside our family tools. A later tag joins the same key.

The package name stays in `Pkgname`, not in a `<FNS:PKG:...>` tag: next to
`Pkgversion` it is where the updater already reads, and one place for the name
cannot drift from a second.

### The updater reads it

`Compare` matches on `Pkgname` first and the COMP name second, so a renamed
toolkit tool stays visible to updates; `_replacePackage` finds it the same way.
**Decided (owner, 2026-10-09):** the package name wins. The update restores
it, as the installer already did, and a takeover does the same. Renaming or
editing a package is not supported.

## Toolkit side: FindStandalone, TakeOver

`FNS_Updater.FindStandalone()` walks the project's COMPs, skipping the toolkit
root, `/sys`, `/ui` and `/local`, and never descending into a package (a COMP
that declares a version), so a copy nested in another tool is never found. A
COMP matches by the tag or `Pkgname`, and an older, unstamped copy by COMP name
or Global OP Shortcut, but only when it declares a version: a user's own COMP
that happens to be called `CookBar` is never taken for ours. Read-only, no
network; with `Compare` it ran in 31 ms in the dev project.

`Compare()` reports each one as `standalone` (path in `note` and `path`); it
is never queued as an update, and never overrides the managed copy's variant
in the update plan.

`FNS_Updater.TakeOver(path, confirm=False)` is a dry run unless confirmed (the
installer's two-call shape) and accepts only a path `FindStandalone` reports,
so it can never delete an arbitrary COMP.

- **The toolkit has no copy:** the standalone copy **moves in**. Saved to
  `store/_backup/<Name>.standalone.tox` (its own name, so it never overwrites
  the managed copy's update backup), destroyed, loaded into the toolkit root
  under its package name, recorded as installed; restored where it was if the
  load fails. The update rail's own mechanics.
- **The toolkit has its own:** the standalone copy is deleted. The managed
  copy keeps its own, newer settings.

### Why a move, not a fresh install with carry-over

The design was to install the managed copy fresh and carry parameters, an
allow-list of storage keys and external tables across. The updater never
installs (the installer does, and may need a download first), and the survey
of the 48 tools showed the carry-over buys little: 40 of them keep their
settings in the roaming config file through a ConfigRegistry host, storage is
mostly transient state (probe flags, drag state), and every table the survey
found lives in the shared palette `tables/` folder, read by both copies alike.
Moving the copy in keeps everything it has, with no carry-over code, because it
is the same component; the next ordinary update replaces it whole, exactly as
it replaces every installed tool, settings saved through the config registry
first.

### What breaks

Anything that held the standalone copy by path. `TakeOver` lists the
parameter expressions in the copy's own network that named it. A project-wide
`findChildren(parExpr=...)` was tried first and held TouchDesigner's main
thread for minutes in this project: it matches every parameter of every
operator, `/sys` and `/ui` included. Never run that from an action a user
clicks.

### The console

The Updates tab shows a `standalone copy` row under Needs attention with a
Take over button. The dialog shows the plan (move or delete, and what refers
to it), and Take over runs it, deferred out of the web server callback like
Update (`ConsoleRegistryExt.UiUpdatesTakeOver`, `POST /api/updates/takeover`).
Verified by clicking through the live console page.

## Tool side: release the shortcut

A standalone copy runs no toolkit code, so the step-aside ships inside it: the
`fns_standalone_guard` Execute DAT, Create on. Create fires when the
component is loaded from disk, pasted, or the project starts (Execute DAT
docs). Thirty frames later (the toolkit may load after the copy) it checks,
through a guarded `getattr(op, 'FNS', None)`, whether the toolkit holds this
package:

- **It does:** the copy remembers its Global OP Shortcut in storage, clears it,
  clears the stale "Multiply defined" error TouchDesigner leaves on it, and
  logs one line pointing at the console.
- **It does not** (no toolkit, or a toolkit without this tool): a remembered
  shortcut is put back. A show project carried to a machine without FNSTools
  works as before.

Nothing is moved or deleted from the tool side. An extension's init, like this
DAT's Create, runs on every project open, not only on a drop; a tool that moved
or deleted itself would do it to a show project that bundles a tool to travel
with it, and to a user's own fork.

**Only the shortcut.** Turning the copy's cooking off would also silence its
hotkeys, but measured on TD 2025.33070, an Execute DAT inside a COMP with
cooking off never gets `onCreate`, so a copy switched off could never switch
itself back on. Duplicate hotkeys and buttons stay until the copy is taken
over; the console says so. The guard cannot be a utility op (`utility` exists
only on COMPs), so it is an ordinary DAT in the tool's root.

## A standalone copy takes the registrations over

Found by the end-to-end test on a real exported tool: a standalone copy's
registry hosts register under the SAME canonical names as the toolkit copy's,
so the registry entry moves to the copy. The toolbar's `QuickTime` entry
pointed at the dropped copy's button, and deleting the copy left it pointing
at nothing: the button went dead. So:

- `TakeOver`, deleting a copy, pulses `Register` on every registry host of
  the toolkit's own copy (`_reregisterHosts`), and the entries point home.
- The guard, when it steps aside, does the same, after the copy's own hosts
  have registered (30 frames in), so the toolkit's registration lands last.
- A copy removed any other way (deleted by hand, undone) still leaves the
  entry dangling until the toolkit copy registers again; that is the
  registries' own behaviour and outside this design.

## End to end on a real tool (2026-10-09)

`FNS_QuickTime` exported through the release path (Embody's export, its
pre_release hook, `ScrubArtifact`) to a scratch file, never `dist/`:

- the file carried `<FNS:GLOBAL>`, the one-line comment, `Pkgname` on the
  Identity page (read-only, off `To Deploy`), the MIT note as a utility
  annotation, the guard (Create on, the right package), its shortcut, and no
  PI markers or errors;
- loaded into the project like a dropped download, the guard released
  `FNS_QUICKTIME`, cleared the stale error and, with the fix above, pointed
  the toolbar entry back at the toolkit's QuickTime; `FindStandalone` and the
  console's Updates rows found it by its tag;
- Take over through the console's own handler deleted it, and the toolbar
  entry, both hosts and the shortcut stayed with the toolkit's copy;
- the move path, into a root without QuickTime, kept a changed parameter, a
  stored value, the licence note and the tag, and recorded the install.

`FNS_BackupCleaner` (preview, so gated) exported with the Patreon licence and
no MIT text, plus tag, guard and `Pkgname`.

## Verified live (TD 2025.33070, 2026-10-09)

- Duplicate shortcut behaviour, as above, in `/sys` probes.
- `FindStandalone` on synthetic copies found exactly the name, shortcut and
  tag matches, and left alone a user's own `CookBar` with no version, a global
  tool nested in another package, a core package, a family operator and a
  tagged copy of a core package.
- `TakeOver`: a dry run listed an expression referring to the copy by path; a
  non-candidate was refused; the delete path removed the copy and the shortcut
  conflict cleared; the move path put the copy into a test root with its
  storage and version, recorded it, and wrote its backup under its own name.
- The release stamp on a scratch copy of the released `FNS_QuickTime.tox`:
  tag, `Pkgname` (Identity page, read-only, `To Deploy` untouched) all came
  back after save and reload, and the updater's own reader returned the name.
- The guard: pasted beside the toolkit's QuickTime it released and remembered
  `FNS_QUICKTIME` while the toolkit kept it; with no toolkit copy it put the
  shortcut back and forgot it.
- The console: row, dialog, confirm, row gone, copy deleted.

## The picker never installs a second copy

`InstallerExt.InstallPlan` asks the updater beside it (`FindStandalone`, the one
home of the matching rules) before loading a global tool the toolkit does not
hold yet. A standalone copy in the project refuses that one install with a
sentence naming the copy and pointing at Take over; nothing is loaded. The
picker's result text and the quick-launch install (failed in the palette
footer) both say it. An updater too old to have `FindStandalone`, or none,
answers nothing and the install goes ahead as before. Core packages are never
refused. Verified by executing the installer source against a synthetic copy.

The installer ships in the rails (`FNS_Installer` inside the bootstrap, a
text copy refreshed at build), so this reaches users with the next rails
rebuild, which bumps `INSTALLER_VERSION`.

## Keeping a fork: remove the tag

A user who wants their own version of a tool copies it out, renames it and
removes `<FNS:GLOBAL>`. The release stamps the tag and `Pkgname` together, so
a copy with `Pkgname` and no tag had it taken off on purpose: `FindStandalone`
skips it, the picker does not count it, and its guard stands down (and gives
back a shortcut it had released). Verified live: of two stamped copies, only
the tagged one was found.

## Telling people and agents

A package is replaced whole on every update; nothing technical stops someone
editing inside it, so the rule is written where each reader looks:

| Reader | Where | |
|---|---|---|
| People | `/docs/guides/working-in-your-project/` | what an update replaces, what is safe to change, the fork recipe, single downloads |
| Agents reading the site | `/llms.txt` ([llmstxt.org](https://llmstxt.org/), a proposed convention) | the same rules in a few lines, links to the docs |
| Agents in a project | the bootstrap's `README` DAT at the toolkit root (`build_installer.BOOTSTRAP_README`) | one notice for every tool in the container |
| Anyone reading a standalone copy | its root COMP `comment`, one line (`package_identity.NOTICE`) | `get_op` returns it; a tool's own comment, credits included, follows it |

None is enforcement: the update restoring the package name is what holds.

## Still open

- **The download tooltip** can promise "if you install FNSTools later, it
  offers to take this copy over" once these releases are out.
- **Core packages for developers:** standalone downloads plus one developer
  page on the registry contracts; a developer zip waits until someone asks.

## Rollout

Nothing reaches a user until a release: `FNS_Updater` and `FNS_Console` carry
the find, the console and the takeover, each global tool gets its tag,
`Pkgname`, guard and comment when it is next exported, the picker refusal and
the README ride the next rails rebuild, and the guide and `/llms.txt` go out
with the next website publish. Copies downloaded before that
are still found, by name or shortcut, and can be taken over; they only lack
the guard.
