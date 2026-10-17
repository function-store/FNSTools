"""ConfigRegistry callbacks for FNS_Hub.

Persists every configurator tab's `state` table -- dividers, hideable-group
brackets, adopted built-ins' order/display/width (plus their original
`td_order`, so Restore still works after roaming). A configurator is any
direct child of the hub whose extension promotes SnapshotState/RestoreState;
the payload is keyed by that child's name (ToolbarConfigurator,
NavbarConfigurator, MainMenuConfigurator, ...).

Everything else on a bar is persisted by the publishing tool's own host
parameters. These tables are the one piece of layout the configurators own
outright: without them a bar layout dies with the component and never
follows the user to another project.

Restore REPLACES rather than merges -- each table is one coherent per-user
layout -- and re-applies it to the live registry immediately (the payload
lands long after the configurator's boot republish).

The hub's own Hub-page pars (Activetab, Tabuserorder) roam as plain
persisted parameters; they are not part of this payload.

Only a table the user CHANGED roams (2026-10-14). A release ships each
configurator's table and a copy of it as `state_default`
(packaging/surface_defaults.py); a table equal to that copy is the shipped
layout and is left out, so the next release's layout reaches the user.
Schema 1 tables were written before this rule and cannot be told from a
default, so they are ignored once (the owner's bar got the pre-10-10 dev
group back from one).

And a table is WRITTEN only when the user changed that surface this session
(its registry's markLayoutChanged, set by the configurators' edits and the
bar's group eye): otherwise the file's previous table is carried over, so a
project that merely loaded with another table keeps it to itself.
"""

STATE_SCHEMA = 2
STATE_DEFAULT = 'state_default'


def _configurators():
	out = {}
	for c in me.parent().children:
		if not c.isCOMP:
			continue
		try:
			ready = c.extensionsReady
		except Exception:
			ready = False
		if ready and hasattr(c, 'SnapshotState') and hasattr(c, 'RestoreState'):
			out[c.name] = c
	return out


def _layoutChanged(c):
	"""Did the user change the surface this configurator drives, this session?"""
	ext = c.extensions[0] if c.extensions else None
	reg = getattr(op, getattr(ext, 'REGISTRY_SHORTCUT', '') or '_', None)
	rext = getattr(reg.ext, getattr(ext, 'REGISTRY_EXT', ''), None) if reg is not None else None
	fn = getattr(rext, 'layoutChanged', None)
	return bool(fn()) if fn is not None else True     # unknown: behave as before


def _previousStates():
	"""The configurator tables the settings file holds now."""
	cfg = getattr(op, 'FNS_CONFIGREGISTRY', None)
	try:
		tools = (cfg.ConfigData or {}).get('tools', {}) if cfg is not None else {}
	except Exception:
		return {}
	section = tools.get('FNS_Hub') or next(
		(t for t in tools.values() if isinstance(t, dict)
		 and isinstance(t.get('state'), dict) and 'configurators' in t['state']), {})
	state = section.get('state') or {}
	if int(state.get('schema') or 1) < STATE_SCHEMA:
		return {}
	return state.get('configurators') or {}


def onConfigSave():
	states = {}
	previous = None
	for name, c in _configurators().items():
		if not _layoutChanged(c):
			if previous is None:
				previous = _previousStates()
			if previous.get(name):
				states[name] = previous[name]     # untouched: keep what the file had
			continue
		# SnapshotState refreshes live groups' collapsed state from the
		# registry (the bar-side eye writes only there) before dumping
		rows = c.SnapshotState()
		if not rows:
			continue
		shipped = c.op(STATE_DEFAULT)
		if shipped is not None and [[str(v) for v in r] for r in rows] == 				[[cell.val for cell in r] for r in shipped.rows()]:
			continue        # the shipped layout: let the next release's apply
		states[name] = rows
	if not states:
		return {}
	return {'schema': STATE_SCHEMA, 'configurators': states}


def onConfigLoad(data):
	if int(data.get('schema') or 1) < 2:
		return          # written before only-changes roamed: see the docstring
	states = data.get('configurators') or {}
	cfgs = _configurators()
	for name, rows in states.items():
		c = cfgs.get(name)
		# row 0 is the header, and it travels with the payload so a table
		# written by an older/newer column set still migrates on restore
		if c is None or not rows or 'kind' not in rows[0] or 'name' not in rows[0]:
			continue
		c.RestoreState(rows)
	return
