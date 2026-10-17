---
status: landed
summary: 'A consumer agent skill shipped with the toolkit, so a user''s own coding agent can drive the installed FNSTools: one authored core page plus one generated reference page per public package, built in the release pipeline, validated against the dist build, installed into a project or user skills folder by a quick-launch command. No contributor skill, no MCP layer.'
since: 2026-10-15
verified: 2026-10-17
---

# Agent skill: let a user's own agent drive the installed toolkit

Owner's question, 2026-10-15: is there validity in shipping agent skills or
tool files for the toolkit, for OTHER agents to use. Answer: yes, for one
narrow form of it. This document is the brief for that form, written so it
can be executed from and so the contract it fixes is in git from day one.

## 1. The gap

A user who runs a coding agent (Claude Code, Cursor, Codex, anything that
reads a project folder and may drive TouchDesigner over an MCP bridge) and
has FNSTools installed gets a network full of `FNS_*` COMPs, fifteen or so
global shortcuts (`op.FNS_COMMANDREGISTRY`, `op.FNS_MEDIA`,
`op.FNS_CONFIGREGISTRY`, ...), promoted methods, hotkeys and config files,
and no explanation of any of it. The agent queries the network and guesses.
It will rebuild something a tool already does, call a method that is a
callback, or write to a config file by hand.

The toolkit already holds the material an agent would need, in machine
readable form:

- 103 per-package docs in `packaging/docs/<Name>.md`, each with frontmatter
  (`summary`, `feature_list` with `does` lines, anchors). They are the source
  the docs site is generated from.
- `packaging/manifest.json`, derived live from the project per release:
  `help_url`, `surfaces`, `hotkeys`, `alternatives_for`, `family`,
  `requires`, `version`, `search`.
- Promoted extension methods with docstrings, and quick-launch commands
  declared with `@FNSCommand.fns_command` (label, help, typed params). The
  manifest build already reflects over these (`build_manifest.py`, the
  commands harvester) to decide launcher capabilities.
- Hotkeys read off `FNS_HotkeyManager.Discover()`, never from prose
  ([DocsEvidenceDerivation.md](DocsEvidenceDerivation.md)).

So a skill is mostly a third output of a pipeline that already exists. The
cost is the generator, the validation gate and the install command. The
risk is drift, and the design below is shaped around that risk.

## 2. The decision

**Build one consumer skill: "drive FNSTools from an agent".** Skip the
other two forms:

- **A contributor skill** ("extend FNSTools": register a command, offer an
  alternative, join a registry). The internal `fns-*` skills in this repo
  are that already, soaked in private process (PrivateInvestigator,
  SaveDirty, nested suspects). A public subset is possible later, when a
  third party asks. Small audience, deferred.
- **An MCP layer or tools file.** A bridge such as Envoy already gives the
  agent `execute_python` and method execution, so the toolkit's promoted
  methods already are the tools. A second server would duplicate that and
  tie the toolkit to one bridge. What an agent needs is the catalog of
  those methods, which is the skill's reference half.

The skill must not depend on any particular bridge. Without one, the agent
still uses it to write scripts and DAT code the user runs; with one, it
drives TD directly. The core page says so in its first lines.

## 3. Shape

The canonical form is the Agent Skills layout (`SKILL.md` with `name` and
`description` frontmatter, progressive disclosure into `references/`),
because Claude Code reads it natively and the format is an open spec other
agents have adopted. Other agent formats get thin pointers, never a second
source (section 7).

```
fnstools/
  SKILL.md                    authored core page, read on every trigger
  VERSION                     the toolkit release it was generated from
  references/
    index.md                  generated: one line per package, with category,
                              summary, help_url, what it is an alternative for
    <Package>.md              generated: one per public package
    registries.md             authored: the registry globals and what each owns
    commands.md               generated: every quick-launch command, by tool
```

### 3a. The core page (authored, `packaging/agent_skill/SKILL.md`)

Short. The description line is the trigger: it must name the things an
agent sees in a user's project (`FNS_`, `op.FNS_`, FNSTools, the Hub, the
toolbar, quick-launch commands), since a skill fires on its description.
The body:

- What the toolkit is, in three sentences, and that it is installed per
  machine in `<user palette>/FNSTools` ([PaletteFolderContract.md](PaletteFolderContract.md)).
- How a package is reached: a global shortcut when it has one, a placed
  copy's promoted methods otherwise. The three namespace tiers from
  `td-python.md`: only `UpperCamelCase` members are the agent's API; a
  lowercase member is wiring and must not be called from outside.
- The registries: what each `op.FNS_*REGISTRY` owns, and the rule that a
  consumer registers with the registry and never writes into its tables
  ([ConfigScope.md](ConfigScope.md), the registry docs). Detail lives in
  `references/registries.md`.
- Quick-launch commands: that they exist, that `commands.md` lists them,
  and how to run one from code.
- Op alternatives: that a stock operator type may have an FNS alternative
  and how placement works ([OpAlternatives.md](OpAlternatives.md)).
- Config and hotkeys: where they live, that the registries own the files,
  and that an agent changes them through the registries' promoted methods
  and never by editing JSON.
- One fact an agent cannot infer: `op.FNS` is the toolkit root and does
  not exist when a tool runs on its own, so it needs a guard
  (`tests/test_root_shortcut_guards.py` reasoning). Beyond that the page
  describes the toolkit and leaves working rules to the user's own agent;
  it is a reference, not a process document (owner, 2026-10-15).
- How to find out more: `references/index.md`, then the package page,
  then the `help_url`.

### 3b. The package pages (generated)

One page per package in the manifest that is public (not `preview`, not
`foreign` unless the foreign row carries docs of its own). Each section is
derived from one named source, after [DocsEvidenceDerivation.md](DocsEvidenceDerivation.md):

| Section | Source |
|---|---|
| Title, summary, category, version, help_url | manifest row |
| What it does | `feature_list[].does` from the doc frontmatter |
| Reach it | `shortcut` from the manifest, else "place a copy" with the `family` op name or the palette path |
| Promoted API | reflection over the extension class at build time: every `UpperCamelCase` method, its signature and the first docstring line. Members with no docstring are listed with the signature only and counted (section 5) |
| Commands | the `_fns_command` specs the harvester already reads: label, help, params |
| Hotkeys | manifest `hotkeys`, which come from `HotkeyManager.Discover()` |
| Alternative for | manifest `alternatives_for` |
| Requires | manifest `requires` |

Nothing on a package page is typed by hand. A package with no doc file
still gets a page from the manifest and the reflection, marked as such.

The reflection step runs inside TD during `build_manifest.Build()`, where
the commands harvester already runs; the markdown rendering is pure Python
in a new `packaging/agent_skill.py`, loaded by path like
`packaging/search_index.py`, so `tests/` can run it on a fixture manifest
without TouchDesigner.

## 4. Generation and release

- `build_manifest.Build()` gains one more derived field per package,
  `api`: the reflected promoted methods and their docstring heads. It
  rides the manifest row like `search` does. Everything else the skill
  needs is already there.
- `packaging/agent_skill.py` renders the bundle from the manifest and the
  authored pages into `packaging/dist/agent-skill/`. `VERSION` holds the
  release string. No archive in the first release (owner, 2026-10-15): the
  bundle is a folder, and both consumers below copy a folder.
- The bundle is also synced into the palette folder as
  `<user palette>/FNSTools/agent-skill/` by the same installer step that
  lays out the family folder, so the install command (section 6) copies
  from a local source and works offline.
- `release_notes.md` carries a line when the authored pages change, like
  any package.

## 5. The validation gate

Drift is the whole risk. A skill that names a method that no longer exists
is worse than no skill, because the agent trusts it. Two checks, both in
`pre_release_common.py` so a release cannot ship without them:

1. **Every name the authored pages mention resolves in the dist build.**
   A test parses `SKILL.md` and `references/registries.md` for `op.FNS_*`
   shortcuts and `Shortcut.Method(` references, loads the dist toxes
   cooking off (the same loader the storage leak check uses) and asserts
   each shortcut exists and each method is a callable `UpperCamelCase`
   member. A miss fails the release.
2. **Coverage report.** The generator counts promoted methods with no
   docstring and packages with no doc file, and prints them. Not a gate at
   first; the number is the backlog for the owner's docstring pass. It
   becomes a gate once it reaches zero, so it cannot climb back.

The generated pages need no gate: they are reflected from the build they
ship with. `tests/test_agent_skill.py` covers the renderer on a fixture
manifest.

## 6. Distribution: a quick-launch command

A command on the root host, authored per `/fns-command-registration`:

```python
@FNSCommand.fns_command(help='Copy the FNSTools agent skill into this project or your user skills folder')
def InstallAgentSkill(self, where: Literal['project', 'user'] = 'project'):
```

- `project` writes `<project folder>/.claude/skills/fnstools/`;
  `user` writes `~/.claude/skills/fnstools/`. Both are what Claude Code
  reads. Other agents' locations are section 7.
- Source is `<user palette>/FNSTools/agent-skill/`.
- Idempotent: compares `VERSION`, replaces an older copy, leaves a newer
  one and says so in the console. Never touches anything outside the
  `fnstools/` folder it owns.
- Logs the destination to the console tab, so the user sees where it went.

The Hub gets a button for the same command on its Install tab, only if the
tab already has a place for actions ([HubContract.md](HubContract.md));
otherwise the command alone is the surface for the first release.

## 7. Other agent formats

One canonical source, thin pointers for the rest, added only when a user
asks for that agent:

- `AGENTS.md`: the install command can append a short block that says the
  toolkit is installed and points at `.claude/skills/fnstools/SKILL.md`.
  Opt-in flag on the command; off by default so the command never edits a
  file it does not own without being asked.
- Cursor rules, Codex, Windsurf: not in the first release. Record requests
  in the backlog below.

## 8. Entitlement and scope

- The bundle covers every public package, like the docs site does. It
  carries nothing a page on functionstore.tools does not already show, so
  there is nothing to gate. Preview packages stay out, per
  [PreviewPackages.md](PreviewPackages.md).
- The package page says which tier a package needs (`access`), so an agent
  does not propose a tool the user has not installed as if it were free.
- No installed-set filtering in the first release. An agent reading about
  a package the user lacks is a lead for the picker, which the page's
  `help_url` serves.

## 9. Success criteria

The work is done when all of these hold:

1. A release build produces `packaging/dist/agent-skill/`, and `VERSION`
   matches the release.
2. Every public package has a `references/<Package>.md`, with a Promoted
   API section listing every `UpperCamelCase` method of its extension.
3. `pre_release_common.py` fails a release where `SKILL.md` names a
   shortcut or method the dist build does not have; verified by breaking
   one on purpose once.
4. `InstallAgentSkill` places the bundle into a fresh project, a second run
   reports "already current", and an older copy is replaced.
5. A cold session of Claude Code in a project with the skill installed,
   asked to "toggle realtime through FNSTools", finds the right command
   from `commands.md` without querying the network. One such smoke run,
   recorded in this document's verified field.
6. `tests/test_agent_skill.py` passes without TouchDesigner.
7. Docs index regenerated, release notes line added, this document moved
   to `landed` with the verification date.

## 10. Order of work

1. `packaging/agent_skill.py` renderer plus the fixture test, from a
   checked-in manifest. No TD needed.
2. The `api` field in `build_manifest.Build()`. Run a build, inspect the
   coverage report, note the docstring backlog.
3. The authored core page and `registries.md`.
4. The gate in `pre_release_common.py`, with the dist loader.
5. Installer sync of `agent-skill/` into the palette folder.
6. The quick-launch command on the root host.
7. Smoke run in a fresh project (criterion 5), then the release line.

Steps 1 and 3 can run in parallel. Step 4 needs 3. Step 6 needs 5.

## 11. Open questions for the owner

Asked 2026-10-17 with the defaults below taken; the owner may still turn
either one around (see section 13).

- Should the package pages include parameter lists (name, label, style,
  default, help) reflected from the custom pages? It is one more derived
  section and the richest one for an agent, but it doubles page length.
  Proposal: include, collapsed under a heading the agent reads on demand.
  **Taken: included**, as the last section of each page ("Parameters",
  one line per parameter under its page), read from
  `packaging/parameters.json`, which the same `Build()` pass writes.
- Is the root host (`FNS`, `FNS_ConfigHost`) the right owner for the
  command, or should it live on the Hub's own extension?
  **Taken: `FNS_Updater`.** The toolkit root has no extension at all (its
  commands live on child COMPs), and `FNS_ConfigHost` is a config-registry
  host whose commands belong to the `/sys` global by the registry
  family's owner guard. The updater is core, always installed, already
  owns the palette folder and the family-folder sync that step 5 extends,
  and already declared two commands.

## 12. Backlog

- Contributor skill (public subset of the `fns-*` skills).
- Cursor, Codex and Windsurf pointer files.
- Installed-set filtering of the bundle.
- A downloadable archive of the bundle on the docs site or the GitHub
  release, for a user with no TD install. Deferred 2026-10-15: adding it
  later costs nothing, while a published download link is a commitment.
- A `metadata` block in `SKILL.md` frontmatter carrying the version, once
  every reader is known to tolerate it.

## 13. What landed (2026-10-17)

Steps 2 to 7 of section 10, each verified in the running TouchDesigner
before the next. Where the build differs from the sections above, this
section is the record.

- **Step 2, the reflected fields.** `build_manifest.Build()` carries two
  presence-style row fields: `api` (`PromotedApi`: every UpperCamelCase
  method, property and instance attribute of the package's promoted
  extensions, with the signature and the docstring's first sentence, read
  across the wrapped lines of the first paragraph) and `commands`
  (`Commands`: the `_fns_command` marks and `FnsCommands()` specs of the
  package root and of every descendant tagged `fnscommands`, which is how
  the built-in TouchDesigner commands under `FNS_CommandRegistry` reach the
  pages; an untagged registry host inside a tool is not an owner). Label
  and help come from the live registry's `Commands()` rows when the owner
  has announced, else from the registry's own derivation. A registry
  master also carries `global_shortcut` (its extension's `SHORTCUT`), kept
  apart from `shortcut`, which the updater reads to recognise standalone
  copies. Preview rows carry none of the three. Measured on v3.2.71: 86
  pages, 802 promoted members, 141 commands; `api` and `commands` add 115
  KB raw, 21 KB gzipped, to the manifest (`search` adds 55 KB raw).
- **The docstring backlog (section 5, check 2):** 239 promoted members
  with no docstring on 2026-10-17, listed by `CoverageText` at every build
  and counted as a Preflight warning. The list is in the side-session
  notes of that day; the heaviest packages are QuickMarks (14),
  FNS_Updater (13), FNS_ColorUI, FNS_CustomParTools and oscMapper (10).
- **Step 3, the authored pages.** `packaging/agent_skill/SKILL.md` and
  `references/registries.md`, facts only, the `op.FNS` guard the one
  working rule, per the owner's 2026-10-15 decision. "Reach it" on a
  generated page follows the manifest's `placement`: absent is a child of
  the toolkit root (`op.FNS.op('CookBar')`), `root` is beside the toolkit
  at the project root, `none` is the store tox to place by hand, a family
  member is the FNS tab, a registry is its `/sys` global.
- **Step 4, the gate, in `Preflight()` and not in `pre_release_common.py`.**
  That file is a per-package hook exec'd on a staged copy inside an
  export; it cannot load dist toxes, and the release gate that refuses on
  a blocker is `release_one.Preflight()`. `_agentSkillProblems()` parses
  the authored pages (`agent_skill.MentionedNames`), loads only the
  packages they name into one cooking-off holder in `/sys/quiet`, checks
  a package shortcut against the loaded copy's `opshortcut` and a
  registry global against the extension class's `SHORTCUT`, and checks
  every `op.X.Method(` against the class read statically from the DAT
  text of the dist copy (`ClassMembers`, following bases such as
  `RegistryBase`), since extensions never initialise there. It also fails
  the release when the bundle on disk is not the one the manifest hashes,
  or an authored page changed after the last `Build()`. Criterion 3 was
  verified by breaking a page on purpose: a bogus method, a bogus
  shortcut and the edited page each blocked; a lowercase member was
  ignored; a real method resolved. The gate takes about 4 s.
- **Transport (section 4).** No archive, as decided, but the folder has
  to travel: `Build()` writes `packaging/dist/agent-skill/fnstools/` and
  one `packaging/dist/agent-skill.json` (the bundle's files as one JSON
  document, deterministic), and the manifest carries an `agent_skill`
  block (version, bytes, sha256, url pinned under the release). `Stage()`
  stages the document beside the rails, re-hashed, and a release that
  changes only the skill passes the no-change guard; `upload.py` prunes
  it with the rails; `verify_release.py` verifies it.
- **Step 5, the updater.** A store refresh or update pass fetches the
  document when the store's copy is absent or stale (a manifest-only
  refresh does not), through the same `.part` staging and hash check as
  an artifact, on the network and local rails. `SyncAgentSkillFolder()`
  unpacks it into `<user palette>/FNSTools/agent-skill/fnstools/` beside
  `FNS/`, writing only what differs and pruning the rest, and runs beside
  `SyncFamilyFolder()` at its three call sites. The source checkout
  unpacks its own `packaging/dist/agent-skill.json` instead, so the dev
  machine's copy is the build just rendered.
- **Step 6, the command.** `FNS_Updater.InstallAgentSkill(where:
  Literal['project', 'user'] = 'project', agents_md: bool = False)`,
  registered as `Install agent skill` with a menu and a toggle. Verified
  through `op.FNS_COMMANDREGISTRY.Run`: installed, current, an older
  copy replaced, a newer copy kept, a same-version copy with different
  files refreshed (the dev-machine case), 91 files. `agents_md` appends
  one marked block to `AGENTS.md` once (section 7). No Hub button: the
  Hub's Install tab is the console's web page, not a native tab with an
  actions area, so the command is the surface, as section 6 allows.
- **Step 7, the smoke run (criterion 5).** 2026-10-17, Claude Code
  2.1.257, headless (`claude -p "toggle realtime through FNSTools"`), a
  fresh folder holding only `.claude/skills/fnstools/` as the command
  placed it, no MCP servers, tools limited to Read, Glob and Grep. The
  session loaded the skill, grepped the references for "realtime", and
  answered with `op.FNS_COMMANDREGISTRY.Run(op.FNS.op('FNS_CommandRegistry/FNS_BuiltinCommands/TD_Session').path + '#togglerealtime')`
  and the direct `ToggleRealtime()` call, in 5 turns. A first run, before
  the command lines carried the id and the key recipe, found the command
  too but guessed its id from the method name and its path under `/sys`;
  the page format was corrected and the run repeated.
- **Not verified live:** the network fetch of `agent-skill.json` by an
  installed updater against the bucket, which needs the next release to
  publish one (the local rail and the queue were exercised in code; the
  store refresh of the dev checkout does not run against the bucket).
- **Tests.** `tests/test_agent_skill.py` (the renderer, the transport,
  the parser, the static resolver, the committed manifest and parameter
  reference), `tests/test_publish_guards.py` (staging the document).

- **The docstring pass (same day).** The 239 became 0: 152 members got a
  first sentence (121 in externalised extension files, landed live in four
  batches of single-tool files with both error surfaces checked after each,
  31 in extension DATs embedded in their tox, edited as DAT text); the
  per-block `Chan` properties the constant tools build at runtime carry
  their sentence through the factory's `doc`; 25 in the registry extension
  files, which are bound into every host by file, landed with TouchDesigner
  closed; and the reflector learned two kinds it should not count: a
  property TouchDesigner's own modules make (a StorageManager stored item,
  a TDFunctions dependable; listed as "stored", 50 of them) and a member a
  TD base class contributes (`CallbacksExt`, left off the page). With the
  count at zero `Preflight()` blocks on it.

Backlog additions: the updater could refresh the skill folder at project
open so a fresh install holds it before any refresh.
