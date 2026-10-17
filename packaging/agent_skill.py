"""AgentSkill -- the consumer agent skill bundle rendered from the manifest
(docs/AgentSkill.md).

A user's coding agent sees a project full of `FNS_*` COMPs and `op.FNS_*`
shortcuts and guesses. This module renders the Agent Skills bundle that
explains them: one authored core page (`SKILL.md`), one generated reference
page per public package, an index, and the list of every quick-launch
command. Nothing on a generated page is typed by hand; each section reads
one named source (docs/AgentSkill.md section 3b).

Pure Python, no TouchDesigner imports: build_manifest.Build() loads it by
path inside TD, and tests/test_agent_skill.py loads it the same way and
renders a fixture manifest without TouchDesigner.

The bundle:

    fnstools/
      SKILL.md                copied from packaging/agent_skill/SKILL.md
      VERSION                 the manifest's release string
      references/
        index.md              one line per package
        commands.md           every quick-launch command, by package
        <Package>.md          one per public package
        <other>.md            any authored page under agent_skill/references/

A package is public when its row is not `preview` and, for a `foreign` row,
only when a doc file exists for it. The `api` and `commands` row fields are
reflected inside TD by build_manifest.Build() (docs/AgentSkill.md section 4),
and the Parameters section reads packaging/parameters.json from the same
build; a manifest without them says so on the page, and the coverage report
Render() returns counts the gaps: promoted methods with no docstring, and
packages with no doc file.

Two more things live here because they are pure Python and tested without
TD: the TRANSPORT document (WriteTransport / Unpack), the whole bundle as
one JSON file the release publishes beside the manifest and the updater
unpacks into <user palette>/FNSTools/agent-skill/; and MentionedNames, the
parser the release gate (release_one.Preflight) runs over the authored
pages to find every `op.FNS_*` shortcut and `op.X.Method(` call they name.
"""
import hashlib
import io
import json
import os
import re
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
AUTHORED_DIR = os.path.join(_HERE, 'agent_skill')
BUNDLE_NAME = 'fnstools'
NO_API_LINE = ('No promoted API: the package has no extension. Its parameters, '
               'listed below, are its surface.')
NO_COMMANDS_LINE = 'No commands recorded for this package.'
NO_DOC_LINE = ('No documentation file for this package; the manifest summary '
               'above is all there is.')
NO_PARAMS_LINE = 'No parameter reference recorded for this package.'
TRANSPORT_SCHEMA = 1


# ---------------------------------------------------------------- docs

def _unquote(value):
    """A YAML scalar as js-yaml writes it: bare, 'single' ('' escapes) or
    "double" (JSON escapes)."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except ValueError:
            return value[1:-1]
    return value


def ReadDoc(text):
    """A packaging/docs page as {'summary', 'feature_list', 'body'}.

    Reads the frontmatter block js-yaml writes (the CMS saves through it):
    one `key: value` per line, list items as `- key: value` with one
    `key: value` per following line. The same reading as
    tests/test_feature_list.py; a feature_list line in any other shape
    raises, so a doc written some other way fails loudly instead of
    rendering as empty."""
    m = re.match(r'---\r?\n([\s\S]*?)\r?\n---\r?\n?', text)
    if not m:
        return {'summary': '', 'feature_list': [], 'body': text}
    lines = m.group(1).splitlines()
    out = {'summary': '', 'feature_list': [], 'body': text[m.end():]}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('summary:'):
            out['summary'] = _unquote(line[len('summary:'):])
        elif line.strip() == 'feature_list:':
            i += 1
            while i < len(lines) and lines[i].startswith(' '):
                s = lines[i].strip()
                if s.startswith('- '):
                    out['feature_list'].append({})
                    s = s[2:]
                if not out['feature_list'] or ':' not in s:
                    raise ValueError('unreadable feature_list line: %r' % lines[i])
                k, v = s.split(':', 1)
                out['feature_list'][-1][k.strip()] = _unquote(v)
                i += 1
            continue
        i += 1
    return out


def DocPath(docs_dir, name):
    return os.path.join(docs_dir, name + '.md')


def LoadDoc(docs_dir, name):
    """The package's doc, read, or None when there is no file for it."""
    path = DocPath(docs_dir, name)
    if not os.path.isfile(path):
        return None
    with io.open(path, encoding='utf-8') as f:
        return ReadDoc(f.read())


# ------------------------------------------------------------ selection

def IsPublic(row, has_doc):
    """A row gets a page unless it is a preview, or foreign with no doc."""
    if row.get('preview') or row.get('access') == 'preview':
        return False
    if row.get('foreign') and not has_doc:
        return False
    return True


def PublicRows(rows, docs_dir):
    """[(row, doc-or-None)] for every row that gets a page, by name."""
    out = []
    for row in sorted(rows, key=lambda r: r['name']):
        doc = LoadDoc(docs_dir, row['name'])
        if IsPublic(row, doc is not None):
            out.append((row, doc))
    return out


# ------------------------------------------------------------ rendering

def _tierLabels(manifest):
    labels = {'free': 'Free'}
    for t in (manifest.get('toolkit') or {}).get('tiers') or []:
        if isinstance(t, dict) and t.get('id'):
            labels[str(t['id'])] = str(t.get('label') or t['id'])
    return labels


def AccessLabel(row, tiers):
    access = str(row.get('access', 'free') or 'free')
    return tiers.get(access, access)


def _code(s):
    return '`%s`' % s


def ReachLine(row):
    """How an agent reaches the package: its shortcut, a registry's /sys
    global, a family member's operator, or where the installer puts it
    (manifest `placement`, packaging/InstallerExt.py: absent = a child of
    the toolkit root, 'root' = beside the toolkit at the project root,
    'none' = never placed, the store holds the tox)."""
    shortcut = (row.get('shortcut') or '').strip()
    if shortcut:
        return ('%s is its global shortcut: call its promoted methods on that '
                'object from anywhere in the project.' % _code('op.' + shortcut))
    gs = (row.get('global_shortcut') or '').strip()
    if gs:
        return ('A registry. %s is its global shortcut, promoted into '
                '/sys/FNS_Registries while the toolkit runs: call its promoted '
                'methods on that object from anywhere in the project, never on '
                'the master inside the toolkit root. See registries.md.' % _code('op.' + gs))
    fam = row.get('family') or {}
    if fam.get('op_name'):
        return ('No global shortcut. Place a copy: it is the FNS operator family '
                'member %s (%s) on the FNS tab of the OP Create dialog, also at '
                '%s. Its promoted methods are called on the placed copy.'
                % (_code(fam['op_name']), fam.get('op_label') or fam['op_name'],
                   _code('<user palette>/FNSTools/FNS/%s.tox' % row['name'])))
    placement = str(row.get('placement') or '')
    if placement == 'root':
        return ('No global shortcut. Installed beside the toolkit root at the '
                'project root, as %s; its promoted methods are called on that COMP.'
                % _code("op('/%s')" % row['name']))
    if placement == 'none':
        return ('No global shortcut. The installer never places it into a '
                'network: its tox is in the store at %s for the user to place '
                'by hand, and its promoted methods are called on that copy.'
                % _code('<user palette>/FNSTools/store/%s.tox' % row['name']))
    return ('No global shortcut. A child of the toolkit root, reached as %s; '
            'its promoted methods are called on that COMP.'
            % _code("op.FNS.op('%s')" % row['name']))


def _paramText(p):
    if isinstance(p, dict):
        name = str(p.get('name') or '?')
        t = p.get('style') or p.get('type')
        s = name + (': %s' % t if t else '')
        if 'default' in p and p['default'] is not None:
            s += ' = %r' % (p['default'],)
        elif p.get('required'):
            s += ' (required)'
        return s
    return str(p)


def CommandLines(row):
    """Markdown lines for the row's quick-launch commands, [] when none.

    One line per command: the label, the id (the half of the registry key
    after `#`, what Run() and the launcher key on), the help, the promoted
    method that implements it and, when a COMP inside the package declares
    it, that owner's path under the package, then the params."""
    lines = []
    for c in row.get('commands') or []:
        if not isinstance(c, dict):
            continue
        label = c.get('label') or c.get('name') or '?'
        cid = c.get('id') or (c.get('name') or '').lower()
        text = '- **%s**' % label
        if cid:
            text += ' (id %s)' % _code(cid)
        if c.get('help'):
            text += ': %s' % c['help']
        tail = []
        if c.get('name'):
            tail.append('Method %s%s.' % (_code(c['name']),
                                         ' on %s' % _code(c['owner']) if c.get('owner') else ''))
        params = c.get('params') or []
        if params:
            tail.append('Params: %s.' % ', '.join(_code(_paramText(p)) for p in params))
        if tail:
            text += ' ' + ' '.join(tail)
        lines.append(text)
    return lines


def ApiLines(row):
    """Markdown lines for the reflected promoted API, and the names of the
    methods and properties that have no docstring. A method is listed with
    its signature; a property, a stored item (a value TouchDesigner's
    StorageManager keeps on the COMP) or a promoted attribute (a dependable
    with no docstring to carry) by name, with its kind."""
    lines, undocumented = [], []
    for m in row.get('api') or []:
        if not isinstance(m, dict) or not m.get('name'):
            continue
        kind = m.get('kind') or 'method'
        doc = (m.get('doc') or '').strip()
        if kind == 'method':
            head = _code(m['name'] + (m.get('signature') or '()'))
        elif kind == 'stored':
            head = '%s (stored item: a value the extension keeps on the COMP, read as an attribute)' % _code(m['name'])
        else:
            head = '%s (%s)' % (_code(m['name']), kind)
        if doc:
            lines.append('- %s: %s' % (head, doc))
        else:
            lines.append('- %s' % head)
            if kind not in ('attribute', 'stored'):
                undocumented.append(m['name'])
    return lines, undocumented


def _defaultText(value):
    if isinstance(value, bool):
        return 'on' if value else 'off'
    return str(value)


def ParameterLines(name, parameters):
    """Markdown lines for the package's own custom parameters, from the
    parameter reference packaging/parameters.json writes beside the
    manifest (docs/AgentSkill.md section 11, owner's call 2026-10-17):
    one line per parameter under its page, with the label, the name an
    agent writes in code, the style, the default, the menu entries and
    the help text. [] when the package has no custom parameters, None
    when the reference has no entry for it at all."""
    rows = ((parameters or {}).get('packages') or {}).get(name)
    if rows is None:
        return None
    lines, page = [], None
    for p in rows:
        if not isinstance(p, dict) or not p.get('name'):
            continue
        if p.get('page') != page:
            page = p.get('page')
            if page:
                lines += ['', '### %s' % page, '']
        head = '- **%s** (%s, %s' % (p.get('label') or p['name'],
                                    _code('par.' + p['name']), p.get('style') or '?')
        if (p.get('size') or 1) > 1:
            head += ' x%d' % p['size']
        head += ')'
        if 'default' in p and p['default'] not in (None, ''):
            head += ', default %s' % _code(_defaultText(p['default']))
        menu = [m for m in (p.get('menu') or []) if isinstance(m, dict) and m.get('name')]
        if menu:
            head += ', menu %s' % ', '.join(_code(str(m['name'])) for m in menu)
        help_ = (p.get('help') or '').strip()
        lines.append(head + (': ' + help_ if help_ else ''))
    while lines and lines[0] == '':
        lines.pop(0)
    return lines


def HotkeyLines(row):
    lines = []
    for h in row.get('hotkeys') or []:
        if not isinstance(h, dict) or not h.get('keys'):
            continue
        where = ''
        if h.get('par'):
            where = ' (%s' % _code(h['par'])
            if h.get('op'):
                where += ' on %s' % _code(h['op'])
            where += ')'
        lines.append('- %s%s' % (_code(h['keys']), where))
    return lines


def PackagePage(row, doc, tiers, parameters=None):
    """One reference page, every section from its named source."""
    name = row['name']
    title = row.get('title') or name
    out = ['# %s' % title, '']
    if title != name:
        out += ['Package %s.' % _code(name), '']
    out.append(row.get('description') or (doc or {}).get('summary') or '')
    out += ['',
            '- Category: %s' % row.get('category', ''),
            '- Version: %s' % row.get('version', ''),
            '- Access: %s' % AccessLabel(row, tiers),
            '- Docs: %s' % row.get('help_url', ''),
            '']
    out += ['## What it does', '']
    feats = (doc or {}).get('feature_list') or []
    if doc is None:
        out.append(NO_DOC_LINE)
    elif not feats:
        out.append('The doc file has no feature list; see the summary above and the docs link.')
    else:
        for f in feats:
            does = f.get('does') or ''
            out.append('- **%s**: %s' % (f.get('name', ''), does) if does
                       else '- **%s**' % f.get('name', ''))
    out += ['', '## Reach it', '', ReachLine(row), '']
    out += ['## Promoted API', '']
    api_lines, undocumented = ApiLines(row)
    out += api_lines or [NO_API_LINE]
    out += ['', '## Commands', '']
    out += CommandLines(row) or [NO_COMMANDS_LINE]
    out += ['', '## Hotkeys', '']
    out += HotkeyLines(row) or ['None.']
    out += ['', '## Alternative for', '']
    alts = row.get('alternatives_for') or []
    out += ['- %s' % _code(a) for a in alts] or ['None.']
    out += ['', '## Requires', '']
    reqs = row.get('requires') or []
    out += ['- %s' % _code(r) for r in reqs] or ['Nothing.']
    # Last, and the longest section: the agent reads it when it needs a
    # parameter, not to learn what the package is.
    out += ['', '## Parameters', '']
    plines = ParameterLines(name, parameters)
    if plines is None:
        out.append(NO_PARAMS_LINE)
    elif not plines:
        out.append('None.')
    else:
        out += plines
    out.append('')
    return '\n'.join(out), undocumented


def IndexPage(pairs, release, tiers):
    out = ['# FNSTools packages (%s)' % release, '',
           'One line per package: category, summary, docs link, what it is an '
           'alternative for. The page of the same name under this folder has '
           'the detail.', '']
    for row, doc in pairs:
        line = '- **%s** (%s, v%s, %s): %s [docs](%s)' % (
            row['name'], row.get('category', ''), row.get('version', ''),
            AccessLabel(row, tiers), row.get('description', ''), row.get('help_url', ''))
        alts = row.get('alternatives_for') or []
        if alts:
            line += ' Alternative for %s.' % ', '.join(_code(a) for a in alts)
        sc = (row.get('shortcut') or row.get('global_shortcut') or '').strip()
        if sc:
            line += ' Shortcut %s.' % _code('op.' + sc)
        out.append(line)
    out.append('')
    return '\n'.join(out)


def CommandsPage(pairs):
    out = ['# Quick-launch commands', '',
           'Every quick-launch command the public packages declare, by package. '
           'A command is run through the command registry by its key, the '
           'declaring COMP\'s path, `#`, and the id shown on its line: for a '
           'package\'s own command '
           '`op.FNS_COMMANDREGISTRY.Run(op.FNS.op(\'FNS_Updater\').path + \'#checkforupdates\')`, '
           'and for a command a COMP inside the package declares (the line says '
           '"Method X on `<path under the package>`") '
           '`op.FNS_COMMANDREGISTRY.Run(op.FNS.op(\'FNS_CommandRegistry/FNS_BuiltinCommands/TD_Session\').path + \'#togglerealtime\')`. '
           '`op.FNS_COMMANDREGISTRY.Commands()` lists the live commands with '
           'their keys (`key`, `tool`, `id`, `label`, `help`, `path`). The method '
           'named on the line is the command\'s implementation and can be called '
           'on the declaring COMP directly. The built-in TouchDesigner commands '
           '(toggle realtime, open a dialog, ...) are declared by COMPs under '
           'FNS_CommandRegistry.', '']
    total = 0
    for row, doc in pairs:
        lines = CommandLines(row)
        if not lines:
            continue
        total += len(lines)
        out += ['## %s' % row['name'], ''] + lines + ['']
    if not total:
        out += ['No commands recorded in this manifest.', '']
    return '\n'.join(out), total


# ---------------------------------------------------------------- bundle

def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def Render(manifest, docs_dir, out_dir, authored_dir=AUTHORED_DIR, parameters=None):
    """Render the bundle into `<out_dir>/fnstools/` and return the coverage
    report: {'release', 'bundle', 'files', 'packages', 'methods',
    'commands', 'methods_without_doc': [(package, name)],
    'packages_without_doc': [name]}. `methods` counts the callable
    surface (methods and properties), not promoted attributes.

    `parameters` is the parsed packaging/parameters.json (or None): the
    source of each page's Parameters section.

    The `fnstools/` folder is replaced whole, so a package dropped from the
    manifest leaves no stale page behind."""
    bundle = os.path.join(out_dir, BUNDLE_NAME)
    if os.path.isdir(bundle):
        shutil.rmtree(bundle)
    refs = os.path.join(bundle, 'references')
    os.makedirs(refs)
    release = str(manifest.get('release') or '')
    tiers = _tierLabels(manifest)
    pairs = PublicRows(manifest.get('packages') or [], docs_dir)
    files = []

    core = os.path.join(authored_dir, 'SKILL.md')
    with io.open(core, encoding='utf-8') as f:
        _write(os.path.join(bundle, 'SKILL.md'), f.read())
    files.append('SKILL.md')
    _write(os.path.join(bundle, 'VERSION'), release + '\n')
    files.append('VERSION')

    authored_refs = os.path.join(authored_dir, 'references')
    if os.path.isdir(authored_refs):
        for fn in sorted(os.listdir(authored_refs)):
            if fn.endswith('.md'):
                with io.open(os.path.join(authored_refs, fn), encoding='utf-8') as f:
                    _write(os.path.join(refs, fn), f.read())
                files.append('references/' + fn)

    report = {'release': release, 'bundle': bundle, 'packages': len(pairs),
              'methods': 0, 'commands': 0,
              'methods_without_doc': [], 'packages_without_doc': []}
    for row, doc in pairs:
        page, undocumented = PackagePage(row, doc, tiers, parameters)
        _write(os.path.join(refs, row['name'] + '.md'), page)
        files.append('references/%s.md' % row['name'])
        report['methods'] += sum(1 for m in (row.get('api') or [])
                                 if isinstance(m, dict) and m.get('kind') not in ('attribute', 'stored'))
        report['methods_without_doc'] += [(row['name'], n) for n in undocumented]
        if doc is None:
            report['packages_without_doc'].append(row['name'])
    _write(os.path.join(refs, 'index.md'), IndexPage(pairs, release, tiers))
    files.append('references/index.md')
    commands, total = CommandsPage(pairs)
    _write(os.path.join(refs, 'commands.md'), commands)
    files.append('references/commands.md')
    report['commands'] = total
    report['files'] = sorted(files)
    return report


def CoverageText(report):
    """The coverage report as the lines a build prints."""
    out = ['agent skill %s: %d packages, %d promoted methods, %d commands'
           % (report['release'], report['packages'], report['methods'], report['commands'])]
    out.append('  methods without a docstring: %d' % len(report['methods_without_doc']))
    for pkg, name in report['methods_without_doc']:
        out.append('    %s.%s' % (pkg, name))
    out.append('  packages without a doc file: %d' % len(report['packages_without_doc']))
    for pkg in report['packages_without_doc']:
        out.append('    %s' % pkg)
    return '\n'.join(out)


# ------------------------------------------------------------- transport

def BundleFiles(bundle_dir):
    """{relative path: text} of every file in the bundle, '/'-separated,
    in sorted order."""
    out = {}
    for base, dirs, files in os.walk(bundle_dir):
        dirs.sort()
        for fn in sorted(files):
            full = os.path.join(base, fn)
            rel = os.path.relpath(full, bundle_dir).replace('\\', '/')
            with io.open(full, encoding='utf-8') as f:
                out[rel] = f.read()
    return out


def WriteTransport(bundle_dir, out_path):
    """The bundle as ONE document the release publishes beside the
    manifest: {'schema', 'version' (the VERSION file), 'bundle' (the
    folder name, fnstools), 'files': {path: text}}. The folder stays the
    canonical form (docs/AgentSkill.md section 4: no archive); this is
    how it travels, one fetch and one hash for the updater, no archive
    format on either end. Deterministic bytes for the same folder.
    Returns {'path', 'bytes', 'sha256', 'files'}."""
    files = BundleFiles(bundle_dir)
    doc = {'schema': TRANSPORT_SCHEMA,
           'version': (files.get('VERSION') or '').strip(),
           'bundle': os.path.basename(os.path.normpath(bundle_dir)),
           'files': files}
    text = json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    with io.open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    with io.open(out_path, 'rb') as f:
        data = f.read()
    return {'path': out_path, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'files': len(files)}


def ReadTransport(path):
    """A transport document, parsed; raises on a document of another
    schema or with no files."""
    with io.open(path, encoding='utf-8') as f:
        doc = json.load(f)
    if doc.get('schema') != TRANSPORT_SCHEMA or not isinstance(doc.get('files'), dict):
        raise ValueError('not an agent skill transport document: %s' % path)
    return doc


def Unpack(doc, dest_dir):
    """Lay a transport document out as the folder it was made from:
    <dest_dir>/<bundle>/<path> for every file, written only when the text
    differs, and any other file under <dest_dir>/<bundle>/ removed, since
    the folder is derived, never authored. The updater carries the same
    lines (ExtUpdater.SyncAgentSkillFolder) so a release never depends on
    this module being present; this is the reference and the tested copy.
    Returns {'folder', 'version', 'written', 'removed'}."""
    bundle = str(doc.get('bundle') or BUNDLE_NAME)
    folder = os.path.join(dest_dir, bundle)
    files = doc.get('files') or {}
    written, removed = [], []
    for rel, text in sorted(files.items()):
        path = os.path.join(folder, *rel.split('/'))
        cur = None
        if os.path.isfile(path):
            with io.open(path, encoding='utf-8') as f:
                cur = f.read()
        if cur != text:
            _write(path, text)
            written.append(rel)
    keep = {rel.lower() for rel in files}
    for base, dirs, names in os.walk(folder, topdown=False):
        for fn in names:
            full = os.path.join(base, fn)
            rel = os.path.relpath(full, folder).replace('\\', '/')
            if rel.lower() not in keep:
                os.remove(full)
                removed.append(rel)
        for d in dirs:
            try:
                os.rmdir(os.path.join(base, d))
            except OSError:
                pass
    return {'folder': folder, 'version': str(doc.get('version') or ''),
            'written': written, 'removed': removed}


# -------------------------------------------------------------- the gate

SHORTCUT_RE = re.compile(r'\bop\.([A-Za-z][A-Za-z0-9_]*)')
METHOD_RE = re.compile(r'\bop\.([A-Za-z][A-Za-z0-9_]*)\.([A-Z][A-Za-z0-9_]*)\s*\(')


def MentionedNames(text):
    """What a page names of the toolkit, for the release gate
    (docs/AgentSkill.md section 5): {'shortcuts': {'FNS_X', ...},
    'methods': {('FNS_X', 'Method'), ...}}. `op.<Shortcut>` is a
    shortcut; `op.<Shortcut>.<Method>(` is a call on it. A lowercase
    member after the shortcut (`.ext`, `.op(`, `.par`) is wiring or TD's
    own API, not a promoted method, and is not collected. A name ending in
    an underscore (`op.FNS_ shortcuts` in the core page's description) is
    prose about the prefix, not a shortcut, and is not collected either."""
    return {'shortcuts': {s for s in SHORTCUT_RE.findall(text) if not s.endswith('_')},
            'methods': {(s, m) for s, m in METHOD_RE.findall(text) if not s.endswith('_')}}


def AuthoredPages(authored_dir=AUTHORED_DIR):
    """[(relative path, text)] of every authored page: SKILL.md and the
    markdown under references/."""
    out = []
    core = os.path.join(authored_dir, 'SKILL.md')
    if os.path.isfile(core):
        with io.open(core, encoding='utf-8') as f:
            out.append(('SKILL.md', f.read()))
    refs = os.path.join(authored_dir, 'references')
    if os.path.isdir(refs):
        for fn in sorted(os.listdir(refs)):
            if fn.endswith('.md'):
                with io.open(os.path.join(refs, fn), encoding='utf-8') as f:
                    out.append(('references/' + fn, f.read()))
    return out

# ------------------------------------------------- static class resolution
# The release gate checks a method the authored pages name against the
# DIST build, where extensions are never initialised (the copy sits in a
# cooking-off holder), so the class is read from the DAT text instead:
# the extension slot's expression names the DAT and the class, and the
# class body plus its bases (RegistryBase sits in another DAT) name the
# members. Pure Python over source text, so tests/test_agent_skill.py
# covers it without TouchDesigner.

EXT_OBJECT_RE = re.compile(
    r"op\(\s*'(?:\./)?([A-Za-z0-9_]+)'\s*\)\.module\.([A-Za-z_][A-Za-z0-9_]*)")


def ExtensionTarget(object_expr):
    """"op('./BeatModExt').module.BeatModExt(me)" -> ('BeatModExt',
    'BeatModExt'): the DAT and the class an extension slot names. None for
    any other shape."""
    m = EXT_OBJECT_RE.search(object_expr or '')
    return (m.group(1), m.group(2)) if m else None


def _classDefs(sources):
    """{class name: ClassDef} over every parseable source text; the first
    definition of a name wins."""
    import ast
    out = {}
    for text in sources:
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name not in out:
                out[node.name] = node
    return out


def _classMembers(defs, name, seen):
    import ast
    node = defs.get(name)
    if node is None:
        return None
    seen.add(name)
    out = set()
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.add(item.name)
        elif isinstance(item, ast.Assign):
            for t in item.targets:
                if isinstance(t, ast.Name):
                    out.add(t.id)
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            out.add(item.target.id)
    for base in node.bases:
        bname = None
        if isinstance(base, ast.Name):
            bname = base.id
        elif isinstance(base, ast.Attribute):
            bname = base.attr
        if bname and bname not in seen:
            inherited = _classMembers(defs, bname, seen)
            if inherited:
                out |= inherited
    return out


def ClassMembers(sources, class_name):
    """The names a class defines or inherits, from source text alone: every
    def and class-level assignment in its body, plus those of every base
    class found among `sources` (a list of source texts). None when the
    class is in none of them."""
    return _classMembers(_classDefs(sources), class_name, set())


def ClassConstant(sources, class_name, const):
    """The string a class assigns to `const` in its body (SHORTCUT =
    'FNS_CONFIGREGISTRY'), the subclass winning over a base that also
    assigns it; None when nothing does."""
    import ast
    defs = _classDefs(sources)
    seen = set()
    queue = [class_name]
    while queue:
        name = queue.pop(0)
        node = defs.get(name)
        if node is None or name in seen:
            continue
        seen.add(name)
        for item in node.body:
            if (isinstance(item, ast.Assign) and isinstance(item.value, ast.Constant)
                    and isinstance(item.value.value, str)
                    and any(isinstance(t, ast.Name) and t.id == const for t in item.targets)):
                return item.value.value
        for base in node.bases:
            if isinstance(base, ast.Name):
                queue.append(base.id)
            elif isinstance(base, ast.Attribute):
                queue.append(base.attr)
    return None
