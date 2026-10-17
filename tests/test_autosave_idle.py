"""FNS_Autosave: Wait For Mouse Rest.

A due save waits until the mouse has rested for Idleseconds. Nothing runs
per frame for it: the Mouse In CHOP is on only while a save waits, and the
check is a run() every IDLE_POLL_MS. This drives the extension outside
TouchDesigner with fakes for run(), the CHOP, the pars and the clock.

    python tests/test_autosave_idle.py
"""
import io
import os
import time as _time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Autosave', 'FNSAutosaveExt.py')
PRE = os.path.join(_ROOT, 'modules', 'suspects', 'FNSTools', 'FNS_Autosave', 'pre_release.py')
FAILS = []


def check(label, cond, detail=''):
    if cond:
        print('  PASS  %s' % label)
    else:
        FAILS.append(label)
        print('  FAIL  %s   %s' % (label, detail))


class _Par:
    def __init__(self, v):
        self.v = v

    def eval(self):
        return self.v


class _Pars:
    def __getattr__(self, name):
        return None


class _Chan:
    def __init__(self, v):
        self.v = v

    def eval(self):
        return self.v


class _WritablePars(_Pars):
    """par.active = 'on' in the extension, as on a real CHOP: the value is
    wrapped so .eval() keeps working."""
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value if isinstance(value, _Par) else _Par(value))


class _MouseIn:
    def __init__(self):
        self.par = _WritablePars()
        self.par.active = 'off'
        self.pos = {'tx': 0.0, 'ty': 0.0}

    def __getitem__(self, name):
        return _Chan(self.pos.get(name, 0.0))


class _Comp:
    def __init__(self):
        self.par = _Pars()
        for k, v in dict(Active=True, Waitidle=True, Idleseconds=2.0, Onlymodified=False,
                         Skipperform=False, Status='', Interval=10.0).items():
            setattr(self.par, k, _Par(v))
        self.mouse = _MouseIn()
        self.valid = True

    def op(self, name):
        return self.mouse if name == 'mousein_idle' else None


class _Clock:
    t = 100.0

    def monotonic(self):
        return self.t

    def __getattr__(self, name):
        return getattr(_time, name)


SCHEDULED = []


def fake_run(*args, **kw):
    SCHEDULED.append((args, kw))


src = io.open(EXT, encoding='utf-8').read()
g = {'run': fake_run, 'debug': lambda *a: None, 'op': type('O', (), {'TDResources': None})()}
exec(compile(src, EXT, 'exec'), g)
Ext = g['FNSAutosaveExt']
clock = _Clock()
g['time'] = clock

comp = _Comp()
ext = Ext.__new__(Ext)                   # skip __init__: no TD to defer into
ext.ownerComp = comp
ext._last_save = None
ext._saving = False
ext._idleWait = None
ext._idleGen = 0
saves = []
ext.Autosave = lambda: saves.append(clock.t)
status = []
ext._setStatus = lambda m: status.append(m)


def mouse_state():
    return comp.mouse.par.active.eval()


def poll():
    """Run the scheduled checks due now: the last scheduled idlePoll."""
    pending = [s for s in SCHEDULED if 'idlePoll' in str(s[0][0])]
    del SCHEDULED[:]
    for args, kw in pending:
        check_ms = kw.get('delayMilliSeconds')
        assert check_ms == ext.IDLE_POLL_MS, kw
        ext.idlePoll(args[2])
    # the deferred save is a lambda run a frame later
    for args, kw in [s for s in SCHEDULED if callable(s[0][0])]:
        args[0]()
    SCHEDULED[:] = [s for s in SCHEDULED if not callable(s[0][0])]


print('1. a due save waits, then goes once the mouse rests')
ext.Tick()
check('the wait started instead of a save', ext._idleWait is not None and saves == [])
check('the Mouse In turned on only now', mouse_state() == 'on', mouse_state())
check('one check is scheduled, by time, through the COMP (reinit-safe)',
      len(SCHEDULED) == 1 and 'args[0].ext.FNSAutosaveExt.idlePoll' in SCHEDULED[0][0][0]
      and SCHEDULED[0][1].get('delayMilliSeconds') == 250, SCHEDULED)
check('the status says it is waiting', status and 'waiting' in status[-1], status)
ext.Tick()
check('another cycle while waiting adds nothing', ext._idleGen == 1 and len(SCHEDULED) == 1)
poll()                                  # first look records the position
for step in range(7):                   # still for 1.75 s: not yet
    clock.t += 0.25
    poll()
check('not before the rest time', saves == [] and ext._idleWait is not None, saves)
clock.t += 0.25
poll()
clock.t += 0.25
poll()
check('the save goes after Idleseconds of rest', len(saves) == 1, saves)
check('the Mouse In is off again', mouse_state() == 'off', mouse_state())
check('nothing is scheduled any more', SCHEDULED == [], SCHEDULED)

print('2. movement restarts the rest')
saves.clear()
ext.Tick()
poll()
for step in range(8):
    clock.t += 0.25
    comp.mouse.pos['tx'] += 3.0          # moving the whole time
    poll()
check('a moving mouse holds the save', saves == [] and ext._idleWait is not None)
for step in range(9):
    clock.t += 0.25
    poll()
check('it saves once the mouse has rested', len(saves) == 1, saves)

print('3. switched off mid-wait')
saves.clear()
ext.Tick()
poll()
comp.par.Waitidle = _Par(False)
clock.t += 0.25
poll()
check('Wait For Mouse Rest turned off: the waiting save goes now', len(saves) == 1, saves)
comp.par.Waitidle = _Par(True)
saves.clear()
ext.Tick()
poll()
comp.par.Active = _Par(False)
clock.t += 0.25
poll()
check('Active turned off: the waiting save is dropped', saves == [] and ext._idleWait is None)
check('and the Mouse In is off', mouse_state() == 'off')
comp.par.Active = _Par(True)

print('4. a stale check from an earlier wait does nothing')
ext.Tick()
old = ext._idleGen
ext._endIdleWait()
ext.Tick()
del SCHEDULED[:]
ext.idlePoll(old)
check('a check for an older wait schedules nothing', SCHEDULED == [])

print('5. what never waits')
ext._endIdleWait()
del SCHEDULED[:]
saves.clear()
ext._skipReason = lambda: 'unmodified'
ext.Tick()
check('a save that would be skipped does not start a wait',
      ext._idleWait is None and any(callable(s[0][0]) for s in SCHEDULED))
del ext._skipReason
comp.par.Waitidle = _Par(False)
del SCHEDULED[:]
ext.Tick()
check('with the option off a due save is deferred a frame as before',
      ext._idleWait is None and len(SCHEDULED) == 1 and callable(SCHEDULED[0][0][0]))

print('6. shipping')
pre = io.open(PRE, encoding='utf-8').read()
check('the release bakes the new settings to their defaults',
      "'Waitidle', 'Idleseconds'" in pre)
check('and ships the Mouse In off', "_m.par.active = 'off'" in pre)
check('the launcher can read and write them',
      "'wait_idle': 'Waitidle'," in src and "'idle_seconds': 'Idleseconds'," in src
      and "'waiting_idle': self._idleWait is not None," in src)

print()
if FAILS:
    print('%d check(s) failed:' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all autosave idle checks pass')
