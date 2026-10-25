"""Pre-commit reminder: new per-frame Python that says nothing about Perform.

docs/PerformMode.md section 6. Called by scripts/hooks/pre-commit; it only
warns, the commit always proceeds. A staged .py under modules/suspects/
is flagged when it GAINS per-frame work this commit:

  - an onFrameStart / onFrameEnd callback with a real body (the Execute
    DAT template's `return` stubs do not count), or
  - a self-rescheduling loop: a function that hands itself back to run()
    (`run('...myTick()', delayFrames=1)`, `run(self.myTick, ...)`).

and its text mentions neither `Perform` nor a `fns_perform` / `fns_show`
tag. A frame DAT tagged in TouchDesigner carries its tag in the tox, not in
the .py, so a tagged one can be reported here; the Preflight audits are
the gate (perform_audit.py reads the tags live, perform_cook_audit.py
measures). Everything else that cooks every frame has no Python to read,
and only the cook audit sees it.

    python scripts/perform_commit_check.py          # the staged files
"""

import ast
import subprocess
import sys

FRAME_CALLBACKS = ('onFrameStart', 'onFrameEnd')
MENTIONS = ('Perform', 'fns_perform', 'fns_show')


def _git(*args):
    r = subprocess.run(('git',) + args, capture_output=True)
    return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None


def _trivial(fn):
    """A body of docstring, pass and bare returns only: the template stub."""
    for st in fn.body:
        if isinstance(st, ast.Pass):
            continue
        if isinstance(st, ast.Return) and (st.value is None or isinstance(st.value, ast.Constant)):
            continue
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant):
            continue
        return False
    return True


def _reschedulesItself(fn):
    for node in ast.walk(fn):
        if not (isinstance(node, ast.Call) and node.args):
            continue
        f = node.func
        if not ((isinstance(f, ast.Name) and f.id == 'run')
                or (isinstance(f, ast.Attribute) and f.attr == 'run')):
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            if fn.name + '(' in first.value:
                return True
        elif isinstance(first, ast.JoinedStr):
            if any(isinstance(v, ast.Constant) and fn.name + '(' in str(v.value)
                   for v in first.values):
                return True
        elif isinstance(first, ast.Name) and first.id == fn.name:
            return True
        elif isinstance(first, ast.Attribute) and first.attr == fn.name:
            return True
    return False


def FrameWork(src):
    """The per-frame work a source defines, as a set of labels."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in FRAME_CALLBACKS and not _trivial(node):
                found.add(node.name + ' callback')
            elif _reschedulesItself(node):
                found.add(node.name + ' reschedules itself through run()')
    return found


def main():
    names = _git('diff', '--cached', '--name-only', '--diff-filter=AM',
                 '--', 'modules/suspects')
    if not names:
        return 0
    hits = []
    for path in names.split():
        if not path.endswith('.py'):
            continue
        staged = _git('show', ':' + path)
        if staged is None or any(m in staged for m in MENTIONS):
            continue
        before = _git('show', 'HEAD:' + path) or ''
        gained = sorted(FrameWork(staged) - FrameWork(before))
        if gained:
            hits.append((path, gained))
    if hits:
        print('perform mode: new per-frame work that does not read Perform:', file=sys.stderr)
        for path, gained in hits:
            print('  %s: %s' % (path, ', '.join(gained)), file=sys.stderr)
        print("  gate it on the root's Perform, or tag the DAT fns_perform / fns_show "
              '(fns-definition-of-done, "Per-frame work answers to Perform Mode")', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
