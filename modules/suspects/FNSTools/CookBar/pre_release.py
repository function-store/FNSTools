# Embody/PI pre_release hook -- runs on the STAGED COPY in /sys/quiet before
# the portable tox is written (extensions NOT initialized there; direct
# par/table edits only). args[0] = resolved save path.
exec(open('packaging/pre_release_common.py').read())

# Cook Bar ships switched off. It draws as a layer of FNS_OverlayRegistry
# (docs/NetworkOverlayRegistry.md), so it holds no state about any network:
# what the earlier backdrop method stored is dropped here too.
_c0.par.Active.val = False
_c0.par.Active.enable = True
_c0.comment = ''
for _k in ('targetCOMP', 'winWidth', 'winHeight', 'netX', 'netY', 'netZoom',
           'netWidth', 'netHeight', 'netRatio', 'paneId', 'init', 'putBackForSave',
           'hiddenDisplay', 'dimmedAnnotations'):
    if _k in _c0.storage:
        _c0.unstore(_k)
_c0.store('active', False)
_p = _c0.par['Annotationalpha']
if _p is not None:
    _p.val = 0.2
_p = _c0.par['Maxops']
if _p is not None:
    _p.val = 100
# the Top List margin and the Values option ship at their defaults
_p = _c0.par['Topmargin']
if _p is not None:
    _p.val = 12
_p = _c0.par['Showvalues']
if _p is not None:
    _p.val = False
_p = _c0.par['Topcollapsed']
if _p is not None:
    _p.val = False
_p = _c0.par['Toporder']
if _p is not None:
    _p.val = 100

# The Global Hog CHOP (toolbar right-click) exists to eat frame time on
# purpose; it ships switched off.
_hog = _c0.op('hog_global')
if _hog is not None:
    _hog.par.active.val = False

# The Values labels of the last frame drawn.
_t = _c0.op('table_values')
if _t is not None:
    _t.text = 'x\ty\ttext\tfontalpha'

# The Top List as last drawn: each row's label and the operator it frames,
# and the network they were ranked in, are this checkout's operators
# (v3.2.69's first staging carried them, 2026-10-12). Exact keys: unstore()
# globs.
_w = _c0.op('widget_top')
if _w is not None:
    if 'network' in _w.storage:
        _w.unstore('network')
    for _row in _w.findChildren(name='row*', maxDepth=1):
        if _row.par['text'] is not None:
            _row.par.text.val = ''
        if 'opname' in _row.storage:
            _row.unstore('opname')

# The last frame's measurements of the network it was drawing.
_t = _c0.op('table_op_info')
if _t is not None:
    _t.text = '\t'.join(('name', 'x', 'y', 'width', 'height', 'border', 'isCOMP',
                         'cooking', 'cookTime', 'childrenCooking',
                         'childrenCookTime', 'gpuMemory', 'childrenGpuMemory'))
