# CookBar's helpers.
#
# FNSTools, 2026-10-11: the bars draw through FNS_OverlayRegistry
# (docs/NetworkOverlayRegistry.md). The registry follows the network editor
# you work in, composites CookBar's layer with every other tool's and shows
# it above the nodes through one utility annotation. Nothing here edits the
# viewed network any more: the original planted a Select TOP and a suicide
# DAT in it, switched its other TOPs' display flags off and dimmed its
# annotations, and had to put all of that back on leaving and around every
# save. retireBackdrop() removes whatever that method may have left behind.

TABLE_HEADER = ('name', 'x', 'y', 'width', 'height', 'border', 'isCOMP',
				'cooking', 'cookTime', 'childrenCooking', 'childrenCookTime',
				'gpuMemory', 'childrenGpuMemory')


def active(active):
	"""Active switched (parexec_active, execute_play_state). The overlay
	host's Displayed follows Active by expression; all that is left here is
	not to show the last frame's bars when it comes back on."""
	parent().store('active', active)
	if not active:
		clearTable()
	# the Top List widget comes and goes with the bar
	ext = getattr(parent().ext, 'CookBarExt', None)
	if ext is not None:
		ext.syncWidget()


def check():
	"""Kept for the callbacks that still call it: the registry follows the
	pane now, so there is nothing to check."""
	return


def clearTable():
	t = op('table_op_info')
	if t is not None:
		t.text = '\t'.join(TABLE_HEADER)


def retireBackdrop():
	"""Put back anything the backdrop method left: its Select TOP and
	suicide DAT in the network it last drew in, display flags it switched
	off, annotation alphas it dropped. Each record is cleared once used."""
	comp = parent()
	target = comp.fetch('targetCOMP', None, search=False)
	if target is not None and getattr(target, 'valid', False):
		for name in ('select_cook_bar_bg', 'text_cook_bar_suicide'):
			o = target.op(name)
			if o is not None:
				o.destroy()
	for path in comp.fetch('hiddenDisplay', [], search=False) or []:
		o = op(path)
		if o is not None:
			o.display = True
	for compPath, name, kind, value in comp.fetch('dimmedAnnotations', [], search=False) or []:
		owner = op(compPath)
		found = owner.findChildren(name=name, type=annotateCOMP, maxDepth=1, includeUtility=True) if owner is not None else []
		p = getattr(found[0].par, 'Backcoloralpha', None) if found else None
		if p is None:
			continue
		if kind == 'expr':
			p.expr = value
			p.mode = ParMode.EXPRESSION
		elif kind == 'bind':
			p.bindExpr = value
			p.mode = ParMode.BIND
		else:
			p.val = value
	for key in ('targetCOMP', 'hiddenDisplay', 'dimmedAnnotations', 'putBackForSave', 'init',
				'netX', 'netY', 'netZoom', 'netWidth', 'netHeight', 'netRatio', 'paneId',
				'winWidth', 'winHeight'):
		if key in comp.storage:
			comp.unstore(key)
