"""Licence notices stamped into every shipped artifact (docs/LicenseNotices.md).

A .tox that is downloaded, installed or handed on carries no licence unless
the file itself says so. The release step stamps one Annotate COMP per notice
onto the ARTIFACT copy (build_manifest.ScrubArtifact, and the bootstrap in
build_installer.BuildBootstrap), never the live master:

  free package      the repo's MIT licence, in full -- MIT's one condition is
                    that this text travels with every copy
  anything else     the Patreon licence (a tier id, `preview`, a .pro build):
                    the rule is "not free", so a new gate value can never fall
                    through to MIT
  third_party       one more notice per catalog `third_party` entry, with the
                    full text of each file it names (SearchPalette owes Yea
                    Chen's MIT notice, the operator family TDFam's Apache 2.0
                    NOTICE and licence)
  foreign package   nothing: not ours to licence (it is never exported here)

Long texts stay annotations, not DATs: annotations are utility ops, so a
tool's own findChildren walks never see them, where a stray text DAT could be
picked up by a tool scanning its children.

Plain Python with no TD globals, loaded by path from both callers (the same
pattern as search_index.py); Stamp() takes the Annotate COMP type from its
caller. Tested outside TD by tests/test_license_notices.py.
"""
import io
import os
import re
import time

FREE = 'free'
NOTE_PREFIX = 'fns_license'
LICENSE_FILE = 'LICENSE'
COPYRIGHT_RE = re.compile(r'^Copyright \(c\) .*$', re.M)
FIRST_YEAR = 2023
HOLDER = 'Daniel Molnar / Function Store'
SITE = 'https://functionstore.tools'
TERMS = SITE + '/terms/'

MIT_TITLE = 'FNSTools - MIT licence'
# the line every copy of the MIT template carries; a LICENSE DAT holding it
# is FNS_About's, rewritten to the package's own licence at release
MIT_MARK = 'Permission is hereby granted, free of charge'
GATED_TITLE = 'FNSTools - Patreon licence, not MIT'

GATED_BODY = (
    '{copyright}. All rights reserved.\n'
    '\n'
    'Licensed to the person whose Patreon membership or Gumroad licence key\n'
    'unlocked it, for their own work, personal and commercial. Handing a client\n'
    'or venue a project that uses it, so they can run that project, is fine;\n'
    'they may not take it out and use it elsewhere.\n'
    '\n'
    'You may not redistribute, resell or publish this package, or use its\n'
    'networks, code or shaders, as they are or reworked, in a tool, component,\n'
    'plugin, library, template or project pack that you distribute, sell or\n'
    'publish.\n'
    '\n'
    'Full terms: ' + TERMS
)

# Annotation geometry, in network units: wide enough for an 80-column licence
# line, tall enough for its line count (Envoy's create_annotation uses the
# same 22 units per line).
NOTE_WIDTH = 1000
LINE_HEIGHT = 22
NOTE_PAD = 80
NOTE_GAP = 100


def copyrightLine(year=None):
    year = int(year or time.localtime().tm_year)
    span = str(FIRST_YEAR) if year <= FIRST_YEAR else '%d-%d' % (FIRST_YEAR, year)
    return 'Copyright (c) %s %s' % (span, HOLDER)


def isFree(access):
    return str(access or '') == FREE


def _read(repo, rel):
    with io.open(os.path.join(repo, rel), encoding='utf-8') as f:
        return f.read().strip('\n')


def mitBody(repo, year=None):
    """The repo's own LICENSE with its copyright line re-derived for the
    release year and the site under it. Raises when LICENSE has no
    copyright line or is not MIT: a release must never ship a guessed text."""
    text = _read(repo, LICENSE_FILE)
    if not text.startswith('MIT License') or not COPYRIGHT_RE.search(text):
        raise ValueError('%s is not the MIT licence this stamp expects' % LICENSE_FILE)
    return COPYRIGHT_RE.sub(lambda m: copyrightLine(year) + '\n' + SITE, text, count=1)


def thirdPartyProblems(entries, repo):
    """Human sentences for a catalog `third_party` value; empty when fine.
    Shape: a list of {name, url, license, files: [repo-relative paths]}."""
    if entries is None:
        return []
    if not isinstance(entries, list):
        return ['third_party must be a list']
    out = []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            out.append('third_party[%d] must be an object' % i)
            continue
        for k in ('name', 'license'):
            if not str(e.get(k, '') or '').strip():
                out.append('third_party[%d] has no %s' % (i, k))
        files = e.get('files')
        if not isinstance(files, list) or not files:
            out.append('third_party[%d] names no licence files' % i)
            continue
        for rel in files:
            if not isinstance(rel, str) or not os.path.isfile(os.path.join(repo, rel)):
                out.append('third_party[%d] file not found: %s' % (i, rel))
    return out


def _slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_') or 'x'


def Notices(access, third_party, repo, year=None):
    """The notices for one artifact, in stamping order:
    [{'name', 'title', 'body'}]. The first is always ours."""
    if isFree(access):
        own = {'name': NOTE_PREFIX, 'title': MIT_TITLE, 'body': mitBody(repo, year)}
    else:
        own = {'name': NOTE_PREFIX, 'title': GATED_TITLE,
               'body': GATED_BODY.format(copyright=copyrightLine(year))}
    out = [own]
    problems = thirdPartyProblems(third_party, repo)
    if problems:
        raise ValueError('; '.join(problems))
    for e in third_party or []:
        name = str(e['name']).strip()
        head = '%s (%s)' % (name, str(e['license']).strip())
        url = str(e.get('url', '') or '').strip()
        for rel in e['files']:
            body = _read(repo, rel)
            if url:
                body = name + '\n' + url + '\n\n' + body
            out.append({'name': '%s_%s_%s' % (NOTE_PREFIX, _slug(name),
                                              _slug(os.path.splitext(os.path.basename(rel))[0])),
                        'title': 'Third party: ' + head,
                        'body': body})
    return out


def licenseFileText(notice):
    """What a LICENSE DAT carries for `notice`: the MIT text as it is (it
    opens with 'MIT License'), any other licence under its title."""
    body = notice['body']
    return body if body.startswith('MIT License') else notice['title'] + '\n\n' + body


def RewriteLicenseDats(comp, notice):
    """FNS_About carries a LICENSE DAT with the MIT text and copies it into
    its package on Deploy, so a Patreon tool shipped saying MIT inside it
    (owner, 2026-10-12). Every LICENSE DAT in `comp` that holds the MIT
    template gets `notice`'s text, the package's own licence. A DAT with
    other text is left alone: the scene changers' own licence, TDFam's
    Apache attribution. Reads each back and raises when TD did not keep it.
    Returns the paths rewritten."""
    text = licenseFileText(notice)
    done = []
    for d in comp.findChildren(name=LICENSE_FILE, includeUtility=True):
        current = getattr(d, 'text', None)
        if current is None or MIT_MARK not in current:
            continue
        if current != text:
            d.text = text
        if d.text != text:
            raise RuntimeError('LICENSE %s did not take the licence text' % d.path)
        done.append(d.path)
    return done


def Stamp(comp, notices, annotate_type):
    """Place `notices` as annotations in `comp`'s network, above everything
    in it, left-aligned with it, and give every MIT-template LICENSE DAT in it
    the first notice's text (RewriteLicenseDats). Idempotent: notes from an
    earlier stamp are replaced. Reads each one back and raises when TD did
    not keep the text, so a silent failure cannot ship an unlicensed or
    mislicensed artifact. Returns the annotation names."""
    for old in comp.findChildren(name=NOTE_PREFIX + '*', maxDepth=1, includeUtility=True):
        old.destroy()
    kids = comp.findChildren(maxDepth=1, includeUtility=True)
    left = min([int(c.nodeX) for c in kids] or [0])
    y = max([int(c.nodeY + c.nodeHeight) for c in kids] or [0]) + 2 * NOTE_GAP
    made = []
    for n in notices:
        a = comp.create(annotate_type)
        # TD ignores a name given at create time for an annotation
        a.name = n['name']
        a.utility = True
        a.par.Mode = 'annotate'
        a.par.Titletext = n['title']
        a.par.Bodytext = n['body']
        a.nodeWidth = NOTE_WIDTH
        a.nodeHeight = NOTE_PAD + LINE_HEIGHT * (n['body'].count('\n') + 1)
        a.nodeX = left
        a.nodeY = y
        y += int(a.nodeHeight) + NOTE_GAP
        made.append(a.name)
    for n in notices:
        hit = comp.findChildren(name=n['name'], maxDepth=1, includeUtility=True)
        if len(hit) != 1 or str(hit[0].par.Bodytext.eval()) != n['body'] \
                or str(hit[0].par.Titletext.eval()) != n['title']:
            raise RuntimeError('licence notice %s did not stamp onto %s'
                               % (n['name'], comp.path))
    if notices:
        RewriteLicenseDats(comp, notices[0])
    return made
