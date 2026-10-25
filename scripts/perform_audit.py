"""Perform Mode audit: per-frame Python in the toolkit that nobody has classified.

docs/PerformMode.md. Every Execute DAT under the toolkit root with a frame
callback (framestart or frameend) either stops while the root's Perform Mode
is on, or runs during a show on purpose. This lists the ones that say
neither. A DAT is classified when:

  - its `active` expression or its own text reads `Perform` (the frame gates
    of CookBar, QuickMarks and POPOverlay), or
  - it carries the tag `fns_perform`: it stops while performing and the
    gate lives in its extension (FNS_RadialMenu's execute_frame), or
  - it carries the tag `fns_show`: it keeps running while performing, on
    purpose (a show tool's own clock or tweener).

The overlay registry's frame DAT lives on the /sys global, outside the
root, and is gated in Python (_shownLayers / _shownWidgets); it is not
scanned. Run it in TouchDesigner against the live root:

    exec(open('scripts/perform_audit.py').read())
    PerformAudit(op.FNS)
"""

PERFORM_TAGS = ('fns_perform', 'fns_show')


def PerformAudit(root):
    """Every frame-callback Execute DAT under `root`, classified, and the
    unclassified ones by path. Reads only; never writes."""
    rows = []
    unclassified = []
    for d in root.findChildren(type=executeDAT, includeUtility=True):
        try:
            frame = bool(d.par.framestart.eval()) or bool(d.par.frameend.eval())
        except Exception:
            frame = True
        if not frame:
            continue
        ap = d.par.active
        expr = ap.expr if ap.mode == ParMode.EXPRESSION else ''
        try:
            active = bool(ap.eval())
        except Exception:
            active = None              # an expression that errors here (a pane-bar master)
        tag = next((t for t in PERFORM_TAGS if t in d.tags), None)
        reads = 'Perform' in expr or 'Perform' in d.text
        how = tag or ('reads Perform' if reads else None)
        rows.append({'path': d.path, 'active': active, 'how': how})
        if how is None:
            unclassified.append(d.path)
    return {'frame_dats': len(rows), 'unclassified': unclassified, 'rows': rows}
