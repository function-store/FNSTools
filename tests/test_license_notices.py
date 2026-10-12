"""Every shipped artifact carries its licence (docs/LicenseNotices.md).

Free packages carry the repo's MIT licence in full; anything not free carries
the Patreon licence; a package with catalog `third_party` entries also carries
the full text of each notice it owes. The release step stamps them onto the
ARTIFACT copy as annotations (build_manifest.ScrubArtifact, and the bootstrap
in build_installer.BuildBootstrap), never the live master.

Runs outside TouchDesigner: license_notices.py is plain Python, and Stamp()
is exercised on small fakes.

    python tests/test_license_notices.py
"""
import fnmatch
import importlib.util
import io
import json
import os
import re
import types

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(label, cond, detail=''):
    if cond:
        print('  PASS  %s' % label)
    else:
        FAILS.append(label)
        print('  FAIL  %s   %s' % (label, detail))


def read(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8').read()


spec = importlib.util.spec_from_file_location(
    'license_notices', os.path.join(_ROOT, 'packaging', 'license_notices.py'))
ln = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ln)

catalog = json.loads(read('packaging', 'catalog.json'))['packages']
LICENSE = read('LICENSE').strip('\n')

# ------------------------------------------------------------------ 1
print('1. free packages carry the MIT licence, in full')
free = ln.Notices('free', None, _ROOT, year=2027)
check('one notice, ours', len(free) == 1 and free[0]['name'] == ln.NOTE_PREFIX)
check('titled MIT', free[0]['title'] == ln.MIT_TITLE)
body = free[0]['body']
check('the copyright line is derived for the release year',
      'Copyright (c) 2023-2027 Daniel Molnar / Function Store\n' + ln.SITE in body)
check('everything else is the repo LICENSE, word for word',
      ln.COPYRIGHT_RE.sub('', LICENSE) == ln.COPYRIGHT_RE.sub('', body).replace('\n' + ln.SITE, '', 1))
check('MIT\'s condition is there (the notice travels with every copy)',
      'shall be included in all\ncopies or substantial portions of the Software.' in body)

# ------------------------------------------------------------------ 2
print('2. anything not free carries the Patreon licence')
for access in ('8323905', '8291595', 'preview', 'patreon', '', None):
    n = ln.Notices(access, None, _ROOT, year=2027)[0]
    check('access %r is not MIT' % (access,),
          n['title'] == ln.GATED_TITLE and 'Permission is hereby granted' not in n['body'])
gated = ln.Notices('8323905', None, _ROOT, year=2027)[0]['body']
check('it names the holder and the year', gated.startswith(
    'Copyright (c) 2023-2027 Daniel Molnar / Function Store. All rights reserved.'))
check('it forbids derived tools, templates and packs', 'networks, code or shaders' in gated
      and 'plugin, library, template or project pack' in gated)
check('it never forbids handing on a project outright (client deliveries are allowed)',
      'anything you hand on' not in gated)
check('it allows client deliveries', 'client\nor venue a project that uses it' in gated)
check('it points at the full terms', gated.rstrip().endswith(ln.TERMS))
check('every catalog access value that is not free reads as gated',
      all(ln.isFree(m.get('access', 'free')) == (str(m.get('access', 'free')) == 'free')
          for m in catalog.values()))

# ------------------------------------------------------------------ 3
print('3. third-party notices: the catalog entries and their texts')
owed = {n: m['third_party'] for n, m in catalog.items() if 'third_party' in m}
check('SearchPalette and the operator family declare what they owe',
      set(owed) >= {'FNS_SearchPalette', 'FNS_OpFamily'}, sorted(owed))
for name, entries in sorted(owed.items()):
    check('%s: the entries are well formed and the files exist' % name,
          not ln.thirdPartyProblems(entries, _ROOT),
          ln.thirdPartyProblems(entries, _ROOT))
    check('%s is ours, not a foreign package' % name,
          not isinstance(catalog[name].get('source'), dict))
sp = ln.Notices('free', owed['FNS_SearchPalette'], _ROOT)
check('SearchPalette ships MIT plus Yea Chen\'s notice',
      len(sp) == 2 and 'Copyright (c) 2020 Yea chen' in sp[1]['body']
      and sp[1]['title'] == 'Third party: TD-SearchPalette by Yea Chen (MIT)')
fam = ln.Notices('free', owed['FNS_OpFamily'], _ROOT)
check('the operator family ships the TDFam NOTICE and the full Apache licence',
      len(fam) == 3 and 'preserve the Apache-2.0' in fam[1]['body']
      and 'END OF TERMS AND CONDITIONS' in fam[2]['body'])
check('every notice name is unique', len({n['name'] for n in fam}) == 3)
notices_md = read('THIRD_PARTY_NOTICES.md')
for entries in owed.values():
    for e in entries:
        for rel in e['files']:
            check('%s matches THIRD_PARTY_NOTICES.md word for word' % rel,
                  read(rel).strip('\n') in notices_md)
check('a broken entry is refused, not shipped half-licensed',
      ln.thirdPartyProblems([{'name': 'X', 'license': 'MIT', 'files': ['nope.txt']}], _ROOT)
      and ln.thirdPartyProblems('x', _ROOT) and ln.thirdPartyProblems([{}], _ROOT))
try:
    ln.Notices('free', [{'name': 'X'}], _ROOT)
    raised = False
except ValueError:
    raised = True
check('Notices raises on a broken entry (the export then fails)', raised)


# ------------------------------------------------------------------ 4
print('4. Stamp places annotations on the copy and reads them back')


class Par(object):
    def __init__(self, v=''):
        self.val = v

    def eval(self):
        return self.val


class Pars(object):
    def __init__(self, keep=True):
        object.__setattr__(self, '_p', {})
        object.__setattr__(self, '_keep', keep)

    def __getattr__(self, k):
        return self._p.setdefault(k, Par())

    def __setattr__(self, k, v):
        self._p.setdefault(k, Par()).val = v if self._keep else ''


class Node(object):
    def __init__(self, parent, name, x=0, y=0, w=100, h=100, keep=True):
        self.parent, self.name = parent, name
        self.nodeX, self.nodeY, self.nodeWidth, self.nodeHeight = x, y, w, h
        self.utility = False
        self.par = Pars(keep)
        self.path = '/comp/' + name

    def destroy(self):
        self.parent.kids.remove(self)


class Comp(object):
    path = '/comp'

    def __init__(self, keep=True):
        self.kids = []
        self.keep = keep

    def create(self, kind):
        n = Node(self, 'annotate%d' % (len(self.kids) + 1), keep=self.keep)
        self.kids.append(n)
        return n

    def findChildren(self, name='*', maxDepth=1, includeUtility=False):
        return [k for k in self.kids if fnmatch.fnmatchcase(k.name, name)
                and (includeUtility or not k.utility)]


class TextDat(Node):
    """A LICENSE DAT; `nested` stands for one deeper in the network (the
    fake's findChildren is flat, as TD's is with no depth given)."""
    def __init__(self, parent, text, keep=True):
        Node.__init__(self, parent, 'LICENSE')
        self._text, self._keep = text, keep

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, v):
        if self._keep:
            self._text = v


c = Comp()
c.kids.append(Node(c, 'base1', x=-300, y=0, w=200, h=150))
c.kids.append(Node(c, 'null1', x=200, y=-400))
made = ln.Stamp(c, fam, 'annotateCOMP')
notes = [k for k in c.kids if k.name.startswith(ln.NOTE_PREFIX)]
check('one annotation per notice, named for it', made == [n['name'] for n in fam])
check('utility, so a tool\'s own findChildren walks never see them',
      all(k.utility for k in notes) and not [k for k in c.findChildren() if k in notes])
check('mode annotate, title and body as derived',
      all(k.par.Mode.eval() == 'annotate' for k in notes)
      and notes[0].par.Bodytext.eval() == fam[0]['body'])
check('left-aligned with the network and above all of it',
      all(k.nodeX == -300 for k in notes) and min(k.nodeY for k in notes) > 150)
check('stacked without overlapping', all(
    notes[i].nodeY + notes[i].nodeHeight < notes[i + 1].nodeY for i in range(len(notes) - 1)))
check('sized for the text', notes[2].nodeHeight >= 22 * fam[2]['body'].count('\n'))
ln.Stamp(c, free, 'annotateCOMP')
check('re-stamping replaces earlier notes, never stacks them',
      [k.name for k in c.kids if k.name.startswith(ln.NOTE_PREFIX)] == [ln.NOTE_PREFIX]
      and len(c.kids) == 3)
try:
    ln.Stamp(Comp(keep=False), free, 'annotateCOMP')
    raised = False
except RuntimeError:
    raised = True
check('a stamp that did not keep its text raises (no unlicensed artifact)', raised)

print('4b. MIT-template LICENSE DATs take the package\'s own licence')
MIT_DAT = 'Copyright 2025 Daniel Molnar / Function Store\n\n' + ln.MIT_MARK + ', to any person ...'
TDFAM = 'TDFam\n\nCopyright 2025-2026 Lyell Hintz, Dan Molnar ... Apache License, Version 2.0.'
OWN = 'SimpleSceneChanger (Base and Pro)\nCopyright 2025-2026 Daniel Molnar / Function Store. All rights reserved.'
gnot = ln.Notices('8323905', None, _ROOT, year=2027)
g = Comp()
dats = [TextDat(g, MIT_DAT), TextDat(g, MIT_DAT), TextDat(g, TDFAM), TextDat(g, OWN)]
g.kids.extend(dats)
ln.Stamp(g, gnot, 'annotateCOMP')
check('a gated artifact\'s MIT LICENSE DATs carry the Patreon licence, under its title',
      dats[0].text == dats[1].text == ln.GATED_TITLE + '\n\n' + gnot[0]['body']
      and ln.MIT_MARK not in dats[0].text)
check('a third party\'s notice and a package\'s own licence are left alone',
      dats[2].text == TDFAM and dats[3].text == OWN)
f = Comp()
fdat = TextDat(f, MIT_DAT)
f.kids.append(fdat)
ln.Stamp(f, free, 'annotateCOMP')
check('a free artifact\'s LICENSE DAT carries the release-year MIT text',
      fdat.text == free[0]['body'] and fdat.text.startswith('MIT License'))
h = Comp()
h.kids.append(TextDat(h, MIT_DAT, keep=False))
try:
    ln.Stamp(h, gnot, 'annotateCOMP')
    raised = False
except RuntimeError:
    raised = True
check('a LICENSE DAT that did not take the text raises', raised)

# ------------------------------------------------------------------ 5
print('5. wiring: every artifact passes through the stamp')
bm = read('packaging', 'build_manifest.py')
scrub = bm[bm.index('def ScrubArtifact('):bm.index('def ExportPackage(')]
check('ScrubArtifact stamps the loaded COPY, then saves it',
      "_licenseNotices().Stamp(loaded, notices, annotateCOMP)" in scrub
      and 'if changed or notices' in scrub)
check('ExportPackage hands its notices to the scrub',
      'ScrubArtifact(dest, notices=notices' in bm)
check('the base build is stamped by its own access',
      "Notices(entry['access']," in bm and 'ExportPackage(comp, notices=notices' in bm)
check('a variant build is stamped by the VARIANT\'s access (ColorGen.pro is not MIT)',
      "vrow['access'], meta.get('third_party')" in bm and 'notices=vnotices' in bm)
check('the catalog check refuses a broken third_party',
      'thirdPartyProblems(meta.get(\'third_party\')' in bm)
bi = read('packaging', 'build_installer.py')
boot = bi[bi.index('def BuildBootstrap('):]
check('the bootstrap is stamped MIT before it is exported',
      boot.index('ln.Stamp(root, ln.Notices(ln.FREE') < boot.index('info = _export(root'))

print()
if FAILS:
    print('%d check(s) failed:' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all licence-notice checks pass')
