"""Offline test of ExtUpdater's kept-children carry (KEEP_TAG).

Runs outside TouchDesigner: the module is loaded with the TD builtins it
touches stubbed, and the operators are small fakes that copy, destroy and
store like COMPs do. It covers the bookkeeping a live run cannot easily
force -- an extension-bearing kept child, a holder that must outlive a
failed put-back, a reload that did nothing -- and that every path either
puts the held children in or leaves the holder and says where it is.

The live check (both rails on FNS_RadialMenu) is in docs/UpdaterHardening.md.

Run it from anywhere:

    python tests/test_updater_carry.py
"""
import builtins
import itertools
import os
import sys
import types

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    _ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Updater', 'ExtUpdater.py')

_IDS = itertools.count(100)
_OPS = {}


class Node:
    """Enough of an OP for the carry: children, tags, copy, destroy, store."""

    def __init__(self, name, tags=(), comp=True, ext=False, kids=()):
        self.name = name
        self.tags = set(tags)
        self.isCOMP = comp
        self.ext = ext
        self.id = next(_IDS)
        self.nodeX = self.nodeY = 0
        self.allowCooking = True
        self.valid = True
        self.storage = {}
        self.parentNode = None
        self._kids = []
        for k in kids:
            self._adopt(k)

    def _adopt(self, k):
        k.parentNode = self
        self._kids.append(k)
        return k

    @property
    def path(self):
        return (self.parentNode.path if self.parentNode else '') + '/' + self.name

    @property
    def children(self):
        return list(self._kids)

    def findChildren(self):
        out = []
        for k in self._kids:
            out.append(k)
            out.extend(k.findChildren())
        return out

    def pars(self, pattern):
        assert pattern == 'ext*object', pattern
        return [types.SimpleNamespace(expr='', val="op('./X').module.X(me)")] if self.ext else []

    def op(self, name):
        return next((k for k in self._kids if k.name == name), None)

    def clone(self, name=None):
        n = Node(name or self.name, self.tags, self.isCOMP, self.ext,
                 [k.clone() for k in self._kids])
        n.nodeX, n.nodeY = self.nodeX, self.nodeY
        n.storage = dict(self.storage)
        return n

    def copy(self, other, name=None):
        if name and self.op(name) is not None:
            raise RuntimeError('name taken: %s' % name)
        return self._adopt(other.clone(name))

    def create(self, typ, name):
        return self._adopt(Node(name))

    def destroy(self):
        self.parentNode._kids.remove(self)
        self.valid = False

    def store(self, key, value):
        self.storage[key] = value

    def errors(self, recurse=True):
        return ''


_RUNS = []
builtins.op = lambda p=None: _OPS.get(p)
builtins.op.TDResources = None
builtins.debug = lambda *a, **k: None
builtins.run = lambda *a, **k: _RUNS.append((a, k))
builtins.baseCOMP = 'baseCOMP'
builtins.ui = types.SimpleNamespace(messageBox=lambda *a, **k: None)
builtins.project = types.SimpleNamespace(name='test')


def _fake_fns_command(fn=None, **kw):
    if fn is not None:
        return fn
    return lambda f: f


_fake_mod = types.SimpleNamespace(fns_command=_fake_fns_command,
                                  fns_announce=lambda comp: None)
_fake_extutils = types.SimpleNamespace(tags={'ExtUtils'}, mod=lambda name: _fake_mod)
builtins.me = types.SimpleNamespace(docked=[_fake_extutils])
builtins.tdu = types.SimpleNamespace()

src = open(SRC, encoding='utf-8').read()
mod = types.ModuleType('ExtUpdater')
mod.__dict__['__file__'] = SRC
exec(compile(src, SRC, 'exec'), mod.__dict__)
KEEP, MARK = mod.KEEP_TAG, mod.CARRY_MARK

FAILS = []


def check(label, cond, detail=''):
    print('  %s  %s %s' % ('PASS' if cond else 'FAIL', label, '' if cond else detail))
    if not cond:
        FAILS.append(label)


def fresh_updater():
    ext = mod.ExtUpdater.__new__(mod.ExtUpdater)
    ext.ownerComp = Node('FNS_Updater', kids=[Node('some_dat', comp=False)])
    return ext


def radial(label):
    """A package with a kept wheels COMP holding one wheel, one plain child,
    and a kept child that runs an extension somewhere inside it."""
    wheel = Node('Wheel_2', tags={'fns_radialmenu_wheel'})
    wheel.storage['label'] = label
    wheels = Node('wheels', tags={KEEP}, kids=[wheel])
    wheels.nodeX, wheels.nodeY = 2000, -1600
    extkid = Node('helper', tags={KEEP}, kids=[Node('inner', ext=True)])
    pkg = Node('FNS_RadialMenu', kids=[wheels, Node('wheel_master'), extkid])
    Node('FNSTools')._adopt(pkg)
    return pkg


def held_label(pkg):
    w = pkg.op('wheels')
    w2 = w.op('Wheel_2') if w else None
    return w2.storage.get('label') if w2 else None


print('1. nothing tagged -> no holder, no refusal')
ext = fresh_updater()
holder, carried, refused, why = ext._carryOut(Node('P', kids=[Node('a')]), 'P')
check('no holder', holder is None)
check('nothing carried or refused', carried == [] and refused == [] and why == '')
check('updater untouched', [c.name for c in ext.ownerComp.children] == ['some_dat'])

print('2. carry out: kept child held cooking-off, extension-bearing one refused')
ext = fresh_updater()
old = radial('live')
holder, carried, refused, why = ext._carryOut(old, 'FNS_RadialMenu')
check('holder inside the updater', holder is not None and holder.parentNode is ext.ownerComp)
check('holder does not cook', holder is not None and holder.allowCooking is False)
check('carried names + position', carried == [['wheels', 2000, -1600]], repr(carried))
check('extension-bearing kept child refused', refused == ['helper'], repr(refused))
check('no refusal of the replace', why == '')
check('holder holds the wheel', holder.op('wheels').op('Wheel_2') is not None)

print('3. embedded: carry into the NEW copy, in place of its shipped child')
new = radial('shipped')
new.op('wheels').nodeX, new.op('wheels').nodeY = 400, 400
res = {}
note = ext._settleCarry(new, {'holder': holder.name, 'children': carried}, res)
check('no note', note == '', repr(note))
check('live wheel won over shipped', held_label(new) == 'live', repr(held_label(new)))
check('at the new copy\'s position', (new.op('wheels').nodeX, new.op('wheels').nodeY) == (400, 400))
check('one wheels COMP only', [c.name for c in new.children].count('wheels') == 1)
check('marked with this process id', new.op('wheels').storage.get(MARK) == os.getpid())
check('the mark is set to expire', any(
    a[1] is new.op('wheels') and a[2] == MARK and k.get('delayFrames') == mod.CARRY_MARK_FRAMES
    for a, k in _RUNS), repr(_RUNS))
check('result names it', res.get('carried') == ['wheels'])
check('holder removed', not holder.valid and ext.ownerComp.op(holder.name) is None)

print('4. a second carry while a holder exists gets its own name')
ext = fresh_updater()
h1, c1, _, _ = ext._carryOut(radial('a'), 'FNS_RadialMenu')
h2, c2, _, _ = ext._carryOut(radial('b'), 'FNS_RadialMenu')
check('distinct holders', h1.name != h2.name, '%s %s' % (h1.name, h2.name))

print('5. package gone -> holder kept, the note says where')
ext = fresh_updater()
holder, carried, _, _ = ext._carryOut(radial('live'), 'FNS_RadialMenu')
note = ext._settleCarry(None, {'holder': holder.name, 'children': carried})
check('holder kept', holder.valid)
check('note names the holder', holder.path in note, repr(note))

print('6. a put-back that fails keeps the holder and fails loud')
ext = fresh_updater()
holder, carried, _, _ = ext._carryOut(radial('live'), 'FNS_RadialMenu')
holder.op('wheels').destroy()            # the held copy is somehow gone
note = ext._settleCarry(radial('shipped'), {'holder': holder.name, 'children': carried})
check('holder kept', holder.valid)
check('note names the child and the holder',
      'wheels' in note and holder.path in note, repr(note))

print('7. bound rail: the carry lands when the reload is judged')
ext = fresh_updater()
pkg = radial('live')
holder, carried, _, _ = ext._carryOut(pkg, 'FNS_RadialMenu')
token = sorted(c.id for c in pkg.children)
for c in pkg.children:                    # the reload recreates every child
    c.destroy()
for c in radial('shipped').children:
    pkg._adopt(c.clone())
_OPS.clear()
_OPS[pkg.path] = pkg
job = {'results': [{'package': 'FNS_RadialMenu', 'ok': True, 'verify': pkg.path,
                    'reload_token': token,
                    'carry': {'holder': holder.name, 'children': carried}}]}
ext._settleVerifications(job)
r = job['results'][0]
check('still ok', r['ok'] is True, repr(r))
check('live wheel back', held_label(pkg) == 'live', repr(held_label(pkg)))
check('carry bookkeeping cleared', 'carry' not in r and r.get('carried') == ['wheels'])
check('holder removed', not holder.valid)

print('8. bound rail: a reload that did nothing drops the holder, children untouched')
ext = fresh_updater()
pkg = radial('live')
holder, carried, _, _ = ext._carryOut(pkg, 'FNS_RadialMenu')
_OPS.clear()
_OPS[pkg.path] = pkg
job = {'results': [{'package': 'FNS_RadialMenu', 'ok': True, 'verify': pkg.path,
                    'reload_token': sorted(c.id for c in pkg.children),
                    'carry': {'holder': holder.name, 'children': carried}}]}
ext._settleVerifications(job)            # tick 1: looks again
check('holder kept while still judging', holder.valid)
ext._settleVerifications(job)            # tick 2: called a no-op
check('marked not ok', job['results'][0]['ok'] is False)
check('holder dropped', not holder.valid)
check('the original wheel untouched', held_label(pkg) == 'live')

print('9. bound rail: package gone after reload keeps the holder')
ext = fresh_updater()
holder, carried, _, _ = ext._carryOut(radial('live'), 'FNS_RadialMenu')
_OPS.clear()
job = {'results': [{'package': 'FNS_RadialMenu', 'ok': True, 'verify': '/gone',
                    'reload_token': [1],
                    'carry': {'holder': holder.name, 'children': carried}}]}
ext._settleVerifications(job)
r = job['results'][0]
check('fails', r['ok'] is False)
check('why names the holder', holder.path in r['why'], repr(r['why']))
check('holder kept', holder.valid)

print()
if FAILS:
    print('FAILED: %d check(s)' % len(FAILS))
    sys.exit(1)
print('all checks passed')
