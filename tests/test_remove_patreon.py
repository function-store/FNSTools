"""Remove Patreon Tools on the toolkit root.

A .toe handed on carries every package embedded in it, and the Patreon
licence does not let those be redistributed. The root's Remove Patreon Tools
pulse takes them out: the first press lists, a second within the window
removes (no blocking dialog). This runs outside TouchDesigner:

  1. the GENERATED handler (build_installer.ROOT_PULSE_TEXT) with fakes,
     for the two-press arm;
  2. InstallerExt's detection helpers (LicensedAccess, FindLicensedCopies)
     against fake COMPs;
  3. the source contracts the fakes cannot reach.

    python tests/test_remove_patreon.py
"""
import io
import os
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(_ROOT, 'packaging', 'build_installer.py')
INST = os.path.join(_ROOT, 'packaging', 'InstallerExt.py')
NOTICES = os.path.join(_ROOT, 'packaging', 'license_notices.py')
FAILS = []


def check(label, cond, detail=''):
    if cond:
        print('  PASS  %s' % label)
    else:
        FAILS.append(label)
        print('  FAIL  %s   %s' % (label, detail))


gen = {'__name__': 'build_installer_under_test'}
exec(compile(io.open(GEN, encoding='utf-8').read(), GEN, 'exec'), gen)
TEXT = gen['ROOT_PULSE_TEXT']
inst_src = io.open(INST, encoding='utf-8').read()
gen_src = io.open(GEN, encoding='utf-8').read()

print('1. the root pulse')
names = [n for n, _, _ in gen['ROOT_PROJECT_PULSES']]
check('Remove Patreon Tools is a root pulse', names == ['Removepatreon'], names)
check('it is not one of the entry points',
      'Removepatreon' not in [n for n, _, _ in gen['ROOT_ENTRY_POINTS']])
check('the forwarder hears it',
      "pe.par.pars = ' '.join(n for n, _, _ in ROOT_ENTRY_POINTS + ROOT_PROJECT_TOGGLES\n"
      "                           + ROOT_PROJECT_PULSES)" in gen_src)
check('it opens its own section on the page',
      'par.startSection = i == 0' in gen_src)
help_text = gen['ROOT_PROJECT_PULSES'][0][2]
check('its help says two presses, a copy first, and that a client hand-off needs none of it',
      'press again within 10 seconds' in help_text and 'Save a' in help_text
      and 'client' in help_text)
check('the window in the help is the window in the handler',
      gen['REMOVE_PATREON_WINDOW'] == 10)


class _Installer:
    def __init__(self, dry):
        self.dry = dry
        self.calls = []

    def RemovePatreon(self, confirm=False):
        self.calls.append(confirm)
        return self.dry


class _Root:
    def __init__(self, installer):
        self._inst = installer

    def op(self, name):
        return self._inst if name == gen['COMP_NAME'] else None


def handler(installer):
    """A fresh module of the generated forwarder, with the run() calls kept."""
    runs, out = [], []
    g = {'op': type('O', (), {'TDResources': None})(),
         'parent': lambda: _Root(installer),
         'debug': lambda *a: out.append(' '.join(str(x) for x in a)),
         'print': lambda *a: out.append(' '.join(str(x) for x in a)),
         'run': lambda *a, **k: runs.append((a, k))}
    exec(compile(TEXT, 'ROOT_PULSE_TEXT', 'exec'), g)
    pulse = lambda: g['onPulse'](type('Par', (), {'name': 'Removepatreon'})())
    return pulse, runs, out


DRY = {'ok': True, 'would_remove': ['/FNSTools/ComplexOp', '/project1/complexop1'],
       'forgotten': ['SeqMod'], 'kept': [], 'notes': []}

print('2. the two presses')
inst = _Installer(DRY)
pulse, runs, out = handler(inst)
pulse()
check('the first press only asks what would happen', inst.calls == [False], inst.calls)
check('and removes nothing', runs == [], runs)
check('it lists every copy and the record it would forget',
      any('/FNSTools/ComplexOp' in l for l in out)
      and any('/project1/complexop1' in l for l in out)
      and any('SeqMod' in l for l in out), out)
check('and says how to go on', any('again within 10 seconds' in l for l in out), out)
pulse()
check('the second press removes, deferred out of the callback',
      len(runs) == 1 and 'reportPatreonRemoval()' in runs[0][0][0]
      and runs[0][1].get('delayFrames') == 1, runs)
check('and does not ask again', inst.calls == [False], inst.calls)
pulse()
check('a third press starts over with a fresh list', inst.calls == [False, False]
      and len(runs) == 1, (inst.calls, runs))

print('3. the window')
inst = _Installer(DRY)
pulse, runs, out = handler(inst)
real = time.time
try:
    t = [1000.0]
    time.time = lambda: t[0]
    pulse()
    t[0] += 11
    pulse()
finally:
    time.time = real
check('a second press after the window lists again instead of removing',
      runs == [] and inst.calls == [False, False], (runs, inst.calls))

print('4. nothing to remove, refused, no installer')
inst = _Installer({'ok': True, 'would_remove': [], 'forgotten': [], 'kept': [], 'notes': []})
pulse, runs, out = handler(inst)
pulse()
pulse()
check('nothing found never arms', runs == [] and inst.calls == [False, False], runs)
check('and says so', any('no Patreon tools' in l for l in out), out)
inst = _Installer({'ok': False, 'why': 'the toolkit SOURCE root'})
pulse, runs, out = handler(inst)
pulse()
pulse()
check('a refusal never arms and gives its reason',
      runs == [] and any('SOURCE root' in l for l in out), out)
pulse, runs, out = handler(None)
pulse()
check('a root without an installer reports, never raises',
      any('no installer' in l for l in out), out)

print('5. what counts as a Patreon copy')
block = inst_src[inst_src.index('# --- Patreon-licensed copies'):inst_src.index('def ExposeConsoleHosts')]
det = {}
exec(compile(block, 'licensed', 'exec'), det)
notices = {}
exec(compile(io.open(NOTICES, encoding='utf-8').read(), NOTICES, 'exec'), notices)
check('the licence title matches the one the release stamps',
      det['PATREON_LICENCE_TITLE'] == notices['GATED_TITLE']
      and det['LICENCE_NOTE_PREFIX'] == notices['NOTE_PREFIX'])


class _Val:
    def __init__(self, v):
        self.v = v

    def eval(self):
        return self.v


class _Pars:
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, _Val(v))


class _Comp:
    def __init__(self, path, family='COMP', kids=(), notes=(), about=None, **pars):
        self.path = path
        self.name = path.rsplit('/', 1)[-1]
        self.family = family
        self.children = list(kids)
        self._notes = list(notes)
        self._about = about
        self.par = _Pars(**pars)

    def op(self, name):
        return self._about if name == 'FNS_About' else None

    def findChildren(self, name='', maxDepth=None, includeUtility=False):
        return [n for n in self._notes if n.name.startswith(name.rstrip('*'))]


def note(title):
    n = _Comp('/x/fns_license_patreon')
    n.par = _Pars(Titletext=title)
    return n


def about(**pars):
    return _Comp('/x/FNS_About', **pars)


INDEX = {
    'ComplexOp': {'name': 'ComplexOp', 'access': '8323905'},
    'ColorGen': {'name': 'ColorGen', 'access': 'free',
                 'variants': {'pro': {'access': '8323905'}}},
    'Preview': {'name': 'Preview', 'access': 'preview'},
    'AltSelect': {'name': 'FNS_AltSelect', 'access': 'free'},
    'TDXMap': {'name': 'TDXMap', 'access': '8323905', 'foreign': True},
}
LA = det['LicensedAccess']
check('a gated package is Patreon',
      LA(_Comp('/r/ComplexOp', about=about(Pkgname='ComplexOp')), INDEX) is not None)
check('a preview package is Patreon too (anything not free)',
      LA(_Comp('/r/Preview', about=about(Pkgname='Preview')), INDEX) is not None)
check('a free package is not',
      LA(_Comp('/r/AltSelect', about=about(Pkgname='AltSelect')), INDEX) is None)
check('the Pro build of a free package is',
      LA(_Comp('/r/ColorGen', about=about(Pkgname='ColorGen', Pkgvariant='pro')), INDEX)
      is not None)
check('its Base build is not',
      LA(_Comp('/r/ColorGen', about=about(Pkgname='ColorGen')), INDEX) is None)
check('a foreign package is not ours to licence',
      LA(_Comp('/r/TDXMap', about=about(Pkgname='TDXMap')), INDEX) is None)
check('the licence note answers offline, with no manifest',
      LA(_Comp('/n/anything', notes=[note(notices['GATED_TITLE'])], Pkgname='X'), {})
      is not None)
check('an MIT note does not',
      LA(_Comp('/n/anything', notes=[note(notices['MIT_TITLE'])], Pkgname='X'), {}) is None)
check('a COMP name stands in for Pkgname only when asked (the toolkit\'s own children)',
      LA(_Comp('/r/ComplexOp'), INDEX, by_name=True) is not None
      and LA(_Comp('/user/ComplexOp'), INDEX) is None)

print('6. where copies are found')
nested = _Comp('/p/show/ComplexOp_inner', about=about(Pkgname='ComplexOp'))
placed_free = _Comp('/p/show/scene', about=about(Pkgname='AltSelect'), kids=[nested])
placed = _Comp('/p/show/complexop1', about=about(Pkgname='ComplexOp'))
show = _Comp('/p/show', kids=[placed, placed_free, _Comp('/p/show/null1', family='CHOP')])
root = _Comp('/FNSTools', kids=[
    _Comp('/FNSTools/ComplexOp', about=about(Pkgversion='1.0.0')),
    _Comp('/FNSTools/AltSelect', about=about(Pkgname='AltSelect'))])
sysc = _Comp('/sys/hidden', about=about(Pkgname='ComplexOp'))
top = _Comp('/', kids=[root, _Comp('/p', kids=[show]), _Comp('/sys', kids=[sysc])])
toolkit, elsewhere = det['FindLicensedCopies'](root, INDEX, top)
check('the toolkit\'s Patreon child is found, its free one is not',
      [c.path for c, _ in toolkit] == ['/FNSTools/ComplexOp'], [c.path for c, _ in toolkit])
check('a copy placed in the user\'s network is found',
      [c.path for c, _ in elsewhere] == ['/p/show/complexop1'], [c.path for c, _ in elsewhere])
check('nothing inside another package is (it ships under that package\'s licence)',
      '/p/show/ComplexOp_inner' not in [c.path for c, _ in elsewhere])
check('/sys is never searched', '/sys/hidden' not in [c.path for c, _ in elsewhere])
check('the toolkit is not searched twice',
      all(not c.path.startswith('/FNSTools') for c, _ in elsewhere))

print('7. the removal')
rp = inst_src[inst_src.index('    def RemovePatreon(self'):inst_src.index('    def reportPatreonRemoval(self')]
check('dry run by default', 'def RemovePatreon(self, confirm=False):' in rp
      and rp.index('if not confirm:') < rp.index('RemoveTools('))
check('the dev source root refuses, like every install and removal',
      rp.index('locked = SourceLock(root.path)') < rp.index('FindLicensedCopies('))
check('installed tools leave through RemoveTools (record, project files, families)',
      "'to_remove': [c.name for c, _ in toolkit]" in rp)
check('placed copies release their families before they go',
      '_releaseFamilies(c)' in rp and rp.index('_releaseFamilies(c)') < rp.index('c.destroy()'))
check('Embody-authored copies are listed, never touched',
      'kept = [c.path for c, _ in elsewhere if _embodyRows(c.path)]' in rp)
check('the install record forgets every Patreon package left in it',
      'rec_t.deleteRow(i)' in rp and 'not p.get(\'foreign\')' in rp)
check('it never raises', rp.rstrip().endswith("% str(e)[:200]}"))

print()
if FAILS:
    print('%d check(s) failed:' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all remove-patreon checks pass')
