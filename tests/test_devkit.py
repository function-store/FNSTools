"""The developer kit (docs/DeveloperKit.md): the eleven registries, each as
its own tox, zipped with a README and the licence, built by BuildDevKit()
and shipped as a third rail.

Pins the pieces that have to stay in step across files: the registry list
build_installer builds from and release_one reports staleness against,
the rail's name in publish, upload and release_one, the site's link, and
what the kit must never carry (the console, the hub, the updater, the
installer).

    python tests/test_devkit.py
"""
import io
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def read(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8').read()


def check(label, cond, detail=''):
    if cond:
        print('  PASS  %s' % label)
    else:
        FAILS.append(label)
        print('  FAIL  %s   %s' % (label, detail))


def packages(src, label):
    m = re.search(r'DEVKIT_PACKAGES = \((.*?)\)', src, re.S)
    assert m, 'no DEVKIT_PACKAGES in ' + label
    return re.findall(r"'([A-Za-z_]+)'", m.group(1))


bi = read('packaging', 'build_installer.py')
ro = read('packaging', 'release_one.py')
pub = read('packaging', 'publish.py')
up = read('packaging', 'upload.py')
site = read('website', 'index.html')
guide = read('website', 'content', 'guides', 'getting-started.md')
readme = read('README.md')
doc = read('docs', 'DeveloperKit.md')

RAIL = 'FNSTools-DevKit.zip'
build = bi.split('def BuildDevKit(')[1].split('\ndef ')[0]

print('1. the registry list is one list')
kit = packages(bi, 'build_installer')
check('eleven registries', len(kit) == 11, kit)
check('every name is a registry', all(n.endswith('Registry') for n in kit), kit)
check('release_one keeps the same list', packages(ro, 'release_one') == kit)
surf = re.findall(r"\('(FNS_\w+)', ", bi.split('DEVKIT_SURFACES = (')[1].split('\n)')[0])
check('the README table names every registry once', sorted(surf) == sorted(kit), surf)
for out in ('FNS_Console', 'FNS_Hub', 'FNS_Updater', 'FNS_Installer', 'FNS_OverlayRegistry'):
    check('%s stays out of the kit' % out, out not in kit)

print('2. the build')
check('BuildDevKit exists and writes the rail',
      'def BuildDevKit(out_path=OUT_DEVKIT):' in bi and "DEVKIT_RAIL = '%s'" % RAIL in bi)
check('it is a zip of separate toxes, no TD staging',
      "zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)" in build
      and "z.write(_repo('packaging', 'dist', name + '.tox'), name + '.tox')" in build
      and '_stage(' not in build and 'loadTox' not in build)
check('the README and the licence ride in the zip',
      "z.writestr('README.md', DEVKIT_README.format(release=release, table=table))" in build
      and "z.writestr('LICENSE.txt', notices)" in build)
check('the kit refuses to build from missing dist toxes',
      "'dist toxes missing: %s -- run Build() first'" in bi)
check('the README says a host keeps its own copy without a root, and to delete the loose registries first',
      'keeps its own copy of the' in bi and 'delete the loose registries first' in bi)
check('the README stamps from the dropped master, not the /sys global',
      "op('/FNS_ToolbarRegistry').StampHost(op('/my_tool'))" in bi)
check('the version recorded is the toolkit release',
      '_recordRailVersionAs(os.path.basename(out_path), release)' in build
      and 'def _toolkitRelease():' in bi)

print('3. the rail')
check('publish hashes it into the manifest rails',
      "for rail in ('FNS_Installer.tox', 'FNSTools.tox', '%s'):" % RAIL in pub)
check('publish reports it when missing', "'%s')" % RAIL in pub.split("'rails_missing'")[1][:200])
check('upload prunes it with the other rails', "'%s'," % RAIL in up)
check('release_one counts it among the rail artifacts',
      "('packaging', 'dist', '%s'))" % RAIL in ro and "DEVKIT_RAIL = '%s'" % RAIL in ro)
check('its staleness answers to the registry artifacts, not the installer sources',
      'newest = newest_kit if parts[-1] == DEVKIT_RAIL else newest_src' in ro
      and "DEVKIT_SOURCES = (('packaging', 'build_installer.py'),) + tuple(" in ro)
check('nothing still names the one-tox kit',
      'FNSTools-DevKit.tox' not in bi + ro + pub + up + site + guide + readme)

print('4. the site and the README')
link = 'https://storage.functionstore.tools/fnstools/latest/%s' % RAIL
check('the Get section links the latest alias', link in site)
check('the kit link is not a toolkit download button (the alias test counts those)',
      not re.search(r'js-fns-download[^>]*%s' % re.escape(RAIL), site)
      and not re.search(r'%s[^>]*js-fns-download' % re.escape(RAIL), site))
check('the getting-started guide has the section', '## Building a tool against FNSTools' in guide and link in guide)
check('the repository README has the section', '## For tool developers' in readme and link in readme)

print('5. the record')
check('docs/DeveloperKit.md is open and names the rail', 'status: open' in doc and RAIL in doc)

print()
if FAILS:
    print('%d FAILED: %s' % (len(FAILS), '; '.join(FAILS)))
    sys.exit(1)
print('all developer-kit checks pass')
