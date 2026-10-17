"""A registry host with nothing to clone from must switch cloning off
before any par is written (docs/DeveloperKit.md, "Without a toolkit root").

Enable Cloning on with an empty Clone par crashes TD natively on the next
custom-par write (bisected 2026-10-11). StampHost wires every host's clone
as a guarded op.FNS expression, so a host in a project without a toolkit
root (a registry tox dropped alone, a standalone copy of a tool) sits in
exactly that state. RegistryBase._ensureCloneSane is the guard, and it has
to run first.

    python tests/test_registry_host_guard.py
"""
import io
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


src = io.open(os.path.join(_ROOT, 'scripts', 'shared', 'RegistryBase.py'), encoding='utf-8').read()
init = src[src.index('\tdef __init__(self, ownerComp):'):]
init = init[:init.index('\n\tdef ', 1)]
guard = src[src.index('\tdef _ensureCloneSane(self):'):]
guard = guard[:guard.index('\n\tdef ', 1)]

print('1. the guard runs first')
check('_ensureCloneSane is the first call in __init__, right after ownerComp is set',
      re.search(r"def __init__\(self, ownerComp\):\n\t\tself\.ownerComp = ownerComp\n(\t\t#[^\n]*\n)*\t\tself\._ensureCloneSane\(\)\n", init) is not None)
check('it runs before the dangling-bind repair (the first par access)',
      init.index('self._ensureCloneSane()') < init.index('self._repairDanglingHostBinds()'))

print('2. what it does')
check('cloning off while the clone reads None',
      'if enabled and target is None:' in guard and 'c.par.enablecloning = False' in guard)
check('cloning back on only for a clone the registry wired itself, once it resolves',
      'elif not enabled and ours and target is not None:' in guard
      and 'c.par.clone.expr == self.CLONE_EXPR' in guard and 'c.par.enablecloning = True' in guard)
check('a failure in the guard never kills init', 'except Exception as e:' in guard)

print('3. StampHost still wires the guarded clone the guard expects')
stamp = src[src.index('\tdef StampHost('):]
stamp = stamp[:stamp.index('\n\tdef ', 1)]
check('the host clone is the registry expression with cloning on',
      'host.par.clone.expr = self.CLONE_EXPR' in stamp and 'host.par.enablecloning = True' in stamp)

print()
if FAILS:
    print('%d FAILED: %s' % (len(FAILS), '; '.join(FAILS)))
    sys.exit(1)
print('all registry host guard checks pass')
