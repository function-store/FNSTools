
CustomParHelper: CustomParHelper = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('CustomParHelper').CustomParHelper # import
###

RegistryBase = mod('RegistryBase').RegistryBase


class OverlayRegistryExt(RegistryBase):
	"""FNS_OverlayRegistry: one overlay over the network editor you work in,
	composited from every registered tool's layer TOP
	(docs/NetworkOverlayRegistry.md).

	The global owns the view (published on its View page), one Composite TOP
	of the shown layers, and ONE utility annotation in the viewed network that
	shows the composite through its OP viewer, above the nodes. Nothing of the
	user's network is touched: no display flag, no annotation, no child the
	user or op() can see. Idle (no shown layer) there is no annotation and no
	per-frame work. The method is TDCollab's partner overlay
	(CollabPaneSyncHandler._drawOverlay, RemoteTD), generalised.
	"""
	SHORTCUT = 'FNS_OVERLAYREGISTRY'
	EXT_NAME = 'OverlayRegistryExt'
	REGISTRY_NAME = 'FNS_OverlayRegistry'

	# Standardized 'Registry' page on the parent tool (see RegistryBase).
	TOOL_PAGE_PREFIX = 'Ov'
	TOOL_PAGE_LABEL = 'Network Overlay'
	TOOL_PAGE_PARS = ('Autoregister', 'Register', 'Regstatus', 'Menuorder', 'Displayed')

	CLONE_EXPR = "op.FNS.op('FNS_OverlayRegistry') if hasattr(op, 'FNS') else None"

	OVERLAY_TAG = 'fns_network_overlay'	# the annotation showing the composite
	WIDGET_TAG = 'fns_network_overlay_widget'	# one per interactive panel widget
	WIDGET_ANCHORS = ('topleft', 'topright', 'bottomleft', 'bottomright')
	WIDGET_ORDER = 100		# a widget's default place in its corner's stack
	WIDGET_MARGIN = 12		# a widget's default margin, in screen points
	RETIRED_PAGE = 'Widgets'	# the package's margin/gap page, 2026-10-11 only
	RETIRED_PARS = ('Widgetmargin', 'Widgetgap')
	ORDER_LABEL = 'Layer Order'
	LAYER_PREFIX = 'layer_'
	MARGIN = 0.15			# how far past the view the overlay reaches on each side
	MAX_PIXELS = 4096		# the render's longest side, at most
	HEAL_EVERY = 15			# frames between checks of the annotation's warning

	VIEW_PAGE = 'View'
	VIEW_PARS = (
		# name, style, label, help
		('Viewx0', 'Float', 'View Left', 'Left edge of the overlay, in network units.'),
		('Viewy0', 'Float', 'View Bottom', 'Bottom edge of the overlay, in network units.'),
		('Viewx1', 'Float', 'View Right', 'Right edge of the overlay, in network units.'),
		('Viewy1', 'Float', 'View Top', 'Top edge of the overlay, in network units.'),
		('Resolutionw', 'Int', 'Resolution W', 'Width every layer renders at, in pixels.'),
		('Resolutionh', 'Int', 'Resolution H', 'Height every layer renders at, in pixels.'),
		('Unitsperpixel', 'Float', 'Units per Pixel', 'Network units per overlay pixel.'),
		('Pixelsperpoint', 'Float', 'Pixels per Point', 'Overlay pixels per screen point (the monitor DPI scale, capped).'),
		('Zoom', 'Float', 'Zoom', "The network editor's zoom: screen points per network unit."),
		('Network', 'Str', 'Network', 'Path of the network the overlay is drawn over, empty when there is none.'),
	)

	# --- stamping: a host is not the package ---

	def StampHost(self, target_comp, canonical_name=None, autoregister=True,
				  promote_pars=True, par_values=None):
		"""RegistryBase.StampHost, then shaped like every other registry host."""
		host = super().StampHost(target_comp, canonical_name=canonical_name,
								 autoregister=autoregister, promote_pars=promote_pars,
								 par_values=par_values)
		if host is not None:
			self._shapeHost(host)
		return host

	def _shapeHost(self, host):
		"""Drop what came along from the master that a host must not carry:
		its FNS_About, its annotation, its View page and the overlay
		operators (FNS_PaneSearchRegistry, same rule)."""
		for p in host.customPars:
			if p.page.name == 'About' and p.mode != ParMode.CONSTANT:
				p.val = p.eval()
		fa = host.op('FNS_About')
		if fa is not None:
			fa.destroy()
		for ann in host.findChildren(type=annotateCOMP, includeUtility=True, maxDepth=1):
			ann.destroy()
		for name in ('constant_clear', 'comp_layers', 'null_overlay', 'execute_frame', 'execute_save'):
			o = host.op(name)
			if o is not None:
				o.destroy()
		for o in host.ops(self.LAYER_PREFIX + '*'):
			o.destroy()
		for p in [p for p in host.customPars if p.page.name == self.VIEW_PAGE]:
			p.destroy()
		for pg in list(host.customPages):
			if pg.name == self.VIEW_PAGE and not pg.pars:
				pg.destroy()

	# --- lifecycle ---

	def postInit(self):
		super().postInit()
		if self.ownerComp == self._masterComp():
			self._ensureMasterNotCloning()
		if not self._is_sys_global():
			self._ensureLayerActive()
		if self.ownerComp == self._masterComp() or self._is_sys_global():
			self._retireWidgetLayoutPage()
		if self._is_sys_global():
			self._ensureViewPars()
			self._ensureOverlayOps()
			self._sweepStrayOverlays()
			self._syncSurface()

	def onDestroyTD(self):
		# a reinit or a removal: the annotation lives in the user's network,
		# and a new instance cannot know it (it sweeps by tag on init anyway)
		try:
			self._removeOverlay()
			self._removeWidgets()
		except Exception:
			pass
		super().onDestroyTD()

	def _preInit(self):
		self._overlay = None		# the annotation showing the composite
		self._frame = None			# (rect, resolution, scale, zoom, pane pixels) as last placed
		self._paneId = None			# the network editor followed
		self._ticks = 0
		self._widgetAnns = {}		# canonical -> the annotation showing that widget
		self._widgetZoom = None		# the zoom seen last frame, and the frames it has held
		self._zoomHeld = 0

	# --- surface hooks (RegistryBase contract) ---

	def _ensureSelectionExecuteRole(self):
		# no selection DAT; hosts must not keep a parallel table
		if not self._is_sys_global():
			self.stored['PaneRegistry'].clear()

	def _syncSurface(self, attempts=40):
		"""Idempotent: one Select TOP per shown layer, wired into the
		composite top layer first, and the frame driver on only while there
		is something to show."""
		self._pane_sync_queued = False
		if not self._is_sys_global():
			return
		comp = self.ownerComp.op('comp_layers')
		clear = self.ownerComp.op('constant_clear')
		if comp is None or clear is None:
			return
		self._pruneDeadLayers(sync=False)
		shown = self._shownLayers()
		keep = set()
		selects = []
		for i, (canonical, layer) in enumerate(reversed(shown)):	# highest order on top
			name = self.LAYER_PREFIX + tdu.legalName(canonical)
			keep.add(name)
			sel = self.ownerComp.op(name)
			if sel is None:
				sel = self.ownerComp.create(selectTOP, name)
			if sel.par.top.eval() != layer:
				sel.par.top = layer.path
			sel.nodeX = comp.nodeX - 400
			sel.nodeY = comp.nodeY + 200 * (len(shown) - i)
			selects.append(sel)
		for o in self.ownerComp.ops(self.LAYER_PREFIX + '*'):
			if o.name not in keep:
				o.destroy()
		# A Composite TOP needs two sources ("Not enough sources specified"
		# with one, measured): the clear layer fills the second slot at rest.
		wanted = selects + [clear]
		if len(wanted) < 2:
			wanted.append(clear)
		# compare slot by slot: comp.inputs skips an empty slot, which hid a
		# gap left by a destroyed Select TOP
		current = []
		for conn in comp.inputConnectors:
			current.append(conn.connections[0].owner if conn.connections else None)
		while current and current[-1] is None:
			current.pop()
		if current != wanted:
			for conn in comp.inputConnectors:
				conn.disconnect()
			for i, src in enumerate(wanted):
				comp.inputConnectors[i].connect(src)
		widgets = self._shownWidgets()
		running = bool(selects) or bool(widgets)
		frame = self.ownerComp.op('execute_frame')
		if frame is not None and bool(frame.par.active.eval()) != running:
			frame.par.active = running
		if not selects:
			self._removeOverlay()
		if not widgets:
			self._removeWidgets()

	def _healRegistryEntries(self):
		super()._healRegistryEntries()
		if self._is_sys_global():
			self._syncSurface()

	# --- the view and the annotation (global only) ---

	def onFrame(self):
		"""Every frame while a layer is shown (execute_frame): fit the
		annotation over our view of the network we look at, publish the view
		when it changed, and move the annotation when the network changed."""
		if not self._is_sys_global():
			return
		# Nothing to show (a layer switched off or deleted while this DAT was
		# still active, a reinit landing mid-frame): the sync tears down and
		# switches this driver off. Never draw an overlay with no layer.
		layers = self._shownLayers()
		widgets = self._shownWidgets()
		if not layers and not widgets:
			self._syncSurface()
			return
		pane = self._overlayPane()
		if pane is not None and not self._drawableNetwork(pane.owner):
			pane = None
		if layers:
			self._drawLayers(pane)
		else:
			self._removeOverlay()
		self._placeWidgets(pane, widgets)
		self._ticks += 1
		if self._ticks % self.HEAL_EVERY == 0:
			self._healOverlay()
			self._pruneDeadLayers()

	def _drawLayers(self, pane):
		"""Fit the overlay annotation over the view and publish the view."""
		if pane is None:
			self._removeOverlay()
			self._publishView(None)
			return
		bl, tr = pane.bottomLeft, pane.topRight
		zoom = pane.zoom or 1.0
		width = max(1.0, (tr.x - bl.x) * (1 + 2 * self.MARGIN))
		height = max(1.0, (tr.y - bl.y) * (1 + 2 * self.MARGIN))
		dpi = monitors.primary.dpiScale or 1.0
		scale = min(dpi, self._maxPixels() / max(width, height))
		overlay = self._overlay
		if overlay is not None and (not overlay.valid or overlay.parent() != pane.owner):
			self._removeOverlay()
			overlay = None
		if overlay is None:
			overlay = self._createOverlay(pane.owner)
			if overlay is None:
				return
		px = (tr.x - bl.x, tr.y - bl.y)
		prev = self._frame
		if prev is not None and self._viewStillCovered(prev, pane, zoom, px):
			return
		rect = (round(pane.x - width / zoom / 2), round(pane.y - height / zoom / 2),
				max(1, round(width / zoom)), max(1, round(height / zoom)))
		resolution = (max(1, round(width * scale)), max(1, round(height * scale)))
		if prev is None or (rect, resolution, scale) != prev[:3]:
			self._frame = (rect, resolution, scale, zoom, px)
			resized = prev is None or prev[0][2:] != rect[2:] or prev[1:3] != (resolution, scale)
			overlay.nodeX, overlay.nodeY, overlay.nodeWidth, overlay.nodeHeight = rect
			x0, y0, w, h = overlay.nodeX, overlay.nodeY, overlay.nodeWidth, overlay.nodeHeight  # as TD keeps them
			self._publishView((x0, y0, x0 + w, y0 + h, resolution[0], resolution[1],
							   w / resolution[0], scale, zoom, pane.owner.path))
			# The annotation's panels size its viewer from its width and height
			# by expression; cooked here so a resize never leaves them stale
			# (TDCollab, user report: marks sat off their operators). Only on
			# a resize: a pan keeps the size, and the forced cook pulls the
			# composite and every layer inside this callback.
			if resized:
				for path in ('annotation/opview', 'annotation/opview/opviewer', 'annotation/opview/select_opviewer'):
					panel = overlay.op(path)
					if panel is not None:
						panel.cook(force=True)

	# How far the zoom may drift from the one the overlay was placed at
	# before it is placed again: within it the layers render at most 15%
	# coarser or finer than the screen.
	REPLACE_ZOOM = 1.15

	def _viewStillCovered(self, frame, pane, zoom, px):
		"""True while the overlay as placed still serves this view: the
		visible network sits inside the annotation (it reaches MARGIN past
		the view on every side), the zoom is within REPLACE_ZOOM of the one
		it was placed at, and the pane is the same size. Placing it moves
		and re-renders every layer, ~7 ms a frame inside this callback when
		done on every frame of a pan or a zoom (measured 2026-10-12), and
		the layers draw in network units, so a placement that still covers
		the view needs no change."""
		rect, _res, _scale, zoom0, px0 = frame
		if px0 != px or not zoom0:
			return False
		ratio = zoom / zoom0
		if ratio > self.REPLACE_ZOOM or ratio < 1.0 / self.REPLACE_ZOOM:
			return False
		hw, hh = px[0] / zoom / 2.0, px[1] / zoom / 2.0
		x0, y0, w, h = rect
		return (pane.x - hw >= x0 and pane.x + hw <= x0 + w
				and pane.y - hh >= y0 and pane.y + hh <= y0 + h)

	def _shownLayers(self):
		"""(canonical, layer TOP) for every layer in the overlay, bottom
		first: registered, displayed by the user, active by its tool, and its
		TOP still there (docs/OverlayManager.md, two flags per layer)."""
		shown = []
		for canonical in self._registeredNamesInOrder():
			info = self.stored['PaneRegistry'][canonical]
			if str(info.get('display', '1')) != '1' or str(info.get('active', '1')) != '1':
				continue
			layer = self._resolvePanelOp(info)
			if layer is not None and layer.family == 'TOP':
				shown.append((canonical, layer))
		return shown

	def _pruneDeadLayers(self, sync=True):
		"""A tool deleted while its layer is shown never says so: TD calls no
		onDestroyTD for a host dying inside its parent's subtree. Its entry
		would keep the overlay up and the frame driver running, so every sync
		and the heal tick drop entries whose layer no longer exists."""
		entries = self.stored['PaneRegistry']
		dead = [n for n, info in entries.items() if self._resolvePanelOp(info) is None]
		for name in dead:
			entries.pop(name, None)
			self.fnsLog(f'{self.REGISTRY_NAME}: dropped layer "{name}" (its TOP is gone)')
		if dead and sync:
			self._syncSurface()

	def _drawableNetwork(self, network):
		"""False for a clone master. A child added to a COMP that others
		clone replicates into every clone: drawn in the FNS_OverlayRegistry
		master's network, the overlay annotation appeared in each stamped
		host too, its path broken (2026-10-11). RegistryBase's
		_isClonedByOthers walks the project, so the answer is kept per
		network for the life of this instance; clone wiring rarely changes."""
		cache = self.__dict__.setdefault('_cloneMasters', {})
		key = int(network.id)
		if key not in cache:
			cache[key] = not self._isClonedByOthers(network)
		return cache[key]

	NON_COMMERCIAL_MAX = 1280	# the Non-Commercial licence's TOP resolution limit

	def _maxPixels(self):
		"""The render's longest side: MAX_PIXELS, or the Non-Commercial
		licence's TOP limit (CookBar halved its image there for the same
		reason)."""
		try:
			if licences.type == 'Non-Commercial':
				return min(self.MAX_PIXELS, self.NON_COMMERCIAL_MAX)
		except Exception:
			pass
		return self.MAX_PIXELS

	def _overlayPane(self):
		"""The network editor you work in: the current pane, else the one
		followed last while another pane type is current, else none."""
		def usable(p):
			return p is not None and p.type == PaneType.NETWORKEDITOR and getattr(p, 'open', True) \
				and p.owner is not None
		cur = ui.panes.current
		if usable(cur):
			self._paneId = cur.id
			return cur
		for p in ui.panes:
			if usable(p) and p.id == self._paneId:
				return p
		return None

	def _publishView(self, view):
		"""Write the View page, only what changed: layers bound to it recook
		when the view moves and never otherwise."""
		names = ('Viewx0', 'Viewy0', 'Viewx1', 'Viewy1', 'Resolutionw', 'Resolutionh',
				 'Unitsperpixel', 'Pixelsperpoint', 'Zoom', 'Network')
		if view is None:
			view = (0.0, 0.0, 1.0, 1.0, 8, 8, 1.0, 1.0, 1.0, '')
		for name, value in zip(names, view):
			p = self.ownerComp.par[name]
			if p is not None and p.eval() != value:
				p.val = value

	def _createOverlay(self, network):
		"""A utility annotation in `network` showing the composite, above the
		nodes (a displayed TOP's backdrop would hide it below them).
		Creating an operator makes it the network's current one, so the
		user's current and selected operators are put back (TDCollab)."""
		image = self.ownerComp.op('null_overlay')
		if image is None or network is None or not network.isCOMP:
			return None
		was_current = network.currentChild
		was_selected = list(network.selectedChildren)
		try:
			mark = network.create(annotateCOMP)
		except Exception as e:
			debug(f'{self.REGISTRY_NAME}: no overlay in {network.path}: {e}')
			return None
		mark.current = False
		mark.selected = False
		if was_current is not None and was_current.valid:
			was_current.current = True
		for node in was_selected:
			if node.valid and not node.selected:
				node.selected = True
		mark.par.utility = True		# hidden from op(), .children and observers
		mark.tags.add(self.OVERLAY_TAG)
		# Its internals first cook under a provisional name and keep that
		# Component warning until cooked again (TDCollab, measured).
		back = mark.op('annotation/back')
		if back is not None:
			for frames in (1, 10):
				run("args[0].valid and args[0].cook(force=True)", back,
					delayFrames=frames, delayRef=op.TDResources)
		mark.par.enable = False		# cannot be clicked or dragged
		mark.par.layerzone = 'abovenodes'
		mark.par.Mode = 'annotate'
		mark.par.Titletext = ''
		mark.par.Titleheight = 0
		mark.par.Bodytext = ''
		mark.par.Backcoloralpha = 0
		mark.par.Opviewer = mark.relativePath(image)
		mark.par.Opviewerdisplay = True
		mark.par.Opvieweroversize = 'autofit'
		mark.par.Opviewerfillbodytitle = True
		mark.par.Opviewerfillalpha = 0
		self._overlay = mark
		self._frame = None
		self.ownerComp.store('overlay_path', mark.path)
		return mark

	def _healOverlay(self):
		for mark in [self._overlay] + list(self._widgetAnns.values()):
			back = mark.op('annotation/back') if mark is not None and mark.valid else None
			if back is not None and back.warnings():
				back.cook(force=True)

	def _removeOverlay(self):
		if self._overlay is not None and self._overlay.valid:
			self._overlay.destroy()
		self._overlay = None
		self._frame = None

	def _sweepStrayOverlays(self):
		"""Remove an overlay this registry lost track of (an extension reinit,
		a crash autosave): the one it made last, by path, and any tagged one
		in the network that path names."""
		path = self.ownerComp.fetch('overlay_path', '', search=False)
		network = op(path.rsplit('/', 1)[0] or '/') if path else None
		if network is not None:
			for stray in network.findChildren(tags=[self.OVERLAY_TAG], includeUtility=True, maxDepth=1):
				if stray != self._overlay:
					stray.destroy()
		# A tool saved (Private Investigator, a tox export) while the overlay
		# sat in its network carries the annotation in its tox, and a stamped
		# host copies whatever the master's network holds: once per boot, the
		# whole toolkit is swept too (pre_release_common strips artifacts).
		root = getattr(op, 'FNS', None)
		if root is not None:
			for stray in root.findChildren(tags=[self.OVERLAY_TAG], includeUtility=True):
				if stray != self._overlay:
					stray.destroy()
		# widgets: the instance that made them is gone; the next frame makes
		# fresh ones wherever you look
		live = set(self._widgetAnns.values())
		for top in ([network] if network is not None else []) + ([root] if root is not None else []):
			for stray in top.findChildren(tags=[self.WIDGET_TAG], includeUtility=True):
				if stray not in live:
					stray.destroy()

	def onProjectPreSave(self):
		"""execute_save: the annotation lives in the user's network, so it
		leaves before TD writes the .toe; the next frame draws it again."""
		if self._is_sys_global():
			self._removeOverlay()
			self._removeWidgets()

	# --- interactive panel widgets (global only) ---
	#
	# A panel cannot go through the composite: it is one TOP, and an OP viewer
	# passes clicks only to the operator it shows. So each widget is its OWN
	# small utility annotation showing the tool's panel COMP, interactive
	# (Opviewerinteractive, enable on), pinned to a corner of the view at a
	# constant on-screen size (docs/NetworkOverlayRegistry.md, "Widgets").
	# Registrations live in storage (strings, they outlive a reinit); the
	# annotations are kept as OPs: op() never finds a utility operator, and a
	# path lookup made a new one every frame in the spike.

	def _widgetSpecs(self):
		return dict(self.ownerComp.fetch('widgets', {}, search=False) or {})

	def _liveWidgets(self):
		"""(canonical, panel COMP, spec) for every registered widget whose
		panel still exists; the rest are dropped."""
		specs = self._widgetSpecs()
		live, dead = [], []
		for canonical, spec in sorted(specs.items()):
			panel = self._resolveByIdOrPath(spec.get('panel_id'), spec.get('panel_path'))
			if panel is None or not panel.isPanel:
				dead.append(canonical)
			else:
				live.append((canonical, panel, spec))
		if dead:
			for canonical in dead:
				specs.pop(canonical, None)
				self.fnsLog(f'{self.REGISTRY_NAME}: dropped widget "{canonical}" (its panel is gone)')
			self.ownerComp.store('widgets', specs)
		return live

	def _shownWidgets(self):
		"""The live widgets the user shows and whose tool is on. A widget is
		registered for as long as its tool exists, so the overlay manager can
		list a hidden one (docs/OverlayManager.md)."""
		return [w for w in self._liveWidgets()
				if str(w[2].get('shown', '1')) == '1' and str(w[2].get('active', '1')) == '1']

	# A widget spec stays flat, strings and numbers only: storing one that
	# carried a nested dict and bools crashed TD natively inside store()
	# (2026-10-12, py-spy: RegisterPanelWidget -> store). So the tool's
	# parameter names travel as 'show=Toplist corner=Topcorner ...'.

	@staticmethod
	def _encodeWidgetPars(pars):
		return ' '.join('%s=%s' % (k, v) for k, v in sorted((pars or {}).items())
						if v and ' ' not in str(v) and '=' not in str(k))

	@staticmethod
	def _decodeWidgetPars(text):
		out = {}
		for item in str(text or '').split():
			k, _sep, v = item.partition('=')
			if k and v:
				out[k] = v
		return out

	# Frames the zoom must hold before a widget is placed again. Moving a
	# widget annotation while the zoom changes made TD redraw its viewer
	# inside the frame callback: ~7.5 ms a frame of a zoom, ~2-4 ms of real
	# frame time (a pan, same zoom: ~0.5 ms; measured 2026-10-12). So a
	# widget follows a pan live and snaps back to its corner once a zoom
	# settles.
	WIDGET_SETTLE = 3

	def _placeWidgets(self, pane, widgets):
		"""One annotation per widget in the viewed network, pinned to its
		corner. Each widget sits its own margin (the tool's setting) from the
		editor's edges, and its own margin away from the widget before it in
		the same corner, lowest order nearest the corner. Compared with the
		LIVE geometry every frame, so a user's resize or drag of the
		annotation is undone at once; held while a zoom moves
		(WIDGET_SETTLE)."""
		names = {c for c, _p, _s in widgets}
		for canonical in [c for c in self._widgetAnns if c not in names]:
			self._removeWidget(canonical)
		if pane is None:
			self._removeWidgets()
			return
		net = pane.owner
		zoom = pane.zoom or 1.0
		if zoom != self._widgetZoom:
			self._widgetZoom = zoom
			self._zoomHeld = 0
		else:
			self._zoomHeld += 1
		settling = self._zoomHeld < self.WIDGET_SETTLE
		bl, tr = pane.bottomLeft, pane.topRight
		half_w = (tr.x - bl.x) / 2 / zoom
		half_h = (tr.y - bl.y) / 2 / zoom
		stacked = {}		# anchor -> points already taken along the stack
		widgets = sorted(widgets, key=lambda w: (float(w[2].get('order', self.WIDGET_ORDER)), w[0]))
		for canonical, panel, spec in widgets:
			ann = self._widgetAnns.get(canonical)
			if ann is not None and (not ann.valid or ann.parent() != net):
				self._removeWidget(canonical)
				ann = None
			fresh = ann is None
			if fresh:
				ann = self._createWidget(net, panel, canonical)
				if ann is None:
					continue
			w = max(1.0, float(panel.width)) / zoom
			h = max(1.0, float(panel.height)) / zoom
			anchor = spec.get('anchor', 'topleft')
			margin = max(0.0, float(spec.get('margin', self.WIDGET_MARGIN)))
			along = stacked.get(anchor, 0.0)
			stacked[anchor] = along + margin + max(1.0, float(panel.height))
			ox = margin / zoom
			oy = (along + margin) / zoom
			x = pane.x - half_w + ox if 'left' in anchor else pane.x + half_w - ox - w
			y = pane.y + half_h - oy - h if 'top' in anchor else pane.y - half_h + oy
			rect = (round(x), round(y), max(1, round(w)), max(1, round(h)))
			cur = (ann.nodeX, ann.nodeY, ann.nodeWidth, ann.nodeHeight)
			if cur != rect and (fresh or not settling):
				ann.nodeX, ann.nodeY, ann.nodeWidth, ann.nodeHeight = rect
				# The viewer panels size from the annotation's width and
				# height: cooked again only when those change. A pan moves
				# the widget every frame at the same size, and cooking its
				# three panels each frame cost ~7.5 ms of a 16.7 ms frame
				# (measured 2026-10-12).
				if cur[2:] != rect[2:]:
					for path in ('annotation/opview', 'annotation/opview/opviewer', 'annotation/opview/select_opviewer'):
						p = ann.op(path)
						if p is not None:
							p.cook(force=True)

	def _createWidget(self, network, panel, canonical):
		"""An interactive utility annotation showing `panel`, the user's
		current and selected operators put back (creating an op makes it
		current)."""
		if network is None or not network.isCOMP:
			return None
		was_current = network.currentChild
		was_selected = list(network.selectedChildren)
		try:
			ann = network.create(annotateCOMP)
		except Exception as e:
			debug(f'{self.REGISTRY_NAME}: no widget in {network.path}: {e}')
			return None
		ann.current = False
		ann.selected = False
		if was_current is not None and was_current.valid:
			was_current.current = True
		for node in was_selected:
			if node.valid and not node.selected:
				node.selected = True
		ann.par.utility = True
		ann.tags.add(self.WIDGET_TAG)
		back = ann.op('annotation/back')
		if back is not None:
			for frames in (1, 10):
				run("args[0].valid and args[0].cook(force=True)", back,
					delayFrames=frames, delayRef=op.TDResources)
		ann.par.layerzone = 'abovenodes'
		ann.par.Mode = 'annotate'
		ann.par.Titletext = ''
		ann.par.Titleheight = 0
		ann.par.Bodytext = ''
		ann.par.Backcoloralpha = 0
		ann.par.Opviewer = ann.relativePath(panel)
		ann.par.Opviewerdisplay = True
		ann.par.Opviewerinteractive = True
		ann.par.Opvieweroversize = 'autofit'
		ann.par.Opviewerfillbodytitle = True
		ann.par.Opviewerfillalpha = 0
		ann.par.enable = True		# a widget takes clicks: keep it small
		self._widgetAnns[canonical] = ann
		return ann

	def _removeWidget(self, canonical):
		ann = self._widgetAnns.pop(canonical, None)
		if ann is not None and ann.valid:
			ann.destroy()

	def _removeWidgets(self):
		for canonical in list(self._widgetAnns):
			self._removeWidget(canonical)

	def RegisterPanelWidget(self, panel, canonical, anchor='topleft', order=None, margin=None,
							shown=True, active=True, tool=None, pars=None):
		"""Show `panel` (a panel COMP) as an interactive widget pinned to a
		corner of the network editor you work in, at its own size on screen.
		anchor: topleft, topright, bottomleft or bottomright. order: its place
		in that corner's stack, lowest nearest the corner (default 100, the
		layer bands' numbers). margin: screen points from the editor's edges
		and from the widget before it in the stack (default 12); offer it as
		a parameter of the tool. Register again to change any of them.

		Register for as long as the tool exists and say whether it shows:
		shown is the user's switch, active the tool's own on/off, and only a
		widget with both is placed. tool (the tool COMP) and pars ({'show',
		'corner', 'margin', 'order'} -> that tool's parameter names) let the
		overlay manager in FNS_Hub write those settings where they live."""
		api = self._registryApi()
		if api is not None and api is not self:
			return api.RegisterPanelWidget(panel, canonical, anchor=anchor, order=order, margin=margin,
										   shown=shown, active=active, tool=tool, pars=pars)
		if not self._is_sys_global():
			return False
		if panel is None or not getattr(panel, 'isPanel', False):
			debug(f'{self.REGISTRY_NAME}: RegisterPanelWidget({canonical!r}): not a panel COMP')
			return False
		anchor = anchor if anchor in self.WIDGET_ANCHORS else 'topleft'
		specs = self._widgetSpecs()
		spec = {'panel_path': panel.path, 'panel_id': int(panel.id), 'anchor': anchor,
				'order': float(self.WIDGET_ORDER if order is None else order),
				'margin': max(0.0, float(self.WIDGET_MARGIN if margin is None else margin)),
				'shown': '1' if shown else '0', 'active': '1' if active else '0',
				'tool_path': tool.path if tool is not None else '',
				'pars': self._encodeWidgetPars(pars)}
		if specs.get(canonical) != spec:
			specs[canonical] = spec
			self.ownerComp.store('widgets', specs)
			self.fnsLog(f'{self.REGISTRY_NAME}: widget "{canonical}" ({panel.path}, {anchor})')
		self._syncSurface()
		return True

	def UnregisterPanelWidget(self, canonical):
		"""Take a widget off the network editor."""
		api = self._registryApi()
		if api is not None and api is not self:
			return api.UnregisterPanelWidget(canonical)
		if not self._is_sys_global():
			return False
		specs = self._widgetSpecs()
		if specs.pop(canonical, None) is not None:
			self.ownerComp.store('widgets', specs)
		self._removeWidget(canonical)
		self._syncSurface()
		return True

	def PanelWidgets(self):
		"""The registered widget names."""
		api = self._registryApi() or self
		return sorted(api._widgetSpecs())

	def WidgetSpecs(self):
		"""Every registered widget as {canonical: spec}: panel_path, anchor,
		order, margin, shown, active, tool_path and pars (the overlay
		manager's view; a copy, editing it changes nothing)."""
		api = self._registryApi() or self
		out = {}
		for k, v in api._widgetSpecs().items():
			spec = dict(v)
			spec['pars'] = self._decodeWidgetPars(spec.get('pars', ''))
			spec['shown'] = str(spec.get('shown', '1')) == '1'
			spec['active'] = str(spec.get('active', '1')) == '1'
			out[k] = spec
		return out

	def LayerEntries(self):
		"""Every registered layer as {canonical: entry}, bottom first:
		panel_path, display (the user's), active (the tool's), menu_order,
		source_registry (its host). A copy."""
		api = self._registryApi() or self
		entries = api.stored['PaneRegistry']
		return {n: dict(entries[n]) for n in api._registeredNamesInOrder()}

	# --- the registry's own operators (global only) ---

	# `me.parent()`, not `parent()`: the same operator, and PI's local
	# Release (prerelease_all) keeps an expression on the released COMP only
	# when it reads `me.` or `op('.`; `parent()` shipped flattened.
	LAYER_ACTIVE_EXPR = "bool(me.parent().par.Active) if hasattr(me.parent().par, 'Active') else True"
	_OLD_LAYER_ACTIVE_EXPR = "bool(parent().par.Active) if hasattr(parent().par, 'Active') else True"

	def _ensureLayerActive(self):
		"""Layer Active, the tool's half of a layer's visibility
		(docs/OverlayManager.md): an expression on the tool's own switch,
		kept on the host and never promoted, so the user's Displayed stays a
		constant the overlay manager can write. Until 2026-10-12 the tool's
		switch lived in Ovdisplayed itself (`me.par.Active`); such an
		expression moves here and Ovdisplayed becomes True. Writes only what
		is missing or still in the old shape."""
		c = self.ownerComp
		par = c.par['Layeractive']
		if par is None:
			page = next((pg for pg in c.customPages if pg.name == 'Registration'), None)
			if page is None:
				return
			par = page.appendToggle('Layeractive', label='Layer Active')[0]
			par.help = ("The tool's own half of whether its layer is drawn: an expression on "
						"the tool's on/off switch (Active unless the tool says otherwise). The "
						'layer shows only when this AND Displayed are on; Displayed is yours.')
			par.defaultExpr = self.LAYER_ACTIVE_EXPR
			par.defaultMode = ParMode.EXPRESSION
			disp = c.par['Displayed']
			if disp is not None:
				par.order = disp.order + 0.5
			par.expr = self.LAYER_ACTIVE_EXPR
		# a constant here is a flattened expression (a release hook before
		# 2026-10-12 did it), never a choice: the default already reads True
		# for a tool with no Active. A tool with its own expression
		# (QuickMarks) re-asserts it from its init.
		if par.mode != ParMode.EXPRESSION or par.expr == self._OLD_LAYER_ACTIVE_EXPR:
			par.expr = self.LAYER_ACTIVE_EXPR
			par.mode = ParMode.EXPRESSION
		disp = c.par['Displayed']
		if disp is None or self.ownerComp == self._masterComp():
			return
		# the old shape: the tool's switch as an expression on Ovdisplayed
		# (promoted: Displayed is bound to it) or on Displayed itself
		source = disp
		if disp.mode == ParMode.BIND:
			source = None
			try:
				m = disp.bindMaster
				source = m if isinstance(m, Par) else None
			except Exception:
				source = None
		if source is None:
			return
		if source.mode != ParMode.EXPRESSION:
			# moved already: drop the dormant text too, or one click on the
			# expression toggle (or a roamed settings file) brings it back
			if source.mode == ParMode.CONSTANT and source.expr:
				source.expr = ''
			return
		expr = source.expr or ''
		if source.owner is not c:
			expr = expr.replace('me.par.', 'me.parent().par.')
		par.expr = expr
		par.mode = ParMode.EXPRESSION
		source.val = True
		source.expr = ''
		self.fnsLog(f'{self.REGISTRY_NAME}: {c.path} Layer Active now follows {expr!r}; '
					f'{source.owner.name}.{source.name} is yours (True)')

	def _ensureMasterNotCloning(self):
		"""The master is cloned FROM; it clones nothing. With Enable Cloning
		on and an empty Clone par, any custom-par write on it crashed TD
		natively a few seconds later or at the next save (seven crashes,
		bisected 2026-10-11; the Toolbar, Timeline and Config masters have
		it off). Written only when wrong."""
		c = self.ownerComp
		if c.par.enablecloning.eval() and c.par.clone.eval() is None:
			c.par.enablecloning = False
			self.fnsLog(f'{self.REGISTRY_NAME}: Enable Cloning switched off on the master')

	def _retireWidgetLayoutPage(self):
		"""Take away the package-wide Widgets page (Margin, Gap) that lived
		on the master for one day (2026-10-11): each tool now sets its own
		widget's margin. Pars first, then the empty page (TD moves a
		destroyed page's pars elsewhere). Only when present."""
		c = self.ownerComp
		for name in self.RETIRED_PARS:
			p = c.par[name]
			if p is not None:
				p.destroy()
		for pg in list(c.customPages):
			if pg.name == self.RETIRED_PAGE and not pg.pars:
				pg.destroy()

	def _ensureViewPars(self):
		"""Get-or-create the View page: read-only, written by the global."""
		page = next((pg for pg in self.ownerComp.customPages if pg.name == self.VIEW_PAGE), None)
		if page is None:
			page = self.ownerComp.appendCustomPage(self.VIEW_PAGE)
		at_rest = {'Viewx1': 1.0, 'Viewy1': 1.0, 'Resolutionw': 8, 'Resolutionh': 8,
				   'Unitsperpixel': 1.0, 'Pixelsperpoint': 1.0, 'Zoom': 1.0}
		for name, style, label, help_text in self.VIEW_PARS:
			p = self.ownerComp.par[name]
			if p is None:
				p = getattr(page, 'append' + style)(name, label=label)[0]
				if name in at_rest:
					p.default = at_rest[name]
					p.val = at_rest[name]
			p.help = help_text
			p.readOnly = True

	def _ensureOverlayOps(self):
		"""Get-or-create the composite chain and the two Execute DATs."""
		c = self.ownerComp
		res_w, res_h = "parent().par.Resolutionw", "parent().par.Resolutionh"
		clear = c.op('constant_clear')
		if clear is None:
			clear = c.create(constantTOP, 'constant_clear')
			clear.nodeX, clear.nodeY = 600, -600
		# The clear layer only fills the Composite TOP's second slot, and the
		# composite fits every input to its own size (Pre-Fit Fill): 8x8 of
		# transparent composites exactly like the full overlay size did, and
		# frees that size's whole texture (18 MB at 2975x1519, measured
		# 2026-10-12).
		clear.par.outputresolution = 'custom'
		clear.par.resolutionw.mode = ParMode.CONSTANT
		clear.par.resolutionh.mode = ParMode.CONSTANT
		clear.par.resolutionw, clear.par.resolutionh = 8, 8
		clear.par.colorr, clear.par.colorg, clear.par.colorb, clear.par.alpha = 0, 0, 0, 0
		clear.par.format = 'rgba8fixed'
		comp = c.op('comp_layers')
		if comp is None:
			comp = c.create(compositeTOP, 'comp_layers')
			comp.nodeX, comp.nodeY = 1000, -600
		comp.par.operand = 'over'
		comp.par.prefit = 'fill'			# the 8x8 clear layer relies on it
		comp.par.outputresolution = 'custom'
		comp.par.resolutionw.expr, comp.par.resolutionh.expr = res_w, res_h
		comp.par.format = 'rgba8fixed'
		null = c.op('null_overlay')
		if null is None:
			null = c.create(nullTOP, 'null_overlay')
			null.nodeX, null.nodeY = 1400, -600
		if comp not in null.inputs:
			null.inputConnectors[0].connect(comp)
		frame = c.op('execute_frame')
		if frame is None:
			frame = c.create(executeDAT, 'execute_frame')
			frame.nodeX, frame.nodeY = 600, -1000
			frame.par.active = False
		want = ("# FNS_OverlayRegistry: fit the overlay every frame while a layer\n"
				"# is shown (the registry switches this DAT's Active).\n\n"
				"def onFrameStart(frame):\n"
				"\tparent().ext.OverlayRegistryExt.onFrame()\n"
				"\treturn\n")
		if frame.text != want:
			frame.text = want
		for name, val in (('framestart', True), ('start', False), ('create', False),
						  ('exit', False), ('frameend', False), ('playstatechange', False),
						  ('devicechange', False), ('projectpresave', False), ('projectpostsave', False)):
			p = frame.par[name]
			if p is not None and bool(p.eval()) != val:
				p.val = val
		save = c.op('execute_save')
		if save is None:
			save = c.create(executeDAT, 'execute_save')
			save.nodeX, save.nodeY = 1000, -1000
		want = ("# FNS_OverlayRegistry: the overlay annotation lives in the user's\n"
				"# network, so it leaves before every project save.\n\n"
				"def onProjectPreSave():\n"
				"\tparent().ext.OverlayRegistryExt.onProjectPreSave()\n"
				"\treturn\n")
		if save.text != want:
			save.text = want
		for name, val in (('framestart', False), ('start', False), ('create', False),
						  ('exit', False), ('frameend', False), ('playstatechange', False),
						  ('devicechange', False), ('projectpresave', True), ('projectpostsave', False),
						  ('active', True)):
			p = save.par[name]
			if p is not None and bool(p.eval()) != val:
				p.val = val

	# --- public API ---

	def View(self):
		"""Everything a client layer needs to render, as one dict. The client
		draws whatever it likes into its own TOP over this rectangle; the
		registry composites it and shows the result. Shader clients bind to
		the View page instead (op.FNS_OVERLAYREGISTRY.par.Viewx0 ...).

		x0 y0 x1 y1  the rectangle the layer covers, in network units
		width height the resolution to render at, in pixels
		unitsPerPixel   network units per layer pixel
		pixelsPerPoint  layer pixels per screen point (keeps lines a fixed
		                width on screen at any zoom)
		zoom         the network editor's zoom (points per network unit)
		network      the COMP being viewed, or None
		shown        whether the overlay is on screen now
		"""
		api = self._registryApi() or self
		p = api.ownerComp.par
		def val(name, default):
			par = p[name]
			return par.eval() if par is not None else default
		net = str(val('Network', '') or '')
		return {
			'x0': val('Viewx0', 0.0), 'y0': val('Viewy0', 0.0),
			'x1': val('Viewx1', 1.0), 'y1': val('Viewy1', 1.0),
			'width': val('Resolutionw', 8), 'height': val('Resolutionh', 8),
			'unitsPerPixel': val('Unitsperpixel', 1.0),
			'pixelsPerPoint': val('Pixelsperpoint', 1.0),
			'zoom': val('Zoom', 1.0),
			'network': op(net) if net else None,
			'shown': getattr(api, '_overlay', None) is not None,
		}

	def NetworkToPixel(self, x, y):
		"""A point in network units to layer pixels (origin bottom left)."""
		v = self.View()
		return ((x - v['x0']) / v['unitsPerPixel'], (y - v['y0']) / v['unitsPerPixel'])

	def WidgetTarget(self, canonical):
		"""The live layer TOP registered under `canonical`, or None."""
		info = self.stored['PaneRegistry'].get(canonical)
		return self._resolvePanelOp(info) if info else None

	def Widgets(self):
		"""The registered names, bottom layer first."""
		return self._registeredNamesInOrder()

	@property
	def Overlay(self):
		"""The annotation showing the composite, or None."""
		api = self._registryApi()
		return api._overlay if api is not None else None

	def _registeredNamesInOrder(self):
		entries = self.stored['PaneRegistry']
		ordered, unordered = [], []
		for name, info in entries.items():
			order = self._normalizeMenuOrder(info.get('menu_order'))
			(ordered if order is not None else unordered).append((order, name))
		ordered.sort(key=lambda t: (t[0], t[1].lower()))
		return [n for _, n in ordered] + [n for _, n in unordered]

	def RegisterWidget(self, widget_op, canonical_name, order=None, display=True,
					   callback=None, source_registry=None, active=True):
		"""Publish a TOP as a layer of the network overlay under canonical_name.
		display is the user's show switch, active the tool's own on/off; the
		layer is drawn only with both (docs/OverlayManager.md)."""
		if not self._is_sys_global():
			api = self._registryApi()
			if api is not self:
				return api.RegisterWidget(
					widget_op, canonical_name, order=order, display=display,
					callback=callback, source_registry=source_registry, active=active)
			debug(f'{self.REGISTRY_NAME}: RegisterWidget ignored on {self.ownerComp.path}'
				  f' -- no global /sys registry ready')
			return
		err = self._validateWidget(widget_op)
		if err:
			debug(f'{self.REGISTRY_NAME}: RegisterWidget({canonical_name!r}) rejected: {err}')
			return
		entry = {
			'panel_path': widget_op.path,
			'panel_id': int(widget_op.id),
			'display': '1' if display else '0',
			'active': '1' if active else '0',
		}
		norm_order = self._normalizeMenuOrder(order)
		if norm_order is not None:
			entry['menu_order'] = norm_order
		if callback is not None:
			entry['callback_path'] = callback.path
			entry['callback_id'] = int(callback.id)
		if source_registry is not None:
			entry['source_registry'] = source_registry.path
			entry['source_registry_id'] = int(source_registry.id)
		self.stored['PaneRegistry'][canonical_name] = entry
		self.fnsLog(f'{self.REGISTRY_NAME}: registered layer "{canonical_name}" ({widget_op.path})')
		self._syncSurface()

	def UnregisterWidget(self, canonical_name):
		if not self._is_sys_global():
			api = self._registryApi()
			if api is not self:
				return api.UnregisterWidget(canonical_name)
			return
		self.stored['PaneRegistry'].pop(canonical_name, None)
		self.fnsLog(f'{self.REGISTRY_NAME}: unregistered layer "{canonical_name}"')
		self._syncSurface()

	# RegistryBase healing calls self.UnregisterPanel(name); alias it.
	def UnregisterPanel(self, canonical_name):
		return self.UnregisterWidget(canonical_name)

	def _validateWidget(self, widget_op):
		if widget_op is None:
			return 'No layer TOP selected'
		if widget_op.family != 'TOP':
			return f'{widget_op.path} is not a TOP'
		return None

	# --- host registration (Registration page) ---

	def _applyHostRegistration(self, force=False):
		if self._is_sys_global():
			self._setRegStatus('Idle (global)')
			return
		if self._isUnderSysOrUi():
			self._clearHostRegistration()
			self._setRegStatus('Skipped (/sys or /ui)')
			return
		if not force and not self._isAutoRegister():
			self._clearHostRegistration()
			self._setRegStatus('Idle')
			return
		# Every registration, not only init: a roamed settings file restores
		# the tool's Ovdisplayed AFTER init, in the old expression form it was
		# saved in, and its change re-registers through here (2026-10-12,
		# CookBar came back hidden after a cold boot).
		self._ensureLayerActive()
		# The master was copied from FNS_PaneSearchRegistry, whose Menuorder
		# reads "Toolbar Order"; cloning never carries a host's own pars, so
		# every host heals its label here (the tool's Registry page follows).
		order_par = self.ownerComp.par['Menuorder']
		if order_par is not None and order_par.label != self.ORDER_LABEL:
			order_par.label = self.ORDER_LABEL
		# The layer is its own TOP par; Comp stays the base's COMP par (the
		# tool, '..'), which names the canonical by default.
		layer_par = self.ownerComp.par['Layer']
		layer = layer_par.eval() if layer_par is not None else None
		if not layer:
			if not force:
				self._clearHostRegistration()
			self._setRegStatus('Error: no layer TOP')
			return
		canonical = self._hostCanonicalName()
		if not canonical:
			if not force:
				self._clearHostRegistration()
			self._setRegStatus('Error: empty canonical name')
			return
		err = self._validateWidget(layer)
		if err:
			if not force:
				self._clearHostRegistration()
			self._setRegStatus(f'Error: {err}')
			return
		prev = self.stored['HostCanonical']
		api = self._registryApi()
		if prev and prev != canonical:
			self._unregisterOwnedMenuName(prev, api=api)
		api.RegisterWidget(
			layer, canonical,
			order=self._hostMenuOrder(),
			display=self._parBool('Displayed', True),
			callback=self._hostCallbackDat(),
			source_registry=self.ownerComp,
			active=self._parBool('Layeractive', True),
		)
		self.stored['HostCanonical'] = canonical
		self._setRegStatus(f'Registered: {canonical} -> {layer.path}')
		self._ensureToolRegistryPage()

	def onParAutoregister(self, _par, _val, _prev):
		self._hostExtFromPar(_par)._applyHostRegistration()

	def onParRegister(self, _par):
		self._hostExtFromPar(_par)._applyHostRegistration(force=True)

	def onParCanonicalname(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()

	def onParComp(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()

	def onParLayer(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()

	def onParMenuorder(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()

	def onParDisplayed(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()

	def onParLayeractive(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()

	def onParCallback(self, _par, _val, _prev):
		ext = self._hostExtFromPar(_par)
		if ext._isAutoRegister():
			ext._applyHostRegistration()
