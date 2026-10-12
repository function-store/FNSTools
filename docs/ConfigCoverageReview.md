---
status: open
summary: Review of config roaming coverage (2026-10-10) -- global tools without a config host, surface positions no host persists, project data that roams, hotkeys persisted twice, dev values that ship.
since: 2026-10-10
skill: fns-config-scope
---

# Config coverage review (2026-10-10)

## Status

| Item | State |
|---|---|
| 1. OpFamily without a host | **landed**: a host that roams only `Installonstart` (`Cfexcludepars = '* ^Installonstart'`), the "install this family when a project opens" choice (owner) |
| 2. Surface positions | **landed**: a tool's section carries `surfaces`; iopBrowser and ParentHierarchy got config hosts |
| 3. Project data that roams | **landed**: operator references never roam (`OP_REF_STYLES`); TimelineTools excludes `Markerfile Exportfile`, VSCodeTools `Workspace Folder`; exclusions now filter apply too |
| 4. Hotkeys persisted twice | **landed**: the Hotkey Manager owns them (owner); config skips them inside the toolkit while it is installed |
| 5. Dev values that ship | **landed**: `shipped_values` in packaging/surface_defaults.json ships VSCodeTools `Workspace` and TimelineTools `Exportfile` empty; a real VSCodeTools export read back with `Workspace` empty while the dev project kept its own. `Folder = scripts` ships on purpose (a convention, not this machine). |

Verified live: the filter re-run leaves only the preferences of item 3's
keep-list roaming and no hotkeys; Volume's bar width saved, nudged and
loaded back (100 -> 101 -> 100); a full `SaveAll` wrote 68 sections with no
hotkey or operator-reference par and 10 tools carrying `surfaces` (all 14
widgets of item 2); `ScopeAudit()` empty; both error surfaces clean.
Not verified: a real TouchDesigner restart.

Measured live against the `/sys` FNS_ConfigRegistry's own entries (52
registered hosts, none with `Persistpars` off), its exclusion matcher and
its skip rules (pages About, Version Ctrl, Info, Callbacks, Common; pulses,
headers, read-only pars). Expressions and binds roam as their text.

## 1. Global tools without a config host (17 of 62)

| Tool | Verdict |
|---|---|
| The registries (Command, Config, Hub, MainMenu, Navbar, OpMenu, Palette, PaneType, PaneSearch, Timeline, Toolbar), FNS_Console, FNS_ConfigHost, FNS_CommandKit | infrastructure with no user setting; nothing to do |
| FNS_OpMenuRegistry | its one par is a hotkey (`Shortcutalternatives`), which the Hotkey Manager persists |
| FNS_iopBrowser, FNS_ParentHierarchy | no settings of their own; their navbar position is item 2 |
| **FNS_OpFamily** | 16 settable pars and no host. Most are family plumbing that must never roam (`Family`, `Opfolder`, `Namingconvention`, `Callbackdat`, `Opcomp`, `Famuicomp`, `Index`, `Compatibletypes`, the Stubs page targets); the user-facing ones are `Install`, `Installonstart`, `Color`, `Colorfileops`. Owner's call whether those four roam. |

## 2. Surface positions no host persists (14 widgets)

A config host snapshots its OWN tool's pars. These widgets keep their
surface pars on a child operator, so a user's reorder or hide of them is
lost when the tool reloads from its tox (from the code; no restart test
yet):

CookBar `button_cookbar`; BorderlessTD `gridshow` and `BorderlessWindow`
(main menu); CustomParTools `hijack_dragdrop` and `PathCellClickInject`;
GlobalVolControl `button_mute` and `slider_volume`; Misc `background1` and
`input_mouse`; OpMenuMods `IOFilter`; ParentHierarchy and iopBrowser
`nbwidget`; PreviewPanel `UI/POPtoDAT_panel`; midiMapper
`button_midi_learn`.

Proposed: the tool's config host also snapshots the surface pars of the
surface hosts inside it (one host per tool, an additive key in the
section), first proven with a restart test.

## 3. Project data that roams (should be excluded)

| Tool | Par | Why |
|---|---|---|
| FNS_Output | `Performwindow` | an operator path in this project |
| FNS_TimelineTools | `Markerfile`, `Exportfile`, `Animation`, `Refs0op` | project files and operators |
| FNS_Remote | `Createtarget` | an operator in this project |
| FNS_VSCodeTools | `Workspace`, `Folder` | this project's workspace and script folder |
| FNS_Updater | `Target` | the toolkit COMP in this project |
| QuickExt (CustomParTools) | `Comp` | a transient target |
| midiMapper, oscMapper | `Mappingtablerepositorie` | an internal table reference; pointed elsewhere it would break other projects |

Left roaming on purpose (preferences): BackupCleaner `Pattern`,
`Keeplast`; BeatMod `Divisions`; PasteFromClipboard `Folderpath` (a
project-relative convention); VSCodeTools `Codeexe` and Updater
`Storefolder` (machine paths, and the config file is per machine);
SearchFix `Maxresults`; ResetPLS `Count`. To check: ColorUI `File`.

## 4. Hotkeys persisted twice (20 tools)

Hotkey pars roam through the tool's config section AND the Hotkey
Manager's rows. BeatMod and CommandPalette exclude theirs from config
(BeatMod still roams `Shortcutrecord`, added later); the other 18 do not.
One owner should hold them. The Hotkey Manager has defaults, reset and the
per-project declaration, but it is optional: a user without it would lose
roaming hotkeys if config stopped carrying them. Owner's call.

## 5. Dev values that ship

| Artifact | Par | Shipped value |
|---|---|---|
| FNS_VSCodeTools | `Workspace` | `FunctionStore_tools_2023.code-workspace` (the old dev project) |
| FNS_TimelineTools | `Exportfile` | `test.csv` |

The project-data pars of item 3 are the same class: whatever the dev
project holds there ships. Proposed: the export resets them to an authored
default, the way packaging/surface_defaults.json does for layout
(docs/ShippedSurfaceDefaults.md), so dev, own use and shipped stay
separate.

## Checked and fine

- The Updater's `Licensekey` ships empty and is empty in the dev project.
  It would roam in plain text in the config file once set; one key per
  machine is probably the intent.
- Existing exclusions (QuickMarks `Marks`, ResetPLS `Root Except`, Remote's
  pairing and control pars, TimelineTools' scope and media, OpTemplates'
  `Templates Target`, BackupCleaner `Root`) hold project data, as they
  should.
