"""FNS_OverlayRegistry and CookBar on it (docs/NetworkOverlayRegistry.md).

Pins the contract and the rules paid for while building it: the registry is
a package found through its host (not core), the composite always has two
sources, a deleted tool cleans up, saves and clone masters never hold the
overlay, artifacts ship without it; CookBar renders a premultiplied layer
from the registry's View and no longer edits the viewed network.

Runs outside TouchDesigner: it reads the sources.

    python tests/test_overlay_registry.py
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


TOOLS = ('modules', 'suspects', 'FNSTools')
ext = read(*TOOLS, 'FNS_OverlayRegistry', 'OverlayRegistryExt.py')
pre = read(*TOOLS, 'FNS_OverlayRegistry', 'pre_release.py')
bm = read('packaging', 'build_manifest.py')
common = read('packaging', 'pre_release_common.py')

print('packaging')
check('the manifest finds the host (REGISTRY_OWNER)',
      "'FNS_OverlayRegistry': 'FNS_OverlayRegistry'," in bm)
check('...names its surface', "'FNS_OverlayRegistry': 'overlay'," in bm and "'overlay': 'Network editor overlay'" in bm)
core = re.search(r'CORE = \((.*?)\)\n', bm, re.S)
check('it is a package, not core (owner)', core is not None and 'FNS_OverlayRegistry' not in core.group(1))
catalog = json.loads(read('packaging', 'catalog.json'))
pk = catalog.get('packages', catalog)
check('a catalog entry', 'FNS_OverlayRegistry' in pk)
doc = read('packaging', 'docs', 'FNS_OverlayRegistry.md')
check('a user doc for the same package', doc.startswith('---\npackage: FNS_OverlayRegistry\n'))
check('the hook runs the common strip', "exec(open('packaging/pre_release_common.py').read())" in pre)
check('the hook ships it idle', "p.Autoregister = False" in pre and "comp.ops('layer_*')" in pre)

print('the registry')
check('identity', "SHORTCUT = 'FNS_OVERLAYREGISTRY'" in ext and "REGISTRY_NAME = 'FNS_OverlayRegistry'" in ext)
check('a layer must be a TOP', "widget_op.family != 'TOP'" in ext)
check('the layer is its own TOP par, Layer', "self.ownerComp.par['Layer']" in ext)
check('the composite always has two sources', 'if len(wanted) < 2:' in ext)
check('wiring compared slot by slot', 'conn.connections[0].owner if conn.connections else None' in ext)
check('every sync drops layers whose TOP is gone', 'self._pruneDeadLayers(sync=False)' in ext)
check('the frame driver stops itself with nothing shown',
      'if not layers and not widgets:' in ext and 'frame.par.active = running' in ext)
check('never drawn in a clone master', '_drawableNetwork' in ext and '_isClonedByOthers' in ext)
check('taken out before a project save', "('projectpresave', True)" in ext and 'def onProjectPreSave' in ext)
check('a utility annotation above the nodes',
      "mark.par.utility = True" in ext and "mark.par.layerzone = 'abovenodes'" in ext)
check('the Non-Commercial licence cap', 'NON_COMMERCIAL_MAX = 1280' in ext)
check('clients get View() and NetworkToPixel()', 'def View(self):' in ext and 'def NetworkToPixel(self' in ext)
check('strays swept across the toolkit at boot', "root.findChildren(tags=[self.OVERLAY_TAG], includeUtility=True)" in ext)

check('the clear layer is 8x8: the composite fills each input to its own size (18 MB saved)',
      "clear.par.resolutionw, clear.par.resolutionh = 8, 8" in ext and "comp.par.prefit = 'fill'" in ext)
print('widgets')
check('a widget API', 'def RegisterPanelWidget(self, panel, canonical' in ext and 'def UnregisterPanelWidget' in ext)
check('widgets are interactive annotations', 'ann.par.Opviewerinteractive = True' in ext and 'ann.par.enable = True' in ext)
check('widget annotations kept as OPs, never looked up by path', 'self._widgetAnns[canonical] = ann' in ext)
check('pinned against the LIVE geometry', 'cur = (ann.nodeX, ann.nodeY, ann.nodeWidth, ann.nodeHeight)' in ext
      and 'if cur != rect' in ext)
check('four corner anchors', "WIDGET_ANCHORS = ('topleft', 'topright', 'bottomleft', 'bottomright')" in ext)
check('widgets also leave before a save', ext.count('self._removeWidgets()') >= 4)
check('the shipped registry carries no widget registrations', "'overlay_path', 'widgets'" in pre)
check('each tool passes its own margin with its corner and order, no offset',
      "def RegisterPanelWidget(self, panel, canonical, anchor='topleft', order=None, margin=None," in ext
      and 'offset' not in ext and "'margin': max(0.0," in ext)
check('widgets in one corner stack in order, each its own margin from the one before',
      'stacked[anchor] = along + margin + ' in ext and 'oy = (along + margin) / zoom' in ext
      and "key=lambda w: (float(w[2].get('order', self.WIDGET_ORDER)), w[0])" in ext)
check('the package-wide Widgets page is retired, pars before page',
      'def _retireWidgetLayoutPage' in ext and "RETIRED_PARS = ('Widgetmargin', 'Widgetgap')" in ext
      and 'self._ensureWidgetLayoutPars()' not in ext and 'Widgetmargin' not in pre)
check('the master never has cloning on (with it on, par writes crashed TD, 2026-10-11)',
      'self._ensureMasterNotCloning()' in ext and 'c.par.enablecloning = False' in ext)

print('artifacts')
check('no artifact ships the overlay',
      "_c0.findChildren(tags=['fns_network_overlay', 'fns_network_overlay_widget'], includeUtility=True)" in common)
check('...stripped before the surface defaults (no try after them)',
      common.index('no artifact ships the network overlay') < common.index('shipped surface layout is the authored default'))

print('CookBar on it')
CB = TOOLS + ('CookBar',)
funcs = read(*CB, 'text_funcs.py')
scan = read(*CB, 'execute_op_info.py')
frag = read(*CB, 'text_cook_bar_frag.frag')
cbext = read(*CB, 'CookBarExt.py')
cbpre = read(*CB, 'pre_release.py')
check('no Select TOP planted in the viewed network', 'create(selectTOP' not in funcs)
check('no display flag switched off', '.display = False' not in funcs)
check('no annotation dimmed', 'limit' not in funcs and 'retireBackdrop' in funcs)
check('the scan reads the registry View', "getattr(op, 'FNS_OVERLAYREGISTRY', None)" in scan and 'reg.View()' in scan)
check('the shader is premultiplied and transparent outside the bars',
      'return vec4(forground.rgb * opacity, opacity);' in frag and 'vec4 color = vec4(0.0);' in frag)
check('cook times are read only for operators in view, and only after a cook (0.3 ms a read in a viewed network)',
      scan.index('reach = edgeRel * 10 + 11') < scan.index('cookTime = _cookTimeOf(child)')
      and 'child.cookTime + child.gpuCookTime' not in scan.split('def frameStart')[1])
check('Values is optional: a switch picks bars only, so the text layer cooks only when on',
      "ensure('Showvalues', 'Toggle', 'Values', False" in cbext and 'if showValues:' in scan
      and 'def _writeValues(' in scan)
check('the extension keeps no save hooks', 'beforeSave' not in cbext and 'putBack' not in cbext)
check('retired files are gone',
      not any(os.path.exists(os.path.join(_ROOT, *CB, f))
              for f in ('execute_pane_info.py', 'execute_save.py', 'text_store_win_res.py')))
check('the Top List registers at its corner, in its order, with its own List Margin',
      'anchor=corner, order=order, margin=margin,' in cbext
      and "ensure('Topmargin', 'Int', 'List Margin'" in cbext and '_onTopmarginValueChange' in cbext
      and "ensure('Toporder', 'Int', 'List Order', self.TOP_ORDER" in cbext and '_onToporderValueChange' in cbext)
check('the Top List margin and Values ship at their defaults',
      "_c0.par['Topmargin']" in cbpre and "_c0.par['Showvalues']" in cbpre)
check('List Margin is one Int, not an XY pair (no parameter-group callback for it)',
      "ensure('Topmargin', 'Int'" in cbext and "appendXY" not in cbext)
check('the Top List has rank tabs and a row click that frames the operator',
      'def onTopRankClick(self, tab):' in cbext and 'pane.homeSelected(zoom=True)' in cbext)
check('a widget never stays selected, or framing it zooms out each click',
      "network.findChildren(tags=['fns_network_overlay_widget'], maxDepth=1," in cbext)
helper = read(*TOOLS, 'QuickExt', 'ExtUtils', 'CustomParHelper.py')
check('a tuplet on a tool that never called Init is skipped, not dereferenced',
      re.search(r"_comp = cls\._extForComp\(_par\.owner\)\r?\n(?:\s*#.*\r?\n)*\s*if _comp is None:\r?\n\s*continue",
                helper) is not None)
sd = json.loads(read('packaging', 'surface_defaults.json'))
check("CookBar's layer order ships from the defaults file",
      sd['packages'].get('CookBar', {}).get('.', {}).get('Ovmenuorder') == 100)  # the marks band

print('QuickMarks on it')
QM = TOOLS + ('QuickMarks',)
qmext = read(*QM, 'QuickmarkStorageExt.py')
qmpre = read(*QM, 'pre_release.py')
check('the mark list registers under the Top List, with its own corner, margin and order',
      'LIST_ORDER = 150' in qmext and 'reg.RegisterPanelWidget(panel, self.LIST_CANONICAL,' in qmext
      and "margin=int(c.par.Listmargin.eval())" in qmext
      and "ensure('Listorder', 'Int', 'List Order', self.LIST_ORDER" in qmext and '_onListorderValueChange' in qmext)
check('a list row jumps like Ctrl+number', 'self.RetrieveQuickmark(int(slot))' in qmext)
check('list and pins are rewritten only on change',
      'if sig == self._listSig:' in qmext and 'if text != self._pinsText:' in qmext)
check('outlines only for marks of the viewed network whose area overlaps the view',
      "data.get('current_network') != path" in qmext
      and 'if left > w or bottom > h or left + rw < 0 or bottom + rh < 0:' in qmext)
check('a release ships no marks and the overlay at its defaults',
      "'Mark%dname' % _i, 'Mark%ddata' % _i" in qmpre and "('Showpins', False)" in qmpre)
check("QuickMarks' pins ship in the labels band", sd['packages'].get('QuickMarks', {}).get('.', {}).get('Ovmenuorder') == 200)
check('a mark stores the size of the area it saved, and the outline uses it',
      "quickmark_value['w'] = " in qmext and "aw, ah = data.get('w'), data.get('h')" in qmext
      and 'aw, ah = pane_w / zoom, pane_h / zoom' in qmext)
check('outlines are drawn by a constant-bounded GLSL loop, rewritten only on change',
      'if glsl is not None and sig != self._rectsSig:' in qmext)
check('a missing mark is labelled and dimmed', "label += '   (missing)'" in qmext and 'row.par.fontalpha = 0.45 if gone else 1' in qmext)
check('right-click renames through the non-blocking PopDialog, Cancel ignored',
      'dialog.OpenDefault(' in qmext and "if info.get('buttonNum') != 1:" in qmext and 'messageBox' not in qmext)
check('both widgets fold, and the fold ships open',
      "ensure('Listcollapsed', 'Toggle', 'Mark List Collapsed', False" in qmext
      and "ensure('Topcollapsed', 'Toggle', 'Top List Collapsed', False" in cbext
      and "('Listcollapsed', False)" in qmpre and "_c0.par['Topcollapsed']" in cbpre)

check('one hotkey and one command hide the list and the outlines, marks keep working',
      "@FNSCommand.fns_command(label='Toggle QuickMarks overlay', state={'method': 'OverlayShown'})" in qmext
      and "for name in ('Showlist', 'Showpins'):" in qmext
      and "OVERLAY_SHORTCUT = 'alt.shift.m'" in qmext
      and "ensure('Overlayshortcut', 'Str', 'Overlay Hotkey'" in qmext
      and "('Overlayshortcut', 'alt.shift.m')" in qmpre)
check('the Keyboard In follows the hotkey pars by expression (it had held a constant copy)',
      "KEYBOARD_SHORTCUTS_EXPR = \"parent().par.Shortcuts + ' ' + parent().par.Overlayshortcut\"" in qmext
      and 'sp.mode = ParMode.EXPRESSION' in qmext)
check('the overlay hotkey is checked first, matched by its parts',
      qmext.index('if self._isOverlayShortcut(shortcutName):') < qmext.index("key_number = shortcutName.split('.')[-1]")
      and "frozenset(str(text).lower().replace('+', '.').split('.'))" in qmext)

opinfo = read(*CB, 'execute_op_info.py')
check('QuickMarks ships on with its overlay off (v3.2.68 shipped the overlay on)',
      "_p.val = True\n\n# The overlay" in qmpre
      and "('Showlist', False)" in qmpre and "('Showpins', False)" in qmpre
      and "ensure('Showlist', 'Toggle', 'Mark List', False" in qmext
      and "ensure('Showpins', 'Toggle', 'Pins', False" in qmext)
check('nothing of an overlay tool cooks while nothing of it would draw',
      "FRAME_GATE = (\"parent().par.Active and ((parent().par.Showpins and \"" in qmext
      and "ex = c.op('execute_overlay')" in qmext
      and "FRAME_GATE = (\"parent().par.Active and ((parent().par['Ovdisplayed'] is None\"" in cbext
      and 'self._ensureFrameGate()' in cbext)
check("CookBar draws its bars only while their layer is shown; the Top List runs either way",
      opinfo.index('ext.updateTopList(targetCOMP)') < opinfo.index("ovd = parent().par['Ovdisplayed']"))

print('the overlay manager (docs/OverlayManager.md)')
cfg = read(*TOOLS, 'FNS_Hub', 'OverlayConfigurator', 'ConfiguratorExt.py')
check('a layer draws only when the user shows it AND its tool is on',
      "str(info.get('display', '1')) != '1' or str(info.get('active', '1')) != '1'" in ext
      and "'active': '1' if active else '0'," in ext
      and "active=self._parBool('Layeractive', True)," in ext and 'def onParLayeractive' in ext)
check("the tool's switch moves off Ovdisplayed onto Layer Active, on every host's init",
      'def _ensureLayerActive(self):' in ext and 'self._ensureLayerActive()' in ext
      and "expr.replace('me.par.', 'me.parent().par.')" in ext and 'source.val = True' in ext)
check('a widget is registered while its tool exists and placed only when shown and active',
      'def _shownWidgets(self):' in ext and ext.count('self._shownWidgets()') >= 2
      and 'reg.UnregisterPanelWidget(self.TOP_CANONICAL)\n\t\t\treturn' in cbext
      and 'shown=toplist is None or bool(toplist.eval()),' in cbext
      and 'shown=shown, active=active, tool=c,' in qmext)
check('a widget spec stays flat: strings and numbers (a nested dict in store() crashed TD)',
      "'shown': '1' if shown else '0', 'active': '1' if active else '0'," in ext
      and "'pars': self._encodeWidgetPars(pars)}" in ext and 'def _decodeWidgetPars(text):' in ext)
check('each tool declares the parameters the manager writes',
      "pars={'show': 'Toplist', 'corner': 'Topcorner'," in cbext
      and "pars={'show': 'Showlist', 'corner': 'Listcorner'," in qmext)
check('the tab writes to the tool, never to the registry entry',
      "host.par.Displayed = bool(visible)" in cfg and "host.par.Menuorder = int(value)" in cfg
      and "self._writeWidget(info, 'show', bool(visible))" in cfg
      and "self._writeWidget(info, 'corner', corner)" in cfg
      and "self._writeWidget(info, 'margin', int(margin))" in cfg)
check('Show never touches a tool switch', 'Active' not in cfg.split('class ConfiguratorExt')[0].split('def SetWidgetDisplay')[1].split('def SetWidgetCorner')[0])
check('a reorder swaps the existing numbers, so the bands stay',
      'def _renumber(names, values, write):' in cfg and 'values = sorted(values)' in cfg)
check('the tab is a Hub configurator with no groups, drops or built-ins',
      "HUB_TAB = 'overlay'" in cfg and 'HAS_GROUPS = False' in cfg and 'SUPPORTS_DROP = False' in cfg
      and 'ADOPTS_BUILTINS = False' in cfg)
check('a corner click reads the tool par, not the registry copy that lags a frame',
      "par = api._toolPar(info, 'corner')" in cfg)
check('the order pars ship at their defaults',
      "_c0.par['Toporder']" in cbpre and "('Listorder', 150)" in qmpre)
check('the doc exists', os.path.exists(os.path.join(_ROOT, 'docs', 'OverlayManager.md')))
check('Layer Active ships as an expression: the hook skips it when it flattens Registration',
      "if _p.name == 'Layeractive':" in pre)
check("Layer Active reads me.parent(): PI's local Release keeps only me./op('. expressions",
      'LAYER_ACTIVE_EXPR = "bool(me.parent().par.Active)' in ext
      and "LAYER_ACTIVE_EXPR = 'me.parent().par.Active and me.parent().par.Showpins'" in qmext)
check('a constant Layer Active is healed back to the expression',
      'if par.mode != ParMode.EXPRESSION or par.expr == self._OLD_LAYER_ACTIVE_EXPR:' in ext)
check('the heal also runs on every registration (a roamed settings file restores late)',
      ext.index('self._ensureLayerActive()', ext.index('def _applyHostRegistration')) < ext.index('def onParAutoregister'))
check('the old expression text is dropped, not left dormant', "source.expr = ''" in ext)

# Pan and zoom cost (2026-10-12): moving an annotation made TD redraw its
# viewer inside the frame callback, ~7.5 ms a frame of a pan or a zoom.
_draw = ext.split('def _drawLayers')[1].split('\n\tdef ')[0]
_place = ext.split('def _placeWidgets')[1].split('\n\tdef ')[0]
check('the overlay stays put while it still covers the view and the zoom is near',
      'self._viewStillCovered(prev, pane, zoom, px)' in _draw and 'REPLACE_ZOOM = 1.15' in ext)
check('the overlay and a widget force-cook their viewer only on a resize',
      'if resized:' in _draw and 'if cur[2:] != rect[2:]:' in _place)
check('a widget follows a pan live and waits for a zoom to settle',
      'WIDGET_SETTLE = 3' in ext and 'if cur != rect and (fresh or not settling):' in _place)

print()
if FAILS:
    print('FAILED %d: %s' % (len(FAILS), ', '.join(FAILS)))
    sys.exit(1)
print('all passed')
