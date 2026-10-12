---
status: landed
summary: A licence notice inside every shipped tool, stamped by the release step from the package's access - MIT in full for free tools, the Patreon licence for anything not free, plus the third-party notices SearchPalette (MIT) and the operator family (TDFam, Apache 2.0) owe. Free tools stay MIT; the terms gained No derived tools and Projects you deliver. Built and verified 2026-10-09; reaches each tool at its next release.
verified: 2026-10-09
since: 2026-10-09
skill: fns-packaging
---

# Licence notices inside the tools

The licence lives on the website (`/terms/`, `/patreon/`) and in the repo
(`LICENSE`, `THIRD_PARTY_NOTICES.md`). A `.tox` someone downloads, installs or
gets handed carries none of it. This puts a short notice inside every shipped
tool, so the file says what it is licensed under wherever it ends up.

## Decided: free tools stay MIT

Owner and Claude, 2026-10-09. The aim was to stop people reselling the tools or
building paid tools out of them. MIT allows both, so the question was whether
to move free tools off MIT. They stay:

- MIT is what the TouchDesigner community expects; a studio adopts an MIT tool
  without a legal review.
- Every free version already released stays MIT forever, so a reseller would
  take the last MIT version and a new licence would protect little.
- `/terms/` promises "That will not change for a package that is already
  free", and `/patreon/` "Nothing that is free today becomes paid later".
  Breaking that costs more trust than it buys.
- Reselling something that is free on functionstore.tools mostly fails on its
  own; what has value (updates, integration, the Patreon tools) cannot be resold.
- MIT does require the copyright and licence notice to stay in every copy.
  With the notice inside the file, a copy that strips it breaks the licence,
  which is something a marketplace takedown can stand on.

The promise covers packages **already free**. A tool that is new and free later
may launch under another licence without breaking it; that is decided per tool
when it comes up.

The protection goes where the paid value is: the Patreon tools, whose terms get
one explicit clause (below) and whose files get the notice.

## Gaps this closes

- **Gated tools say nothing in the file.** A copy passed on carries no sign that
  it is licensed per person.
- **SearchPalette** (`FNS_SearchPalette`) is based on Yea Chen's
  TD-SearchPalette, MIT. MIT requires their copyright and permission notice
  in every copy; today it is only in the repo's `THIRD_PARTY_NOTICES.md`, not
  in the artifact.
- **The operator family** (`FNS_OpFamily`) is built with TDFam, Apache 2.0,
  which requires recipients to get a copy of the licence. Same gap.

## How it is built

The release step stamps the notice onto the **artifact copy**, never the live
master, the same way `pre_release_common.py` already rewrites
`FNS_About.Owner` and the `_dev` paths on the copy. The repo's masters stay
unchanged, so no PI churn.

- **Which text** comes from the package's access in the catalog: `free` gets
  the MIT notice; anything else gets the Patreon notice. In the v3.2.67
  manifest that is a Patreon tier id (24 packages) or `preview` (14, not yet
  public), plus every `.pro` variant build. The rule is "not `free`", so a new
  gate value can never fall through to MIT. A variant is judged by the artifact being
  built: `ColorGen` is MIT, `ColorGen.pro` is not.
- **Foreign packages** (TDXMap and any with a catalog `source` block) are not
  ours to licence and get nothing.
- **Third-party notices** come from the catalog, beside the existing credit
  fields (`author`, `homepage`): a `third_party` list of
  `{name, url, license, files}`, each file a licence text under
  `packaging/licenses/` (kept word for word in step with
  `THIRD_PARTY_NOTICES.md`; the test checks it). Each file becomes one more
  annotation. Long texts (Apache 2.0, 10,300 characters) are
  annotations too, not text DATs: annotations are utility ops, so a tool's
  own `findChildren` walks never see them, where a stray DAT inside
  FNS_OpFamily could be picked up by the tool scanning its children.
- **The toolkit bootstrap** (`FNSTools.tox`, built by `build_installer.py`,
  which skips the package scrub) gets the MIT notice in its own step.
- **Placement:** Annotate COMPs stacked above everything in the tool's network,
  left-aligned with it, named `fns_license*`. Re-stamping replaces them.
  Network only: annotations do not draw in a panel.
- **A failed stamp fails the export.** `Stamp` reads every note back and
  raises when TD did not keep the text, and a broken `third_party` entry
  raises in `Notices`, so no artifact ships unlicensed or half-licensed.
- **The year** is derived at release: `2023-<release year>`.

## Where it lives

| Piece | File |
|---|---|
| The texts, the access rule, the stamp | `packaging/license_notices.py` |
| Third-party licence texts | `packaging/licenses/` |
| What each package owes | `packaging/catalog.json`, `third_party` |
| Package artifacts (base and variant builds) | `build_manifest.ScrubArtifact`, called by `ExportPackage` |
| The bootstrap `FNSTools.tox` | `build_installer.BuildBootstrap` |
| Catalog validation | `build_manifest.CatalogProblems` |
| Test | `tests/test_license_notices.py` |

The texts are in `license_notices.py`, not here, so they cannot drift.

- **Free:** title `FNSTools - MIT licence`; the body is the repo's `LICENSE`
  word for word with its copyright line derived for the release year and the
  site under it. The full text, because MIT's one condition is that it travels
  with every copy.
- **Patreon:** title `FNSTools - Patreon licence, not MIT`; copyright, licensed
  to the person whose membership or key unlocked it, client deliveries allowed,
  no redistribution and no derived tool, component, plugin, library, template
  or project pack, and a link to `/terms/`.
- **Third party:** titled `Third party: <name> (<licence>)`, the project name
  and URL, then the licence file in full.

## The terms (landed 2026-10-09)

`/terms/`, The Patreon packages, has two new items after "What you do not
get", which no longer says "bundle the package into something you hand on":
that phrase also forbade handing a client the project they paid for.

- **No derived tools.** A Patreon package's networks, code or shaders, as they
  are or reworked, may not go into a tool, component, plugin, library,
  template or project pack that is distributed, sold or published. What people
  make with it is theirs.
- **Projects you deliver** (owner, 2026-10-09: allowed). Handing a client or
  venue a project that uses a Patreon package, so they can run that project,
  is fine; they may not take the package out and use it elsewhere.

`/patreon/`, "Can I still read the source of a Patreon tool?", says the same
in one sentence. Both pages changed in one commit, as their source comments
require. Per `/terms/`, changes apply going forward, never to a licence
already held.

## Verified (2026-10-09, TD 2025.33070)

On a scratch copy of the released `FNS_SearchPalette.tox`, through the same
`/sys/quiet` holder the release scrub uses:

- `comp.create(annotateCOMP)` then rename, `utility = True`, `Mode =
  'annotate'`: both notes came back after save and reload, with title and body
  exactly as derived, line breaks included. A 10,300-character body (the
  Apache licence) survives intact.
- The tool's own child count was unchanged (16 before and after): the notes
  are utility ops, invisible to default `findChildren` and `.children`.
- No errors on the reloaded copy; notes sit above the network's top edge.
- Re-stamping with a different access replaced the earlier notes instead of
  stacking them, and the gated title replaced the MIT one.

Not yet seen: how the notes read in a network editor at real zoom. The size is
derived from line count at Envoy's 22 units per line.

## LICENSE DATs say the same (2026-10-12)

FNS_About carries a `LICENSE` text DAT with the MIT text, copyright 2025, and
its Deploy copies it into the package, so 151 such DATs sat in the toolkit,
gated packages included: a Patreon tool shipped with the Patreon notice on
top and MIT inside it (owner, 2026-10-12). `Stamp` now also rewrites every
`LICENSE` DAT that holds the MIT template (it carries "Permission is hereby
granted, free of charge") with the package's own licence: the release-year
MIT text for a free tool, the Patreon licence under its title for anything
else. A `LICENSE` DAT with other text is left alone: the scene changers' own
Patreon licence, TDFam's Apache attribution (its full text is the separate
`LICENSE_Apache`). Read back like the notes; a DAT that did not take the text
raises. The masters keep the MIT template; the artifact is what changes.

Verified on real exports through the portable export: LayerSep3D (Base) came
out with its FNS_About `LICENSE` reading the Patreon licence;
FNS_SimpleSceneChanger kept its own `LICENSE` and only FNS_About's changed.

## Rollout

The stamp runs on every export, and `ReleaseMany` exports only the packages a
release bumps, so each tool gets its notice at its next release. Getting every
artifact covered at once means re-exporting every package in one release; that
is a release decision, not part of this change. The bootstrap gets it at the
next rails rebuild, which bumps `INSTALLER_VERSION` like any rails change.
