"""Search visibility for functionstore.tools: sitemap, robots.txt, sharing
tags and structured data.

docs/SiteSearchVisibility.md. Verified 2026-10-10 on a local build: 108
pages built, 108 in the sitemap, none missing either way; 103 JSON-LD
blocks (WebSite + Organization on the landing page, BreadcrumbList on 102
pages) all parse; og:url equals the canonical on every page.

The first half pins the wiring in the build script. The second half reads
the built site when there is one (`npm run build` in website/), so a run
after a build checks the output, and a run on a fresh clone checks the
wiring only.

    python tests/test_site_search.py
"""
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'website')
SITE = 'https://functionstore.tools'
FAILS = []


def check(label, ok, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + label + ('' if ok else '   ' + str(detail)[:300]))
    if not ok:
        FAILS.append(label)


def read(*parts):
    return io.open(os.path.join(ROOT, *parts), encoding='utf-8').read().replace('\r\n', '\n')


site = read('website', 'tools', 'build-site.mjs')
landing = read('website', 'index.html')
ignore = read('website', '.gitignore')

print('1. the build')
check('head() puts every indexable page in the sitemap',
      'if (!noindex) sitemapUrls.add(canonical);' in site)
check('a noindex page says so', "noindex ? 'noindex, follow' : 'index, follow'" in site)
check('a community draft is noindex', 'noindex: t.draft === true' in site)
check('the two pages built without head() are added by hand',
      'sitemapUrls.add(`${SITE}/`);' in site and 'sitemapUrls.add(`${SITE}/get/`);' in site)
check('a sitemap URL with no built page refuses the build',
      'sitemap URLs with no built page' in site)
check('robots.txt names the sitemap', 'Sitemap: ${SITE}/sitemap.xml' in site)
check('tool page titles carry TouchDesigner', '${forTD(p.title)} | FNSTools docs' in site)
check('the share image URL is versioned by its content', "og-image.png?v=" in site)
check('the landing page has its SEO markers',
      '<!-- SEO:START -->' in landing and '<!-- SEO:END -->' in landing)
check('the landing page carries no hand-written og:image or canonical outside the markers',
      'og:image' not in re.sub(r'<!-- SEO:START -->[\s\S]*?<!-- SEO:END -->', '', landing)
      and 'rel="canonical"' not in re.sub(r'<!-- SEO:START -->[\s\S]*?<!-- SEO:END -->', '', landing))
check('sitemap.xml and robots.txt are build output, not committed',
      '/sitemap.xml' in ignore.split('\n') and '/robots.txt' in ignore.split('\n'))

print('2. the built site')
sitemap = os.path.join(WEB, 'sitemap.xml')
if not os.path.exists(sitemap):
    print('  SKIP  no build in website/ (run `npm run build` there to check the output)')
else:
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    locs = [e.text for e in ET.parse(sitemap).getroot().iter(ns + 'loc')]
    check('sitemap lists no URL twice', len(locs) == len(set(locs)))
    check('every sitemap URL is on the site', all(u.startswith(SITE + '/') for u in locs))
    built = set()
    for dirpath, dirnames, files in os.walk(WEB):
        dirnames[:] = [d for d in dirnames if d not in ('node_modules', 'pagefind', '.vercel', '.git')]
        if 'index.html' in files:
            rel = os.path.relpath(dirpath, WEB).replace('\\', '/')
            built.add('/' if rel == '.' else '/' + rel + '/')
    listed = {u[len(SITE):] for u in locs}
    pages = {}
    for rel in built:
        pages[rel] = io.open(os.path.join(WEB, *rel.strip('/').split('/'), 'index.html'),
                             encoding='utf-8').read()
    noindex = {rel for rel, html in pages.items() if 'content="noindex' in html}
    check('every indexable built page is in the sitemap', built - noindex - listed == set(),
          sorted(built - noindex - listed))
    check('every sitemap URL has a built page', listed - built == set(), sorted(listed - built))
    check('no noindex page is in the sitemap', not (noindex & listed), sorted(noindex & listed))
    robots = io.open(os.path.join(WEB, 'robots.txt'), encoding='utf-8').read()
    check('robots.txt blocks nothing and names the sitemap',
          'Disallow' not in robots and f'Sitemap: {SITE}/sitemap.xml' in robots)

    bad, mismatched, crumbs = [], [], 0
    for rel, html in pages.items():
        head = html.split('</head>')[0]
        canon = re.search(r'rel="canonical" href="([^"]+)"', head)
        og = re.search(r'property="og:url" content="([^"]+)"', head)
        if not (canon and og and canon.group(1) == og.group(1) == SITE + rel):
            mismatched.append(rel)
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
            try:
                data = json.loads(block)
            except ValueError as e:
                bad.append(f'{rel}: {e}')
                continue
            if data.get('@type') == 'BreadcrumbList':
                crumbs += 1
                items = data['itemListElement']
                if [i['position'] for i in items] != list(range(1, len(items) + 1)) \
                        or items[-1]['item'] != SITE + rel:
                    bad.append(f'{rel}: breadcrumb trail does not end at the page')
    check('canonical, og:url and the page address agree on every page', not mismatched, mismatched)
    check('every JSON-LD block parses and every breadcrumb ends at its page', not bad, bad)
    check('tool, guide and community pages carry breadcrumbs', crumbs >= len(pages) - 10, crumbs)
    home = pages.get('/', '')
    check('the landing page names the site for Google (WebSite) and its publisher',
          '"@type":"WebSite"' in home and '"name":"FNSTools"' in home and '"@type":"Organization"' in home)

print()
print('FAIL: ' + ', '.join(FAILS) if FAILS else 'all checks pass')
sys.exit(1 if FAILS else 0)
