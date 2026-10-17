"""RegistryBase re-fetches the tool's Registry page after sorting the pages.

A TD Page is an index: after sortCustomPages the Page object held across the
sort names whatever now sits at its old slot. _ensureToolRegistryPage held it
and appended every promoted par onto the tool's About page (reported by the
TDCollab session, reproduced on a throwaway COMP, 2026-10-13; backlog 35).

Runs outside TouchDesigner: it reads the source.

    python tests/test_registrybase_page_ref.py
"""
import io
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(_ROOT, 'scripts', 'shared', 'RegistryBase.py'), encoding='utf-8-sig').read()
FAILS = []


def check(label, ok):
    print('  %s  %s' % ('PASS' if ok else 'FAIL', label))
    if not ok:
        FAILS.append(label)


body = src.split('def _ensureToolRegistryPage', 1)[1].split('\n\tdef ', 1)[0]
sort_at = body.find('self._orderToolRegistryPage(tool)')
check('the ensure path still orders the pages', sort_at >= 0)
after = body[sort_at:]
refetch = re.search(r"page = next\(\(pg for pg in tool\.customPages if pg\.name == self\.TOOL_PAGE_NAME\)", after)
first_append = after.find('page.append')
check('the Registry page is looked up by name again after the sort', refetch is not None)
check('...before anything is appended to it',
      refetch is not None and (first_append < 0 or refetch.start() < first_append))
check('pages are sorted in one place only', src.count('sortCustomPages(') == 1)
print()
if FAILS:
    print('FAILED %d' % len(FAILS))
    sys.exit(1)
print('all passed')
