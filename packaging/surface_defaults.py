"""Shipped surface layout: the authored defaults every release ships.

What a new user sees on the toolbar, navbar, main menu, op menu, pane-type
menu and hub tabs comes from packaging/surface_defaults.json, never from
the development project's live arrangement (docs/ShippedSurfaceDefaults.md).
The author arranges those surfaces like any user; the arrangement reaches
releases only when they decide it should, by taking a snapshot:

    exec(open('packaging/surface_defaults.py').read(), sd := {})
    sd['WriteSnapshot'](op('/FNSTools'))          # in TouchDesigner

Two kinds of state are captured and applied:

- each tool's own surface parameters: the tool par a registry host's
  layout par is bound to (`Tbmenuorder` behind the toolbar host's
  `Menuorder`, `Hbtaborder` behind the hub host's `Taborder`, ...);
- the Hub configurators' `state` tables: TD's built-ins, dividers and
  groups. A group's start bracket stores its whole membership, so it still
  forms on an install that lacks some of its tools.

A third, hand-written key, `shipped_values`, holds any other par whose
dev value must not ship ({package: {relative path: {par: value}}}): the
dev workspace VSCodeTools opens, a test file TimelineTools exported to.
The snapshot never writes it and carries it over unchanged; the owner
edits it by hand (docs/ShippedSurfaceDefaults.md).

`Apply` runs from pre_release_common on the STAGED copy of each package,
so the live component is never touched. Plain Python at module level: the
offline test imports this file without TouchDesigner.
"""

import json

DEFAULTS_PATH = 'packaging/surface_defaults.json'

# Registry hosts whose layout a release ships, by the host operator's name.
HOST_NAMES = (
	'FNS_ToolbarRegistry', 'FNS_NavbarRegistry', 'FNS_MainMenuRegistry',
	'FNS_HubRegistry', 'FNS_OpMenuRegistry', 'FNS_PaneTypeRegistry',
	'FNS_OverlayRegistry',  # a layer's stacking order (Menuorder)
)

# The host pars that are layout. Registration switches (Autoregister,
# Register, ...) are a tool's behaviour, not its place, and stay as authored.
LAYOUT_HOST_PARS = ('Menuorder', 'Displayed', 'Barwidth', 'Align', 'Anchor',
					'Taborder', 'Tablabel')

CONFIGURATORS = ('ToolbarConfigurator', 'NavbarConfigurator',
				 'MainMenuConfigurator', 'OpMenuConfigurator')

ANCHOR_SEP = '|'   # FNS_Hub ConfiguratorBase.ANCHOR_SEP
BIND_PREFIX = 'parent().par.'


def _boundToolPar(host, host_par_name):
	"""The tool par a host's layout par is bound to, as (owner, name), or
	None when the host par is not bound that way."""
	p = getattr(host.par, host_par_name, None)
	if p is None:
		return None
	expr = str(p.bindExpr or '')
	if p.mode.name != 'BIND' or not expr.startswith(BIND_PREFIX):
		return None
	name = expr[len(BIND_PREFIX):].strip()
	if not name.isidentifier():
		return None
	return host.parent(), name


def _relPath(pkg, comp):
	return '.' if comp == pkg else comp.path[len(pkg.path) + 1:]


def _packageNames(catalog_path='packaging/catalog.json'):
	with open(catalog_path, encoding='utf-8') as f:
		cat = json.load(f)
	pk = cat.get('packages', cat)
	if isinstance(pk, dict):
		return set(pk.keys())
	return {p.get('name') for p in pk if isinstance(p, dict)}


def SnapshotPackage(pkg):
	"""{relative owner path: {tool par: value}} for one live package."""
	out = {}
	for host_name in HOST_NAMES:
		for host in pkg.findChildren(name=host_name):
			for hp in LAYOUT_HOST_PARS:
				bound = _boundToolPar(host, hp)
				if bound is None:
					continue
				owner, name = bound
				tp = owner.par[name]
				if tp is None or tp.mode.name != 'CONSTANT':
					continue
				v = tp.eval()
				if isinstance(v, float) and v.is_integer():
					v = int(v)
				out.setdefault(_relPath(pkg, owner), {})[name] = v
	return out


def SnapshotConfigurator(cfg):
	"""The configurator's state table, with every group's start bracket
	holding the group's members in their current order."""
	t = cfg.op('state')
	if t is None:
		return None
	rows = [[c.val for c in r] for r in t.rows()]
	ext = cfg.extensions[0] if cfg.extensions else None
	api = ext._api() if ext is not None and hasattr(ext, '_api') else None
	if api is None or not rows:
		return rows
	head = rows[0]
	ki, gi, ai = head.index('kind'), head.index('group_id'), head.index('anchor')
	ni = head.index('name')
	# a group's visibility row outlives its brackets when the group is
	# emptied: dev-side leftovers, not a layout anyone ships
	bracketed = {r[gi] for r in rows[1:] if r[ki] == 'groupstart'}
	rows = [head] + [r for r in rows[1:]
					 if not (r[ki] == 'group' and r[ni] not in bracketed)]
	groups = getattr(api, 'Groups', {}) or {}
	widgets = api.Widgets
	for r in rows[1:]:
		if r[ki] != 'groupstart':
			continue
		members = [m for m in (groups.get(r[gi]) or {}).get('members', [])
				   if not api._isGroupMarker(widgets.get(m))]
		if members:
			r[ai] = ANCHOR_SEP.join(members)
	return rows


def Snapshot(root, hub=None):
	"""Every package's surface pars plus the Hub configurators' tables."""
	names = _packageNames()
	packages = {}
	for c in root.children:
		if c.name not in names:
			continue
		got = SnapshotPackage(c)
		if got:
			packages[c.name] = got
	hub = hub or root.op('FNS_Hub')
	configurators = {}
	if hub is not None:
		for n in CONFIGURATORS:
			cfg = hub.op(n)
			if cfg is not None:
				rows = SnapshotConfigurator(cfg)
				if rows:
					configurators[n] = rows
	return {'packages': dict(sorted(packages.items())),
			'configurators': configurators}


def WriteSnapshot(root, path=DEFAULTS_PATH):
	"""Take the live arrangement as the new release default. The
	hand-written `shipped_values` of the file already there are kept."""
	data = Snapshot(root)
	try:
		kept = Load(path).get('shipped_values')
	except (OSError, ValueError):
		kept = None
	if kept:
		data['shipped_values'] = kept
	problems = Problems(data)
	if problems:
		raise ValueError('surface defaults not written: ' + '; '.join(problems))
	with open(path, 'w', encoding='utf-8', newline='\n') as f:
		json.dump(data, f, indent=1, ensure_ascii=False)
		f.write('\n')
	return data


def Load(path=DEFAULTS_PATH):
	with open(path, encoding='utf-8') as f:
		return json.load(f)


def Apply(pkg, data):
	"""Write the defaults onto a STAGED package copy. Returns what changed,
	as (path, par, value) triples; raises on a par the file names that the
	package no longer has, so a stale file fails the export loudly."""
	changed = []
	owners = []
	for key in ('packages', 'shipped_values'):
		owners.extend((data.get(key, {}).get(pkg.name) or {}).items())
	for rel, pars in owners:
		owner = pkg if rel == '.' else pkg.op(rel)
		if owner is None:
			raise LookupError(f'surface defaults: {pkg.name}/{rel} not found')
		for name, value in pars.items():
			p = owner.par[name]
			if p is None:
				raise LookupError(f'surface defaults: {owner.path} has no {name}')
			# ParMode is a script global in TD, not an attribute of the td
			# module, and this file is exec'd into a bare namespace: take the
			# enum from the par itself
			constant = type(p.mode).CONSTANT
			if p.mode != constant:
				p.mode = constant
			if p.val != value:
				p.val = value
				changed.append((owner.path, name, value))
	for name, rows in (data.get('configurators') or {}).items():
		cfg = pkg.op(name)
		t = cfg.op('state') if cfg is not None else None
		if t is None:
			continue
		if [[c.val for c in r] for r in t.rows()] != rows:
			t.clear()
			for r in rows:
				t.appendRow([str(c) for c in r])
			changed.append((t.path, 'rows', len(rows)))
	return changed


ORDER_SUFFIXES = ('menuorder', 'taborder')


def Problems(data):
	"""What is wrong with a defaults document, as sentences (empty = fine).
	Pure Python: the offline test runs it on the committed file."""
	out = []
	if (not isinstance(data, dict) or not {'packages', 'configurators'} <= set(data)
			or set(data) - {'packages', 'configurators', 'shipped_values'}):
		return ['the file holds "packages", "configurators" and optionally "shipped_values"']
	for pkg, owners in (data.get('shipped_values') or {}).items():
		if not isinstance(owners, dict) or not all(
				isinstance(p, dict) and p for p in owners.values()):
			out.append(f'shipped_values/{pkg}: expected {{path: {{par: value}}}}')
			continue
		for rel, pars in owners.items():
			for name in pars:
				if name in (data['packages'].get(pkg) or {}).get(rel, {}):
					out.append(f'shipped_values/{pkg}/{rel}.{name} is also a surface par')
	seen = {}
	for pkg, owners in data['packages'].items():
		for rel, pars in owners.items():
			for name, value in pars.items():
				low = name.lower()
				if low.endswith(ORDER_SUFFIXES):
					if not isinstance(value, int):
						out.append(f'{pkg}/{rel}.{name} is not a whole number')
						continue
					if value < 0:
						continue
					key = (name, value)
					if key in seen:
						out.append(f'{pkg}/{rel}.{name} = {value} ties with {seen[key]}')
					else:
						seen[key] = f'{pkg}/{rel}'
	for cfg, rows in data['configurators'].items():
		if not rows or not isinstance(rows, list):
			out.append(f'{cfg}: no rows')
			continue
		head = rows[0]
		for col in ('kind', 'name', 'group_id', 'anchor'):
			if col not in head:
				out.append(f'{cfg}: no "{col}" column')
		if out:
			continue
		ki, gi, ai = head.index('kind'), head.index('group_id'), head.index('anchor')
		ni = head.index('name')
		starts, ends, vis = {}, {}, []
		for r in rows[1:]:
			if len(r) != len(head):
				out.append(f'{cfg}: a row has {len(r)} cells, the header {len(head)}')
				continue
			if r[ki] == 'groupstart':
				starts[r[gi]] = r[ai]
			elif r[ki] == 'groupend':
				ends[r[gi]] = r[ai]
			elif r[ki] == 'group':
				vis.append(r[ni])
		for gid in vis:
			if gid not in starts:
				out.append(f'{cfg}: group {gid} has a visibility row but no brackets')
		for gid in sorted(set(starts) | set(ends)):
			if gid not in starts or gid not in ends:
				out.append(f'{cfg}: group {gid} has only one bracket')
			elif not starts[gid].strip():
				out.append(f'{cfg}: group {gid} has no members')
	return out
