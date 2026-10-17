"""FNS_HotkeyManager does not flatten an expression-driven hotkey on start.

A row saved before a keyboardin started following its tool's parameter held
a constant, and setAllHotkeys wrote it back on every start: QuickMarks lost
Alt+Shift+M that way, and ResetPLS, QuickPane and ParOPDrop had their
followers turned into constants (2026-10-12).

Runs outside TouchDesigner: it reads the source.

    python tests/test_hotkey_follower.py
"""
import io
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_HotkeyManager',
                           'HotkeyManagerExt.py'), encoding='utf-8').read()
body = src[src.index('def setAllHotkeys'):src.index('def _isPackageSource')]
ok = ("if (not _expr and _par.mode == ParMode.EXPRESSION and _par.expr" in body
      and "'app.osName' not in _par.expr):" in body
      and body.index("'app.osName' not in _par.expr") < body.index('_par.val = _val'))
print('  %s  a stored constant never overwrites a follower expression' % ('PASS' if ok else 'FAIL'))
if not ok:
    sys.exit(1)
print('all passed')
