"""Releases ship the authored surface layout (docs/ShippedSurfaceDefaults.md).

What a new user sees on the toolbar, navbar, main menu, op menu, pane-type
menu and hub tabs comes from packaging/surface_defaults.json, applied by
pre_release_common to the staged copy of every package. The author's live
arrangement reaches it only through a snapshot.

Runs outside TouchDesigner: surface_defaults.py is plain Python at module
level, and Apply() is exercised on small fakes with a stand-in `td`.

    python tests/test_surface_defaults.py
"""
import copy
import importlib.util
import io
import json
import os
import re
import sys
import textwrap
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
    'surface_defaults', os.path.join(_ROOT, 'packaging', 'surface_defaults.py'))
sd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sd)

data = json.loads(read('packaging', 'surface_defaults.json'))

print('the committed defaults')
check('the file has no problems', sd.Problems(data) == [], sd.Problems(data))
catalog = json.loads(read('packaging', 'catalog.json'))
pk = catalog.get('packages', catalog)
names = set(pk) if isinstance(pk, dict) else {p.get('name') for p in pk}
unknown = sorted(set(data['packages']) - names)
check('every package it names is in the catalog', not unknown, unknown)
tb = data['configurators'].get('ToolbarConfigurator') or []
head = tb[0] if tb else []
groups = [r for r in tb[1:] if head and r[head.index('kind')] == 'groupstart']
check('the toolbar ships its groups', bool(groups))
check('every toolbar group start holds its member list',
      all(sd.ANCHOR_SEP in r[head.index('anchor')] for r in groups), groups)
check('no shipped parameter is a registration switch',
      not any(n.lower().endswith(('autoregister', 'register', 'unregister', 'regstatus'))
              for o in data['packages'].values() for p in o.values() for n in p))

print('Problems catches what would ship broken')
bad = copy.deepcopy(data)
first = next(iter(bad['packages'].values()))
rel, pars = next(iter(first.items()))
pars['Tbmenuorder'] = 5
second = dict(bad['packages'])
second['ZZ_fake'] = {'.': {'Tbmenuorder': 5}}
bad['packages'] = second
check('a tie in one order par', any('ties with' in p for p in sd.Problems(bad)))
bad2 = copy.deepcopy(data)
rows = bad2['configurators']['ToolbarConfigurator']
h = rows[0]
bad2['configurators']['ToolbarConfigurator'] = [h] + [
    r for r in rows[1:] if r[h.index('kind')] != 'groupend']
check('a group with only one bracket',
      any('only one bracket' in p for p in sd.Problems(bad2)))
bad3 = copy.deepcopy(data)
mm = bad3['configurators']['MainMenuConfigurator']
row = [''] * len(mm[0])
row[mm[0].index('kind')], row[mm[0].index('name')], row[mm[0].index('display')] = 'group', 'Gx', '1'
mm.append(row)
check('a leftover group row with no brackets',
      any('no brackets' in p for p in sd.Problems(bad3)))
check('an unknown top-level key',sd.Problems({'packages': {}, 'configurators': {}, 'x': 1}) != [])


print('Apply writes the defaults onto a staged copy')


class Mode:
    """Stands in for td.ParMode: Apply reaches CONSTANT through the par's
    own mode (type(p.mode).CONSTANT), as TD's enum allows."""
    def __init__(self, name):
        self.name = name


CONSTANT, EXPRESSION, BIND = Mode('CONSTANT'), Mode('EXPRESSION'), Mode('BIND')
Mode.CONSTANT, Mode.EXPRESSION, Mode.BIND = CONSTANT, EXPRESSION, BIND
check('Apply needs no td module', 'import td' not in read('packaging', 'surface_defaults.py'))


class Par:
    def __init__(self, val, mode=CONSTANT, default=-1):
        self.val, self.mode, self.default = val, mode, default


class Pars(dict):
    def __getitem__(self, k):
        return self.get(k)


class Cell:
    def __init__(self, v):
        self.val = v


class Table:
    path = '/sys/quiet/x/FNS_Hub/ToolbarConfigurator/state'

    nodeX = nodeY = 0

    def __init__(self, rows=()):
        self._rows = [list(r) for r in rows]

    def rows(self):
        return [[Cell(c) for c in r] for r in self._rows]

    def clear(self):
        self._rows = []

    def appendRow(self, r):
        self._rows.append(list(r))


class Comp:
    def __init__(self, name, path, pars=None, kids=None):
        self.name, self.path = name, path
        self.par = Pars(pars or {})
        self.kids = kids or {}
        self.tags = set()

    def op(self, rel):
        return self.kids.get(rel)

    def create(self, cls, name):
        self.kids[name] = cls()
        return self.kids[name]


tool = Comp('FNS_Fake', '/q/FNS_Fake', {'Tbmenuorder': Par(99), 'Tbdisplayed': Par(0, EXPRESSION)})
fake = {'packages': {'FNS_Fake': {'.': {'Tbmenuorder': 3, 'Tbdisplayed': True}}},
        'configurators': {}}
changed = sd.Apply(tool, fake)
check('the order lands', tool.par['Tbmenuorder'].val == 3)
check('an expression becomes the authored constant',
      tool.par['Tbdisplayed'].mode is CONSTANT and tool.par['Tbdisplayed'].val is True)
check('Apply reports what it changed', len(changed) == 2, changed)
check('a second Apply changes nothing', sd.Apply(tool, fake) == [])
check('the shipped place is stamped as the default too (roams only as a change)',
      tool.par['Tbmenuorder'].default == 3 and tool.par['Tbdisplayed'].default is True)
check('...and the owner is tagged as stamped', sd.LAYOUT_TAG in tool.tags)
missing = {'packages': {'FNS_Fake': {'.': {'Nope': 1}}}, 'configurators': {}}
try:
    sd.Apply(tool, missing)
    raised = False
except LookupError:
    raised = True
check('a par the package lost fails the export', raised)
check('a package the file does not name is left alone',
      sd.Apply(Comp('Other', '/q/Other'), fake) == [])
state = Table([['kind', 'name'], ['builtin', 'old']])
hub = Comp('FNS_Hub', '/q/FNS_Hub', kids={'ToolbarConfigurator': Comp(
    'ToolbarConfigurator', '/q/FNS_Hub/ToolbarConfigurator', kids={'state': state})})
want = [['kind', 'name'], ['builtin', 'perform'], ['divider', 'D1']]
sd.Apply(hub, {'packages': {}, 'configurators': {'ToolbarConfigurator': want}})
check('a configurator table is replaced whole', state._rows == want, state._rows)
shipped = hub.op('ToolbarConfigurator').op(sd.STATE_DEFAULT)
check('...and a copy of it ships as state_default',
      shipped is not None and shipped._rows == want)

print('shipped_values: dev values that must not ship')
sv = data.get('shipped_values') or {}
check('the dev workspace ships empty',
      sv.get('FNS_VSCodeTools', {}).get('.', {}).get('Workspace') == '')
check("TimelineTools' test export file ships empty",
      sv.get('FNS_TimelineTools', {}).get('.', {}).get('Exportfile') == '')
check("oscMapper ships with receive and talkback off (each project turns them on)",
      sv.get('oscMapper', {}).get('.', {}).get('Active') is False
      and sv.get('oscMapper', {}).get('.', {}).get('Active2') is False)
vs = Comp('FNS_VSCodeTools', '/q/FNS_VSCodeTools',
          {'Workspace': Par('FunctionStore_tools_2023.code-workspace'), 'Folder': Par('scripts')})
sd.Apply(vs, {'packages': {}, 'configurators': {}, 'shipped_values': sv})
check('Apply writes a shipped value onto the staged copy', vs.par['Workspace'].val == '')
check('...and leaves a par the file does not name', vs.par['Folder'].val == 'scripts')
check('a shipped value is not a layout default: no stamp, no tag',
      vs.par['Workspace'].default == -1 and sd.LAYOUT_TAG not in vs.tags)
src_sd = read('packaging', 'surface_defaults.py')
check('a snapshot keeps the hand-written shipped_values',
      "data['shipped_values'] = kept" in src_sd)
bad4 = copy.deepcopy(data)
bad4['shipped_values'] = {'FNS_X': {'.': 'not a dict'}}
check('a malformed shipped_values entry is caught', sd.Problems(bad4) != [])

print('group brackets survive a missing member (FNS_Hub ConfiguratorBase)')
src = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'ConfiguratorBase.py')
m = re.search(r'\n(\tdef _anchorMembers\(.*?)(?=\n\tdef )', src, re.S)
check('the anchor helper is there', m is not None)
if m:
    ns = {}
    exec('class B:\n\tANCHOR_SEP = "|"\n' + m.group(1), ns)
    b = ns['B']()
    check('a member list reads in order',
          b._anchorMembers('A|B|C', 'C') == ['A', 'B', 'C'])
    check('two single names still read as first and last',
          b._anchorMembers('A', 'C') == ['A', 'C'])
check('the start bracket opens before the first member present',
      'anchor=min(present, key=base.index)' in src)
check('the end bracket closes after the last member present',
      'anchor=max(present, key=base.index)' in src)
check('the writer stores the whole membership',
      "'groupstart': self.ANCHOR_SEP.join(members)" in src)
check('ANCHOR_SEP agrees between the Hub and the packaging module',
      "ANCHOR_SEP = '|'" in src and sd.ANCHOR_SEP == '|')

print('the export applies it')
common = read('packaging', 'pre_release_common.py')
check('pre_release_common applies the defaults file',
      "_sd['Apply'](_c0, _sd['Load']())" in common)
tail = common[common.index('shipped surface layout is the authored default'):]
code = [ln for ln in tail.splitlines() if ln.strip() and not ln.lstrip().startswith('#')]
check('...outside any try, so a stale file fails loudly',
      not any(ln.strip().startswith('try:') for ln in code), code)

print()
if FAILS:
    print('FAILED %d: %s' % (len(FAILS), ', '.join(FAILS)))
    sys.exit(1)
print('all passed')
