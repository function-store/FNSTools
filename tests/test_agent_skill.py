"""tests/test_agent_skill.py -- the consumer agent skill bundle rendered from
a manifest (docs/AgentSkill.md, sections 3, 3b, 4, 9 and 10).

packaging/agent_skill.py turns a manifest plus the authored pages into the
`fnstools/` Agent Skills bundle. This pins the file set, which rows get a
page, that every section of a package page carries its named source value,
and that the coverage report counts the gaps the owner's docstring pass
has to close. Runs without TouchDesigner, on a fixture manifest written
here plus three real docs from packaging/docs.

    python tests/test_agent_skill.py
"""
import importlib.util
import io
import os
import re
import shutil
import tempfile

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(_ROOT, 'packaging')
DOCS = os.path.join(PKG, 'docs')
FAILS = []


def check(label, cond, detail=''):
    if cond:
        print('  PASS  %s' % label)
    else:
        FAILS.append(label)
        print('  FAIL  %s   %s' % (label, detail))


spec = importlib.util.spec_from_file_location('agent_skill', os.path.join(PKG, 'agent_skill.py'))
ask = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ask)


def read(*parts):
    with io.open(os.path.join(*parts), encoding='utf-8') as f:
        return f.read()


def section(page, heading):
    """The text under `## heading` up to the next heading."""
    m = re.search(r'^## %s\n(.*?)(?=^## |\Z)' % re.escape(heading), page, re.S | re.M)
    return m.group(1) if m else None


# The fixture: every row shape the renderer has to decide on. Three rows
# have real docs in packaging/docs (ChopBank, FNS_BeatMod, TDXMap); the
# rest have none, on purpose.
MANIFEST = {
    'release': 'v9.9.9-test',
    'toolkit': {'tiers': [{'id': '8323905', 'label': 'Base'},
                          {'id': '8291595', 'label': 'Pro'}]},
    'packages': [
        {   # a shortcut package with everything reflected
            'name': 'FNS_BeatMod', 'title': 'BeatMod', 'category': 'Control & mapping',
            'description': 'Modulate any parameter to the beat.', 'version': '2.3.4',
            'help_url': 'https://functionstore.tools/docs/fns-beatmod/',
            'shortcut': 'FNS_BEATMOD', 'access': '8323905',
            'requires': ['FNS_ConfigRegistry', 'FNS_HotkeyManager'],
            'alternatives_for': [],
            'hotkeys': [{'keys': 'alt.g', 'op': 'FNS_BeatMod', 'par': 'Shortcutlfo'},
                        {'keys': 'alt.r', 'op': 'FNS_BeatMod', 'par': 'Shortcuttap'}],
            'api': [{'name': 'SetBpm', 'signature': '(bpm: float = 120)', 'doc': 'Set the project tempo.'},
                    {'name': 'TapTempo', 'signature': '()', 'doc': ''},
                    {'name': 'OpenManager', 'signature': '()', 'doc': 'Open the modulator manager.'},
                    {'name': 'Bpm', 'kind': 'property', 'doc': 'The live tempo.'},
                    {'name': 'IsRunning', 'kind': 'attribute'},
                    {'name': 'Marks', 'kind': 'stored'}],
            'commands': [{'name': 'SetBpm', 'label': 'Set BPM', 'help': 'Set the project tempo',
                          'params': [{'name': 'bpm', 'style': 'float', 'default': 120}]},
                         {'name': 'TapTempo', 'label': 'Tap tempo', 'help': '', 'params': []},
                         {'name': 'ToggleRealtime', 'id': 'togglerealtime', 'label': 'Toggle Realtime',
                          'help': 'Toggle realtime playback mode.', 'owner': 'Builtin/TD_Session'}],
        },
        {   # a family member with no shortcut, alternatives, no api yet
            'name': 'ChopBank', 'title': 'ChopBank', 'category': 'CHOPs & sensing',
            'description': 'A bank of channel processors.', 'version': '1.0.3',
            'help_url': 'https://functionstore.tools/docs/chopbank/',
            'shortcut': '', 'access': 'free', 'requires': ['FNS_OpMenuRegistry'],
            'alternatives_for': ['constantCHOP', 'mathCHOP'], 'hotkeys': [],
            'family': {'op_type': 'chopbank', 'op_name': 'chopBank', 'op_label': 'Chop Bank'},
        },
        {   # a preview row WITH a doc file: no page
            'name': 'FNS_BackupCleaner', 'title': 'BackupCleaner', 'category': 'Project',
            'description': 'Every .toe backup under a folder.', 'version': '3.2.7',
            'help_url': 'https://functionstore.tools/docs/fns-backupcleaner/',
            'shortcut': '', 'access': 'preview', 'preview': True, 'requires': [],
            'hotkeys': [], 'api': [{'name': 'Scan', 'signature': '()', 'doc': ''}],
        },
        {   # a foreign row with a doc, installed at the project root: a page
            'name': 'TDXMap', 'title': 'TDXMap', 'category': 'Control & mapping',
            'description': 'MIDI controller mapping with a live web UI.', 'version': '1.2.0',
            'help_url': 'https://tdxmap.functionstore.xyz/docs/', 'foreign': True,
            'shortcut': '', 'access': 'free', 'requires': [], 'hotkeys': [], 'placement': 'root',
        },
        {   # a toolkit-resident tool with no shortcut: reached as a child of op.FNS
            'name': 'FNS_RootTool', 'title': 'RootTool', 'category': 'Project',
            'description': 'A twin for the reach test.', 'version': '1.0.0',
            'help_url': 'https://functionstore.tools/docs/fns-roottool/',
            'shortcut': '', 'access': 'free', 'requires': [], 'hotkeys': [],
        },
        {   # never placed by the installer: the store holds the tox
            'name': 'StoreOnlyTool', 'title': 'StoreOnlyTool', 'category': 'Misc',
            'description': 'Placed by hand.', 'version': '1.0.0',
            'help_url': 'https://functionstore.tools/docs/storeonlytool/',
            'shortcut': '', 'access': 'free', 'requires': [], 'hotkeys': [], 'placement': 'none',
        },
        {   # a foreign row without a doc: no page
            'name': 'ForeignNoDoc', 'title': 'ForeignNoDoc', 'category': 'Miscellaneous',
            'description': 'A foreign tool with no doc.', 'version': '0.1.0',
            'help_url': 'https://example.com/', 'foreign': True,
            'shortcut': '', 'access': 'free', 'requires': [], 'hotkeys': [],
        },
        {   # a registry master: no shortcut on the master, a /sys global
            'name': 'FNS_HubRegistry', 'title': 'HubRegistry', 'category': 'Core', 'kind': 'core',
            'description': 'The registry behind Hub\'s tab bar.', 'version': '3.2.6',
            'help_url': 'https://functionstore.tools/docs/fns-hubregistry/',
            'shortcut': '', 'global_shortcut': 'FNS_HUBREGISTRY', 'access': 'free',
            'requires': [], 'hotkeys': [],
            'api': [{'name': 'RegisterTab', 'signature': '(comp, canonical)', 'doc': 'Publish a tab.'}],
        },
        {   # a public row with no doc file and one undocumented method
            'name': 'FNS_NoDocTool', 'title': 'NoDocTool', 'category': 'Developer',
            'description': 'A tool whose doc is still to be written.', 'version': '0.2.0',
            'help_url': 'https://functionstore.tools/docs/fns-nodoctool/',
            'shortcut': 'FNS_NODOC', 'access': '8291595', 'requires': [], 'hotkeys': [],
            'api': [{'name': 'Poke', 'signature': '(n: int = 1)', 'doc': ''}],
        },
    ],
}

# The parameter reference (packaging/parameters.json): BeatMod has two pages,
# ChopBank has an entry with no custom pars, TDXMap (foreign) has no entry.
PARAMETERS = {
    'packages': {
        'FNS_BeatMod': [
            {'name': 'Bpm', 'label': 'BPM', 'style': 'Float', 'default': 120.0,
             'help': 'The timeline tempo, mirrored live.', 'page': 'Beat Mod'},
            {'name': 'Tap', 'label': 'Tap Tempo', 'style': 'Pulse', 'page': 'Beat Mod'},
            {'name': 'Wave', 'label': 'Default Wave', 'style': 'Menu', 'default': 'sine',
             'menu': [{'name': 'sine', 'label': 'Sine'}, {'name': 'square', 'label': 'Square'}],
             'page': 'Beat Mod'},
            {'name': 'Color', 'label': 'Colour', 'style': 'RGB', 'size': 3, 'default': 1.0,
             'help': 'The manager tint.', 'page': 'Manager'},
            {'name': 'Autoopen', 'label': 'Open On Start', 'style': 'Toggle', 'default': False,
             'page': 'Manager'},
        ],
        'ChopBank': [],
        'FNS_NoDocTool': [{'name': 'N', 'label': 'Count', 'style': 'Int', 'default': 1,
                           'help': 'How many.', 'page': 'Tool'}],
    },
}

for n in ('ChopBank', 'FNS_BeatMod', 'TDXMap', 'FNS_BackupCleaner', 'FNS_HubRegistry'):
    assert os.path.isfile(os.path.join(DOCS, n + '.md')), 'fixture needs the real doc ' + n
assert not os.path.isfile(os.path.join(DOCS, 'FNS_NoDocTool.md'))
assert not os.path.isfile(os.path.join(DOCS, 'FNS_RootTool.md'))
assert not os.path.isfile(os.path.join(DOCS, 'StoreOnlyTool.md'))
assert not os.path.isfile(os.path.join(DOCS, 'ForeignNoDoc.md'))

tmp = tempfile.mkdtemp(prefix='agent_skill_')
try:
    report = ask.Render(MANIFEST, DOCS, tmp, parameters=PARAMETERS)
    bundle = os.path.join(tmp, 'fnstools')
    refs = os.path.join(bundle, 'references')

    print('1. the file set (docs/AgentSkill.md section 3)')
    expected = {'SKILL.md', 'VERSION', 'references/index.md', 'references/commands.md',
                'references/registries.md',
                'references/FNS_BeatMod.md', 'references/ChopBank.md', 'references/FNS_HubRegistry.md',
                'references/TDXMap.md', 'references/FNS_NoDocTool.md',
                'references/FNS_RootTool.md', 'references/StoreOnlyTool.md'}
    on_disk = set()
    for base, dirs, files in os.walk(bundle):
        for fn in files:
            on_disk.add(os.path.relpath(os.path.join(base, fn), bundle).replace('\\', '/'))
    check('the bundle holds exactly the expected files', on_disk == expected,
          sorted(on_disk ^ expected))
    check('the report lists the same files', set(report['files']) == expected,
          sorted(set(report['files']) ^ expected))
    check('VERSION is the manifest release', read(bundle, 'VERSION').strip() == 'v9.9.9-test')
    skill = read(bundle, 'SKILL.md')
    authored = read(PKG, 'agent_skill', 'SKILL.md')
    check('SKILL.md is the authored core page, copied whole', skill == authored)
    fm = re.match(r'---\n(.*?)\n---', skill, re.S)
    check('SKILL.md frontmatter names the skill fnstools',
          fm is not None and re.search(r'^name: fnstools$', fm.group(1), re.M) is not None)
    desc = re.search(r'^description: (.*)$', fm.group(1), re.M).group(1) if fm else ''
    check('the description line names what an agent sees: FNS_, op.FNS_, FNSTools, the Hub, quick-launch',
          all(x in desc for x in ('FNS_', 'op.FNS_', 'FNSTools', 'Hub', 'quick-launch')), desc)

    print('2. which rows get a page')
    check('a preview row produces no page, doc or not',
          not os.path.exists(os.path.join(refs, 'FNS_BackupCleaner.md')))
    check('a foreign row without a doc produces no page',
          not os.path.exists(os.path.join(refs, 'ForeignNoDoc.md')))
    check('a foreign row with a doc gets a page', os.path.exists(os.path.join(refs, 'TDXMap.md')))
    check('a public row with no doc file still gets a page, from the manifest',
          os.path.exists(os.path.join(refs, 'FNS_NoDocTool.md')))
    check('the report counts the pages', report['packages'] == 7, report['packages'])

    print('3. every section of a package page carries its source value (section 3b)')
    page = read(refs, 'FNS_BeatMod.md')
    head = page.split('## What it does')[0]
    check('title from the manifest row', page.startswith('# BeatMod\n'))
    check('summary, category, version, help_url from the manifest row',
          all(x in head for x in ('Modulate any parameter to the beat.',
                                  'Category: Control & mapping', 'Version: 2.3.4',
                                  'https://functionstore.tools/docs/fns-beatmod/')), head)
    check('access tier is named, from the toolkit tiers', 'Access: Base' in head, head)
    beatmod_doc = ask.ReadDoc(read(DOCS, 'FNS_BeatMod.md'))
    does = section(page, 'What it does') or ''
    check('What it does lists every feature_list `does` line of the doc frontmatter',
          beatmod_doc['feature_list'] and all(f.get('does', '') in does
                                              for f in beatmod_doc['feature_list']),
          does[:300])
    check('Reach it names the global shortcut', 'op.FNS_BEATMOD' in (section(page, 'Reach it') or ''))
    api = section(page, 'Promoted API') or ''
    check('Promoted API lists every method with its signature and docstring head',
          '`SetBpm(bpm: float = 120)`: Set the project tempo.' in api
          and '`OpenManager()`: Open the modulator manager.' in api, api)
    check('a method with no docstring is listed with the signature only',
          re.search(r'^- `TapTempo\(\)`$', api, re.M) is not None, api)
    check('a property is listed by name with its kind and docstring',
          '- `Bpm` (property): The live tempo.' in api, api)
    check('a promoted attribute is listed by name with its kind, no parens',
          re.search(r'^- `IsRunning` \(attribute\)$', api, re.M) is not None, api)
    check('a stored item is listed by name with what it is, and is not counted undocumented',
          '- `Marks` (stored item: a value the extension keeps on the COMP, read as an attribute)' in api, api)
    params = section(page, 'Parameters') or ''
    check('Parameters lists each par under its page with label, name, style, default and help',
          '### Beat Mod' in params and '### Manager' in params
          and '- **BPM** (`par.Bpm`, Float), default `120.0`: The timeline tempo, mirrored live.' in params
          and '- **Tap Tempo** (`par.Tap`, Pulse)' in params, params)
    check('a menu par lists its entries', 'menu `sine`, `square`' in params, params)
    check('a tuplet shows its size and a toggle default reads on/off',
          '(`par.Color`, RGB x3), default `1.0`' in params
          and '(`par.Autoopen`, Toggle), default `off`' in params, params)
    check('Parameters is the last section of the page', page.rstrip().split('\n## ')[-1].startswith('Parameters'))
    cmds = section(page, 'Commands') or ''
    check('Commands carries label, help and params',
          'Set BPM' in cmds and 'Set the project tempo' in cmds and 'bpm: float = 120' in cmds
          and 'Tap tempo' in cmds, cmds)
    check('a command line carries the id, the help, the method and the params',
          '- **Set BPM** (id `setbpm`): Set the project tempo Method `SetBpm`. Params: `bpm: float = 120`.' in cmds, cmds)
    check('a command a child COMP declares names its id, its method and the owner under the package',
          '- **Toggle Realtime** (id `togglerealtime`): Toggle realtime playback mode. Method `ToggleRealtime` on `Builtin/TD_Session`.' in cmds, cmds)
    hk = section(page, 'Hotkeys') or ''
    check('Hotkeys from the manifest hotkeys: keys, par, op',
          'alt.g' in hk and 'Shortcutlfo' in hk and 'alt.r' in hk and 'FNS_BeatMod' in hk, hk)
    check('Requires from the manifest', 'FNS_ConfigRegistry' in (section(page, 'Requires') or '')
          and 'FNS_HotkeyManager' in (section(page, 'Requires') or ''))
    check('an empty Alternative for says so', 'None.' in (section(page, 'Alternative for') or ''))

    cb = read(refs, 'ChopBank.md')
    check('Alternative for from manifest alternatives_for',
          'constantCHOP' in (section(cb, 'Alternative for') or '')
          and 'mathCHOP' in (section(cb, 'Alternative for') or ''))
    reach = section(cb, 'Reach it') or ''
    check('no shortcut: Reach it says place a copy, with the family op name',
          'Place a copy' in reach and 'chopBank' in reach and 'Chop Bank' in reach, reach)
    check('no api field yet: the page says no API recorded',
          ask.NO_API_LINE in (section(cb, 'Promoted API') or ''))
    check('no commands field yet: the page says no commands recorded',
          ask.NO_COMMANDS_LINE in (section(cb, 'Commands') or ''))
    check('Access: Free for a free row', 'Access: Free' in cb)
    check('a package with an empty parameter entry says None',
          (section(cb, 'Parameters') or '').strip() == 'None.', section(cb, 'Parameters'))
    tdx = read(refs, 'TDXMap.md')
    check('a package absent from the parameter reference says so',
          ask.NO_PARAMS_LINE in (section(tdx, 'Parameters') or ''))
    check('placement root: Reach it names the project-root COMP',
          "op('/TDXMap')" in (section(tdx, 'Reach it') or ''), section(tdx, 'Reach it'))
    bc2 = read(refs, 'FNS_RootTool.md')
    check('no shortcut, no placement: Reach it is a child of op.FNS',
          "op.FNS.op('FNS_RootTool')" in (section(bc2, 'Reach it') or ''), section(bc2, 'Reach it'))
    so = read(refs, 'StoreOnlyTool.md')
    check('placement none: Reach it points at the store tox to place by hand',
          'store/StoreOnlyTool.tox' in (section(so, 'Reach it') or '')
          and 'never places' in (section(so, 'Reach it') or ''), section(so, 'Reach it'))
    chopbank_doc = ask.ReadDoc(read(DOCS, 'ChopBank.md'))
    check('a quoted `does` line with an escaped apostrophe reads back unquoted',
          any("previous block's settings" in f.get('does', '') for f in chopbank_doc['feature_list']),
          [f.get('does') for f in chopbank_doc['feature_list']])

    nd = read(refs, 'FNS_NoDocTool.md')
    check('a package without a doc file is marked as such',
          ask.NO_DOC_LINE in (section(nd, 'What it does') or ''))
    check('a shortcut package with no family: Reach it is the shortcut', 'op.FNS_NODOC' in nd)
    check('Access: Pro from the tier ladder', 'Access: Pro' in nd)
    hr = read(refs, 'FNS_HubRegistry.md')
    check('a registry master: Reach it names the /sys global, not a placed copy',
          'op.FNS_HUBREGISTRY' in (section(hr, 'Reach it') or '')
          and 'Place a copy' not in (section(hr, 'Reach it') or ''), section(hr, 'Reach it'))

    print('4. index and commands pages')
    index = read(refs, 'index.md')
    check('index has one line per page, none for the skipped rows',
          all(('**%s**' % n) in index for n in ('FNS_BeatMod', 'ChopBank', 'TDXMap', 'FNS_NoDocTool', 'FNS_HubRegistry'))
          and 'FNS_BackupCleaner' not in index and 'ForeignNoDoc' not in index)
    check('the index names a registry by its /sys global', 'Shortcut `op.FNS_HUBREGISTRY`' in index)
    check('an index line carries category, summary, help_url and alternatives',
          re.search(r'\*\*ChopBank\*\* \(CHOPs & sensing, v1\.0\.3, Free\): A bank of channel '
                    r'processors\. \[docs\]\(https://functionstore\.tools/docs/chopbank/\) '
                    r'Alternative for `constantCHOP`, `mathCHOP`\.', index) is not None, index)
    commands = read(refs, 'commands.md')
    check('commands.md lists every command under its package',
          '## FNS_BeatMod' in commands and 'Set BPM' in commands and 'Tap tempo' in commands
          and '## ChopBank' not in commands, commands)
    check('commands.md says how to run one, with the key recipe for both owner shapes',
          "op.FNS.op('FNS_Updater').path + '#checkforupdates'" in commands
          and "FNS_BuiltinCommands/TD_Session').path + '#togglerealtime'" in commands, commands)
    check('commands.md explains a nested owner', 'Toggle Realtime' in commands and 'on `Builtin/TD_Session`' in commands)

    print('5. the coverage report (section 5)')
    check('methods and properties counted over the rendered pages only (not the preview Scan, not an attribute)',
          report['methods'] == 6, report['methods'])
    check('methods without a docstring: BeatMod.TapTempo and NoDocTool.Poke',
          sorted(report['methods_without_doc']) == [('FNS_BeatMod', 'TapTempo'), ('FNS_NoDocTool', 'Poke')],
          report['methods_without_doc'])
    check('packages without a doc file: the three fixtures with none',
          report['packages_without_doc'] == ['FNS_NoDocTool', 'FNS_RootTool', 'StoreOnlyTool'],
          report['packages_without_doc'])
    check('commands counted', report['commands'] == 3, report['commands'])
    text = ask.CoverageText(report)
    check('CoverageText prints the counts and the names',
          'methods without a docstring: 2' in text and 'FNS_BeatMod.TapTempo' in text
          and 'packages without a doc file: 3' in text and 'FNS_NoDocTool' in text, text)

    print('6. determinism and hygiene')
    before = {fn: read(refs, fn) for fn in os.listdir(refs)}
    ask.Render(MANIFEST, DOCS, tmp, parameters=PARAMETERS)
    after = {fn: read(refs, fn) for fn in os.listdir(refs)}
    check('rendering twice gives the same bytes', before == after)
    with io.open(os.path.join(refs, 'Stale.md'), 'w', encoding='utf-8') as f:
        f.write('stale\n')
    ask.Render(MANIFEST, DOCS, tmp, parameters=PARAMETERS)
    check('a re-render leaves no stale page behind', not os.path.exists(os.path.join(refs, 'Stale.md')))
    src = read(PKG, 'agent_skill.py')
    check('agent_skill.py imports nothing from TouchDesigner',
          not re.search(r'^\s*(import td|from td|op\(|parent\()', src, re.M))
    check('no em-dashes in the generated pages', not any('—' in v for v in after.values()))

    print('7. the real docs and the committed manifest render')
    import json
    real = json.load(io.open(os.path.join(PKG, 'manifest.json'), encoding='utf-8'))
    real_params = json.load(io.open(os.path.join(PKG, 'parameters.json'), encoding='utf-8'))
    real_tmp = tempfile.mkdtemp(prefix='agent_skill_real_')
    try:
        rr = ask.Render(real, DOCS, real_tmp, parameters=real_params)
        rows = real['packages']
        check('the committed manifest carries the reflected api and commands (Build() ran since step 2)',
              any('api' in r for r in rows) and any('commands' in r for r in rows) and rr['methods'] > 0,
              rr['methods'])
        check('no preview row carries api or commands',
              not any(('api' in r or 'commands' in r) for r in rows if r.get('preview')))
        check('the committed manifest carries the agent_skill transport block',
              isinstance(real.get('agent_skill'), dict)
              and all(k in real['agent_skill'] for k in ('version', 'sha256', 'url', 'files', 'bytes'))
              and real['agent_skill']['version'] == real['release'], real.get('agent_skill'))
        want = {r['name'] for r in rows
                if not r.get('preview') and (not r.get('foreign')
                                             or os.path.isfile(os.path.join(DOCS, r['name'] + '.md')))}
        check('every registry row of the committed manifest carries its /sys global',
              all(r.get('global_shortcut') for r in rows
                  if r['name'].endswith('Registry') or r['name'] == 'FNS_Console'),
              [r['name'] for r in rows if (r['name'].endswith('Registry') or r['name'] == 'FNS_Console')
               and not r.get('global_shortcut')])
        got = {f[len('references/'):-3] for f in rr['files']
               if f.startswith('references/') and f not in ('references/index.md', 'references/commands.md',
                                                            'references/registries.md')}
        check('every public package of the committed manifest gets a page (%d)' % len(want),
              got == want, sorted(got ^ want))
        print('  ....  ' + ask.CoverageText(rr).replace('\n', '\n  ....  '))
    finally:
        shutil.rmtree(real_tmp, ignore_errors=True)
    print('8. the transport document and the gate parser (sections 4 and 5)')
    tdoc = os.path.join(tmp, 'agent-skill.json')
    t1 = ask.WriteTransport(bundle, tdoc)
    check('the transport holds every bundle file and reports it', t1['files'] == len(expected), t1)
    check('its sha is of the bytes on disk',
          t1['sha256'] == __import__('hashlib').sha256(io.open(tdoc, 'rb').read()).hexdigest())
    t2 = ask.WriteTransport(bundle, tdoc)
    check('writing twice gives the same bytes', t1['sha256'] == t2['sha256'])
    doc = ask.ReadTransport(tdoc)
    check('the document carries the version and the bundle name',
          doc['version'] == 'v9.9.9-test' and doc['bundle'] == 'fnstools')
    dest = os.path.join(tmp, 'palette')
    os.makedirs(os.path.join(dest, 'fnstools', 'references'))
    with io.open(os.path.join(dest, 'fnstools', 'references', 'Gone.md'), 'w', encoding='utf-8') as f:
        f.write('an older release\'s page\n')
    u1 = ask.Unpack(doc, dest)
    unpacked = ask.BundleFiles(os.path.join(dest, 'fnstools'))
    check('Unpack lays the folder out byte for byte', unpacked == ask.BundleFiles(bundle))
    check('Unpack removes a file the document does not carry', u1['removed'] == ['references/Gone.md'], u1)
    u2 = ask.Unpack(doc, dest)
    check('a second Unpack writes nothing', u2['written'] == [] and u2['removed'] == [], u2)
    names = ask.MentionedNames(
        "Call `op.FNS_CONFIGREGISTRY.SaveAll()` or `op.FNS_HOTKEY_MANAGER.Discover ()`; "
        "`op.FNS.op('logger')` is the root, `op.FNS_UPDATER.ext.ExtUpdater.x()` is wiring, "
        "and op.FNS_BEATMOD on its own is a shortcut.")
    check('MentionedNames collects every op.<Shortcut>',
          names['shortcuts'] == {'FNS_CONFIGREGISTRY', 'FNS_HOTKEY_MANAGER', 'FNS', 'FNS_UPDATER', 'FNS_BEATMOD'},
          names['shortcuts'])
    check('and every op.<Shortcut>.<Method>( call, never a lowercase member',
          names['methods'] == {('FNS_CONFIGREGISTRY', 'SaveAll'), ('FNS_HOTKEY_MANAGER', 'Discover')},
          names['methods'])
    prefix = ask.MentionedNames('a project with op.FNS_ shortcuts and op.FNS_ COMPs')
    check('a bare prefix mention (op.FNS_) is prose, not a shortcut',
          prefix['shortcuts'] == set() and prefix['methods'] == set(), prefix)
    pages = ask.AuthoredPages()
    check('AuthoredPages reads SKILL.md and the authored references',
          pages and pages[0][0] == 'SKILL.md' and all(p.startswith('references/') for p, _ in pages[1:]),
          [p for p, _ in pages])
    print('9. the static class resolver the release gate reads the dist build with (section 5)')
    BASE_SRC = "class RegistryBase:\n\tSHORTCUT = None\n\tdef Register(self, x):\n\t\tpass\n\tdef _hidden(self):\n\t\tpass\n"
    EXT_SRC = ("import re\nFNSCommand = None\n\nclass ConfigRegistryExt(RegistryBase):\n\tSHORTCUT = 'FNS_CONFIGREGISTRY'\n"
               "\t@property\n\tdef ConfigPath(self):\n\t\treturn ''\n\t@FNSCommand.fns_command\n\tdef SaveAll(self):\n\t\tpass\n"
               "\tdef SaveTool(self, name):\n\t\tpass\n")
    OTHER_SRC = "class Unrelated:\n\tdef Foo(self):\n\t\tpass\n"
    BROKEN_SRC = "def (\n"
    check('ExtensionTarget reads the DAT and class off the slot expression',
          ask.ExtensionTarget("op('./ConfigRegistryExt').module.ConfigRegistryExt(me)") == ('ConfigRegistryExt', 'ConfigRegistryExt')
          and ask.ExtensionTarget("op('ExtUpdater').module.ExtUpdater(me)") == ('ExtUpdater', 'ExtUpdater')
          and ask.ExtensionTarget("mod.Thing.Thing(me)") is None)
    members = ask.ClassMembers([OTHER_SRC, BROKEN_SRC, EXT_SRC, BASE_SRC], 'ConfigRegistryExt')
    check('ClassMembers lists methods, properties and inherited members, from any source order, past an unparseable one',
          members is not None and {'SaveAll', 'SaveTool', 'ConfigPath', 'Register', 'SHORTCUT'} <= members
          and 'Foo' not in members, members)
    check('an unknown class resolves to None, not an empty set',
          ask.ClassMembers([BASE_SRC], 'Nope') is None)
    check('ClassConstant reads the subclass SHORTCUT over the base None',
          ask.ClassConstant([BASE_SRC, EXT_SRC], 'ConfigRegistryExt', 'SHORTCUT') == 'FNS_CONFIGREGISTRY'
          and ask.ClassConstant([BASE_SRC], 'RegistryBase', 'SHORTCUT') is None)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
if FAILS:
    print('FAILED: %d check(s)' % len(FAILS))
    raise SystemExit(1)
print('all agent skill checks pass')
