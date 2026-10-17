"""New tools are announced once, and family operators stay current.

docs/NewToolsAndFamilyFreshness.md. Field report 2026-09-25: after an
update the FNS tab showed nothing new, and nothing told the user that a
release had added tools.

Part 1 runs the installer's seen-list rules (UnseenTools, MarkSeen) on a
scratch palette, with the first-install cases the owner asked to watch:
a first run is shown nothing, an install with no record yet sees only the
tools this release line introduced that it does not have, and after that
whatever the record lacks. Parts 2 to 4 pin the wiring in the installer,
the updater, the picker and the console.

    python tests/test_new_tools.py
"""
import io
import json
import os
import re
import tempfile

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INS = os.path.join(_ROOT, 'packaging', 'InstallerExt.py')
UPD = os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Updater', 'ExtUpdater.py')
PAGE = os.path.join(_ROOT, 'packaging', 'configurator', 'index.html')
CONSOLE = os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Console', 'console_page.html')
CALLBACKS = os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Console', 'console_server_callbacks.py')
FAILS = []


def check(label, cond, detail=''):
    print(('  PASS  ' if cond else '  FAIL  ') + label + ('' if cond else '   ' + str(detail)[:200]))
    if not cond:
        FAILS.append(label)


def read(p):
    return io.open(p, encoding='utf-8').read()


ins = read(INS)
block = ins[ins.index('# --- tools this machine has been shown'):ins.index('# --- pure helpers (no COMP required)')]
ns = {'os': os, 'json': json, '_fnsPaletteRoot': lambda: ''}
exec(compile(block, 'seen', 'exec'), ns)
Unseen, Seen, Mark = ns['UnseenTools'], ns['SeenPackages'], ns['MarkSeen']
Announce, SetAnnounce = ns['AnnounceNewTools'], ns['SetAnnounceNewTools']

MAN = {'packages': [
    {'name': 'A', 'kind': 'tool', 'whatsnew': 'tooltips.'},
    {'name': 'B', 'kind': 'tool', 'whatsnew': 'new package (Base). Does B.'},
    {'name': 'C', 'kind': 'tool', 'whatsnew': 'New package. Does C.'},
    {'name': 'Core1', 'kind': 'core'},
    {'name': 'Fam', 'kind': 'tool', 'companion': 'family', 'whatsnew': 'new package'},
]}


def pal():
    return tempfile.mkdtemp(prefix='fns-seen-').replace('\\', '/')


print('1. the seen list, first installs first')
r = pal()
check('a first run is shown nothing', Unseen(MAN, (), firstrun=True, root=r) == [])
check('and records every tool as shown', Seen(r) == ['A', 'B', 'C'], Seen(r))
check('companions and core are never tools to announce', 'Fam' not in Seen(r) and 'Core1' not in Seen(r))

r = pal()
got = Unseen(MAN, installed=['C'], firstrun=False, root=r)
check('no record yet: only introduced tools it does not have', got == ['B'], got)
check('the baseline holds everything else', Seen(r) == ['A', 'C'], Seen(r))
check('asking again without answering still shows them', Unseen(MAN, (), root=r) == ['B'])

Mark(['B'], root=r)
check('answered: nothing left', Unseen(MAN, (), root=r) == [])
MAN2 = {'packages': MAN['packages'] + [{'name': 'D', 'kind': 'tool', 'whatsnew': 'tooltips.'}]}
check('the next release shows only what it adds', Unseen(MAN2, (), root=r) == ['D'])
check('the record lives in the palette config folder',
      os.path.isfile(r + '/config/seen_packages.json'))
check('the window opens by itself unless turned off', Announce(r) is True)
SetAnnounce(False, root=r)
Mark(['D'], root=r)
check('turning it off survives marking tools shown', Announce(r) is False and 'D' in Seen(r))
SetAnnounce(True, root=r)
check('and it turns back on', Announce(r) is True)

# Field report 2026-10-06: a fresh machine installing through TDX Launcher
# Ultra (a headless Install, no picker) was greeted with "New since you
# last looked". Its install is a first run: everything is shown.
First = ns['RecordFirstInstall']
MAN3 = {'packages': MAN['packages'] + [{'name': 'P', 'kind': 'tool', 'preview': True,
                                        'whatsnew': 'new package'}]}
r = pal()
check('a headless first install records every current tool', First(MAN3, root=r) is True)
check('so the picker opened later shows nothing',
      Unseen(MAN3, installed=['A'], firstrun=False, root=r) == [], Unseen(MAN3, ['A'], root=r))
check('previews stay out of the record', Seen(r) == ['A', 'B', 'C'], Seen(r))
check('an existing record is never overwritten', First(MAN2, root=r) is False and 'D' not in Seen(r))
r = pal()
check('without it, a bare-root install still announces introduced tools (unchanged)',
      Unseen(MAN3, installed=['A'], firstrun=False, root=r) == ['B', 'C'])

# Field report 2026-10-07: CookBar was picked on /get and installed by the
# paste, and the picker inside TouchDesigner still opened on it ("already
# picked") -- the page and the installer keep separate records. An
# installed tool has been shown: nothing to ask, and it is recorded.
r = pal()
Mark(['A', 'B', 'C'], root=r)
MAN4 = {'packages': MAN['packages'] + [{'name': 'E', 'kind': 'tool', 'whatsnew': 'new package'},
                                       {'name': 'G', 'kind': 'tool', 'whatsnew': 'new package'}]}
got = Unseen(MAN4, installed=['A', 'E'], firstrun=False, root=r)
check('an installed new tool is not news', got == ['G'], got)
check('and it is recorded as shown', 'E' in Seen(r) and 'G' not in Seen(r), Seen(r))
check('so the next look asks only about the other', Unseen(MAN4, installed=['A'], root=r) == ['G'])

print('2. the installer')
check('manifest.js carries FNS_UNSEEN',
      "'window.FNS_UNSEEN = %s;\\n'" in ins and 'unseen = UnseenTools(json.loads(man_text), known_here, firstrun)' in ins)
check('POST /seen records, GET /newtools.json only reads',
      "uri == '/seen'" in ins and 'MarkSeen(names)' in ins
      and "uri == '/newtools.json'" in ins)
check('the console forwards both to the installer',
      "'/seen', '/newtools.json'" in read(CALLBACKS))
inst = ins[ins.index('    def Install(self, remove=None):'):ins.index('    def _firstInstallManifest(self, plan):')]
check('Install decides a first run BEFORE installing, records it after',
      inst.index('first_manifest = self._firstInstallManifest(plan)')
      < inst.index('res = InstallPlan(plan')
      < inst.index('RecordFirstInstall(first_manifest)'))
check('the first-run test is the picker\'s own',
      'return manifest if self._isFirstRun(op(plan[\'target\']), tools) else None' in ins)
check('A: a recorded family member with no file is fetched',
      "not s['present'] or s['placement'] == 'none'" in ins)

print('3. the updater keeps family members current (B)')
upd = read(UPD)
check('Compare reports a stale family member as an update',
      "if placement == 'none' and self._storeCopyStale(index.get(name)):" in upd
      and re.search(r"_storeCopyStale\(index\.get\(name\)\):.*?updates\.append\(name\)", upd, re.S) is not None)
check('stale = missing, or not the manifest bytes', "def _storeCopyStale(self, pkg, vid='base'):" in upd
      and 'return _sha256(path) != want' in upd)
check('the apply refreshes the store copy, never replaces anything',
      re.search(r"def _replacePackage.*?if \(step\.get\('placement'\) == 'none' or step\.get\('store_only'\)\) and placed is None:.*?"
                r"self\.RecordInstalled\(name, digest", upd, re.S) is not None)
check('a member still installed as a toolkit child (before it became none) is replaced in place',
      re.search(r"def _replacePackage.*?placed = root\.op\(name\) or next\(.*?_pkgName\(c\) == name\), None\)"
                r".*?and placed is None:", upd, re.S) is not None)
check('the pass still ends with the family sync', upd.count('self.SyncFamilyFolder()') >= 3)

# 2026-10-12 (owner: "just the store, not the placed operators")
_cmp = upd[upd.index('	def Compare(self'):upd.index('	def _gatedRow(self')]
check('a store-served tool (family member, op menu alternative) whose store copy is older is an update',
      "is_member or pkg.get('alternatives_for')" in _cmp and "'store_only': True" in _cmp
      and 'not os.path.exists(self._storePath(name, vid)) or not self._storeCopyStale(pkg, vid)' in _cmp)
check('it is skipped when the project holds the package itself',
      'if not name or name in reported or name in seen or root.op(name) is not None:' in _cmp)
check('the plan carries the store-only names to the apply step',
      "job['store_only'] = [r['package'] for r in cmp_['rows'] if r.get('store_only')]" in upd
      and "'store_only': name in (job.get('store_only') or ())," in upd)
check('an update records only what the project already recorded',
      re.search(r'if name in self\.Installed\(target\):\s+self\.RecordInstalled\(name, digest', upd) is not None)
check('a newer Patreon build the account lacks is gated, never counted',
      _cmp.count('self._gatedRow(') == 3 and _cmp.count('updates.append(name)') >= 3
      and "'state': 'gated'" in upd)
_sync = upd[upd.index('	def SyncFamilyFolder(self'):upd.index('	def _dropLegacyFamilyTree(self')]
check('the family folder takes a member only from bytes that match its row',
      _sync.index('if self._storeCopyStale(pkg):') < _sync.index('shutil.copyfile(src, dest)')
      and _sync.index('keep.add(side.lower())') < _sync.index('if self._storeCopyStale(pkg):'))
check('the console names the gated state', "gated: ['needs your account', 'warn']," in read(CONSOLE))

print('4. the picker and the console')
page = read(PAGE)
check('served, the installer decides; elsewhere the browser keeps the record',
      'return (window.FNS_UNSEEN || []).filter(' in page and "var SEEN_KEY = 'fns.seen';" in page)
check('a first visit or a frame records everything and shows nothing',
      "if (!stored('fns.visited', null) || FNS_EMBEDDED) { writeSeenLocal(names); return []; }" in page)
# 2026-10-17 (wizard phase 1): a banner on the set screen, not a window
# over the catalog -- the same guard decides whether it appears at all
check('never on a first run or a first visit; a banner on the set, not a window',
      'if (!firstrun && !firstVisit && announceOn && unseenAtLoad.size && !(served && locked)) {' in page
      and 'prepareNewTools();\n    renderNewBanner();' in page)
check('every answer records them as shown',
      "function seen() { markSeen(names); newNames = []; b.remove(); }" in page
      and "later.addEventListener('click', seen);" in page and page.count('seen();') >= 2)
check('unseen tools carry the New badge and the New filter', 'return unseenAtLoad.has(p.name) ||' in page)
check('the window lists only what the viewer can get (no Patreon pestering)',
      '.filter(function (p) { return p && (!isPlus(p) || entitled(p)); }).sort(byTitle);' in page)
check('and the console count follows the same rule',
      "and (access.get(n, 'free') == 'free' or n in owned))" in ins and 'def _ownedProducts(self):' in ins)
check('the banner exists, with See them and Not now',
      "b.id = 'new-tools';" in page and "show.id = 'newshow';" in page and "later.id = 'newlater';" in page)
check('a new tool already in the selection is recorded and left out (no "already picked" row)',
      'if (had.length) markSeen(had);' in page
      and 'list = list.filter(function (p) { return !picked.has(p.name); });' in page
      and page.index('list = list.filter(function (p) { return !picked.has(p.name); });')
      < page.index("if (!box || !names.length) return;"))
check('the console count leaves installed tools out too',
      'and n not in installed' in ins and 'installed |= {rec_t[i, 0].val' in ins)
check('a preference: the window opens by itself only while it is on',
      'if (!firstrun && !firstVisit && announceOn && unseenAtLoad.size' in page
      and "auto.id = 'newauto';" in page and "window.FNS_ANNOUNCE !== false" in page
      and "'window.FNS_ANNOUNCE = %s;\\n'" in ins)
check('and the New filter shows the way back', "'New-tools window: on' : 'New-tools window: off'" in page)
con = read(CONSOLE)
check('the console counts them on Install & remove',
      'data-view="view-tools"' in con and "fetch('/newtools.json'" in con
      and "if (e.data === 'fns:seen') loadNewTools();" in con)

print()
if FAILS:
    print('FAILED: %d check(s)' % len(FAILS))
    raise SystemExit(1)
print('all new-tools checks pass')
