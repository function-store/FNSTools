"""SearchIndex -- the words a package's user-facing doc adds to the install
picker's search (docs/PickerSearch.md).

The picker searched only what a card shows: its title, its one-line
description, its category. Someone asking for "midi" or "lag" never found
ChopBank, because those words live in its documentation. This module turns
each doc into a small word list that rides the manifest row as `search`, so
the picker can match against it without fetching any docs.

Pure Python, no TouchDesigner imports: build_manifest.Build() loads it by
path inside TD, and tests/test_search_index.py loads it the same way.

A doc (packaging/docs/<Package>.md) becomes two space-joined strings of
FOLDED words, sorted, each word once:

    head  the frontmatter summary and feature names, the ## headings and the
          **bold** terms -- what the doc says the tool is about
    body  every other prose word

Words are split and folded by scripts/shared/FuzzyMatch.py (the picker runs
a port of it), so both sides compare like with like: "ChopBank" gives chop,
bank and the compound chopbank; "colour" folds to color. Dropped: words under
three letters, trailing digits (in1, Fader1), numbers, stopwords, fenced and
inline code, link targets and HTML tags, and every word the card itself
already answers to (title, name, description, family and catalog tags), because the
picker scores those fields higher anyway. A word that appears in more than
COMMON_SHARE of all docs ("parameter", "network") says nothing about any one
tool and is dropped from both tiers.

A third string rides along when the doc has a feature_list:

    lead  the first word of each feature name, folded, sorted, once each.
          A feature name leads with what the feature does ("Copy an
          operator reference", "Noise or image displacement"), so a query
          word that starts one says the tool DOES it
          (docs/FeatureSearchPosition.md). Kept whole: neither the common
          cut nor the card words apply, since it records a position, not
          a word the card lacks.
"""
import importlib.util
import io
import os
import re

# A word in more than this share of the docs is dropped corpus-wide.
COMMON_SHARE = 0.30
MIN_LEN = 3

STOPWORDS = frozenset("""
a about above after again against all almost along already also although always
am among an and another any anyone anything anyway are around as at away back
be became because become becomes been before being below between both but by
can cannot could did do does doing done down during each either else enough
even ever every few for from further get gets getting give given gives go goes
going gone got had has have having he her here hers herself him himself his how
however i if in into is it its itself just keep keeps kept least less let lets
like made make makes many may me might mine more most much must my myself near
need needs neither never next no none nor not nothing now of off often on once
one only onto or other others otherwise our ours ourselves out over own per
quite rather really same see seen shall she should since so some something
sometimes still such than that the their theirs them themselves then there
these they this those though through thus to together too toward towards under
until up upon us use used uses using very via want wants was way we well were
what whatever when whenever where whether which while who whole whom whose why
will with within without would yet you your yours yourself yourselves
doesn isn aren wasn weren won didn don couldn wouldn shouldn hasn haven hadn
""".split())

_FENCE = re.compile(r'^\s*(```|~~~).*?^\s*\1', re.S | re.M)
_CODE = re.compile(r'`[^`\n]*`')
_LINK_TARGET = re.compile(r'\]\([^)]*\)')
_TAG = re.compile(r'<[^>\n]*>')
_URL = re.compile(r'https?://\S+')
_HEADING = re.compile(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$', re.M)
_BOLD = re.compile(r'\*\*([^*\n]+)\*\*|__([^_\n]+)__')
# A raw word: letters and digits, joined across inner hyphens and
# underscores (zero-below, Fader_1) so FuzzyMatch can split it and the
# compound survives. Apostrophes end a word ("it's" -> it).
_RAW = re.compile(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*")
_TRAIL_DIGITS = re.compile(r'\d+$')
# An acronym's plural (CHOPs, TOPs, DATs): FuzzyMatch's hump split reads the
# trailing "Ps" as a new word (cho, ps), so it is upper-cased first: CHOPS.
_ACRONYM_PLURAL = re.compile(r'^([A-Z]{2,})s$')

_fm = None


def _fuzzy():
    """scripts/shared/FuzzyMatch.py, loaded by path once."""
    global _fm
    if _fm is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(here), 'scripts', 'shared', 'FuzzyMatch.py')
        spec = importlib.util.spec_from_file_location('FuzzyMatch_searchindex', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _fm = mod
    return _fm


def _keep(word):
    """The form a folded word is indexed under, or None to drop it."""
    w = _TRAIL_DIGITS.sub('', word)
    if len(w) < MIN_LEN or not w[0].isalpha() or w in STOPWORDS:
        return None
    return w


def Words(text):
    """The indexable words of a piece of prose, folded, in order, with repeats.

    ChopBank -> chop, bank, chopbank; zero-below -> zero, below, zerobelow.
    """
    fm = _fuzzy()
    out = []
    for raw in _RAW.findall(text or ''):
        parts = fm.words(_ACRONYM_PLURAL.sub(r'\1S', raw))
        for part in parts:
            w = _keep(part)
            if w:
                out.append(w)
        if len(parts) > 1:
            w = _keep(''.join(parts))
            if w:
                out.append(w)
    return out


def _frontmatter(text):
    """(frontmatter lines, the rest) of a doc; no YAML parser needed."""
    if not text.startswith('---'):
        return [], text
    end = text.find('\n---', 3)
    if end < 0:
        return [], text
    return text[3:end].splitlines(), text[end + 4:]


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in '\'"':
        value = value[1:-1].replace("''", "'")
    return value


def DocTiers(text):
    """(head words, body words) of one doc, each a list in order with repeats."""
    front, rest = _frontmatter(text)
    head_text = []
    for line in front:
        s = line.strip()
        if s.startswith('summary:'):
            head_text.append(_unquote(s[len('summary:'):]))
        elif s.startswith('- name:') or s.startswith('name:'):
            head_text.append(_unquote(s.split(':', 1)[1]))
    prose = _FENCE.sub(' ', rest)
    prose = _CODE.sub(' ', prose)
    prose = _LINK_TARGET.sub(']', prose)
    prose = _URL.sub(' ', prose)
    prose = _TAG.sub(' ', prose)
    head_text.extend(m.group(1) for m in _HEADING.finditer(prose))
    head_text.extend(m.group(1) or m.group(2) for m in _BOLD.finditer(prose))
    head = Words(' '.join(head_text))
    body = Words(prose)
    return head, body


_FEATURE_LIST = re.compile(r'^feature_list:\s*$')
_FEATURE_NAME = re.compile(r'^\s*-\s+name:\s*(.*)$')


def FeatureLeads(text):
    """The folded first word of every feature_list name in a doc, as a set.

    Only the first raw word counts: "Per-channel processing blocks" leads
    with per, a stopword, so it gives nothing, never channel.
    """
    front, _ = _frontmatter(text)
    fm = _fuzzy()
    out, inside = set(), False
    for line in front:
        if _FEATURE_LIST.match(line):
            inside = True
            continue
        if inside and line[:1].strip():          # the next top-level key
            inside = False
        if not inside:
            continue
        m = _FEATURE_NAME.match(line)
        if not m:
            continue
        raw = _RAW.findall(_unquote(m.group(1)))
        parts = fm.words(_ACRONYM_PLURAL.sub(r'\1S', raw[0])) if raw else []
        w = _keep(parts[0]) if parts else None
        if w:
            out.add(w)
    return out


_FEATURE_ITEM = re.compile(r'^\s*-\s+(\w+):\s*(.*)$')
_FEATURE_KEY = re.compile(r'^\s+(\w+):\s*(.*)$')
_MD_LINK = re.compile(r'\[([^\]]+)\]\([^)]*\)')
_MD_BOLD = re.compile(r'\*\*([^*]+)\*\*')


def FeatureLines(text):
    """Every feature_list entry of a doc as one plain line, "name: does", in
    order: what the picker's opened card lists (docs/FinderAndToolRow.md).

    Plain text, since the picker draws it with textContent: backticks, link
    targets and bold markers go, the same as the site build's plainDoes. An
    entry without both a name and a does line is left out; the site build
    refuses such a doc anyway.
    """
    front, _ = _frontmatter(text)
    entries, inside = [], False
    for line in front:
        if _FEATURE_LIST.match(line):
            inside = True
            continue
        if inside and line[:1].strip():          # the next top-level key
            inside = False
        if not inside:
            continue
        m = _FEATURE_ITEM.match(line)
        if m:
            entries.append({m.group(1): _unquote(m.group(2))})
            continue
        m = _FEATURE_KEY.match(line)
        if m and entries:
            entries[-1][m.group(1)] = _unquote(m.group(2))
    out = []
    for e in entries:
        name, does = e.get('name', '').strip(), e.get('does', '').strip()
        if not name or not does:
            continue
        does = _MD_BOLD.sub(r'\1', _MD_LINK.sub(r'\1', does.replace('`', '')))
        out.append('%s: %s' % (name, does))
    return out


def CardWords(row):
    """Every word a manifest row's card fields already answer to."""
    fam = row.get('family') or {}
    texts = [row.get('name', ''), row.get('title', ''), row.get('description', ''),
             fam.get('op_label', ''), fam.get('op_name', ''), fam.get('summary', '')]
    texts.extend(fam.get('search_words') or [])
    texts.extend(row.get('search_words') or [])   # the catalog's own tags
    return set(Words(' '.join(str(t) for t in texts if t)))


def DocPath(docs_dir, name):
    return os.path.join(docs_dir, name + '.md')


def NameWords(row):
    """The words a row's own name fields answer to: name, title, op_label."""
    fam = row.get('family') or {}
    texts = [row.get('name', ''), row.get('title', ''), fam.get('op_label', '')]
    return set(Words(' '.join(str(t) for t in texts if t)))


def BuildIndex(rows, docs_dir):
    """{package name: {'head': str, 'body': str[, 'lead': str]}} for every
    row with a doc.

    `rows` are manifest package rows (only name, title, description and family
    are read). The common-word cut counts every doc in docs_dir, not only the
    rows passed, so indexing a subset gives the same words as indexing all.

    A lead word leaves head and body: the picker scores it higher as a lead,
    so it would only be carried twice. It also leaves out what the row's own
    name answers to, which outranks it anyway.
    """
    tiers, leads = {}, {}
    for fn in sorted(os.listdir(docs_dir)):
        if not fn.endswith('.md'):
            continue
        with io.open(os.path.join(docs_dir, fn), encoding='utf-8') as f:
            text = f.read()
        tiers[fn[:-3]] = DocTiers(text)
        leads[fn[:-3]] = FeatureLeads(text)
    df = {}
    for head, body in tiers.values():
        for w in set(head) | set(body):
            df[w] = df.get(w, 0) + 1
    limit = COMMON_SHARE * max(len(tiers), 1)
    common = {w for w, n in df.items() if n > limit}

    out = {}
    for row in rows:
        name = row.get('name')
        if name not in tiers:
            continue
        head, body = tiers[name]
        lead = leads[name] - NameWords(row)
        drop = common | CardWords(row) | lead
        h = set(head) - drop
        b = set(body) - drop - h
        out[name] = {'head': ' '.join(sorted(h)), 'body': ' '.join(sorted(b))}
        if lead:
            out[name]['lead'] = ' '.join(sorted(lead))
    return out


def Sizes(index):
    """(raw bytes, gzipped bytes) of an index as the manifest would carry it."""
    import gzip
    import json
    raw = json.dumps(index, separators=(',', ':')).encode('utf-8')
    return len(raw), len(gzip.compress(raw))
