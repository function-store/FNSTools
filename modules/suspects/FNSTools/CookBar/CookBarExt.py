"""CookBar: quick-launch commands.

Thin on purpose. The bar itself is Anton Heestand's original scripts
(text_funcs and the callback DATs). Since 2026-10-11 it draws as a layer of
FNS_OverlayRegistry (docs/NetworkOverlayRegistry.md), which shows it above
the nodes without touching the viewed network, so the save and teardown
hooks this extension used to need are gone. On init it retires whatever the
earlier backdrop method left behind (text_funcs.retireBackdrop).
"""

FNSCommand = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('FNSCommand')  # import


class CookBarExt:
	# execute_op_info scans only while something of Cook Bar would draw:
	# Active, and its bars shown (Ovdisplayed, the Overlay tab's Show) or its
	# Top List on. Ovdisplayed arrives with the registry host's promotion, so
	# a missing one reads as shown.
	FRAME_GATE = ("parent().par.Active and ((parent().par['Ovdisplayed'] is None"
				  " or parent().par.Ovdisplayed) or parent().par.Toplist)")

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self._ensureListPars()
		self._ensureFrameGate()

	def _ensureFrameGate(self):
		"""Nothing of Cook Bar cooks while nothing of it would draw (owner,
		2026-10-12). Written only when different."""
		d = self.ownerComp.op('execute_op_info')
		if d is None:
			return
		p = d.par.active
		if p.mode != ParMode.EXPRESSION or p.expr != self.FRAME_GATE:
			p.expr = self.FRAME_GATE
			p.mode = ParMode.EXPRESSION

	def onInitTD(self):
		# The slim ExtUtils has no announcer: announce past the registry's
		# /sys promotion and this module's own compile.
		run('args[0]._announceCommands()', self, delayFrames=60, delayRef=op.TDResources)
		run('args[0].valid and args[0].ext.CookBarExt.retireBackdrop()', self.ownerComp,
			delayFrames=2, delayRef=op.TDResources)
		# past the overlay registry's /sys promotion
		run('args[0].valid and args[0].ext.CookBarExt.syncWidget()', self.ownerComp,
			delayFrames=90, delayRef=op.TDResources)

	def _announceCommands(self):
		FNSCommand.announce(self.ownerComp)

	def retireBackdrop(self):
		"""Remove what the backdrop method may have left in a network."""
		try:
			self.ownerComp.op('text_funcs').module.retireBackdrop()
		except Exception as e:
			debug('CookBar: could not retire the old backdrop: %s' % e)

	# ---------------------------------------------- the top list widget
	#
	# A small list of the viewed network's heaviest operators, shown as an
	# interactive widget of FNS_OverlayRegistry pinned to a corner of the
	# network editor (docs/NetworkOverlayRegistry.md, "Widgets"). Clicking a
	# row makes that operator current and frames the view on it; the tabs
	# along the top switch what it ranks by (Toprank).

	TOP_ROWS_MAX = 12
	TOP_CANONICAL = 'CookBar'
	TOP_ORDER = 100			# its place in the corner's stack: CookBar's band
	TOP_MARGIN = 12			# List Margin's default, screen points

	def _ensureListPars(self):
		"""Get-or-create the Top List pars on the CookBar page, appended
		after what is there (never reordered: a live par reorder crashed TD,
		2026-10-11). Schema re-applied every init; values are the user's."""
		c = self.ownerComp
		page = next((p for p in c.customPages if p.name == 'CookBar'), None)
		if page is None:
			return

		def ensure(name, style, label, default, **attrs):
			p = c.par[name]
			if p is None:
				p = getattr(page, 'append' + style)(name, label=label)[0]
				for k in ('menuNames', 'menuLabels'):
					if k in attrs:
						setattr(p, k, attrs[k])
				p.val = default
			for k, v in attrs.items():
				setattr(p, k, v)
			p.default = default
			return p

		ensure('Toplist', 'Toggle', 'Top List', True, startSection=True,
			   help='Show a list of the viewed network\'s heaviest operators in a corner '
					'of the network editor while Cook Bar is on. Click a row to go there, '
					'or a tab at the top to change what it ranks by.')
		ensure('Toprank', 'Menu', 'Rank By', 'cooktime',
			   menuNames=['cooktime', 'gpumemory'], menuLabels=['Cook Time', 'GPU Memory'],
			   help='What the Top List ranks by: cook time (CPU and GPU per frame, a COMP '
					'with everything inside it) or GPU memory.')
		ensure('Topcorner', 'Menu', 'List Corner', 'topleft',
			   menuNames=['topleft', 'topright', 'bottomleft', 'bottomright'],
			   menuLabels=['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right'],
			   help='Which corner of the network editor the Top List sits in.')
		ensure('Topmargin', 'Int', 'List Margin', self.TOP_MARGIN, min=0, max=400,
			   clampMin=True, normMin=0, normMax=100,
			   help='How far the Top List sits from the edges of the network editor, and '
					'from any other tool\'s widget before it in the same corner, in screen points.')
		ensure('Showvalues', 'Toggle', 'Values', False, startSection=False,
			   help='Write each bar\'s number next to it: the cook time above the operator '
					'and the GPU memory below it. Shown on operators wide enough on screen '
					'to fit them.')
		ensure('Toprows', 'Int', 'List Rows', 8, min=1, max=self.TOP_ROWS_MAX,
			   clampMin=True, clampMax=True, normMin=1, normMax=self.TOP_ROWS_MAX,
			   help='How many operators the Top List shows, 1 to %d.' % self.TOP_ROWS_MAX)

		# The bar settings as one section after the Top List: Max OPs starts
		# it and Values follows it (appended pars all get order 0). Written
		# only when wrong; nothing clones CookBar, so this is not the
		# clone-master crash (docs/NetworkOverlayRegistry.md).
		maxops, values = c.par['Maxops'], c.par['Showvalues']
		if maxops is not None and values is not None:
			if not maxops.startSection:
				maxops.startSection = True
			if values.order != maxops.order + 0.5:
				values.order = maxops.order + 0.5
		corner, margin = c.par['Topcorner'], c.par['Topmargin']
		if corner is not None and margin is not None and margin.order != corner.order + 0.5:
			margin.order = corner.order + 0.5
		ensure('Toporder', 'Int', 'List Order', self.TOP_ORDER, min=0, max=1000,
			   clampMin=True, normMin=0, normMax=300,
			   help='The Top List\'s place among the widgets in the same corner: lower sits '
					'nearer the corner. The Overlay tab in FNS_Hub sets it when you drag.')
		order = c.par['Toporder']
		if margin is not None and order is not None and order.order != margin.order + 0.25:
			order.order = margin.order + 0.25
		ensure('Topcollapsed', 'Toggle', 'Top List Collapsed', False,
			   help='Fold the Top List to its tab row. The arrow at the right of the tabs '
					'does the same.')
		rows, folded = c.par['Toprows'], c.par['Topcollapsed']
		if rows is not None and folded is not None and folded.order != rows.order + 0.5:
			folded.order = rows.order + 0.5

	def syncWidget(self):
		"""Register the list with the overlay registry for as long as Cook
		Bar exists, saying whether it shows: Top List is the user's switch,
		Active the tool's. The registry places it only with both, and the
		Overlay tab in FNS_Hub lists it either way (docs/OverlayManager.md)."""
		reg = getattr(op, 'FNS_OVERLAYREGISTRY', None)
		if reg is None or not hasattr(reg, 'RegisterPanelWidget'):
			return
		c = self.ownerComp
		panel = c.op('widget_top')
		if panel is None:
			reg.UnregisterPanelWidget(self.TOP_CANONICAL)
			return
		toplist = c.par['Toplist']
		corner = str(c.par.Topcorner.eval()) if c.par['Topcorner'] is not None else 'topleft'
		margin = int(c.par.Topmargin.eval()) if c.par['Topmargin'] is not None else self.TOP_MARGIN
		order = int(c.par.Toporder.eval()) if c.par['Toporder'] is not None else self.TOP_ORDER
		reg.RegisterPanelWidget(panel, self.TOP_CANONICAL, anchor=corner, order=order, margin=margin,
								shown=toplist is None or bool(toplist.eval()),
								active=bool(c.par.Active.eval()), tool=c,
								pars={'show': 'Toplist', 'corner': 'Topcorner',
									  'margin': 'Topmargin', 'order': 'Toporder'})

	def updateTopList(self, network):
		"""Rank `network`'s operators and write the rows (execute_op_info,
		every few frames while Cook Bar is on). Writes only what changed."""
		c = self.ownerComp
		panel = c.op('widget_top')
		if panel is None or network is None or c.par['Toprank'] is None:
			return
		gpu = str(c.par.Toprank.eval()) == 'gpumemory'
		rows = int(c.par.Toprows.eval())
		# cookTime is the LAST cook's duration, kept forever: an operator that
		# cooked once at startup would top the list for good (tdPyEnvManager
		# read 13.9 ms in a network running at 13.5 ms a frame). Cook time
		# counts only what cooked within the last second.
		recent = absTime.frame - max(1, int(round(project.cookRate)))
		scored = []
		for child in network.children:
			if not child.expose:
				continue
			if gpu:
				v = child.childrenGPUMemory() if child.isCOMP else (child.gpuMemory if child.isTOP else 0)
			else:
				v = 0.0
				if child.cookAbsFrame >= recent:
					v += child.cookTime + child.gpuCookTime
				if child.isCOMP and child.childrenCookAbsFrame >= recent:
					v += child.childrenCookTime + child.childrenGPUCookTime
			if v > 0:
				scored.append((v, child.name))
		scored.sort(reverse=True)
		if panel.fetch('network', '', search=False) != network.path:
			panel.store('network', network.path)
		for i in range(self.TOP_ROWS_MAX):
			row = panel.op('row%d' % (i + 1))
			if row is None:
				continue
			if i < rows and i < len(scored):
				v, name = scored[i]
				if not gpu:
					amount = '%.2f ms' % v
				elif v >= 1e6:
					amount = '%.1f MB' % (v / 1e6)
				else:
					amount = '%d KB' % max(1, round(v / 1e3))
				label = '%s   %s' % (name, amount)
			else:
				name, label = '', ''
			if row.par.text.eval() != label:
				row.par.text = label
			if row.fetch('opname', '', search=False) != name:
				row.store('opname', name)

	def onTopRowClick(self, row):
		"""A row was clicked (widget_top/click_rows): make that operator
		current and the only selection in the network the list was built
		for, and frame the view on it (TD's Home Selected)."""
		panel = self.ownerComp.op('widget_top')
		name = row.fetch('opname', '', search=False)
		path = panel.fetch('network', '', search=False) if panel is not None else ''
		network = op(path) if path else None
		target = network.op(name) if network is not None and name else None
		if target is None:
			return
		pane = ui.panes.current
		if pane is None or pane.type != PaneType.NETWORKEDITOR or pane.owner != network:
			pane = next((p for p in ui.panes
						 if p.type == PaneType.NETWORKEDITOR and p.owner == network), None)
		for other in list(network.selectedChildren):
			if other != target:
				other.selected = False
		# a selected widget would be framed too, and it is pinned at 1/zoom
		# size: each click would zoom out further
		for ann in network.findChildren(tags=['fns_network_overlay_widget'], maxDepth=1,
										includeUtility=True):
			ann.selected = False
		target.current = True
		target.selected = True
		if pane is not None:
			# home(zoom=False, op=...) only re-centred, and repeated clicks
			# zoomed further out (owner, 2026-10-11)
			pane.homeSelected(zoom=True)

	def onTopCollapseClick(self):
		"""The arrow at the right of the tab row (widget_top/click_fold):
		fold or unfold the list."""
		par = self.ownerComp.par['Topcollapsed']
		if par is not None:
			par.val = not par.eval()

	def onTopRankClick(self, tab):
		"""A tab was clicked (widget_top/click_tabs): rank by the Toprank
		entry it stands for (stored on the tab as 'rank')."""
		rank = tab.fetch('rank', '', search=False)
		p = self.ownerComp.par['Toprank']
		if p is None or rank not in p.menuNames:
			debug('CookBar: tab %s ranks by unknown %r' % (tab.name, rank))
			return
		if p.eval() != rank:
			p.val = rank

	# value changes on the CookBar page (parexec_ext)

	def _onToplistValueChange(self, par, prev):
		self.syncWidget()

	def _onTopcornerValueChange(self, par, prev):
		self.syncWidget()

	def _onTopmarginValueChange(self, par, prev):
		self.syncWidget()

	def _onToporderValueChange(self, par, prev):
		self.syncWidget()

	def _onToprankValueChange(self, par, prev):
		self._refreshTopList()

	def _onToprowsValueChange(self, par, prev):
		self._refreshTopList()

	def _refreshTopList(self):
		panel = self.ownerComp.op('widget_top')
		path = panel.fetch('network', '', search=False) if panel is not None else ''
		network = op(path) if path else None
		if network is not None:
			self.updateTopList(network)

	# ---------------------------------------------- commands

	@FNSCommand.fns_command(label='Toggle cook bar', state={'method': 'BarActive'})
	def ToggleCookBar(self):
		"""Show or hide each operator's cook time and GPU memory above it in the network editor."""
		p = self.ownerComp.par.Active
		if not p.enable:
			return {'ok': False, 'error': 'the timeline is paused; Cook Bar draws while it plays'}
		p.val = not p.eval()
		return {'ok': True, 'active': bool(p.eval())}

	@FNSCommand.fns_command(label='Open Global Hog CHOP')
	def OpenHog(self):
		"""Open the Global Hog CHOP's parameters, to eat frame time on purpose while you watch the bars."""
		hog = self.ownerComp.op('hog_global')
		if hog is None:
			return {'ok': False, 'error': 'hog_global is missing'}
		hog.openParameters()
		return {'ok': True}

	@FNSCommand.fns_command(label='Toggle Global Hog CHOP', hidden=True, state={'method': 'HogActive'})
	def ToggleHog(self):
		"""Switch the Global Hog CHOP on or off. It DELIBERATELY eats frame time (stress test)."""
		hog = self.ownerComp.op('hog_global')
		if hog is None:
			return {'ok': False, 'error': 'hog_global is missing'}
		hog.par.active = not hog.par.active.eval()
		return {'ok': True, 'active': bool(hog.par.active.eval())}

	# ---------------------------------------------- parameter pulses (parexec_ext)

	def _onOpenhogPulse(self, par):
		self.OpenHog()

	def BarActive(self):
		"""Whether the bars are on (the Toggle cook bar chip)."""
		return bool(self.ownerComp.par.Active.eval())

	def HogActive(self):
		"""Whether the Global Hog CHOP is on (the Toggle Global Hog CHOP chip)."""
		hog = self.ownerComp.op('hog_global')
		return bool(hog.par.active.eval()) if hog is not None else False
