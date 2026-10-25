"""Perform Mode cook audit: what still cooks every frame while performing.

docs/PerformMode.md, section 6. perform_audit.py classifies one shape of
per-frame work, frame-callback Execute DATs, by reading them. Everything
else that runs every frame (Time Sliced CHOPs, Timer and LFO CHOPs, Cook
Type Always nulls, CHOP Execute pulls, feedback loops, self-rescheduling
run() loops, expressions on absTime or ui.panes, a COMP parameter that
pulls a time-dependent chain) has no shape a scan can match. This one
measures the effect instead, the phase 0 way: Perform on, the network
editors pointed away from the toolkit, then every operator under the root
whose cook count moved on at least 90% of the sampled frames.

Each such operator is either listed in packaging/perform_floor.json (the
committed floor, each entry with its reason), sits in or under a COMP
tagged `fns_show` (show work, on purpose), or is NEW. Preflight blocks a
release on a new one, and on a measurement older than the newest package
tox, so a tool that starts cooking while performing cannot ship unseen.

Run it in TouchDesigner, in its own namespace (packaging scripts clobber
names, RELEASING.md "Driving a release from an agent session"):

    ns = {}; exec(open('scripts/perform_cook_audit.py').read(), ns)
    ns['StartPerformCookAudit'](op.FNS)     # returns at once

It takes about `settle + sample` frames (450, under 10 s at 60 fps), puts
Perform and every pane back however it ends, and writes RESULT_PATH. Then
`ns['Report']()` reads it against the floor. The panes move while it runs:
do not work in the editor meanwhile.
"""

import fnmatch
import json
import os
import time

try:            # a fresh exec namespace does not see TD's names by itself
    from td import op, run, ui, app, project, absTime, ParMode, PaneType
except ImportError:
    pass        # outside TouchDesigner: Classify and Report still work

RESULT_PATH = 'packaging/.perform_cook_audit.json'   # gitignored, per machine
FLOOR_PATH = 'packaging/perform_floor.json'
NEUTRAL_PANE = '/sys/quiet'      # the staging home the packaging scripts use
HOT_SHARE = 0.9                  # cooked on this share of the sampled frames
SHOW_TAG = 'fns_show'


def _abs(path):
    """Repo-relative paths resolve against the project folder, not the
    process's working directory."""
    if os.path.isabs(path):
        return path
    try:
        return os.path.join(project.folder, path).replace('\\', '/')
    except NameError:
        return path


def _write(path, data):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, sort_keys=True)
    os.replace(tmp, path)


def _read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def _isShow(o, root):
    """True when the operator or a COMP above it, up to the root, carries
    the show tag."""
    while o is not None and o != root:
        if SHOW_TAG in o.tags:
            return True
        o = o.parent()
    return False


def StartPerformCookAudit(root, settle=90, sample=360, out=RESULT_PATH):
    """Measure what cooks every frame under `root` while Perform is on.
    Returns at once; the result lands in `out` about settle + sample
    frames later. Refuses when Perform is not a plain toggle (an
    expression or export would fight the audit) or a run is pending."""
    out = _abs(out)
    perform = getattr(root.par, 'Perform', None)
    if perform is None:
        return {'started': False, 'reason': '%s has no Perform par' % root.path}
    if perform.mode != ParMode.CONSTANT:
        return {'started': False, 'reason': 'Perform is driven by %s; set it constant first'
                % perform.mode}
    prev = _read(out)
    if prev and prev.get('running') and time.time() - prev.get('started', 0) < 120:
        return {'started': False, 'reason': 'a measurement started %.0f s ago is still running'
                % (time.time() - prev['started'])}

    state = {
        'root': root, 'out': out, 'settle': int(settle), 'sample': int(sample),
        'perform_before': bool(perform.eval()),
        'panes': [],
        'started': time.time(),
    }
    _write(out, {'running': True, 'started': state['started'], 'root': root.path})

    neutral = op(NEUTRAL_PANE) or op('/sys')
    try:
        for p in ui.panes:
            if p.type == PaneType.NETWORKEDITOR:
                state['panes'].append((p, p.owner))
                p.owner = neutral
        perform.val = True
    except Exception as e:
        _finish(state, error='setup failed: %r' % (e,))
        return {'started': False, 'reason': repr(e)}
    run(_snapshotStart, state, delayFrames=state['settle'])
    return {'started': True, 'out': out, 'frames': state['settle'] + state['sample']}


def _cookCounts(root):
    return {o.path: o.totalCooks for o in root.findChildren()}


def _snapshotStart(state):
    try:
        state['frame0'] = absTime.frame
        state['cooks0'] = _cookCounts(state['root'])
    except Exception as e:
        _finish(state, error='first snapshot failed: %r' % (e,))
        return
    run(_snapshotEnd, state, delayFrames=state['sample'])


def _snapshotEnd(state):
    root = state['root']
    hot = []
    try:
        frames = absTime.frame - state['frame0']
        cooks0 = state['cooks0']
        prefix = root.path.rstrip('/') + '/'
        for o in root.findChildren():
            before = cooks0.get(o.path)
            if before is None:
                continue                     # created during the run
            moved = o.totalCooks - before
            if frames > 0 and moved >= HOT_SHARE * frames:
                hot.append({
                    'path': o.path[len(prefix):],
                    'type': o.OPType,
                    'cooks': moved,
                    'ms': round(float(o.cpuCookTime) + float(o.gpuCookTime), 4),
                    'show': _isShow(o, root),
                })
        state['result'] = {'frames': frames, 'ops_scanned': len(cooks0),
                           'hot': sorted(hot, key=lambda h: h['path'])}
    except Exception as e:
        _finish(state, error='second snapshot failed: %r' % (e,))
        return
    _finish(state)


def _finish(state, error=None):
    """Put Perform and the panes back, then write the result. Runs on every
    exit path, error or not."""
    root = state['root']
    try:
        root.par.Perform.val = state['perform_before']
    except Exception as e:
        error = (error + '; ' if error else '') + 'Perform not restored: %r' % (e,)
    for p, owner in state['panes']:
        try:
            p.owner = owner
        except Exception:
            pass                             # the pane closed meanwhile
    data = {'running': False, 'root': root.path, 'started': state['started'],
            'measured_at': time.time(),
            'measured': time.strftime('%Y-%m-%d %H:%M:%S'),
            'td_build': '%s.%s' % (app.version, app.build),
            'settle': state['settle'], 'sample': state['sample'], 'error': error}
    data.update(state.get('result') or {})
    _write(state['out'], data)


def Classify(hot, floor):
    """Split measured hot operators against the floor. Pure Python, so
    Preflight can re-read an old measurement against an edited floor.
    Returns new (neither allowed nor show work), allowed, show, and the
    floor entries nothing matched (cooking stopped: delete them)."""
    entries = (floor or {}).get('allowed', [])
    used = set()
    new, allowed, show = [], [], []
    for h in hot:
        match = next((e['match'] for e in entries
                      if fnmatch.fnmatchcase(h['path'], e['match'])), None)
        if match is not None:
            used.add(match)
            allowed.append(h)
        elif h.get('show'):
            show.append(h)
        else:
            new.append(h)
    unused = [e['match'] for e in entries if e['match'] not in used]
    return {'new': new, 'allowed': allowed, 'show': show, 'unused': unused}


def Report(out=RESULT_PATH, floor_path=FLOOR_PATH):
    """The last measurement read against the committed floor."""
    data = _read(_abs(out))
    if data is None:
        return {'measured': None, 'reason': 'no measurement in %s' % out}
    if data.get('running'):
        return {'measured': None, 'reason': 'a measurement is still running'}
    c = Classify(data.get('hot', []), _read(_abs(floor_path)))
    return {'measured': data.get('measured'), 'error': data.get('error'),
            'frames': data.get('frames'), 'ops_scanned': data.get('ops_scanned'),
            'new': c['new'], 'show': [h['path'] for h in c['show']],
            'allowed': len(c['allowed']), 'unused_floor_entries': c['unused']}
