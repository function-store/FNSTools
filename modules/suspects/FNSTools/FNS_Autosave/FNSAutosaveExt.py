"""
FNS Autosave - periodic project save driven by a Timer CHOP.

Standalone by design: drop this COMP into any project and its Autosave
page works on its own, with no toolkit root and no launcher present.

Ported out of the TDXLU launcher companion (2026-08-31), where these
settings BOUND UP to a parent Autosave page on the utility. That parent
no longer exists here, so the pars are plain constants this COMP owns.
Nothing is lost: a launcher drives autosave through the fns.autosave
capability commands (AutosaveState / AutosaveSet), which read and write
this COMP's own pars either way.

Save modes:

  td         project.save() - TouchDesigner's own Save, so it honours the
             "Increment Filename when Saving" / "Copy to Backup Folder"
             preferences the user already set (a new numbered .toe per save
             while increment is on).
  overwrite  the same call with that preference held at Off for the duration,
             so every save lands back in the .toe already open however the
             preference is set. It is done through the preference rather than
             project.save(<path>) deliberately: an explicit-path save is Save
             As, and TD answers an existing target with a modal overwrite
             prompt - fine for one click, fatal for something on a timer.

A save is synchronous and stalls the frame for as long as the .toe takes to
write, so the timer never fires one inside a cook: the Timer CHOP callback
defers it by a frame through run().

Wait For Mouse Rest (Waitidle) holds a due save until the mouse has not
moved for Idleseconds, so the stall never lands in the middle of a drag.
Nothing runs per frame for it: the Mouse In CHOP is switched on only while
a save is waiting (it cooks every frame while on), and Python reads it four
times a second, again only while waiting.
"""

import contextlib
import os
import time


class FNSAutosaveExt:
	"""Save the running project on an interval, without touching the timeline."""

	MODES = ('td', 'overwrite')
	MIN_INTERVAL_MIN = 0.5
	MAX_INTERVAL_MIN = 1440.0

	# Wait For Mouse Rest
	IDLE_POLL_MS = 250
	IDLE_MIN_SEC = 1.0
	MOUSE_IN = 'mousein_idle'
	MOUSE_CHANS = ('tx', 'ty', 'lselect', 'mselect', 'rselect', 'wheel')

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self._last_save = None   # epoch of the last save THIS COMP performed
		self._saving = False
		self._idleWait = None    # {'gen', 'pos', 'since'} while a save waits
		self._idleGen = 0
		run(lambda: self._afterInit(), endFrame=True)
		# Deferred: the registry may still be promoting its /sys global.
		run('args[0]._registerLauncherCommands()', self, delayFrames=60)

	def _afterInit(self):
		self._ensurePars()
		# a reinit drops a waiting save with the old instance; its Mouse In
		# must not be left cooking every frame for nobody
		self._mouseActive(False)
		self._syncTimerFromPars()

	# --- Settings ---------------------------------------------------------

	def _ensurePars(self):
		"""Get-or-create the Wait For Mouse Rest pars on the Autosave page,
		after Skip In Perform Mode. Copies made before them gain them here;
		an existing par keeps its value."""
		c = self.ownerComp
		page = next((p for p in c.customPages if p.name == 'Autosave'), None)
		if page is None:
			return
		anchor = self._par('Skipperform')
		base = float(anchor.order) if anchor is not None else 4.0
		p = self._par('Waitidle')
		if p is None:
			p = page.appendToggle('Waitidle', label='Wait For Mouse Rest')[0]
			p.default = False
			p.val = False
		p.help = ('Hold a due save until the mouse has rested for Mouse Rest '
				  'seconds, so the save never interrupts a drag. Nothing runs '
				  'for this between saves.')
		p.order = base + 0.3
		p = self._par('Idleseconds')
		if p is None:
			p = page.appendFloat('Idleseconds', label='Mouse Rest (sec)')[0]
			p.default = 5.0
			p.val = 5.0
		p.min = self.IDLE_MIN_SEC
		p.clampMin = True
		p.normMin = self.IDLE_MIN_SEC
		p.normMax = 30.0
		p.help = ('Seconds the mouse must stay still (no movement, button or '
				  'wheel) before a waiting save goes ahead.')
		p.enableExpr = "me.par.Waitidle"
		p.order = base + 0.6

	def onSettingChange(self, par):
		"""Wiring for parexec_settings: Active and Interval re-sync the timer
		(a toggle from the dialog or the main menu button used to change
		nothing until the next reinit); the idle pars only refresh the
		status, so tuning them never restarts the countdown."""
		if par.name in ('Active', 'Interval'):
			self._syncTimerFromPars()
		elif self._flag('Active') and self._idleWait is None:
			self._setStatus(self._onText())

	def _par(self, name):
		return getattr(self.ownerComp.par, name, None)

	def _flag(self, name, default=False):
		p = self._par(name)
		if p is None:
			return default
		try:
			return bool(p.eval())
		except Exception:
			return default

	def Interval(self):
		"""Minutes between saves, clamped to what the timer can hold."""
		p = self._par('Interval')
		try:
			value = float(p.eval()) if p is not None else 10.0
		except Exception:
			value = 10.0
		return min(self.MAX_INTERVAL_MIN, max(self.MIN_INTERVAL_MIN, value))

	def Mode(self):
		"""'td' (honour TD's save preferences) or 'overwrite'."""
		p = self._par('Mode')
		try:
			value = str(p.eval()).strip().lower() if p is not None else 'td'
		except Exception:
			value = 'td'
		return value if value in self.MODES else 'td'

	def IdleSeconds(self):
		"""Seconds the mouse must rest before a waiting save goes ahead."""
		p = self._par('Idleseconds')
		try:
			value = float(p.eval()) if p is not None else 5.0
		except Exception:
			value = 5.0
		return max(self.IDLE_MIN_SEC, value)

	def _onText(self):
		text = f'On - every {self._intervalText()}'
		if self._flag('Waitidle'):
			text += f', after {self.IdleSeconds():g}s of mouse rest'
		return text

	def _intervalText(self):
		minutes = self.Interval()
		if minutes < 1.0:
			return f'{round(minutes * 60)}s'
		if abs(minutes - round(minutes)) < 0.01:
			return f'{int(round(minutes))} min'
		return f'{minutes:g} min'

	# --- Readouts ---------------------------------------------------------

	def _setStatus(self, msg):
		p = self._par('Status')
		if p is None:
			return
		try:
			p.val = str(msg)[:120]
		except Exception:
			pass

	def _setLastSave(self, msg):
		p = self._par('Lastsave')
		if p is None:
			return
		try:
			p.val = str(msg)[:120]
		except Exception:
			pass

	# --- Timer ------------------------------------------------------------

	def _syncTimerFromPars(self):
		"""Timer length = Interval minutes; Active drives play / bypass."""
		active = self._flag('Active')
		timer = self.ownerComp.op('timer_autosave')
		if timer:
			try:
				timer.par.length = self.Interval() * 60.0
				timer.par.lengthunits = 'seconds'
				timer.par.cycle = True
				if hasattr(timer.par, 'cyclelimit'):
					timer.par.cyclelimit = False
				timer.par.play = active
				timer.bypass = not active
				if active:
					# Restart the countdown so a settings change never leaves
					# a half-elapsed cycle at the old length.
					timer.par.initialize.pulse()
					timer.par.start.pulse()
			except Exception as e:
				debug(f'FNS_Autosave: timer sync failed: {e}')
		# the countdown restarted (or stopped): a save waiting on the old
		# one is dropped
		self._endIdleWait()
		if active:
			self._setStatus(self._onText())
		else:
			self._setStatus('Off')

	def _syncTimer(self):
		"""Refresh the timer from Active / Interval (called by the parent)."""
		self._syncTimerFromPars()

	def Tick(self):
		"""Timer cycle. Never save inside the CHOP cook - defer a frame."""
		if not self._flag('Active'):
			return
		if self._flag('Waitidle') and self._skipReason() is None:
			self._startIdleWait()
			return
		run(lambda: self.Autosave(), delayFrames=1)

	# --- Wait For Mouse Rest ----------------------------------------------

	def _mouseIn(self, create=True):
		"""The Mouse In CHOP the wait reads, created on first use where a
		copy predates it. Kept Active Off outside a wait."""
		m = self.ownerComp.op(self.MOUSE_IN)
		if m is None and create:
			m = self.ownerComp.create(mouseinCHOP, self.MOUSE_IN)
			m.par.active = 'off'
			m.par.output = 'absolute'
			m.par.lbuttonname = 'lselect'
			m.par.mbuttonname = 'mselect'
			m.par.rbuttonname = 'rselect'
			m.par.wheel = 'wheel'
			m.nodeX, m.nodeY = 400, -400
		return m

	def _mouseActive(self, on):
		m = self._mouseIn(create=on)
		if m is None:
			return None
		want = 'on' if on else 'off'
		if m.par.active.eval() != want:
			m.par.active = want
		return m

	def _mousePos(self, m):
		out = []
		for name in self.MOUSE_CHANS:
			ch = m[name]
			out.append(round(float(ch.eval()), 4) if ch is not None else 0.0)
		return tuple(out)

	def _startIdleWait(self):
		"""A save is due: hold it until the mouse rests. A cycle that comes
		round while one is already waiting adds nothing."""
		if self._idleWait is not None:
			return
		self._mouseActive(True)
		self._idleGen += 1
		self._idleWait = {'gen': self._idleGen, 'pos': None, 'since': time.monotonic()}
		self._setStatus(f'Save due - waiting for {self.IdleSeconds():g}s of mouse rest')
		self._scheduleIdlePoll()

	def _scheduleIdlePoll(self):
		# through the COMP, so a reinit's fresh instance (no wait) ends it
		run('args[0].valid and args[0].ext.FNSAutosaveExt.idlePoll(args[1])',
			self.ownerComp, self._idleGen,
			delayMilliSeconds=self.IDLE_POLL_MS, delayRef=op.TDResources)

	def _endIdleWait(self):
		self._idleWait = None
		self._mouseActive(False)

	def idlePoll(self, gen):
		"""Wiring: one look at the mouse while a save waits (4 times a
		second). Saves once it has rested long enough."""
		w = self._idleWait
		if w is None or w['gen'] != gen:
			return
		if not self._flag('Active'):
			self._endIdleWait()
			return
		ready = not self._flag('Waitidle')     # switched off mid-wait: go now
		if not ready:
			m = self._mouseIn()
			pos = self._mousePos(m)
			now = time.monotonic()
			if pos != w['pos']:
				w['pos'], w['since'] = pos, now
			ready = now - w['since'] >= self.IdleSeconds()
		if not ready:
			self._scheduleIdlePoll()
			return
		self._endIdleWait()
		run(lambda: self.Autosave(), delayFrames=1)

	# --- Saving -----------------------------------------------------------

	def _projectPath(self):
		"""Absolute path of the .toe this session is open on, or None."""
		try:
			folder = project.folder
			name = project.name
		except Exception:
			return None
		if not folder or not name:
			return None
		return os.path.join(folder, name).replace('\\', '/')

	def _performing(self):
		try:
			return bool(ui.performMode)
		except Exception:
			return False

	def _modifiedCount(self):
		"""Operators changed since the last save (project.modified)."""
		try:
			return len(project.modified)
		except Exception:
			# No dirty list -> treat as modified, so a save is never skipped
			# on a TD build that does not report one.
			return 1

	def _skipReason(self):
		"""'perform' or 'unmodified' when the skip toggles say this save
		should not happen, else None. Asked before a save waits for the
		mouse too, so an unchanged project never starts a wait."""
		if self._flag('Skipperform') and self._performing():
			return 'perform'
		if self._flag('Onlymodified', True) and not self._modifiedCount():
			return 'unmodified'
		return None

	def Autosave(self):
		"""One interval save, honouring the skip toggles."""
		return self._save(reason='timer')

	def SaveNow(self):
		"""Save right now whatever the skip toggles say (pulse / launcher)."""
		return self._save(reason='manual', force=True)

	INCREMENT_PREF = 'general.inc'

	@contextlib.contextmanager
	def _noIncrement(self, hold):
		"""Hold TD's "Increment Filename when Saving" preference at Off.

		Only for the duration of one save, and only when hold is True - the
		preference is the user's, so it is always put back, including when
		the save raises. Missing key (an older/newer TD naming it something
		else) degrades to a plain save rather than failing.
		"""
		previous = None
		held = False
		if hold:
			try:
				previous = ui.preferences[self.INCREMENT_PREF]
				if int(previous) != 0:
					ui.preferences[self.INCREMENT_PREF] = 0
					held = True
			except Exception as e:
				debug(f'FNS_Autosave: increment preference unavailable: {e}')
		try:
			yield
		finally:
			if held:
				try:
					ui.preferences[self.INCREMENT_PREF] = previous
				except Exception as e:
					debug(f'FNS_Autosave: could not restore {self.INCREMENT_PREF}: {e}')

	def _save(self, reason='timer', force=False):
		stamp = time.strftime('%H:%M:%S')
		if self._saving:
			return {'ok': False, 'saved': False, 'error': 'a save is already running'}
		path = self._projectPath()
		if not path or not os.path.exists(path):
			# A never-saved project has no file to save into - project.save()
			# would invent one wherever TD's default folder points, so refuse
			# rather than scatter .toe files.
			self._setStatus(f'Idle {stamp} - project has never been saved')
			return {
				'ok': False,
				'saved': False,
				'error': 'project has never been saved to disk - save it once first',
			}
		if not force:
			skip = self._skipReason()
			if skip is not None:
				self._setStatus('Skipped %s - %s' % (
					stamp, 'perform mode' if skip == 'perform' else 'no changes'))
				return {'ok': True, 'saved': False, 'skipped': skip}
		mode = self.Mode()
		self._saving = True
		try:
			with self._noIncrement(mode == 'overwrite'):
				saved = project.save()
		except Exception as e:
			self._setStatus(f'Save failed {stamp}: {e}')
			return {'ok': False, 'saved': False, 'error': str(e)}
		finally:
			self._saving = False
		if not saved:
			# save() returns False when TD declined - e.g. an overwrite the
			# user answered no to.
			self._setStatus(f'Not saved {stamp} - TouchDesigner declined')
			return {'ok': False, 'saved': False, 'error': 'TouchDesigner did not save'}
		self._last_save = time.time()
		how = 'manual' if reason == 'manual' else 'auto'
		self._setStatus(f'Saved {stamp} -> {project.name} ({how})')
		self._setLastSave(f'{stamp} {project.name}')
		return {
			'ok': True,
			'saved': True,
			'name': project.name,
			'path': self._projectPath(),
			'mode': mode,
			'reason': reason,
		}

	# --- Launcher readout -------------------------------------------------

	def _nextIn(self):
		"""Seconds until the next timer cycle, or None when idle."""
		if not self._flag('Active'):
			return None
		timer = self.ownerComp.op('timer_autosave')
		if not timer:
			return None
		# timer_fraction is one of the Timer CHOP's default output channels;
		# timer_seconds only exists when its own output toggle is on.
		try:
			remaining = (1.0 - float(timer['timer_fraction'])) * self.Interval() * 60.0
		except Exception:
			return None
		return max(0.0, remaining)

	# --- self-contained write path + capability -----------------------------
	# Autosave owns its OWN settings here, so this component works as a
	# standalone drop with nothing else installed. Nested in the TDXLU
	# companion its pars bind UP to that COMP (parent masters, child binds
	# up) and a write simply propagates through the bind - which is why the
	# refusal rule below rejects EXPRESSION / EXPORT but NOT bind. Refusing
	# bind would refuse every write while nested, which is the whole normal
	# case.

	FIELDS = {
		'active': 'Active',
		'interval': 'Interval',
		'mode': 'Mode',
		'only_modified': 'Onlymodified',
		'skip_perform': 'Skipperform',
		'wait_idle': 'Waitidle',
		'idle_seconds': 'Idleseconds',
	}

	def _coerce(self, key, value):
		"""JSON value -> what the matching parameter accepts."""
		if key in ('interval', 'idle_seconds'):
			return float(value)
		if key == 'mode':
			mode = str(value).strip().lower()
			if mode not in self.MODES:
				raise ValueError("mode must be one of %s, got %r" % (self.MODES, value))
			return mode
		if isinstance(value, str):
			return 1 if value.strip().lower() in ('1', 'true', 'on', 'yes') else 0
		return 1 if value else 0

	def AutosaveSet(self, fields):
		"""Write autosave settings. Never raises; reports what it refused."""
		if not isinstance(fields, dict):
			return {'ok': False, 'error': 'fields must be an object'}
		applied, refused = {}, []
		for key, par_name in self.FIELDS.items():
			if key not in fields:
				continue
			par = self._par(par_name)
			if par is None:
				refused.append({'field': key, 'error': 'no parameter %s' % par_name})
				continue
			# BIND is fine to write through (it lands on the master); an
			# expression or export would be DESTROYED by a write, so those
			# are refused - the same rule every remote write here keeps.
			if par.mode not in (ParMode.CONSTANT, ParMode.BIND):
				refused.append({'field': key,
								'error': '%s is %s - not writable' % (par_name, par.mode)})
				continue
			try:
				par.val = self._coerce(key, fields[key])
			except Exception as e:
				refused.append({'field': key, 'error': str(e)})
				continue
			applied[key] = par.eval()
		self._syncTimer()
		state = self.AutosaveState() or {}
		state.update({'ok': not refused, 'applied': applied, 'refused': refused})
		return state

	def FnsCommands(self):
		"""Spec list for FNS_CommandRegistry - also called by its rescan.

		Capability `fns.autosave`: a consumer that recognises the id opens
		its own settings UI (the launcher has one); one that does not still
		gets a working Save Now. Announced from HERE rather than from a
		host COMP so the capability travels with the component."""
		cap = 'fns.autosave'
		return [
			{'id': 'autosave', 'label': 'Autosave...',
			 'help': 'Save this project on a timer, from inside TouchDesigner',
			 'method': 'AutosaveState', 'state': 'Active',
			 'surface': ['session', 'context-menu'], 'capability': cap},
			{'id': 'autosave_now', 'label': 'Save now',
			 'help': 'Save immediately, ignoring the skip toggles',
			 'method': 'SaveNow', 'hidden': True, 'capability': cap},
			{'id': 'autosave_get', 'label': 'Autosave: settings',
			 'help': 'Current autosave settings and readouts, as data',
			 'method': 'AutosaveState', 'hidden': True, 'capability': cap},
			{'id': 'autosave_set', 'label': 'Autosave: write settings',
			 'help': 'kwargs: fields {active, interval, mode, wait_idle, idle_seconds, ...}',
			 'method': 'AutosaveSet', 'hidden': True, 'capability': cap},
		]

	def _registerLauncherCommands(self):
		"""Announce the fns.autosave capability. Guarded - no registry is
		ever guaranteed (a standalone drop just skips); the tag makes a
		registry that arrives LATER rediscover this COMP by rescan."""
		try:
			self.ownerComp.tags.add('fnscommands')
		except Exception:
			pass
		try:
			reg = getattr(op, 'FNS_COMMANDREGISTRY', None)
			if reg is not None and hasattr(reg, 'Register'):
				reg.Register(self.ownerComp, self.FnsCommands())
		except Exception:
			pass

	def AutosaveState(self):
		"""Settings + readouts for the launcher (command autosave_get)."""
		path = self._projectPath()
		status = self._par('Status')
		try:
			status_text = str(status.eval()) if status is not None else ''
		except Exception:
			status_text = ''
		return {
			'ok': True,
			'active': self._flag('Active'),
			'interval': self.Interval(),
			'mode': self.Mode(),
			'only_modified': self._flag('Onlymodified', True),
			'skip_perform': self._flag('Skipperform'),
			'wait_idle': self._flag('Waitidle'),
			'idle_seconds': self.IdleSeconds(),
			'waiting_idle': self._idleWait is not None,
			'status': status_text,
			'last_save': self._last_save,
			'next_in': self._nextIn(),
			'modified': self._modifiedCount(),
			'perform': self._performing(),
			'project': project.name,
			'project_path': path,
			'project_saved': bool(path and os.path.exists(path)),
			'project_save_time': str(project.saveTime),
		}
