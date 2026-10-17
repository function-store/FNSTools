---
status: open
summary: Manual end-to-end test plan for the first-run experience — the Start screen on a drop, the wizard picker, "Set up like last time", CMS Recommended, dev-folder guard. Run on a clean TD before the next release.
since: unreleased 2026-08-22 (covers work landed that day; automated checks passed, the cold user-path runs below are still pending)
---

# First-run experience — end-to-end test plan

What the agent verified on 2026-08-22 was **inside the dev project**
(drop tests in `/sys/quiet`, the page driven through the DOM, installs
into a cooking-disabled container). The runs below are the parts only a
real user path proves: a bare `.toe`, a real drop, a real bucket, a cold
restart. Tick them before the release that ships this.

Revised 2026-10-17 for the wizard picker (`docs/InstallerWizardFlow.md`;
records in `docs/InstallSurfaceDesign.md`): the expectations below name
its screens (Start, Your set, Add tools, Install) where they named the
welcome dialog, the step strip under the hero and the install dialogs.
The runs themselves are unchanged.

**Conventions.** "Bare project" = a new, empty `.toe` in a folder that has
no `externalizations.tsv`. "Bootstrap" = the `FNSTools.tox` from
`packaging/dist/` (rebuild with `BuildBootstrap()` after any source
change — Preflight flags a stale one) or, for the release candidate, the
one in `packaging/publish/<release>/`. Between runs that need a *clean
machine*, move `<userPaletteFolder>/FNSTools/config/FNStools_config.json`
aside (the whole roaming config) and clear
`<userPaletteFolder>/FNSTools/store/` if you want to see the catalog
download.

---

## Run 0 — Preconditions (5 min)

1. In the dev project, Textport:
   `exec(open('packaging/build_installer.py').read()); EnsureDevRails(); EnsureRootEntryPoints(op.FNS)`
   then `BuildInstaller(); BuildBootstrap()`. Both report `exported: True`,
   `errors: 'clean'`.
2. `Preflight()` (see RELEASING.md) shows no stale-rail warning.
3. Open `packaging/dist/FNSTools.tox` size: ~260 KB (it now carries the
   root config host; the pre-2026-08-22 bootstrap was ~215 KB).

## Run 1 — First drop on a clean machine (the headline path)

*Setup:* bare project, roaming config moved aside, store emptied.

1. Drag `FNSTools.tox` into the network editor.
   - **Expect:** within ~2 s, without clicking anything, a floating viewer
     opens with the picker on its **Start** screen: the step strip at the
     top (**Start** lit, then **Your set** and **Install**), the title
     **Welcome to FNSTools.** and the line *"Pick a starting point.
     Nothing installs until you review the plan."*
   - While the store is empty the Start screen shows no cards; under the
     title it says *"The starting points appear in a moment."* and
     *"First run: fetching the package catalog from the bucket… this page
     refreshes itself."*, and the page reloads itself every ~2.5 s until
     the catalog lands.
2. The cards appear: **Answer a few questions** / **Recommended** /
   **Everything** / **Pick my own** (no "Set up like last time" — this
   machine has no record). The Recommended card names the count and the
   first four tools. Under the cards: one sentence of counts (*"N tools
   are free, 1 has a free trial, and N come with Patreon."*) with
   **Sign in with Patreon** and **Become a supporter**, then one line with
   the release, the TD build, *every download sha256-verified* and
   **Docs**. **Nothing on the Start screen mentions core.**
3. Click **Pick my own**. The catalog screen (**Add tools**) opens with
   every section open, nothing ticked, the search focused and the footer
   reading **Done · 0 selected**. There is no Esc: Start is a screen, not a
   dialog. Reload the panel (root → **Pick Tools**): it lands on **Your
   set** ("Nothing in your set yet.", with **Add tools**), since a choice
   marks the visit welcomed; a reload *before* any choice lands on Start
   again. **Start over** in the header returns to the cards from any
   screen.
4. Click **Recommended**. The set screen (**Your set**, the **Your set**
   step lit) lists the recommended tools as rows grouped by category; the
   footer shows the recommended count and the download size; the rows
   match `catalog.json`'s `recommended: true` set. **Add tools** opens the
   catalog with the same tools ticked and **Done** returns.
5. **Review install…** — the install screen opens on its plan state
   (**Install plan**, the **Install** step lit): the big count of tools to
   install "with N core packages" and the download size, the installs as
   chips, "Into <root path>"; on an empty store core is in that count.
   **Install**: the progress state (**Installing**: "Downloading… N done,
   M to go", then "Installing…"), then the done state (**Installed**: the
   big count, each tool as a chip linked to its docs, the hint text) with
   **Open Settings** and **Close**.
6. Click **Open Settings**: the same panel navigates to the FNS console on
   its Settings tab. (Textport: the installer's `webserver` DAT goes
   `active = False` within ~2 s.)
7. Look at the network: the dropped root holds core + tools, `installed`
   table, `README`, `exec_root_welcome`, `config_callbacks`,
   `FNS_ConfigHost`, `parexec_root_pulses`. `root.fetch('FNS_welcomed')`
   = `'shown'`. No errors on the root (`root.errors(recurse=True)` empty).
8. The toolbar (if FNS_Toolbar was picked) appears at the top of the
   network editor after a frame.
9. **Save** the project (Ctrl+S). Open the roaming config JSON:
   `tools.FNS.state.last_install` exists, `packages` lists every
   installed package, `project` is this `.toe`, `bind` = `embedded`.
10. **Reopen** the project. **Expect:** no picker opens (flag set), no
    errors, tools come back.

**Fail signals:** picker never opens (check the root's `exec_root_welcome`
→ *Create* toggle on; `op.TDResources` exists); Start returns after a
choice was made (the welcomed flag is set by the choice); core mentioned
on Start; the catalog's Add tools showing a Core section; `Open Settings` errors
("no FNS console installed yet" means FNS_Console did not land or did
not expose — see `ExposeConsoleHosts`).

## Run 2 — "Set up like last time" (same machine, second project)

*Setup:* right after Run 1 (the roaming config now holds the record).
New bare project in another folder.

1. Drop the bootstrap. The picker opens on Start with **five** cards,
   **Set up like last time** first and lit: *"N tools, as in <Run-1 toe>
   on <date>."* (N = tools only; core is not counted.)
2. Before clicking a card: the **Your set** step in the header shows the
   set already holding those N tools (ticked from the record, no state
   chips on a first run); the **Start** step returns to the cards. (Pick
   my own would clear them: a card is a choice, not a dismissal.)
3. Click **Set up like last time**. It is the one card that is also the
   confirmation: the install screen opens on **Setting up like last
   time** with the plan, goes straight into the progress state and ends on
   **Installed** with the same tools. Settings from Run 1 (e.g. a toolbar
   layout change you made there) re-apply once the tools register.
4. Save this project. Reopen **Run 1's** project, change one tool's
   selection there (Pick Tools → uncheck one → Apply), save. Drop a
   bootstrap into a third bare project: the card now reflects **Run 1's**
   newer state — last writer wins, as documented.

**Variant 2a — bind mode rides along.** In Run 1 set the installer's
**Package Files** to *Shared* before installing; after the save the record
carries `bind: shared`; in Run 2 choosing the card sets the new
installer's Package Files to *Shared* (check the par before Install).
Choosing **Recommended** instead leaves it at *Embedded*.

**Variant 2b — catalog drift.** Edit the roaming JSON by hand: add a fake
name to `packages`. The card says *"(1 no longer in the catalog)"* and the
plan never mentions it.

**Variant 2c — project scope.** In Run 1's project set the root's
**Config Scope** to *project* (confirm dialog → Stay/Push as offered),
save. Check the roaming JSON: `last_install` is **unchanged** (not
rewritten). Drop a bootstrap into a new project whose root you flip to
*project* scope before the picker loads (Pick Tools again after the
flip): **no** "Set up like last time" card.

## Run 3 — Paste rail does not double-trigger

1. On `functionstore.tools/get/` pick two tools → **Copy install
   script**. Paste into the Textport of a bare project.
2. **Expect:** the bootstrap lands and installs the selection; **no picker
   opens** over it (`root.fetch('FNS_welcomed')` = `'paste'`).
3. Root → **Pick Tools** afterwards opens the console's Install & remove
   tab normally, on **Your setup** with the two tools as rows marked
   *installed*. (A paste that ticked a Patreon tool opens the picker by
   itself on **Your setup**, the Patreon tool ticked and a line above the
   list offering **Sign in with Patreon**; after the sign-in reload the
   install screen plans and installs it without a click.)

## Run 4 — Existing installs are untouched

1. Open a project installed **before** this change (or Run 1's project).
   Root → **Pick Tools**: the console / picker opens on **Your setup** with
   the project's tools as rows marked *installed* and the **Your set** step
   lit; **no** Start screen, no "last time" card (not a first run); the
   cards are reachable only through **Start over** in the header.
2. Copy the whole root to another project via Ctrl+C / Ctrl+V: no picker
   opens (storage travels with the copy).

## Run 5 — Dev-project guard

*In the dev checkout (this repo).*

1. On `/FNSTools/FNS_Installer` set **Install Into** to a fresh
   cooking-disabled container (`t = op('/sys/quiet').create(baseCOMP,
   'trial'); t.allowCooking = False`), **Selection** to
   `packaging/example-selection.json`, **Package Files** to *This
   project's own folder*, pulse **Plan**.
   - **Expect** (Private Investigator's **DEV** toggle on): Status
     `LOCKED -- Package Files 'project' would write into …/FNStools,
     inside the toolkit's development project (Private Investigator: DEV
     on) …`. **Install** refuses with the same text. Nothing is written
     under `FNStools/`.
2. Set **Package Folder** to a folder outside the project → Plan resolves.
3. Toggle PI's **DEV** off, Plan with the default folder → resolves (the
   guard is the toggle, nothing else). Toggle it back **on**.
4. Reset: Package Files *Embedded*, Package Folder blank, Install Into
   blank, destroy the trial.

## Run 6 — CMS Recommended

1. `cd website && node tools/cms.mjs` → open the URL. Pick a tool, tick
   **Recommended**, ⌘S. `git diff packaging/catalog.json` shows exactly
   one added line (`"recommended": true`) on that package; the list shows
   a `REC` badge. Untick, save: the line is gone.
2. `npm run pages` in `website/` builds clean.
3. In the dev project: `exec(open('packaging/build_manifest.py').read());
   Build()` → `manifest.json` gains/loses the name in `starter`, tools
   only, in manifest order. (Reverting the generated manifest afterwards
   is fine if you are not releasing.)
4. Release → the next bare-project drop's **Recommended** card reflects
   the change. A project served an **older** manifest (no `starter`)
   shows no Recommended card at all, and the Start screen still works
   with the cards it has.

## Run 7 — Cold restart of the dev project

1. Restart TD on the dev project. `/FNSTools` still has
   `exec_root_welcome` (Create on), `config_callbacks`, and
   `FNS_ConfigHost.par.Callback` → `config_callbacks`. No picker opened on
   the dev root (it never welcomes: `externaltox` set).
2. Save the dev project: the dev machine's roaming JSON keeps whatever
   `last_install` it had (the dev root has no `installed` table and
   returns the previous value, never `{}`).

## Run 8 — The developer kit (docs/DeveloperKit.md)

*Setup:* bare project, no toolkit in it. `FNSTools-DevKit.zip` from
`packaging/dist/` (built by `BuildDevKit()` in the dev project, after
`Build()`) or, for the release candidate, from
`packaging/publish/<release>/`. Unzip it: eleven `FNS_*Registry.tox`,
`README.md`, `LICENSE.txt`.

1. Drag `FNS_ToolbarRegistry.tox` alone into the root. **Expect:** no
   picker, no errors (`errors(recurse=True)` and `scriptErrors` empty),
   `/sys/FNS_Registries` holds `FNS_ToolbarRegistry` and nothing else,
   `op.FNS` does not resolve (there is no toolkit root).
2. Create a scratch `baseCOMP` beside it and stamp a toolbar host into it:
   `op('/FNS_ToolbarRegistry').StampHost(op('/scratch'))`. **Expect:** the
   host's Enable Cloning reads off (the clone expression finds no root
   and RegistryBase switches cloning off before any par is written), and
   TD does not crash on the host's registration. Register a button per
   the toolbar contract: it appears on TD's toolbar; no Hub gear anywhere.
3. Drop `FNS_ConfigRegistry.tox` and `FNS_NavbarRegistry.tox` as well.
   **Expect:** three globals, the config registry on project scope (no
   root to follow), the navbar host stamped the same way shows in the
   pane bars.
4. Save and reopen the project. **Expect:** the registries promote again
   on load (per-process state), the button comes back.
5. Delete the loose registries, then drop `FNSTools.tox`. **Expect:** the
   normal first run (Run 1), `op.FNS` the new root, the scratch host's
   Enable Cloning back on and cloning from the real toolkit's master.

**Fail signals:** a picker opening (the kit must carry no installer); a
host with Enable Cloning on and an empty Clone par (the crash of
2026-10-11); a second `FNS_Registries` home; a version contest after
step 5 (same version keeps the incumbent, so the deletion must come before
the drop).

---

## Sign-off

| Run | Result | Date / who |
|---|---|---|
| 0 Preconditions | | |
| 1 First drop, clean machine | | |
| 2 Set up like last time (+2a, 2b, 2c) | | |
| 3 Paste rail | | |
| 4 Existing installs untouched | | |
| 5 Dev-project guard | | |
| 6 CMS Recommended | | |
| 7 Cold restart | | |
| 8 Developer kit | | |

When every row is ticked, flip this file's `status` to `landed` and fold
anything learned into `docs/LastInstallRecord.md` / `packaging/README.md`.
