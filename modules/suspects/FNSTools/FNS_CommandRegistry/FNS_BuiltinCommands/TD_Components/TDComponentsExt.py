"""TD_Components - built-in commands that add third-party components.

Add Embody, Add TDMCP and Add TDX Launcher Utility: each fetches the
component's published release manifest, downloads the .tox it names,
checks the sha256 the manifest pins, and loads it at the project root.
A command is hidden (the registry's `enabled` reference) while its
component is already in the project, so the launcher's own sessions never
offer to add the utility they already carry.

Downloads go through the docked Web Client DAT, never `requests` on the
main thread. Verified files are kept in <system temp>/FNS_ComponentCache:
a cached file matching the manifest's sha skips the download, and with no
network the newest cached copy is loaded and named in the status line.
Reasoning and sources: docs/ComponentAddCommands.md.
"""

FNSCommand = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('FNSCommand')  # import
###

import glob
import hashlib
import json
import os
import re
import tempfile

def _kebab(name):
	return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()


def fns_command(fn=None, enabled=None, **meta):
	"""The shared decorator, branded builtin=True with a canonical id
	`td.components.<kebab-method>` (same derivation as TD_Session).

	`enabled` (docs/CommandAvailability.md) is attached to the harvested
	metadata here because the shared FNSCommand decorator has no keyword
	for it; the registry reads it from `_fns_command` like every other
	field."""
	def mark(f):
		meta.setdefault('canonical', 'td.components.' + _kebab(f.__name__))
		f = FNSCommand.fns_command(builtin=True, **meta)(f)
		if enabled:
			f._fns_command['enabled'] = enabled
		return f
	return mark(fn) if fn is not None else mark


def _embodyRelease(m):
	return m['version'], 'https://github.com/dylanroscover/Embody/releases/download/%s/%s' % (m['tag'], m['asset'])

def _tdmcpRelease(m):
	return m['version'], 'https://github.com/TouchDesigner/TDMCP/releases/download/%s/TDMCP.tox' % m['version']

def _launcherUtilityRelease(m):
	return m['version'], m['url']


# key -> what the component is called, where its manifest lives, how to read
# it, and what means "already in this project": a global OP shortcut, or
# (TDMCP 1.1.56 sets none) a root child carrying the given parent shortcut.
_COMPONENTS = {
	'embody': {
		'label': 'Embody',
		'manifest': 'https://github.com/dylanroscover/Embody/releases/latest/download/embody-release.json',
		'release': _embodyRelease,
		'opshortcut': 'Embody',
	},
	'tdmcp': {
		'label': 'TDMCP',
		'manifest': 'https://github.com/TouchDesigner/TDMCP/releases/latest/download/TDMCP.json',
		'release': _tdmcpRelease,
		'parentshortcut': 'TDMCP',
	},
	'launcherutility': {
		'label': 'TDX Launcher Utility',
		'manifest': 'https://launchdl.functionstore.tools/utility/latest.json',
		'release': _launcherUtilityRelease,
		'opshortcut': 'TDXLU',
	},
}

_HEADERS = {'User-Agent': 'FNS-Components'}
_TIMEOUT_MS = 60000
_MAX_HOPS = 5
_CACHE = os.path.join(tempfile.gettempdir(), 'FNS_ComponentCache')


class TDComponentsExt:
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self._requests = {}  # Web Client request id -> {'key', 'stage', ...}
		run('args[0]._announceCommands()', self, delayFrames=60)

	def onInitTD(self):
		run('args[0]._announceCommands()', self, delayFrames=60)

	def _announceCommands(self):
		FNSCommand.announce(self.ownerComp)

	# --- commands ------------------------------------------------------------

	@fns_command(enabled={'method': 'IsEmbodyMissing'})
	def AddEmbody(self):
		"""Download the latest Embody release and add it to the project root."""
		return self._add('embody')

	@fns_command(label='Add TDMCP', enabled={'method': 'IsTdmcpMissing'})
	def AddTdmcp(self):
		"""Download the latest TDMCP release (Derivative's MCP server) and add it to the project root."""
		return self._add('tdmcp')

	@fns_command(label='Add TDX Launcher Utility', enabled={'method': 'IsLauncherUtilityMissing'})
	def AddLauncherUtility(self):
		"""Download the latest TDX Launcher Utility and add it to the project root."""
		return self._add('launcherutility')

	# --- availability (registry `enabled` refs; query-time, cheap) ----------

	def IsEmbodyMissing(self):
		return self._present('embody') is None

	def IsTdmcpMissing(self):
		return self._present('tdmcp') is None

	def IsLauncherUtilityMissing(self):
		return self._present('launcherutility') is None

	# --- web client (wired from webclient_callbacks) -------------------------

	# The callbacks fire inside the Web Client DAT's own cook: a new request
	# or a loadTox from there is a cook dependency loop, and the load never
	# lands. So they only copy what arrived and hand it on a frame later.

	def onWebResponse(self, statusCode, headerDict, data, requestId):
		job = self._requests.pop(requestId, None)
		if job is not None:
			run(self._onResponse, job, dict(statusCode), dict(headerDict or {}), bytes(data), delayFrames=1)

	def onWebError(self, requestId, error):
		job = self._requests.pop(requestId, None)
		if job is not None:
			run(self._fallBack, job, str(error), delayFrames=1)

	def _onResponse(self, job, statusCode, headerDict, data):
		self._clearWebClient()
		code = statusCode.get('code')
		# The Web Client DAT usually follows GitHub's release redirects, but
		# not always (an unfollowed 302 seen once on 2026-10-22), so follow
		# the Location ourselves.
		location = {k.lower(): v for k, v in headerDict.items()}.get('location')
		if code in (301, 302, 303, 307, 308) and location and job.get('hops', 0) < _MAX_HOPS:
			extra = {k: v for k, v in job.items() if k not in ('key', 'stage', 'url')}
			extra['hops'] = job.get('hops', 0) + 1
			self._request(job['key'], job['stage'], location, **extra)
			return
		if code != 200:
			self._fallBack(job, 'HTTP %s %s fetching the %s (%s)' % (code, statusCode.get('message', ''), job['stage'], job['url']))
			return
		if job['stage'] == 'manifest':
			self._onManifest(job, data)
		else:
			self._onTox(job, data)

	# --- flow ----------------------------------------------------------------

	def _add(self, key):
		label = _COMPONENTS[key]['label']
		found = self._present(key)
		if found is not None:
			return {'ok': False, 'error': '%s is already in this project' % label, 'path': found.path}
		if any(j['key'] == key for j in self._requests.values()):
			return {'ok': False, 'error': '%s is already being fetched' % label}
		self._request(key, 'manifest', _COMPONENTS[key]['manifest'])
		self._status('Fetching the latest %s release...' % label)
		return {'ok': True, 'started': True}

	def _request(self, key, stage, url, **extra):
		rid = self.ownerComp.op('webclient').request(url, 'GET', header=_HEADERS, timeout=_TIMEOUT_MS)
		self._requests[rid] = dict(key=key, stage=stage, url=url, **extra)

	def _onManifest(self, job, data):
		key = job['key']
		try:
			manifest = json.loads(bytes(data).decode('utf-8'))
			version, url = _COMPONENTS[key]['release'](manifest)
			sha = manifest['sha256'].lower()
		except Exception as e:
			self._fallBack(job, 'unreadable release manifest (%s)' % e)
			return
		path = self._cachePath(key, version)
		if os.path.isfile(path) and self._sha(path) == sha:
			self._load(key, path, version)
			return
		self._request(key, 'tox', url, version=version, sha=sha, path=path)
		self._status('Downloading %s %s...' % (_COMPONENTS[key]['label'], version))

	def _onTox(self, job, data):
		data = bytes(data)
		got = hashlib.sha256(data).hexdigest()
		if got != job['sha']:
			self._fail(job['key'], 'checksum mismatch on %s (expected %s, got %s)' % (job['url'], job['sha'], got))
			return
		try:
			os.makedirs(_CACHE, exist_ok=True)
			with open(job['path'], 'wb') as f:
				f.write(data)
		except OSError as e:
			self._fail(job['key'], 'could not write %s (%s)' % (job['path'], e))
			return
		self._load(job['key'], job['path'], job['version'])

	def _fallBack(self, job, why):
		"""No network or a bad answer: load the newest verified cached copy."""
		key = job['key']
		cached = sorted(glob.glob(os.path.join(_CACHE, key + '-*.tox')), key=os.path.getmtime)
		if not cached:
			self._fail(key, why)
			return
		path = cached[-1]
		version = os.path.basename(path)[len(key) + 1:-len('.tox')]
		debug('TD_Components: %s fetch failed (%s); using cached %s' % (key, why, path))
		self._load(key, path, version, note=' (offline, cached copy)')

	def _load(self, key, path, version, note=''):
		label = _COMPONENTS[key]['label']
		if self._present(key) is not None:
			self._status('%s is already in this project' % label)
			return
		home = op('/')
		right = [c.nodeX + c.nodeWidth for c in home.children]
		top = [c.nodeY + c.nodeHeight for c in home.children]
		try:
			comp = home.loadTox(path)
		except Exception as e:
			self._fail(key, 'loadTox failed for %s (%s)' % (path, e))
			return
		# right of everything at the root, top row, on the 200 grid
		comp.nodeX = (int(max(right, default=0)) // 200 + 2) * 200
		comp.nodeY = (int(max(top, default=0)) // 200 - 1) * 200
		self._status('Added %s %s at %s%s. Save the project to keep it.' % (label, version, comp.path, note))

	def _fail(self, key, why):
		label = _COMPONENTS[key]['label']
		debug('TD_Components: Add %s failed: %s' % (label, why))
		self._status('Add %s failed: %s' % (label, why))

	# --- helpers -------------------------------------------------------------

	def _present(self, key):
		"""The component already in this project, or None."""
		spec = _COMPONENTS[key]
		if 'opshortcut' in spec:
			try:
				return getattr(op, spec['opshortcut'])
			except Exception:
				return None
		for c in op('/').children:
			if c.isCOMP and c.par.parentshortcut.eval() == spec['parentshortcut']:
				return c
		return None

	def _cachePath(self, key, version):
		safe = re.sub(r'[^0-9A-Za-z._-]', '_', str(version))
		return os.path.join(_CACHE, '%s-%s.tox' % (key, safe))

	def _sha(self, path):
		with open(path, 'rb') as f:
			return hashlib.sha256(f.read()).hexdigest()

	def _clearWebClient(self):
		"""Drop the request rows the DAT keeps, so a 1.7 MB tox does not
		sit in its text until the next request."""
		self.ownerComp.op('webclient').par.clear.pulse()

	def _status(self, text):
		ui.status = text
