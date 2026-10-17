---
status: open
summary: A developer kit, FNSTools-DevKit.zip, the eleven registries each as its own tox with a README, as a separate download beside the bootstrap, so other developers can build and test tools that publish into FNS surfaces without installing the toolkit; and the RegistryBase guard that lets a host live without a toolkit root. Asked 2026-10-17; the plan, the contents, what stays out and why, the build, the rail, the open points.
since: 2026-10-17
skill: fns-registry
---

# The developer kit: the registries as separate toxes

Owner's ask, 2026-10-17 (by voice): a developer release package that only
contains the registries, for other developers to build their tools
against, as a separate download outside the installer. Registries only:
no console, no hub, no updater. Later the same day, after a first build as
one root tox: a zip of separate toxes with a README instead, so a developer
drops only the registries a tool publishes into.

## What it is

`FNSTools-DevKit.zip` holds the eleven registry masters, each as the dist
tox a release ships for core, plus `README.md` and `LICENSE.txt` (MIT, the
licence of every free package). Built at release and published as a rail
beside `FNSTools.tox`. A registry tox dropped at the root of a development
project does what an installed toolkit's core does for its surface: it
promotes its global into `/sys/FNS_Registries` on init (the newest-wins
rule of `RegistryBase`), so a tool's registry host, stamped from the
dropped master with `StampHost` as `/fns-registry` describes, registers
exactly as it will in a user's project. One registry is enough; they work
together.

| In the kit | Surface |
|---|---|
| `FNS_ToolbarRegistry` | TD's toolbar |
| `FNS_NavbarRegistry` | every pane bar |
| `FNS_MainMenuRegistry` | the main menu bar |
| `FNS_OpMenuRegistry` | the Insert Operator dialog |
| `FNS_PaneTypeRegistry` | the pane-type menu |
| `FNS_PaletteRegistry` | the Palette Browser |
| `FNS_TimelineRegistry` | the timeline dialog |
| `FNS_PaneSearchRegistry` | each pane's find bar |
| `FNS_HubRegistry` | the Hub's tabs (the registry; the Hub itself stays out) |
| `FNS_ConfigRegistry` | the roaming settings file |
| `FNS_CommandRegistry` | the quick-launch command system (what `FNS_CommandKit` publishes into) |

About 1.1 MB. The kit's version is the release its registries were built
in; the README names it.

## What stays out, and why

- **`FNS_Console`, `FNS_Hub`, `FNS_Updater`.** The owner's decision: the
  kit is for building a tool against the registries, not for using the
  toolkit. Without the Hub there are no configurators, and without the
  updater the kit never updates itself: a developer downloads the kit of
  the release they target. `FNS_HubRegistry` stays in because tools
  contribute Hub tabs through it and the contract is the registry's, not
  the Hub's; a tab registered in a kit project shows nothing until the
  real toolkit is there.
- **`FNS_CommandKit` and `FNS_ConfigHost`.** They are packages a
  developer drops into their own component, and the website already
  offers every free package as a single download; they are not part of
  the kit.
- **The installer, the picker, the root's entry points** (Pick Tools, Open
  Settings). They all need the console or the updater.
- **`FNS_OverlayRegistry`.** The one registry that is a package, not core;
  a tool that draws overlays requires it, and the catalog delivers it.

## Without a toolkit root

A registry tox loads and promotes on its own; measured 2026-10-17 with
`FNS_ToolbarRegistry` from dist in `/sys/quiet`: extension ready, no
errors, `StampHost` present. Three things follow from there being no
`op.FNS`:

- **Hosts do not clone.** `StampHost` wires a host's clone as
  `op.FNS.op('<Registry>') if hasattr(op, 'FNS') else None` with Enable
  Cloning on. Without a root the clone reads None while cloning stays on,
  the native crash of 2026-10-11 (a custom-par write on such a COMP), which
  until now only `FNS_OverlayRegistry` guarded on its master. The guard
  moves into `RegistryBase`: the first thing a registry extension does on
  init, before any par of the COMP is touched, is switch Enable Cloning off
  when the clone reads None, and back on when the clone resolves to the
  registry's own clone expression (the real toolkit arrived). Written only
  when wrong, logged. A host without a root keeps its own copy of the
  registry code, which is what a developer wants; a standalone copy of a
  tool in a user's project gets the same safety.
- **The config registry falls back to project scope.** Its scope follows
  the root's Config Scope through `op.FNS.par.Configscope if hasattr(op,
  'FNS') else 'project'`, by design.
- **The toolkit logger is absent.** Every `fnsLog` is guarded.

Nothing else in the eleven reaches for the root; the surfaces address the
globals by shortcut (`op.FNS_TOOLBARREGISTRY`).

## How it is built

`BuildDevKit()` in `packaging/build_installer.py`, beside `BuildBootstrap()`:
plain file work, no staging in TD. It zips the eleven registry toxes from
`packaging/dist/` (built by `Build()`; the build refuses when one is
missing), writes the README (the surfaces table, how to use the kit, the
root notes above) and `LICENSE.txt` from `license_notices`, and records the
release it was built from in `dist/rails_versions.json` beside the
installer version of the other rails.

## How it ships

A third rail. `publish.py` hashes it into the manifest's `rails` and
copies it to `<release>/`, `upload.py` uploads it and aliases it as
`latest/FNSTools-DevKit.zip`, `verify_release.py` checks it like the other
rails, and `release_one.py` counts it among the rail artifacts, stale when
a registry tox or `build_installer.py` is newer than it. The website offers
it from the Get section ("Building a tool for FNSTools?"), the
getting-started guide has a section, and the repository README a "For tool
developers" section.

## How a developer uses it

1. Download `latest/FNSTools-DevKit.zip`, unzip, and drag the registries
   the tool publishes into at the root of a development project. Each
   promotes on load.
2. Stamp a host into the component being built, from the dropped master
   (the `/sys` global refuses to stamp):
   `op('/FNS_ToolbarRegistry').StampHost(comp)`, the same recipe for every
   registry (`/fns-registry`), and register from the component's init as
   the contract for that surface says.
3. Test in TouchDesigner. The surfaces are the real ones.
4. Before installing the real toolkit into the same project, delete the
   loose registries: a same-version registry already promoted keeps the
   global (ties keep the incumbent), which works but is not what anyone
   wants to debug. The stamped hosts then clone from the toolkit's masters,
   cloning switched back on by the guard.

## Landing

1. The kit as a zip, the rail, the site and README links, Run 8 of
   `FirstRunTestPlan.md`, `tests/test_devkit.py`: landed 2026-10-17
   (uncommitted at the time of writing). The one-tox build of earlier that
   day (commit b1abf369) is replaced; nothing of it ships.
2. The `RegistryBase` guard: landed 2026-10-17 in the main tree with
   TouchDesigner closed (prepared in `../FNSTools_PRIV-wt-hostguard`,
   since removed), with `tests/test_registry_host_guard.py`. Verified
   live after the relaunch on a toolbar host stamped from the live master
   into a scratch COMP: the clone set empty plus a reinit reads Enable
   Cloning off; the registry expression restored plus a reinit reads it
   on again, both without errors. A cold boot syncs the file-bound DAT
   into every host without dirtying its tox, so no tox save and no tox
   commit came with the landing (PI dirty: the root only, pre-existing).
   Two consequences for the release: the dist registry toxes in
   `packaging/dist/` predate the guard (a host stamped from one of them
   reinitialises without it, measured), so `Build()` must run before
   `BuildDevKit()`; and the zip must not ship from the old dist.
3. Run 8 on a clean TD, with the release.

## Open points for the owner

1. **The command registry**: in (this doc, since `FNS_CommandKit` publishes
   into it and a tool's commands are part of the surface) or out.
2. **Takeover**: should the installer, when it meets loose registries in
   the project, offer to remove them as part of the first install, the
   way the updater takes over standalone copies? Not built; the README
   says to delete them first.
