"""Preview packages never reach the public changelog (owner, 2026-10-12).

A preview ships for the owner's testing and stays hidden from everyone else,
so release_one._writeChangelog leaves catalog packages flagged `preview` out
of the entry it writes, and the newest CHANGELOG.md section names none.

Runs outside TouchDesigner: it reads the sources.

    python tests/test_changelog_previews.py
"""
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


src = read('packaging', 'release_one.py')
body = src[src.index('def _writeChangelog('):src.index('def _clearReleaseNotes(')]
check('the changelog writer filters previews',
      'previews = _previewNames()' in body and 'if n not in previews' in body)
check('previews come from the catalog flag',
      "e.get('preview')" in src[src.index('def _previewNames('):src.index('def _writeChangelog(')])

cat = json.loads(read('packaging', 'catalog.json'))['packages']
previews = {n for n, e in cat.items() if isinstance(e, dict) and e.get('preview')}
log = read('packaging', 'CHANGELOG.md').replace('\r\n', '\n')
sections = re.split(r'\n(?=## v)', log)
newest = next(s for s in sections if s.startswith('## v'))
named = sorted(n for n in previews if re.search(r'^- %s ' % re.escape(n), newest, re.M))
check('the newest changelog section lists no preview package', not named, named)

print()
if FAILS:
    print('FAILED %d: %s' % (len(FAILS), ', '.join(FAILS)))
    sys.exit(1)
print('all passed')
