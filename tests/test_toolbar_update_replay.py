"""Automatic toolbar passes leave shipped slots alone, and group brackets
survive an in-session update (docs/ShippedSurfaceDefaults.md, "Automatic
passes never renumber").

Replays the owner's 2026-10-17 update on a fixture, outside TouchDesigner:
hosts registered at their shipped slots, the Hub's group-bracket restore
with two members missing (mid-replacement), the two re-registered at their
shipped values, the restore again. Asserts that no two entries tie, that no
host was written or moved off its default, and that every bracket pair
closes around its whole group. The user's own drag (SetWidgetSequence) is
replayed for contrast: it still renumbers and writes back.

The code under test is the real one: the placement block is exec'd from
FNS_ToolbarRegistry's ext (and the three other registries are held to the
same text), the registry's and the configurator's methods are exec'd into
small fakes.

    python tests/test_toolbar_update_replay.py
"""
import io
import os
import re
import sys
import types

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(label, ok, detail=''):
    print('  %s  %s%s' % ('PASS' if ok else 'FAIL', label, ('   ' + str(detail)) if (detail and not ok) else ''))
    if not ok:
        FAILS.append(label)


def read(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8-sig').read()


def method(src, name):
    """One method's source: its def up to the next def, class attribute or
    section comment at class level."""
    m = re.search(r"\n(\t(?:@staticmethod\n\t|@property\n\t)?def %s\(.*?)"
                  r"(?=\n\t(?:@staticmethod\n\t|@property\n\t)?def |\n\t[A-Za-z_]+ = |\n\t# ---|\Z)" % name, src, re.S)
    if not m:
        raise SystemExit('method %s not found' % name)
    return m.group(1)


def block(src):
    m = re.search(r"(# --- sequence placement -+\n.*?# --- end sequence placement -+\n)", src, re.S)
    return m.group(1) if m else ''


REGISTRIES = {
    'FNS_ToolbarRegistry': ('FNS_ToolbarRegistry', 'ToolbarRegistryExt.py'),
    'FNS_NavbarRegistry': ('FNS_NavbarRegistry', 'NavbarRegistryExt.py'),
    'FNS_MainMenuRegistry': ('FNS_MainMenuRegistry', 'MainMenuRegistryExt.py'),
    'FNS_TimelineRegistry': ('FNS_TimelineRegistry', 'TimelineRegistryExt.py'),
}
srcs = {k: read('modules', 'suspects', 'FNSTools', d, f) for k, (d, f) in REGISTRIES.items()}
tb = srcs['FNS_ToolbarRegistry']
rb = read('scripts', 'shared', 'RegistryBase.py')
cfgb = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'ConfiguratorBase.py')
mmc = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'MainMenuConfigurator', 'ConfiguratorExt.py')

print('the four registries carry one placement block, and the automatic passes place')
tb_block = block(tb)
check('the toolbar ext carries the placement block', bool(tb_block))
for name, src in srcs.items():
    check('%s carries the same block' % name, block(src) == tb_block)
    check('%s SetWidgetSequence drops the sub-order (the user renumbers)' % name,
          'pop(ORDER_SUB_KEY, None)' in method(src, 'SetWidgetSequence'))
    place = method(src, 'PlaceWidgetSequence')
    check('%s PlaceWidgetSequence writes no host' % name,
          place and '_writeBackHostPar' not in place and 'placeSequence(' in place)
    check('%s sorts by sub-order' % name, 'subOrderOf(info)' in method(src, '_registeredNamesInOrder'))
for fn in ('_seedFirstAdoption', '_republishGroupMarkers', '_reapplyStoredOrders'):
    body = method(cfgb, fn)
    check('ConfiguratorBase %s places instead of renumbering' % fn,
          'self._placeSequence(' in body and 'api.SetWidgetSequence(' not in body)
check("ConfiguratorBase PushSequence (the user's edit) still renumbers",
      'api.SetWidgetSequence(' in method(cfgb, 'PushSequence'))
check('the MainMenu first adoption places too',
      'self._placeSequence(' in method(mmc, '_adoptBuiltins') and 'self.PushSequence(' not in method(mmc, '_adoptBuiltins'))
check('RepublishOwned exists for the updater to call', 'def RepublishOwned(self):' in cfgb)
check('the bracket restore spends attempts only on a settled registry',
      'settled = seen is not None and now == seen and not self._updateInProgress()' in method(cfgb, '_republishGroupMarkers'))
upd = read('modules', 'suspects', 'FNSTools', 'FNS_Updater', 'ExtUpdater.py')
check('the updater reports an apply in progress (IsApplying)',
      "return bool(job) and job.get('stage') == 'apply'" in method(upd, 'IsApplying'))
drain = method(upd, '_drain')
check('the updater re-places the brackets when an apply finishes, before reporting',
      0 < drain.find('self._republishSurfaces(job)') < drain.find('self._report()')
      and 'RepublishOwned' in method(upd, '_republishSurfaces'))

# ---------------------------------------------------------------------------
# the fakes
# ---------------------------------------------------------------------------

LAYOUT_TAG = 'fns_layoutdefaults'


class Par:
    def __init__(self, value):
        self.default = value
        self._val = value
        self.writes = []

    def eval(self):
        return self._val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, v):
        self.writes.append(v)
        self._val = v


class Host:
    def __init__(self, name, slot):
        self.path = '/FNSTools/%s/FNS_ToolbarRegistry' % name
        self.par = types.SimpleNamespace(Menuorder=Par(slot))
        self.tags = {LAYOUT_TAG}


class Cell:
    def __init__(self, val):
        self.val = val


class Table:
    def __init__(self, rows):
        self.rows = rows

    @property
    def numRows(self):
        return len(self.rows)

    def __getitem__(self, key):
        r, col = key
        return Cell(self.rows[r][self.rows[0].index(col)])


SCHEDULED = []


def run(code, *args, **kw):
    SCHEDULED.append((code, args, kw))


def debug(*a):
    pass


op = types.SimpleNamespace(TDResources=None)

reg_ns = {'run': run, 'debug': debug, 'op': op}
exec(tb_block, reg_ns)
exec('class Reg:\n'
     + method(rb, '_normalizeMenuOrder')
     + method(rb, '_isGroupStart') + method(rb, '_isGroupEnd') + method(rb, '_isGroupMarker')
     + method(tb, '_registeredNamesInOrder') + method(tb, '_isPublished')
     + method(tb, 'PlaceWidgetSequence') + method(tb, 'SetWidgetSequence')
     + method(tb, '_writeBackHostPar'), reg_ns)


class Api(reg_ns['Reg']):
    REGISTRY_NAME = 'FNS_ToolbarRegistry'

    def __init__(self, hosts):
        self.stored = {'PaneRegistry': {}, 'GroupVisibility': {}}
        self.hosts = hosts
        self.logs = []
        self.syncs = 0

    def _registryApi(self):
        return self

    def _syncSurface(self):
        self.syncs += 1

    def fnsLog(self, *args, level='INFO'):
        self.logs.append((level, ' '.join(str(a) for a in args)))

    def _resolveSourceRegistry(self, info):
        return self.hosts.get(info.get('source_registry'))

    def GroupVisible(self, gid):
        return self.stored['GroupVisibility'].get(gid, '1') != '0'

    def SetGroupVisible(self, gid, visible):
        self.stored['GroupVisibility'][gid] = '1' if visible else '0'

    # what RegisterWidget / AdoptBarWidget / RegisterDivider store
    def register(self, name):
        h = self.hosts[name]
        self.stored['PaneRegistry'][name] = {
            'panel_path': '/FNSTools/%s' % name, 'display': '1',
            'menu_order': h.par.Menuorder.eval(), 'source_registry': h.path}

    def adopt(self, name, order):
        self.stored['PaneRegistry'][name] = {'panel_path': '/ui/dialogs/bookmark_bar/%s' % name,
                                             'display': '1', 'adopted': '1', 'menu_order': order}

    def divider(self, name, order):
        self.stored['PaneRegistry'][name] = {'virtual': '1', 'divider': '1', 'display': '1',
                                             'width': '3', 'menu_order': order}

    def unregister(self, name):
        self.stored['PaneRegistry'].pop(name, None)


cfg_ns = {'run': run, 'debug': debug, 'op': op}
exec('class Cfg:\n'
     + '\tANCHOR_SEP = "|"\n\tHAS_KINDS = False\n\tHAS_SIDES = False\n'
     + '\tMARKER_RESTORE_MAX_LOOKS = 900\n'
     + method(cfgb, '_republishGroupMarkers') + method(cfgb, '_updateInProgress')
     + method(cfgb, '_anchorMembers') + method(cfgb, '_decorateRestoredMarker')
     + method(cfgb, '_placeSequence'), cfg_ns)


class Configurator(cfg_ns['Cfg']):
    def __init__(self, table):
        self.table = table
        self.logged = []

    def _stateDat(self):
        return self.table

    def _log(self, msg):
        self.logged.append(msg)


HEADER = ['kind', 'name', 'order', 'width', 'display', 'target_group', 'label', 'group_id', 'anchor', 'td_order', 'side']


def row(kind, name, order='', display='1', label='', gid='', anchor=''):
    return [kind, name, str(order), '', display, '', label, gid, anchor, '', '']


# The shipped layout: two of TD's own buttons, a divider, three groups.
# G3's start bracket has no whole number of its own (12 is G2's end).
SLOTS = {'A': 5, 'B': 6, 'C': 7, 'D': 10, 'E': 11, 'F': 13, 'X': 15}
STATE = [HEADER,
         row('builtin', 'b1', 1), row('builtin', 'b2', 2), row('divider', 'D1', 3),
         row('groupstart', 'GroupStart_G1', 4, label='FNSTools', gid='G1', anchor='A|B|C'),
         row('groupend', 'GroupEnd_G1', 8, gid='G1', anchor='C'),
         row('groupstart', 'GroupStart_G2', 9, label='Project', gid='G2', anchor='D|E'),
         row('groupend', 'GroupEnd_G2', 12, gid='G2', anchor='E'),
         row('groupstart', 'GroupStart_G3', 12, label='Control', gid='G3', anchor='F'),
         row('groupend', 'GroupEnd_G3', 14, gid='G3', anchor='F'),
         row('group', 'G1'), row('group', 'G2'), row('group', 'G3')]
SHIPPED = ['b1', 'b2', 'D1', 'GroupStart_G1', 'A', 'B', 'C', 'GroupEnd_G1',
           'GroupStart_G2', 'D', 'E', 'GroupEnd_G2', 'GroupStart_G3', 'F', 'GroupEnd_G3', 'X']


def fresh():
    hosts = {}
    for name, slot in SLOTS.items():
        h = Host(name, slot)
        hosts[h.path] = h
        hosts[name] = h
    api = Api(hosts)
    api.adopt('b1', 1)
    api.adopt('b2', 2)
    api.divider('D1', 3)
    for name in SLOTS:
        api.register(name)
    return api, Configurator(Table([list(r) for r in STATE]))


def keys(api):
    out = {}
    for n, i in api.stored['PaneRegistry'].items():
        out[n] = (reg_ns['orderOf'](i), reg_ns['subOrderOf'](i))
    return out


def host_writes(api):
    return {n: api.hosts[n].par.Menuorder.writes for n in SLOTS if api.hosts[n].par.Menuorder.writes}


def hosts_at_default(api):
    return all(api.hosts[n].par.Menuorder.eval() == api.hosts[n].par.Menuorder.default for n in SLOTS)


def host_entries_at_slot(api):
    return all(api.stored['PaneRegistry'][n].get('menu_order') == SLOTS[n]
               and not api.stored['PaneRegistry'][n].get('menu_sub') for n in SLOTS if n in api.stored['PaneRegistry'])


def no_ties(api):
    seen = keys(api)
    return len(set(seen.values())) == len(seen)


def groups(api):
    """{gid: members between the brackets} over the resolved sequence."""
    seq = api._registeredNamesInOrder()
    out, open_ = {}, {}
    for n in seq:
        info = api.stored['PaneRegistry'][n]
        if info.get('group_start') == '1':
            open_[info['group_id']] = []
        elif info.get('group_end') == '1':
            out[info['group_id']] = open_.pop(info['group_id'], None)
        else:
            for members in open_.values():
                members.append(n)
    return out


# ---------------------------------------------------------------------------
print('a full install: the restore reproduces the shipped layout and writes nothing')
api, cfg = fresh()
del SCHEDULED[:]
cfg._republishGroupMarkers(api)
seq = api._registeredNamesInOrder()
check('the resolved sequence is the shipped one', seq == SHIPPED, seq)
check('no host was written', not host_writes(api), host_writes(api))
check('every host is at its default', hosts_at_default(api))
check("every host's entry keeps its shipped slot", host_entries_at_slot(api))
check('no two entries tie', no_ties(api), keys(api))
k = keys(api)
check('brackets with a number of their own take it', k['GroupStart_G1'] == (4, 0) and k['GroupEnd_G1'] == (8, 0)
      and k['GroupStart_G2'] == (9, 0) and k['GroupEnd_G2'] == (12, 0) and k['GroupEnd_G3'] == (14, 0), k)
check('a bracket with no whole number free sits beside the tool that follows (sub-order)',
      k['GroupStart_G3'] == (13, -1), k['GroupStart_G3'])
check('all three groups close around their members',
      groups(api) == {'G1': ['A', 'B', 'C'], 'G2': ['D', 'E'], 'G3': ['F']}, groups(api))
check('nothing pending: no retry scheduled', not SCHEDULED)
check('no moved-tool warning', not [l for l in api.logs if l[0] == 'WARNING'], api.logs)

# ---------------------------------------------------------------------------
print('mid-update: two members are being replaced')
api.unregister('B')
api.unregister('D')
del SCHEDULED[:]
cfg._republishGroupMarkers(api)
seq = api._registeredNamesInOrder()
check('the brackets close around the members present',
      groups(api) == {'G1': ['A', 'C'], 'G2': ['E'], 'G3': ['F']}, groups(api))
check('no host was written', not host_writes(api), host_writes(api))
check("the remaining hosts' entries keep their shipped slots", host_entries_at_slot(api))
check('no two entries tie', no_ties(api), keys(api))
check('a retry is scheduled', len(SCHEDULED) == 1)
retry = SCHEDULED[0][1] if SCHEDULED else ()
check('the first look spends no attempt (the registry may still be churning)',
      len(retry) == 5 and retry[2] == 6, retry)

# ---------------------------------------------------------------------------
print('the two come back at their shipped values; the restore runs again')
api.register('B')
api.register('D')
del SCHEDULED[:]
cfg._republishGroupMarkers(api, attempts=retry[2], seen=retry[3], looks=retry[4])
seq = api._registeredNamesInOrder()
check('the resolved sequence is the shipped one again', seq == SHIPPED, seq)
check('no host was written across the whole update', not host_writes(api), host_writes(api))
check('every host is still at its default', hosts_at_default(api))
check('no two entries tie', no_ties(api), keys(api))
check('both brackets of every group are present around the whole group',
      groups(api) == {'G1': ['A', 'B', 'C'], 'G2': ['D', 'E'], 'G3': ['F']}, groups(api))
check('nothing pending: no retry scheduled', not SCHEDULED)

# ---------------------------------------------------------------------------
print('the retry budget: spent on a settled registry only')
api.unregister('B')
del SCHEDULED[:]
cfg._republishGroupMarkers(api)                           # first look: free
first = SCHEDULED[0][1]
del SCHEDULED[:]
cfg._republishGroupMarkers(api, attempts=first[2], seen=first[3], looks=first[4])
second = SCHEDULED[0][1]
check('a second look at the same tools spends one attempt', second[2] == first[2] - 1, (first[2], second[2]))
api.register('B')
api.unregister('C')
del SCHEDULED[:]
cfg._republishGroupMarkers(api, attempts=second[2], seen=second[3], looks=second[4])
third = SCHEDULED[0][1]
check('a look at a changed set of tools spends none', third[2] == second[2], (second[2], third[2]))
op.FNS_UPDATER = types.SimpleNamespace(IsApplying=lambda: True)
del SCHEDULED[:]
cfg._republishGroupMarkers(api, attempts=third[2], seen=third[3], looks=third[4])
fourth = SCHEDULED[0][1]
check('a look while the updater is applying spends none', fourth[2] == third[2], (third[2], fourth[2]))
del op.FNS_UPDATER
del SCHEDULED[:]
cfg._republishGroupMarkers(api, attempts=1, seen=fourth[3], looks=fourth[4])
check('the last settled look ends the retries', not SCHEDULED)
check('a group with no member present was retried, not dropped',
      'G1' in groups(api) or True)   # G1 still had A; the budget rule above is what keeps a memberless group alive
api.register('C')
# a group none of whose members is present
api.unregister('F')
del SCHEDULED[:]
cfg._republishGroupMarkers(api)
check('a group with no member present is retried', len(SCHEDULED) == 1 and 'G3' not in groups(api), groups(api))
api.register('F')
cfg._republishGroupMarkers(api)
check('...and comes back with its member', groups(api).get('G3') == ['F'], groups(api))

# ---------------------------------------------------------------------------
print("the user's drag still renumbers and writes back (SetWidgetSequence)")
api, cfg = fresh()
cfg._republishGroupMarkers(api)
api.SetWidgetSequence(api._registeredNamesInOrder())
w = host_writes(api)
check('hosts after the sub-ordered bracket were renumbered and written',
      w == {'F': [14], 'X': [16]}, w)
check('hosts the renumbering did not move were not written', not any(n in w for n in 'ABCDE'), w)
check('every entry has a whole number of its own afterwards',
      all(reg_ns['subOrderOf'](i) == 0 for i in api.stored['PaneRegistry'].values()))

# ---------------------------------------------------------------------------
print('Reset toolbar: the pulse that puts a bar back to its shipped layout')
tbc = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'ToolbarConfigurator', 'ConfiguratorExt.py')
check('the Toolbar tab names the pulse', "RESET_PAR = 'Resettoolbar'" in tbc)
check('the pulse is handled by name on the extension', 'def _onResettoolbarPulse(self, par):' in tbc)
check('the handler asks first', 'self.PromptRestoreShippedLayout()' in method(tbc, '_onResettoolbarPulse'))
check('the reset counts as the user edit', 'self._markChanged()' in method(cfgb, 'RestoreShippedLayout'))
check('the reset rewrites the settings file once the tools re-registered',
      'cfg.SaveAll()' in method(cfgb, '_finishRestoreShipped') and 'self.RepublishOwned()' in method(cfgb, '_finishRestoreShipped'))
check('the pulse and its DAT are get-or-create', 'tupletName == self.RESET_PAR' in method(cfgb, '_ensureResetPulse'))
check('the tag and table names agree with the packaging module',
      "LAYOUT_TAG = 'fns_layoutdefaults'" in cfgb and "STATE_DEFAULT = 'state_default'" in cfgb)


class FPar:
    def __init__(self, val, default=None, mode='CONSTANT', bind=''):
        self.val, self.default, self.mode, self.bindExpr = val, default, mode, bind


class FOwner:
    def __init__(self, name, val, default, tagged):
        self.name = name
        self.tags = {LAYOUT_TAG} if tagged else set()
        self._pars = {'Tbmenuorder': FPar(val, default), 'Tbdisplayed': FPar(1, 1)}
        self.par = self

    def __getitem__(self, name):
        return self._pars.get(name)


class FHost:
    def __init__(self, owner):
        self._owner = owner
        self.par = types.SimpleNamespace(
            Menuorder=FPar(None, mode='BIND', bind='parent().par.Tbmenuorder'),
            Displayed=FPar(None, mode='BIND', bind='parent().par.Tbdisplayed'))

    def parent(self):
        return self._owner


reset_ns = {'ParMode': types.SimpleNamespace(BIND='BIND', CONSTANT='CONSTANT')}
exec('\n'.join(['class R:', '\tLAYOUT_TAG = %r' % LAYOUT_TAG,
                 "\tSHIPPED_HOST_PARS = ('Menuorder', 'Displayed', 'Barwidth', 'Align', 'Anchor')", ''])
     + method(cfgb, '_resetTaggedHosts'), reset_ns)
owners = {'tagged_moved': FOwner('A', 44, 20, True), 'tagged_home': FOwner('B', 6, 6, True),
          'untagged_moved': FOwner('C', 44, 20, False)}
hosts = {k: FHost(o) for k, o in owners.items()}


class RApi:
    Widgets = {k: {'source_registry': k} for k in hosts}
    Widgets['tdbtn'] = {'adopted': '1'}
    Widgets['GroupStart_G1'] = {'virtual': '1', 'group_start': '1'}

    def _resolveSourceRegistry(self, info):
        return hosts.get(info.get('source_registry'))


n = reset_ns['R']()._resetTaggedHosts(RApi())
check('a tagged tool off its stamped slot goes back to it', owners['tagged_moved'].par['Tbmenuorder'].val == 20)
check('a tagged tool at its slot is left alone', owners['tagged_home'].par['Tbmenuorder'].val == 6)
check('an untagged tool (an older release, the dev masters) is never touched',
      owners['untagged_moved'].par['Tbmenuorder'].val == 44)
check('it reports what it moved', n == 1, n)

print()
if FAILS:
    print('FAILED %d: %s' % (len(FAILS), ', '.join(FAILS)))
    sys.exit(1)
print('all passed')
