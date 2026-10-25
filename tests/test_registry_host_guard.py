"""A registry host with nothing to clone from must switch cloning off
before any par is written (docs/DeveloperKit.md, "Without a toolkit root"),
and outside the dev checkout a host clones nothing at all
(docs/RegistryHostsFrozen.md).

Enable Cloning on with an empty Clone par crashes TD natively on the next
custom-par write (bisected 2026-10-11). StampHost wires a dev host's clone
as a guarded op.FNS expression, so a host in a project without a toolkit
root (a registry tox dropped alone, a standalone copy of a tool) sits in
exactly that state. RegistryBase._ensureCloneSane is the guard, and it has
to run first.

A released host is a frozen copy: the export drops its clone link
(pre_release_common), the guard freezes one an older install had cloned,
and neither the heal nor StampHost re-links a host outside the dev
checkout -- the dev checkout being the toolkit root bound to
modules/suspects/FNSTools.tox.

    python tests/test_registry_host_guard.py
"""
import glob
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


def method(src, head):
    body = src[src.index(head):]
    return body[:body.index('\n\tdef ', 1)]


src = io.open(os.path.join(_ROOT, 'scripts', 'shared', 'RegistryBase.py'), encoding='utf-8').read()
init = method(src, '\tdef __init__(self, ownerComp):')
guard = method(src, '\tdef _ensureCloneSane(self):')
heal = method(src, '\tdef _healHostClones(self):')
stamp = method(src, '\tdef StampHost(')
dev = method(src, '\tdef _devCheckout(cls):')

print('1. the guard runs first')
check('_ensureCloneSane is the first call in __init__, right after ownerComp is set',
      re.search(r"def __init__\(self, ownerComp\):\n\t\tself\.ownerComp = ownerComp\n(\t\t#[^\n]*\n)*\t\tself\._ensureCloneSane\(\)\n", init) is not None)
check('it runs before the dangling-bind repair (the first par access)',
      init.index('self._ensureCloneSane()') < init.index('self._repairDanglingHostBinds()'))

print('2. what it does')
check('cloning off while the clone reads None',
      'if enabled and target is None:' in guard and 'c.par.enablecloning = False' in guard)
check('an expression that raises (a root being torn down) counts as nothing to clone',
      re.search(r"try:\n\t+target = p\.eval\(\)\n\t+except Exception:\n\t+target = None", guard) is not None)
check('cloning back on only for a clone the registry wired itself, once it resolves',
      'elif not enabled and ours and target is not None:' in guard
      and 'p.expr == self.CLONE_EXPR' in guard and 'c.par.enablecloning = True' in guard)
check('a failure in the guard never kills init', 'except Exception as e:' in guard)

print('3. outside the dev checkout a host is frozen')
check('the dev checkout is the root bound to the repo suspect file',
      "_DEV_ROOT_TOX = 'modules/suspects/FNSTools.tox'" in src and 'endswith(cls._DEV_ROOT_TOX)' in dev)
freeze = guard[guard.index('if linked and root is not None and not self._devCheckout():'):]
freeze = freeze[:freeze.index('return')]
check('the guard freezes a toolkit-linked host where a root exists and it is not the dev one',
      'p.val = \'\'' in freeze)
check('it switches cloning off BEFORE clearing the link (never on with an empty clone)',
      freeze.index('c.par.enablecloning = False') < freeze.index("p.val = ''"))
check('the root lookup cannot raise on a root being torn down',
      "root = tdu.tryExcept(lambda: getattr(op, 'FNS', None), None)" in guard)
check('the base heal re-links hosts in the dev checkout only',
      'not self._devCheckout()' in heal.split('\n\t\tmaster')[0])
tb = io.open(os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_ToolbarRegistry',
                          'ToolbarRegistryExt.py'), encoding='utf-8').read()
tb_heal = method(tb, '\tdef _healHostClones(self):')
check('the toolbar heal (which converts EMPTY constants) is gated the same way',
      'if not self._is_sys_global() or not self._devCheckout():' in tb_heal)
check('StampHost wires the clone only in the dev checkout',
      'if self.CLONE_EXPR and self._devCheckout():' in stamp
      and 'host.par.clone.expr = self.CLONE_EXPR' in stamp)
frozen_stamp = stamp[stamp.index('if self.CLONE_EXPR and self._devCheckout():'):]
frozen_stamp = frozen_stamp[frozen_stamp.index('else:'):frozen_stamp.index('host.par.initextonstart = True')]
check('anywhere else StampHost stamps a frozen host, cloning off first',
      frozen_stamp.index('host.par.enablecloning = False') < frozen_stamp.index("host.par.clone.val = ''"))

print('4. the clone expression survives a deleted root')
exts = sorted(glob.glob(os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', '*', '*Ext.py')))
found, legacy = [], []
for path in exts:
    text = io.open(path, encoding='utf-8').read()
    for m in re.finditer(r'^\tCLONE_EXPR = (.+)$', text, re.M):
        found.append((os.path.basename(path), m.group(1)))
        if "hasattr(op, 'FNS')" in m.group(1):
            legacy.append(os.path.basename(path))
check('eleven registries set CLONE_EXPR', len(found) == 11, str(len(found)))
check('every one is tdu.tryExcept(lambda: op.FNS.op(...), None)',
      all(re.fullmatch(r"\"tdu\.tryExcept\(lambda: op\.FNS\.op\('FNS_\w+'\), None\)\"", e) for _, e in found),
      '; '.join(n for n, e in found if 'tryExcept' not in e))
check('none keeps the legacy hasattr form', not legacy, ', '.join(legacy))

print('5. every artifact ships its toolkit clone links frozen')
common = io.open(os.path.join(_ROOT, 'packaging', 'pre_release_common.py'), encoding='utf-8').read()
block = common[common.index('# --- clone links into the toolkit ship frozen'):]
block = block[:block.index('# --- logger FIFOs')]
check('pre_release_common clears toolkit clone links and switches cloning off',
      "_cp.val = ''" in block and '_cc.par.enablecloning = False' in block)
check("TouchDesigner's own clones (op.TD...) are left alone", "startswith('op.TD')" in block)
check('a host a tool hook already emptied ships with cloning OFF, not on with nothing to clone',
      "_cc.par['Regstatus'] is not None and _cc.par.enablecloning.eval()" in block)

print('6. the bootstrap rail gets the same release scrub as a package')
bi = io.open(os.path.join(_ROOT, 'packaging', 'build_installer.py'), encoding='utf-8').read()


def function(src, name):
    """A module-level function's text, up to the next top-level def or EOF."""
    body = src[src.index('\ndef %s(' % name):]
    end = body.find('\ndef ', 1)
    return body if end < 0 else body[:end]


boot = function(bi, 'BuildBootstrap')
scrub = function(bi, '_exportScrubbed')
check('BuildBootstrap exports through _exportScrubbed, not the bare _export',
      '_exportScrubbed(root, out_path, stage)' in boot and 'info = _export(root' not in boot)
check('the staged root gets a pre_release hook that runs pre_release_common',
      "comp.create(textDAT, 'pre_release')" in scrub and 'hook.text = BOOTSTRAP_PRE_RELEASE' in scrub
      and "exec(open('packaging/pre_release_common.py').read())" in bi)
check('the written file goes through build_manifest.ScrubArtifact (PI markers)',
      "_buildManifest()['ScrubArtifact'](info['out'])" in scrub)
check('a failed scrub fails the build', "info['exported'] = False" in scrub)
check('build_manifest is exec\'d in its own namespace, never into this file\'s globals',
      'exec(f.read(), ns)' in bi)

print()
if FAILS:
    print('%d FAILED: %s' % (len(FAILS), '; '.join(FAILS)))
    sys.exit(1)
print('all registry host guard checks pass')
