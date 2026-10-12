"""A standalone copy of a global tool is found and taken over (docs/StandaloneTakeover.md).

A global tool exists once per project: it lands in the toolkit, is no FNS
family member and is not core. The release stamps every artifact with
FNS_About.Pkgname and every global tool with the `<FNS:GLOBAL>` tag
(packaging/package_identity.py, via build_manifest.ScrubArtifact); the
updater finds copies outside the toolkit by that stamp, or by COMP name or
Global OP Shortcut for copies that predate it (FindStandalone), and brings
one under the toolkit on request (TakeOver).

Runs outside TouchDesigner: package_identity.py is plain Python, the
updater's rules are checked on its source, and the stamp runs on fakes.

    python tests/test_standalone_takeover.py
"""
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
    'package_identity', os.path.join(_ROOT, 'packaging', 'package_identity.py'))
pid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pid)

upd = read('modules', 'suspects', 'FNSTools', 'FNS_Updater', 'ExtUpdater.py')
bm = read('packaging', 'build_manifest.py')
man = json.loads(read('packaging', 'manifest.json'))['packages']

# ------------------------------------------------------------------ 1
print('1. which packages are global')
glob = [p['name'] for p in man if pid.IsGlobal(p.get('placement'), p.get('family'), p.get('kind'))]
check('the published manifest has global tools (48 at v3.2.67)', len(glob) > 0, len(glob))
check('no FNS family member is global',
      not [p['name'] for p in man if p.get('family') and p['name'] in glob])
check('no core package is global',
      not [p['name'] for p in man if p.get('kind') == 'core' and p['name'] in glob])
check('only toolkit placement is global',
      all((p.get('placement') or 'toolkit') == 'toolkit' for p in man if p['name'] in glob))
check('a shortcut is not required (15 of the 48 have none at v3.2.67)',
      [n for n in glob if not next(p for p in man if p['name'] == n).get('shortcut')])

# ------------------------------------------------------------------ 2
print('2. the updater reads the same identity the release stamps')
m = re.search(r"^GLOBAL_TAG = '([^']+)'$", upd, re.M)
check('the tag is TDFam-style and identical on both sides',
      m and m.group(1) == pid.GLOBAL_TAG == '<FNS:GLOBAL>', m and m.group(1))
check('both read Pkgname, FNS_About first',
      "for host in (comp.op('FNS_About'), comp):" in upd
      and "getattr(host.par, 'Pkgname', None)" in upd and pid.NAME_PAR == 'Pkgname')
body = upd[upd.index('def _isGlobal('):upd.index('def _isPackageRoot(')]
check('the updater\'s global rule matches IsGlobal (toolkit, not family, not core)',
      "(pkg.get('placement') or 'toolkit') == 'toolkit'" in body
      and "not pkg.get('family')" in body and "!= 'core'" in body)


# ------------------------------------------------------------------ 3
print('3. the stamp on an artifact copy')


class Par(object):
    def __init__(self):
        self.val, self.expr, self.readOnly, self.help = '', '', False, ''

    def eval(self):
        return self.val


class Page(object):
    def __init__(self, owner, name):
        self.owner, self.name = owner, name

    def appendStr(self, name, label=''):
        p = Par()
        setattr(self.owner.par, name, p)
        return [p]


class Comp(object):
    def __init__(self, name, about=True):
        self.name, self.path = name, '/x/' + name
        self.nodeX = self.nodeY = 0
        self.tags = set()
        self.par = types.SimpleNamespace()
        self.customPages = []
        self.kids = {}
        if about:
            self.kids['FNS_About'] = Comp('FNS_About', about=False)

    def op(self, n):
        return self.kids.get(n)

    def appendCustomPage(self, name):
        pg = Page(self, name)
        self.customPages.append(pg)
        return pg


c = Comp('FNS_CustomParTools')
got = pid.Stamp(c, 'FNS_CustomParTools', True)
about = c.op('FNS_About')
check('Pkgname lands on FNS_About, read-only', about.par.Pkgname.val == 'FNS_CustomParTools'
      and about.par.Pkgname.readOnly)
check('on its own Identity page, never To Deploy (Deploy would mirror it onto the tool)',
      [pg.name for pg in about.customPages] == [pid.IDENTITY_PAGE] != ['To Deploy'])
check('a global tool gets the tag', pid.GLOBAL_TAG in c.tags and got.get('tag') == pid.GLOBAL_TAG)
pid.Stamp(c, 'FNS_CustomParTools', True)
check('stamping twice adds no second page', len(about.customPages) == 1)
f = Comp('ComplexMix')
f.tags.add(pid.GLOBAL_TAG)
pid.Stamp(f, 'ComplexMix', False)
check('a non-global package carries no tag, even one copied in by mistake', pid.GLOBAL_TAG not in f.tags)
check('ReadName answers the stamped name, None when unstamped',
      pid.ReadName(c) == 'FNS_CustomParTools' and pid.ReadName(Comp('X')) is None)


class ParNS(object):
    """`op.par.x = v` sets the parameter's value, as in TD."""
    def __init__(self):
        object.__setattr__(self, '_p', {})

    def __getattr__(self, k):
        return self._p.setdefault(k, Par())

    def __setattr__(self, k, v):
        self._p.setdefault(k, Par()).val = v


class Node(object):
    def __init__(self, owner, name):
        self.owner, self.name, self.text = owner, name, ''
        self.nodeX = self.nodeY = 0
        self.par = ParNS()

    def destroy(self):
        self.owner.kids.pop(self.name, None)


def _create(self, kind, name):
    n = Node(self, name)
    self.kids[name] = n
    return n


Comp.create = _create
Comp.children = property(lambda self: list(self.kids.values()))
g = Comp('FNS_QuickTime')
got = pid.Stamp(g, 'FNS_QuickTime', True, 'executeDAT')
guard = g.op(pid.GUARD)
check('a global tool gets the step-aside guard, Create on',
      guard is not None and got.get('guard') == pid.GUARD and guard.par.create.val is True)
check('the guard names its package and compiles',
      "PACKAGE = 'FNS_QuickTime'" in guard.text and compile(guard.text, 'guard', 'exec'))
check('it only releases the shortcut: never turns cooking off (onCreate would never fire again)',
      'allowCooking' not in pid.GUARD_TEXT.split('KEY =')[1]
      and "comp.par.opshortcut = ''" in pid.GUARD_TEXT)
check('and remembers it, putting it back where no toolkit copy exists',
      'comp.store(KEY' in pid.GUARD_TEXT and 'comp.par.opshortcut = held' in pid.GUARD_TEXT)
check('it reaches the toolkit root only through a guarded getattr (no bare op.FNS)',
      "getattr(op, 'FNS', None)" in pid.GUARD_TEXT
      and not re.search(r"\bop\.FNS\b(?!_)", pid.GUARD_TEXT.replace('(op.FNS)', '')))
check('it clears the stale "Multiply defined" error it leaves behind',
      'comp.clearScriptErrors()' in pid.GUARD_TEXT)
pid.Stamp(g, 'FNS_QuickTime', True, 'executeDAT')
check('restamping replaces the guard', len([k for k in g.kids if k == pid.GUARD]) == 1)
pid.Stamp(g, 'FNS_QuickTime', False, 'executeDAT')
check('a package that is no longer global loses tag and guard',
      g.op(pid.GUARD) is None and pid.GLOBAL_TAG not in g.tags)

# ------------------------------------------------------------------ 4
print('4. the release wiring')
scrub = bm[bm.index('def ScrubArtifact('):bm.index('def ExportPackage(')]
check('ScrubArtifact stamps identity on the loaded copy and saves it',
      '_packageIdentity().Stamp(loaded, identity[0], identity[1], executeDAT)' in scrub
      and 'if changed or notices or identity:' in scrub)
check('ExportPackage passes identity through', 'identity=identity)' in bm)
check('base and variant builds both carry the package name and the global rule',
      bm.count("_packageIdentity().IsGlobal(") == 2
      and "identity = (name, _packageIdentity().IsGlobal(" in bm)

# ------------------------------------------------------------------ 5
print('5. the updater: find, compare, take over')
cmp_ = upd[upd.index('\tdef Compare('):upd.index('\tdef FindStandalone(')]
check('Compare matches Pkgname first, then the COMP name',
      'name = _pkgName(child) or child.name' in cmp_ and 'index.get(child.name)' not in cmp_)
check('Compare reports standalone copies and never queues them as updates',
      "'state': 'standalone'" in cmp_ and 'updates.append(st' not in cmp_)
check('a standalone row never overrides the managed copy\'s variant in the plan',
      "and r.get('state') != 'standalone'}" in upd)
find = upd[upd.index('\tdef FindStandalone('):upd.index('\tdef TakeOver(')]
check('the walk skips the toolkit, /sys, /ui and /local',
      "_SCAN_SKIP = ('/sys', '/ui', '/local')" in upd and 'c.path.startswith(root.path' in find)
check('it never descends into a package (nested copies belong to their tool)',
      'another package\'s insides are its own' in find)
check('a name or shortcut match needs a declared version (a user\'s own COMP is not ours)',
      find.index('elif _isPackageRoot(c):') < find.index("pkg, via = c.name, 'name'"))
take = upd[upd.index('\tdef TakeOver('):upd.index('\tdef ', upd.index('\tdef TakeOver(') + 10)]
check('TakeOver acts only on a path FindStandalone reports',
      "self.FindStandalone(target) if r['path'] == path" in take)
check('a dry run unless confirmed', "if not confirm:\n\t\t\treturn plan" in take)
check('it moves in through backup, destroy, loadTox and restores on failure',
      'self._backupPackage(stray' in take and 'root.loadTox(backup)' in take
      and 'self._restorePackage(home, backup' in take)
check('its backup never overwrites the managed copy\'s update backup',
      "name + '.standalone'" in take)
check('the package name wins after the move', 'new.name = name' in take)
check('the reference search stays in the stray\'s own network (a project-wide '
      'parExpr walk held TD for minutes)',
      "op('/').findChildren(parExpr" not in upd and 'stray.parent().findChildren(' in take)
rep = upd[upd.index('\tdef _replacePackage('):]
check('an update finds a renamed copy by Pkgname and restores the package name',
      "_pkgName(c) == name" in rep and 'new.name = name' in rep)

check('deleting a copy re-registers the toolkit copy\'s hosts (the copy\'s hosts had '
      'taken the toolbar entry over, and its removal left it dangling: measured)',
      "plan['reregistered'] = _reregisterHosts(mine)" in take
      and "h.par.Register.pulse()" in upd[upd.index('def _reregisterHosts('):])
check('the guard points the registry entries home when it steps aside',
      'h.par.Register.pulse()' in pid.GUARD_TEXT
      and pid.GUARD_TEXT.index("comp.par.opshortcut = ''") < pid.GUARD_TEXT.index('h.par.Register.pulse()'))
check('a stamped copy with its tag removed is a kept fork, never found',
      "elif stamped:" in find and find.index("if GLOBAL_TAG in c.tags:") < find.index("elif stamped:"))
check('and its guard stands down too',
      "_managedCopy(comp) if '<FNS:GLOBAL>' in comp.tags else None" in pid.GUARD_TEXT)

# ------------------------------------------------------------------ 6
print('6. the picker never installs a second copy')
inst = read('packaging', 'InstallerExt.py')
plan = inst[inst.index('def InstallPlan('):inst.index('\n    return {', inst.index('def InstallPlan('))]
check('the lookup is the updater\'s own FindStandalone, guarded for an older updater',
      "getattr(upd, 'FindStandalone', None)" in inst)
check('a global tool not yet in the toolkit is refused while a standalone copy exists',
      "and str(step.get('kind') or 'tool') != 'core')" in plan
      and "'action': 'skipped (standalone copy)'" in plan)
check('refused BEFORE anything is loaded', plan.index('skipped (standalone copy)')
      < plan.index('dest.loadTox'))
check('looked up once per pass, and only when a step needs it',
      'standalone = None' in plan and 'if standalone is None:' in plan)
check('the picker\'s result text and the quick-launch install both say where it is',
      "StandaloneSentence(r['name'], r['path'])" in inst
      and "'error': StandaloneSentence(name, held[0]['path'])" in inst)

# ------------------------------------------------------------------ 7
print('7. the notices: guide, llms.txt, README, comment')
guide = read('website', 'content', 'guides', 'working-in-your-project.md')
llms = read('website', 'llms.txt')
boot = read('packaging', 'build_installer.py')
readme = boot[boot.index('BOOTSTRAP_README = """'):boot.index('"""', boot.index('BOOTSTRAP_README = """') + 25)]
for label, text in (('the site guide', guide), ('llms.txt', llms), ('the bootstrap README', readme)):
    check('%s says an update replaces a tool whole' % label, 'replaced whole' in text)
    check('%s gives the fork recipe (remove the tag)' % label, '<FNS:GLOBAL>' in text and 'tag' in text)
check('llms.txt follows the convention: H1, summary blockquote, link sections',
      llms.startswith('# FNSTools\n') and '\n> ' in llms and '\n## Docs\n' in llms)
check('the README points at the guide and llms.txt',
      'working-in-your-project' in readme and 'llms.txt' in readme)
check('house style: no em dashes in the guide or llms.txt', '—' not in guide + llms)
cm = Comp('midiMapper')
cm.comment = 'midiMapper v 1.31  by Alpha Moonbase'
cm.create, cm.kids = _create.__get__(cm), cm.kids
pid.Stamp(cm, 'midiMapper', True)
check('a global tool\'s comment gets the one-line notice first, its own text kept after',
      cm.comment == pid.NOTICE + '\nmidiMapper v 1.31  by Alpha Moonbase')
pid.Stamp(cm, 'midiMapper', True)
check('restamping never repeats the notice', cm.comment.count(pid.NOTICE) == 1)
check('the notice is one line', '\n' not in pid.NOTICE)

print()
if FAILS:
    print('%d check(s) failed:' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all standalone-takeover checks pass')
