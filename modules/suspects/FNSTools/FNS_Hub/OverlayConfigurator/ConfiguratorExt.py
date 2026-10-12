"""Overlay Configurator -- the FNS_Hub tab that drives FNS_OverlayRegistry.

The network overlay has no bar: tools hand over LAYERS (one TOP each,
composited over the network editor) and WIDGETS (small interactive panels
pinned to a corner). This tab lists both, lets the user reorder them, show or
hide them, and move a widget to another corner or margin
(docs/OverlayManager.md).

Show never switches a tool off. A layer is drawn when the user shows it
(Displayed, the tool's Ovdisplayed) AND its tool is on (the host's Layer
Active); a widget the same way with the tool's own show parameter. A tool
that is off reads "(off)" in Origin and draws nothing whatever Show says.

Every setting is a parameter of the tool it belongs to, written where it
lives: a layer's order and Show through its host's Registration pars (bound
to the tool's Registry page), a widget's show/corner/margin/order through the
parameter names the tool declared at RegisterPanelWidget. The state table
stays empty: nothing is owned here.

ConfiguratorBase expects the RegistryBase widget model; _OverlayApi adapts
the overlay registry to exactly that shape, as _OpMenuApi does for the OP
menu.
"""

ConfiguratorBase = mod('../ConfiguratorBase').ConfiguratorBase

LAYER = 'layer:'
WIDGET = 'widget:'
CORNERS = ('topleft', 'topright', 'bottomleft', 'bottomright')
CORNER_LABELS = {'topleft': 'Top Left', 'topright': 'Top Right',
				 'bottomleft': 'Bottom Left', 'bottomright': 'Bottom Right'}


class _OverlayApi:
	"""FNS_OverlayRegistry seen through the widget model the base reads.
	Keys are 'layer:<canonical>' and 'widget:<canonical>': a tool may have
	one of each under the same name (QuickMarks does)."""

	def __init__(self, reg):
		self._reg = reg
		self.stored = {'PaneRegistry': {}}   # nothing virtual lives here

	# --- reading -------------------------------------------------------------

	def _layers(self):
		try:
			return self._reg.LayerEntries() or {}
		except Exception:
			return {}

	def _widgets(self):
		try:
			return self._reg.WidgetSpecs() or {}
		except Exception:
			return {}

	@property
	def Widgets(self):
		out = {}
		for name, info in self._layers().items():
			host = op(info.get('source_registry', '')) if info.get('source_registry') else None
			out[LAYER + name] = {
				'kind': 'layer', 'canonical': name,
				'display': str(info.get('display', '1')),
				'active': str(info.get('active', '1')),
				'menu_order': info.get('menu_order', 0),
				'source_registry': info.get('source_registry', ''),
				'tool_path': host.parent().path if host is not None else '',
				'panel_path': info.get('panel_path', ''),
			}
		for name, spec in self._widgets().items():
			out[WIDGET + name] = {
				'kind': 'widget', 'canonical': name,
				'display': '1' if spec.get('shown', True) else '0',
				'active': '1' if spec.get('active', True) else '0',
				'anchor': spec.get('anchor', 'topleft'),
				'order': spec.get('order', 100),
				'margin': spec.get('margin', 12),
				'tool_path': spec.get('tool_path', ''),
				'pars': spec.get('pars', {}),
				'panel_path': spec.get('panel_path', ''),
			}
		return out

	@property
	def WidgetSequence(self):
		"""Layers bottom first, then the widgets corner by corner, nearest
		the corner first."""
		widgets = self.Widgets

		def key(name):
			info = widgets[name]
			if info['kind'] == 'layer':
				return (0, 0, _num(info.get('menu_order')), name.lower())
			corner = info.get('anchor', 'topleft')
			ci = CORNERS.index(corner) if corner in CORNERS else len(CORNERS)
			return (1, ci, _num(info.get('order')), name.lower())
		return sorted(widgets, key=key)

	@property
	def Groups(self):
		return {}

	def _registeredNamesInOrder(self):
		return self.WidgetSequence

	def _isGroupMarker(self, info):
		return False

	def _scanGroups(self, names):
		return {}, []

	def GroupPath(self, name):
		return ''

	def GroupVisible(self, gid):
		return True

	# --- writing: always to the tool's own parameter ---------------------------

	def _tool(self, info):
		p = info.get('tool_path')
		return op(p) if p else None

	def _host(self, info):
		p = info.get('source_registry')
		return op(p) if p else None

	def _toolPar(self, info, role):
		tool = self._tool(info)
		name = (info.get('pars') or {}).get(role)
		if tool is None or not name:
			return None
		return tool.par[name]

	def SetWidgetSequence(self, names):
		"""Each kind keeps its own numbers, handed out again in the new
		order: layers swap Layer Order values (the bands stay: 100, 200,
		210), widgets swap List Order values within their corner."""
		widgets = self.Widgets
		layers = [n for n in names if widgets.get(n, {}).get('kind') == 'layer']
		self._renumber(layers, [_num(widgets[n].get('menu_order')) for n in layers],
					   lambda n, v: self._writeLayerOrder(widgets[n], v))
		for corner in CORNERS:
			members = [n for n in names if widgets.get(n, {}).get('kind') == 'widget'
					   and widgets[n].get('anchor') == corner]
			self._renumber(members, [_num(widgets[n].get('order')) for n in members],
						   lambda n, v: self._writeWidget(widgets[n], 'order', int(v)))

	@staticmethod
	def _renumber(names, values, write):
		values = sorted(values)
		last = None
		for name, v in zip(names, values):
			if last is not None and v <= last:
				v = last + 1
			last = v
			write(name, v)

	def _writeLayerOrder(self, info, value):
		host = self._host(info)
		if host is not None and host.par['Menuorder'] is not None:
			if _num(host.par.Menuorder.eval()) != value:
				host.par.Menuorder = int(value)    # bound: lands on the tool's Ovmenuorder

	def _writeWidget(self, info, role, value):
		par = self._toolPar(info, role)
		if par is None:
			debug(f'OverlayConfigurator: {info.get("canonical")} declared no {role} parameter')
			return False
		if par.eval() != value:
			par.val = value
		return True

	def SetWidgetDisplay(self, name, visible):
		info = self.Widgets.get(name)
		if info is None:
			return
		if info['kind'] == 'layer':
			host = self._host(info)
			if host is not None and host.par['Displayed'] is not None:
				host.par.Displayed = bool(visible)    # bound: the tool's Ovdisplayed
		else:
			self._writeWidget(info, 'show', bool(visible))

	def SetWidgetCorner(self, name, corner):
		info = self.Widgets.get(name)
		if info is not None and info['kind'] == 'widget' and corner in CORNERS:
			self._writeWidget(info, 'corner', corner)

	def SetWidgetMargin(self, name, margin):
		info = self.Widgets.get(name)
		if info is not None and info['kind'] == 'widget':
			self._writeWidget(info, 'margin', int(margin))

	def WidgetTarget(self, name):
		info = self.Widgets.get(name) or {}
		p = info.get('panel_path')
		return op(p) if p else None

	def OpenDocs(self, name):
		info = self.Widgets.get(name) or {}
		if info.get('kind') == 'layer' and hasattr(self._reg, 'OpenDocs'):
			return self._reg.OpenDocs(info.get('canonical'))
		return None

	def _syncSurface(self):
		pass


def _num(v):
	try:
		return float(v)
	except (TypeError, ValueError):
		return 0.0


class ConfiguratorExt(ConfiguratorBase):

	CFG_NAME = 'OverlayConfigurator'
	REGISTRY_SHORTCUT = 'FNS_OVERLAYREGISTRY'
	REGISTRY_EXT = 'OverlayRegistryExt'
	REGISTRY_NAME = 'FNS_OverlayRegistry'
	BAR_PATH = ''                      # no bar: the surface is the network editor
	HUB_TAB = 'overlay'
	ORIGIN_PANE = 'ovcfg_origin'
	PKG_LABEL = 'network overlay layer'

	HAS_GROUPS = False
	SUPPORTS_DROP = False
	ADOPTS_BUILTINS = False

	# a tool re-registers a frame or more after its par changes, a host
	# through the registry's deferred sync: look again soon, then once more
	REFRESH_FRAMES = (3, 15)

	def _api(self):
		reg = getattr(op, self.REGISTRY_SHORTCUT, None)
		if reg is not None and hasattr(reg.ext, self.REGISTRY_EXT):
			return _OverlayApi(reg)
		return None

	def _showBuiltins(self):
		return False

	def _adoptCall(self, api, o, stored, disp):
		pass

	# --- rows ------------------------------------------------------------------

	def _label(self, info):
		name = info.get('canonical', '')
		return name if info.get('kind') == 'layer' else f'{name} list'

	def _originOf(self, info):
		tool = info.get('tool_path', '')
		parts = [p for p in tool.split('/') if p]
		origin = parts[-1] if parts else '-'
		return origin if info.get('active', '1') == '1' else f'{origin} (off)'

	def _cells(self, info):
		"""Corner, Show, Margin, Origin for one entry."""
		widget = info.get('kind') == 'widget'
		corner = CORNER_LABELS.get(info.get('anchor'), info.get('anchor', '')) if widget else '-'
		margin = str(int(_num(info.get('margin')))) if widget else '-'
		return [corner, '0' if info.get('display', '1') == '0' else '1', margin, self._originOf(info)]

	def _entryColumns(self):
		return ['Name', 'Corner', 'Show', 'Margin', 'Origin']

	def _treeColumns(self):
		return ['path', 'Name', 'Corner', 'Show', 'Margin', 'Origin']

	def _entryRow(self, api, name, info, groups, label=None, side=None):
		return [label if label is not None else self._label(info)] + self._cells(info)

	def RefreshTree(self):
		"""Flat: layers bottom first, then the widgets corner by corner. The
		tree's path keys carry the position so its sibling sort keeps it."""
		t = self.ownerComp.op('tree_entries')
		api = self._api()
		if t is None:
			return
		t.clear()
		t.appendRow(self._treeColumns())
		if api is None:
			return
		widgets = api.Widgets
		for i, name in enumerate(api.WidgetSequence):
			info = widgets[name]
			t.appendRow([self._treeSeg(name, i), self._label(info)] + self._cells(info))

	def _refreshSoon(self):
		self.Refresh()
		for frames in self.REFRESH_FRAMES:
			run('args[0].valid and args[0].Refresh()', self.ownerComp,
				delayFrames=frames, delayRef=op.TDResources)

	# --- edits -------------------------------------------------------------------

	def PushSequence(self, names):
		api = self._api()
		if api is not None:
			api.SetWidgetSequence([n for n in names if n])
		self._refreshSoon()

	def ToggleShow(self, name):
		api = self._api()
		info = api.Widgets.get(name) if api is not None else None
		if info is None:
			return
		api.SetWidgetDisplay(name, info.get('display', '1') == '0')
		self._refreshSoon()

	def CycleCorner(self, name):
		"""Move a widget to the next corner, clockwise from top left."""
		api = self._api()
		info = api.Widgets.get(name) if api is not None else None
		if info is None or info.get('kind') != 'widget':
			return
		ring = ('topleft', 'topright', 'bottomright', 'bottomleft')
		# the tool's parameter, not the registry's copy: that one lags a
		# frame or more behind a click
		par = api._toolPar(info, 'corner')
		cur = str(par.eval()) if par is not None else info.get('anchor', 'topleft')
		nxt = ring[(ring.index(cur) + 1) % len(ring)] if cur in ring else 'topleft'
		api.SetWidgetCorner(name, nxt)
		self._refreshSoon()

	def PromptMargin(self, name):
		api = self._api()
		info = api.Widgets.get(name) if api is not None else None
		if info is None or info.get('kind') != 'widget':
			return
		op.TDResources.PopDialog.OpenDefault(
			text=f'Margin for {self._label(info)}, in screen points',
			title='Widget Margin',
			buttons=['Set', 'Cancel'],
			callback=self._onMarginDialog,
			details={'name': name},
			textEntry=str(int(_num(info.get('margin')))),
			escButton=2, enterButton=1)

	def _onMarginDialog(self, info):
		if info.get('buttonNum') != 1:
			return
		name = (info.get('details') or {}).get('name')
		txt = str(info.get('enteredText', '') or '').strip()
		api = self._api()
		if not name or api is None:
			return
		try:
			value = max(0, min(int(float(txt)), 400))
		except (TypeError, ValueError):
			self._log(f'invalid margin {txt!r}')
			return
		api.SetWidgetMargin(name, value)
		self._refreshSoon()

	def NameRightClick(self, name):
		self.OpenOrigin(name)

	def OpenOrigin(self, name):
		"""Floating network editor on the tool that owns an entry."""
		api = self._api()
		info = api.Widgets.get(name) if api is not None else None
		tool = op(info.get('tool_path')) if info and info.get('tool_path') else None
		if tool is None:
			return
		pane = next((p for p in ui.panes if p.name == self.ORIGIN_PANE), None)
		if pane is None:
			pane = ui.panes.createFloating(type=PaneType.NETWORKEDITOR, name=self.ORIGIN_PANE)
		pane.owner = tool.parent()
		tool.current = True
