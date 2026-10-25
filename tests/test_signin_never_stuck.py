"""A Patreon sign-in or membership check never leaves the picker stuck.

Field report 2026-10-17: a sign-in in the in-TD picker needed "I just
pledged" (an adopted machine session carried the gate's cached answer),
and a check that never answers must not hold the page on "checking".
Every path ends on a settled sentence, a refresh, or the reader's Cancel,
with the picks and the step untouched. Walked in the browser pane against
a stand-in server (refuse, timeout, stuck, cancel, adopt, quiet retry);
this pins the source so a later edit cannot quietly undo a guard.

    python tests/test_signin_never_stuck.py
"""
import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH = os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Updater', 'ExtAuth.py')
INST = os.path.join(_ROOT, 'packaging', 'InstallerExt.py')
PAGE = os.path.join(_ROOT, 'packaging', 'configurator', 'index.html')
FAILS = []


def check(label, cond, detail=''):
    if cond:
        print('  PASS  %s' % label)
    else:
        FAILS.append(label)
        print('  FAIL  %s   %s' % (label, detail))


auth = io.open(AUTH, encoding='utf-8').read()
inst = io.open(INST, encoding='utf-8').read()
page = io.open(PAGE, encoding='utf-8').read()

print('1. the updater settles every flow')
signin = auth[auth.index('	def SignIn(self):'):auth.index('		ws = self._ensureServer()')]
check('an adopted machine session runs the forced recheck',
      'res = self.Recheck()' in signin and "'adopted the machine session; checking your membership'" in signin)
check('and settles the status when the recheck cannot start',
      "could not check your membership" in signin)
check('a reinit resets a status left "checking" by the old instance',
      "settleStaleStatus()" in auth and "TRANSITIONAL_STATUS = ('checking', 'waiting', 'finishing')" in auth
      and re.search(r"def settleStaleStatus.*?self\._setStatus\(self\.AuthStatus\(\)\)", auth, re.S) is not None)
check('Cancel drops the sign-in, the recheck wait and any armed timeout',
      re.search(r"def CancelPending.*?self\._cancelSignin\('cancelled'\).*?self\._recheck_cb = None"
                r".*?self\._gate_wait = .*?self\._setStatus\(self\.AuthStatus\(\)\)", auth, re.S) is not None)

print('2. the installer reports what really happened')
check('a refused recheck is the answer, not "Checking"',
      "res = upd.ext.ExtAuth.Recheck() or {}" in inst and "why = 'Could not check: %s'" in inst)
check('a refused sign-in is the answer too', "res = upd.ext.ExtAuth.SignIn() or {}" in inst
      and "why = str(res.get('why') or 'sign-in refused')" in inst)
check('an adopted session says so, not "finish in your browser"',
      "Signed in with this computer's Patreon " in inst)
check('a cancel route', "uri == '/auth/cancel'" in inst and 'upd.ext.ExtAuth.CancelPending()' in inst)

print('3. the picker waits, but never unbounded')
check('every wait starts through one place', 'watchAuth();' in page
      and page.count('startAuthWatch(') >= 6 and 'if (res.ok) watchAuth();' not in page)
check('a check waits a minute, a browser sign-in ten',
      'var CHECK_LIMIT_MS = 60000;' in page and 'var BROWSER_LIMIT_MS = 600000;' in page
      and 'if (Date.now() - authStarted > authLimit) {' in page)
check('an account change during a check waits for it, at most 20 s',
      'var SETTLE_LIMIT_MS = 20000;' in page
      and "&& (!settling || Date.now() - authStarted > SETTLE_LIMIT_MS)) {" in page)
check('the waiting dialog carries Cancel; a settled one does not',
      'id="dlgcancel"' in page and 'false, undefined, true, true);' in page
      and "document.getElementById('dlgcancel').hidden = !cancellable;" in page)
check('Cancel stops the wait and tells the updater',
      re.search(r"getElementById\('dlgcancel'\)\.addEventListener\('click'.*?authCancelled = true;"
                r".*?post\('/auth/cancel'", page, re.S) is not None
      and page.count('if (authCancelled) return;') >= 3)
check('one quiet retry for a brand-new pledge, once per tab',
      "sessionStorage.getItem('fns.quietrecheck')" in page and '}, 30000);' in page
      and "if (acctKey(st) !== acctKey(account)) { reloadKeepingPlace(); return; }" in page)

print()
if FAILS:
    print('%d check(s) failed:' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all sign-in checks pass')
