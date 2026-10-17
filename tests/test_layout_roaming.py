"""Only a user's own layout changes roam (docs/ShippedSurfaceDefaults.md).

After the v3.2.70 update the owner's bar interleaved two numberings: the
settings file replayed an older release's layout over the new defaults
(2026-10-14). Two rules now, across five files that must agree:

- a layout value APPLIES only when it differs from the release-stamped
  default saved beside it: packaging/surface_defaults.py (stamps defaults,
  tag, state_default), FNS_ConfigRegistry (saves the default, applies only
  differences), FNS_Hub config_callbacks (schema 2, a table only when it
  differs from what shipped);
- a layout value is WRITTEN only when the user changed that surface this
  session: RegistryBase's flag, set by the Hub configurators' edits, the
  bar's group eye and the Hub's tab show/hide, never by a boot or restore;
  FNS_ConfigRegistry and config_callbacks carry an untouched surface's
  previous records over.

Runs outside TouchDesigner.

    python tests/test_layout_roaming.py
"""
import io
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(label, ok):
    print('  %s  %s' % ('PASS' if ok else 'FAIL', label))
    if not ok:
        FAILS.append(label)


def read(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8-sig').read()


def method(src, name):
    """One method's source, from its def to the next def at class level."""
    m = re.search(r"\n(\t(?:@staticmethod\n\t)?def %s\(.*?)(?=\n\t(?:@staticmethod\n\t)?def |\Z)" % name, src, re.S)
    return m.group(1) if m else ''


sd = read('packaging', 'surface_defaults.py')
cr = read('modules', 'suspects', 'FNSTools', 'FNS_ConfigRegistry', 'ConfigRegistryExt.py')
cb = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'config_callbacks.py')
rb = read('scripts', 'shared', 'RegistryBase.py')
cfgb = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'ConfiguratorBase.py')
hub = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'HubExt.py')

print('applies only as a change from the stamped default')
tag_sd = re.search(r"^LAYOUT_TAG = '([^']+)'", sd, re.M)
tag_cr = re.search(r"_LAYOUT_TAG = '([^']+)'", cr)
check('one tag name on both sides', tag_sd and tag_cr and tag_sd.group(1) == tag_cr.group(1))
st_sd = re.search(r"^STATE_DEFAULT = '([^']+)'", sd, re.M)
st_cb = re.search(r"^STATE_DEFAULT = '([^']+)'", cb, re.M)
check('one state_default table name on both sides', st_sd and st_cb and st_sd.group(1) == st_cb.group(1))

ns = {}
exec('class C:\n' + method(cr, '_layoutDiffers'), ns)
differs = ns['C']._layoutDiffers
check('a value equal to its saved default does not apply', differs({'val': 31, 'default': 31}) is False)
check('a value the user changed applies', differs({'val': 24, 'default': 31}) is True)
check('an old record with no default never applies', differs({'val': 24}) is False)
check('an old bare surface value never applies', differs(24) is False)
check('a default is saved only for release-stamped owners',
      "if p.name in layout and self._LAYOUT_TAG in tool.tags:" in cr
      and "if self._LAYOUT_TAG in owner.tags:" in cr)
check('layout pars apply only as changes', "if name in layout and not self._layoutDiffers(rec):" in cr)
check('surface values apply only as changes', "if not self._layoutDiffers(rec):" in cr)
check('the Hub roams a table only when it differs from what shipped',
      'shipped = c.op(STATE_DEFAULT)' in cb and 'STATE_SCHEMA = 2' in cb)
check('schema 1 tables are ignored on load', "if int(data.get('schema') or 1) < 2:" in cb)

print('written only when the user changed the surface')
ns = {}
exec('class C:\n' + method(cr, '_carryUnchangedLayout'), ns)


class Fake(ns['C']):
    changed = set()

    def _layoutParNames(self, tool):
        return {'Tbmenuorder': 'FNS_ToolbarRegistry', 'Nbmenuorder': 'FNS_NavbarRegistry'}

    def _surfaceNameHosts(self, tool):
        return {('button_mute', 'Tbmenuorder'): 'FNS_ToolbarRegistry'}

    def _surfaceChanged(self, host):
        return host in self.changed


def section():
    return {'pars': {'Tbmenuorder': {'val': 99, 'default': 31}, 'Nbmenuorder': {'val': 7, 'default': 2},
                     'Volume': {'val': 0.5}},
            'surfaces': {'button_mute': {'Tbmenuorder': {'val': 99, 'default': 17}}}}


prev = {'pars': {'Tbmenuorder': {'val': 24, 'default': 31}},
        'surfaces': {'button_mute': {'Tbmenuorder': {'val': 5, 'default': 17}}}}
f = Fake()
out = f._carryUnchangedLayout(None, section(), prev)
check("untouched surface: the file's previous layout record is kept",
      out['pars']['Tbmenuorder'] == {'val': 24, 'default': 31})
check('untouched surface with no previous record: nothing new is written', 'Nbmenuorder' not in out['pars'])
check('untouched surface: a button inside the tool keeps its previous record too',
      out['surfaces']['button_mute']['Tbmenuorder'] == {'val': 5, 'default': 17})
check('non-layout settings save as before', out['pars']['Volume'] == {'val': 0.5})
f.changed = {'FNS_ToolbarRegistry'}
out = f._carryUnchangedLayout(None, section(), prev)
check('changed surface: the live layout is written',
      out['pars']['Tbmenuorder']['val'] == 99 and out['surfaces']['button_mute']['Tbmenuorder']['val'] == 99)
check('...and only that surface', 'Nbmenuorder' not in out['pars'])

check('SaveAll carries over from the file and clears the flags after writing',
      "carry=tools.get(canonical) or {}" in cr and 'self._clearSurfaceChanges()' in method(cr, 'SaveAll'))
check('SaveTool carries over too', "carry=data.get('tools', {}).get(canonical_name) or {}" in cr)
check('SaveTool never clears the flags (one tool, not the surface)',
      '_clearSurfaceChanges' not in method(cr, 'SaveTool'))
check('an explicit export writes the live layout (no carry)',
      'carry=' not in method(cr, 'UiExport'))
check('one flag key on the registry side', "_LAYOUT_CHANGED_KEY = 'fns_layout_changed'" in rb)
check("the bar's group eye marks the surface", 'self.markLayoutChanged()' in method(rb, 'ToggleGroup'))
check('a boot/restore group change does not', 'markLayoutChanged' not in method(rb, 'SetGroupVisible'))
for fn in ('RestoreBuiltinOrder', 'TreeMoveRows', 'ToggleShow', 'ToggleSide', '_onWidthDialog',
           '_onGroupDialog', 'GroupSelected', 'DissolveGroup', 'AddDivider', 'RemoveSelected', 'PackageDrop'):
    check('configurator %s marks the surface' % fn, 'self._markChanged()' in method(cfgb, fn))
for fn in ('RestoreState', '_boot', 'PushSequence', '_reapplyStoredOrders', '_republishGroupMarkers',
           '_adoptBuiltins'):
    check('%s (boot/restore) does not mark' % fn, 'self._markChanged()' not in method(cfgb, fn))
check('the dialogs mark only when confirmed',
      re.search(r"if info.get\('buttonNum'\) != 1:\s+return\s+self\._markChanged",
                method(cfgb, '_onWidthDialog')) is not None)
check('Hub tab show/hide marks the hub surface', 'ext.markLayoutChanged()' in method(hub, 'ShowTab'))
check('Hub tables of an untouched surface are carried over',
      'if not _layoutChanged(c):' in cb and 'states[name] = previous[name]' in cb)
ovc = read('modules', 'suspects', 'FNSTools', 'FNS_Hub', 'OverlayConfigurator', 'ConfiguratorExt.py')
check('the Overlay tab adapter forwards the mark to the overlay registry',
      'def markLayoutChanged(self):' in ovc and "getattr(self._reg.ext, 'OverlayRegistryExt'" in ovc)
for fn in ('ToggleShow', 'CycleCorner', '_onMarginDialog'):
    check('Overlay tab %s marks the surface' % fn, 'self._markChanged()' in method(ovc, fn))
print()
if FAILS:
    print('FAILED %d' % len(FAILS))
    sys.exit(1)
print('all passed')
