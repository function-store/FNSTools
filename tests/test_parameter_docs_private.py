"""The parameter reference carries no address or device of the author's machine.

packaging/parameters.json is written from the LIVE dev project
(build_manifest.BuildParameters) and feeds the public docs site and the
agent skill. A custom menu that copies a built-in menu listing the computer
itself (an OSC In DAT's Local Address, an Audio Device CHOP's Driver and
Device) put the author's LAN and Tailscale addresses and audio device ids
there (oscMapper, FNS_TimelineTools, 2026-10-20). Such a row now records
`menu_source: 'machine'` and no items (build_manifest.MACHINE_MENU_PARS).

Runs outside TouchDesigner: build_manifest.py loads as plain Python, and
_parRows is driven with small stand-in pars.

    python tests/test_parameter_docs_private.py
"""
import importlib.util
import io
import json
import os
import re
import sys

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


def load(name, *parts):
    spec = importlib.util.spec_from_file_location(name, os.path.join(_ROOT, *parts))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bm = load('build_manifest', 'packaging', 'build_manifest.py')
ask = load('agent_skill', 'packaging', 'agent_skill.py')


class Par:
    def __init__(self, name, style='StrMenu', menu=(), source='', default=''):
        self.tupletName = name
        self.label = name
        self.style = style
        self.help = ''
        self.default = default
        self.readOnly = False
        self.startSection = False
        self.menuNames = list(menu)
        self.menuLabels = list(menu)
        self.menuSource = source


class Page:
    def __init__(self, *pars):
        self.pars = list(pars)


def row(par):
    return bm._parRows(Page(par))[0]


print('a menu that lists this computer ships no items')
r = row(Par('Localaddress', menu=['192.168.1.5', '100.64.0.9'],
            source="op('./oscin1').par.localaddress"))
check('an OSC Local Address copy is marked machine', r.get('menu_source') == 'machine', r)
check('...and carries no items', 'menu' not in r, r)
r = row(Par('Audiodevice', menu=['{0.0.0.00000000}.{c841de8b-3933-4f45-91a5-0c999e44046a}||Speakers||1'],
            source="me.op('audio_devices').par.device", default='default'))
check('an audio Device copy is marked machine', r.get('menu_source') == 'machine' and 'menu' not in r, r)
check('...and keeps its default', r.get('default') == 'default', r)
r = row(Par('Audiodriver', menu=['default', 'asio'], source="me.op('audio_devices').par.driver"))
check('an audio Driver copy is marked machine', r.get('menu_source') == 'machine', r)

print('every other menu keeps its items')
r = row(Par('Format', style='Menu', menu=['useinput', 'rgba8fixed'], source="op('./glsl1').par.format"))
check('a copied fixed built-in menu keeps its items',
      [m['name'] for m in r.get('menu', [])] == ['useinput', 'rgba8fixed'] and 'menu_source' not in r, r)
r = row(Par('Device', style='Menu', menu=['a', 'b'], source="op('./sub').par.Device"))
check("a custom par named Device is not a built-in (case matters)",
      [m['name'] for m in r.get('menu', [])] == ['a', 'b'], r)
r = row(Par('Mode', style='Menu', menu=['x', 'y']))
check('a menu with no source keeps its items', len(r.get('menu', [])) == 2, r)

print('the readers say where the list comes from')
lines = ask.ParameterLines('Tool', {'packages': {'Tool': [
    {'page': 'Custom', 'name': 'Localaddress', 'label': 'Local Address',
     'style': 'StrMenu', 'default': '', 'menu_source': 'machine'}]}})
check('the agent skill says the menu is read from the computer',
      any('read from the computer it runs on' in ln for ln in lines), lines)
site = read('website', 'tools', 'build-site.mjs')
check("the docs site renders a machine menu without items",
      "row.menu_source === 'machine'" in site)

print('the committed parameter reference holds no machine address or device id')
IPV4 = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
GUID = re.compile(r'\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}')
# loopback and the wildcard name no machine
NOT_A_MACHINE = re.compile(r'^(?:127\.|0\.0\.0\.0$)')
doc = json.loads(read('packaging', 'parameters.json'))
rows = [(pkg, r) for pkg, rs in (doc.get('packages') or {}).items() for r in rs]
for reg, rs in (doc.get('registry_sections') or {}).items():
    if isinstance(rs, list):
        rows += [(reg, r) for r in rs if isinstance(r, dict)]
leaks = []
for pkg, r in rows:
    values = [str(r.get('default', ''))]
    for m in r.get('menu') or []:
        values += [str(m.get('name', '')), str(m.get('label', ''))]
    for v in values:
        hits = [h for h in IPV4.findall(v) if not NOT_A_MACHINE.match(h)]
        if hits or GUID.search(v):
            leaks.append('%s.%s: %s' % (pkg, r.get('name'), v[:60]))
check('no network address or device id in any menu or default', not leaks, leaks[:6])
osc = {r.get('name'): r for r in (doc.get('packages') or {}).get('oscMapper', [])}
check("oscMapper's Local Address menus are marked machine",
      all(osc.get(n, {}).get('menu_source') == 'machine' for n in ('Localaddress', 'Localaddress2')),
      {n: osc.get(n) for n in ('Localaddress', 'Localaddress2')})

print()
if FAILS:
    print('FAILED %d: %s' % (len(FAILS), ', '.join(FAILS)))
    sys.exit(1)
print('all passed')
