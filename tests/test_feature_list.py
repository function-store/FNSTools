"""/features/: every package's features on one page, built from the docs.

website/README.md, "Features". Each doc in packaging/docs/ carries a
`feature_list:` in its frontmatter, and website/tools/build-site.mjs builds
/features/ from them. Previews (docs/PreviewPackages.md) are left out unless
FNS_SHOW_PREVIEWS=1, which the CMS's Build site sets and the public build
never does. Pinned here:

  1. the source: every released package lists its features, each entry has a
     name and a `does` line, uses only the known keys and keeps house style;
  2. the build: the flag, its safe default, the refusal for a bad anchor, the
     output path, the links into the page, and that the CMS sets the flag;
  3. a local build, when there is one: built without the flag, it names no
     preview and links every released package that lists features.

Anchors are checked by the build itself (a bad one refuses it), so they are
not re-derived here.

    python tests/test_feature_list.py
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []
KEYS = {'name', 'anchor', 'does', 'authors', 'platform'}
STYLE = re.compile(r'—|(?<=\S) -- (?=\S)|\brather than\b', re.I)


def check(label, ok, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + label + ('' if ok else '   ' + str(detail)[:300]))
    if not ok:
        FAILS.append(label)


def read(*parts):
    return io.open(os.path.join(ROOT, *parts), encoding='utf-8').read().replace('\r\n', '\n')


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if len(v) >= 2 and v[0] == v[-1] == '"':
        return json.loads(v)
    return v


def feature_list(text):
    """The doc's feature_list as a list of dicts, or None when it has none.
    Reads the block js-yaml writes (the CMS saves through it): '- key: value'
    items with one 'key: value' per line. Anything else raises, so a doc
    written some other way fails loudly instead of reading as empty."""
    m = re.match(r'---\n([\s\S]*?)\n---\n', text)
    if not m:
        return None
    lines = m.group(1).split('\n')
    if 'feature_list:' not in lines:
        return None
    out = []
    for line in lines[lines.index('feature_list:') + 1:]:
        if not line.startswith(' '):
            break
        s = line.strip()
        if s.startswith('- '):
            out.append({})
            s = s[2:]
        if not out or ':' not in s:
            raise ValueError('unreadable feature_list line: %r' % line)
        k, v = s.split(':', 1)
        out[-1][k.strip()] = unquote(v)
    return out


catalog = json.loads(read('packaging', 'catalog.json'))
packages = catalog['packages']
released = [n for n, e in packages.items() if e.get('preview') is not True]
previews = [n for n, e in packages.items() if e.get('preview') is True]
docs = {}
for n in packages:
    path = os.path.join(ROOT, 'packaging', 'docs', n + '.md')
    if os.path.exists(path):
        try:
            docs[n] = feature_list(read('packaging', 'docs', n + '.md'))
        except ValueError as e:
            docs[n] = e

print('1. the source: feature_list in every doc')
unreadable = [(n, str(v)) for n, v in docs.items() if isinstance(v, ValueError)]
check('every feature_list parses', not unreadable, unreadable)
lists = {n: v for n, v in docs.items() if isinstance(v, list)}
check('every released package lists its features',
      not [n for n in released if not lists.get(n)], [n for n in released if not lists.get(n)])
bad = []
for n, items in lists.items():
    for i, f in enumerate(items):
        if set(f) - KEYS:
            bad.append('%s[%d] unknown %s' % (n, i, sorted(set(f) - KEYS)))
        if not f.get('name') or not f.get('does'):
            bad.append('%s[%d] needs name and does' % (n, i))
        if f.get('anchor') is not None and not re.match(r'^[a-z0-9-]+$', f['anchor']):
            bad.append('%s[%d] anchor %r is not a slug' % (n, i, f['anchor']))
check('entries have a name and a does line, and only known keys', not bad, bad)
styled = [(n, f['name']) for n, items in lists.items() for f in items
          if STYLE.search(f.get('name', '') + ' ' + f.get('does', ''))]
check('house style: no em-dash, " -- " or "rather than"', not styled, styled)

print('2. the build')
site = read('website', 'tools', 'build-site.mjs')
check('the flag is FNS_SHOW_PREVIEWS=1', "const SHOW_PREVIEWS = process.env.FNS_SHOW_PREVIEWS === '1';" in site)
check('previews are kept only under the flag',
      "const previewPages = SHOW_PREVIEWS ? pages.filter((p) => curated[p.name].preview === true) : [];" in site)
check('the page lists released pages plus previewPages',
      'const listed = [...pages, ...previewPages].filter((p) => featuresOf(p).length);' in site)
check('a bad anchor refuses the build', 'is not a heading on /docs/${p.slug}/' in site)
check('writes website/features/index.html', "fs.writeFileSync(path.join(WEB, 'features', 'index.html')" in site)
check('the page says which way it was built', 'data-previews="${SHOW_PREVIEWS ?' in site)
check('a flagged build is kept out of the sitemap', '{ noindex: SHOW_PREVIEWS, toolList: true }' in site)
check('the docs sidebar links it', '<li><a href="/features/">Feature list</a></li>' in site)
check('each landing fold links its category', 'class="cat-more" href="/features/#${slugify(cat)}"' in site)
# docs/FinderAndToolRow.md: the intro's link reads "Browse all N features"
check('the landing intro links it', '<a href="/features/">Browse all <span class="js-feature-count">' in read('website', 'index.html'))
check("the CMS's Build site sets the flag", "FNS_SHOW_PREVIEWS: '1'" in read('website', 'tools', 'cms.mjs'))
check('the output is not committed', '/features/' in read('website', '.gitignore').split('\n'))
check('the hand-written guide is gone',
      not os.path.exists(os.path.join(ROOT, 'website', 'content', 'guides', 'feature-list.md')))

print('3. a local build, when there is one')
built = os.path.join(ROOT, 'website', 'features', 'index.html')
if not os.path.exists(built):
    print('  SKIP  website/features/index.html not built here (cd website && node tools/build-site.mjs)')
else:
    page = read('website', 'features', 'index.html')
    mode = re.search(r'data-previews="(\w+)"', page)
    if not mode or mode.group(1) != 'hidden':
        print('  SKIP  the local build was made with FNS_SHOW_PREVIEWS=1; rebuild without it to check')
    else:
        slug = lambda n: n.lower().replace('_', '-')
        title = lambda n: packages[n].get('title') or (n[4:] if n.startswith('FNS_') else n)
        named = [n for n in previews if '/docs/%s/' % slug(n) in page or re.search(r'\b%s\b' % re.escape(n), page)
                 or (re.search(r'[a-z][A-Z]', title(n)) and re.search(r'\b%s\b' % re.escape(title(n)), page))]
        check('no preview is linked or named', not named, named)
        unlinked = [n for n in released if lists.get(n) and '<h3><a href="/docs/%s/">' % slug(n) not in page]
        check('every released package with features has its line', not unlinked, unlinked)
        want = sum(len(lists[n]) for n in released if lists.get(n))
        got = len(re.findall(r'<li(?: data-authors)?><(?:a|span) class="fl-name"', page))
        check('every feature in the docs is on the page', got == want, (got, want))

print()
if FAILS:
    print('%d FAILED: %s' % (len(FAILS), '; '.join(FAILS)))
    raise SystemExit(1)
print('all passed')
