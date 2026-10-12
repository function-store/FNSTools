# Pre-release hook -- runs on the STAGED COPY before the portable tox is
# written (extensions NOT initialized there; direct par/storage edits only).
# args[0] = resolved save path.

exec(open('packaging/pre_release_common.py').read())  # generic FNS strip (Version Ctrl / vc_data)

_q = me.parent()

# Marks are this checkout's own places: a release ships with every slot empty
# (they had shipped the author's marks; 2026-10-11).
_seq = _q.seq.Mark if hasattr(_q.seq, 'Mark') else None
if _seq is not None:
    for _i in range(_seq.numBlocks):
        for _name in ('Mark%dname' % _i, 'Mark%ddata' % _i):
            _p = _q.par[_name]
            if _p is not None:
                _p.val = ''

# The legacy StorageManager store keeps the marks from before the sequence
# as a migration backup, and storage rides inside the tox: v3.2.69's first
# staging carried three of the author's marks there (2026-10-12). The
# extension declares the store again on init with every slot empty. Exact
# key: unstore() globs.
if 'QuickmarkStorageExtStored' in _q.storage:
    _q.unstore('QuickmarkStorageExtStored')

# QuickMarks ships switched on, its overlay off (owner, 2026-10-12): the
# keys work from the start, and the mark list and outlines wait for Mark
# List, Pins or Alt+Shift+M. Set explicitly: v3.2.68 shipped whatever the
# dev copy held, the overlay on included.
_p = _q.par['Active']
if _p is not None:
    _p.val = True

# The overlay (FNS_OverlayRegistry) ships at its defaults, off, and holds
# nothing drawn for this checkout.
for _name, _value in (('Showlist', False), ('Listcorner', 'topleft'),
                      ('Listmargin', 12), ('Listorder', 150), ('Overlayshortcut', 'alt.shift.m'), ('Showpins', False), ('Listcollapsed', False)):
    _p = _q.par[_name]
    if _p is not None:
        _p.val = _value
_t = _q.op('table_pins')
if _t is not None:
    _t.text = 'x\ty\ttext'
_g = _q.op('glsl_outlines')
if _g is not None and _g.par['vec0valuex'] is not None:
    _g.par.vec0valuex.val = 0       # no outlines drawn
_w = _q.op('widget_marks')
if _w is not None:
    _w.par.h = 44
    for _i in range(10):
        _r = _w.op('row%d' % _i)
        if _r is not None:
            _r.par.text = ''
            _r.par.display = False
            _r.par.bgalpha = 0
            _r.store('slot', -1)
