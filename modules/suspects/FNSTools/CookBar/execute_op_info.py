# FNSTools: an operator's cook time, cached until it cooks again.
# cookTime and gpuCookTime cost about 0.3 ms per read for an operator shown
# in an open network editor (0.001 ms otherwise; TD 2025.33070, measured
# 2026-10-11), and this scan runs over the viewed network every frame:
# 126 operators in /FNSTools took 66 ms a frame. cookAbsFrame is free, so
# the times are read again only after a cook, and for two frames after it
# (the GPU time arrives a frame late).
_times = {}


def _cookTimeOf(child):
	caf = child.cookAbsFrame
	hit = _times.get(child.id)
	if hit is None or hit[0] != caf or absTime.frame - caf <= 2:
		hit = (caf, child.cookTime + child.gpuCookTime)
		_times[child.id] = hit
	return hit[1]


# FNSTools: the Values option writes each bar's number into table_values,
# which text_values draws over the bars. The numbers change ten times a
# second so they can be read; their positions follow the view every frame.
_labels = {}
VALUE_POINTS = 9		# label size in screen points


def _msText(v):
	return ('%.2f ms' % v) if v < 10 else ('%.1f ms' % v)


def _memText(b):
	if b >= 1e9:
		return '%.1f GB' % (b / 1e9)
	if b >= 1e8:
		return '%d MB' % round(b / 1e6)
	if b >= 1e6:
		return '%.1f MB' % (b / 1e6)
	return '%d KB' % max(1, round(b / 1e3))


def _writeValues(rows, ppp, edgeRel, frame):
	"""rows: (id, x, y, width, height, border, cookMs, memBytes, cooking)
	in layer pixels."""
	t = op('table_values')
	if t is None:
		return
	font = VALUE_POINTS * ppp
	gap = 2 * ppp
	fresh = frame % 6 == 0
	lines = ['x\ty\ttext\tfontalpha']
	for oid, x, y, w, h, border, ms, mem, cooking in rows:
		if w < font * 4:
			continue			# too small on screen to carry a label
		hit = _labels.get(oid)
		if hit is None or fresh:
			hit = (_msText(ms), _memText(mem) if mem > 0 else '')
			_labels[oid] = hit
		alpha = '1' if cooking else '0.6'
		lines.append('%.1f\t%.1f\t%s\t%s' % (x, y + h + border + edgeRel + gap, hit[0], alpha))
		if hit[1]:
			lines.append('%.1f\t%.1f\t%s\t%s' % (x, y - border - edgeRel - gap - font, hit[1], alpha))
	text = '\n'.join(lines)
	if t.text != text:
		t.text = text


def frameStart(frame):

	# FNSTools: the bars are a layer of FNS_OverlayRegistry
	# (docs/NetworkOverlayRegistry.md). The registry follows the network
	# editor and says where the layer draws: its rectangle in network units
	# and how many network units one layer pixel is. Positions below are in
	# layer pixels, origin bottom left, which is what glsl_cook_bar reads.
	if not parent().par.Active.eval():
		return
	reg = getattr(op, 'FNS_OVERLAYREGISTRY', None)
	if reg is None or not hasattr(reg, 'View'):
		return
	view = reg.View()
	targetCOMP = view['network']
	if targetCOMP is None:
		return

	# the Top List widget, a few times a second (it ranks every operator in
	# the network, not only those in view)
	if frame % 10 == 0:
		ext = getattr(parent().ext, 'CookBarExt', None)
		if ext is not None:
			ext.updateTopList(targetCOMP)

	# the bars only while their layer is shown (Ovdisplayed, the Overlay
	# tab's Show); with only the Top List on, the scan stops here
	ovd = parent().par['Ovdisplayed']
	if ovd is not None and not ovd.eval():
		return

	upp = max(float(view['unitsPerPixel']), 1e-6)
	netZoom = 1.0 / upp  # layer pixels per network unit
	netWidth = float(view['width'])
	netHeight = float(view['height'])
	x0 = float(view['x0'])
	y0 = float(view['y0'])
	netX = (x0 + float(view['x1'])) / 2  # the view's centre, network units
	netY = (y0 + float(view['y1'])) / 2

	tableTitles = ['name', 'x', 'y', 'width', 'height', 'border', 'isCOMP', 'cooking', 'cookTime', 'childrenCooking', 'childrenCookTime', 'gpuMemory', 'childrenGpuMemory']
	tableText = '\t'.join(tableTitles)

	tableRowsDistDict = []
	if len(_times) > 20000:
		_times.clear()
		_labels.clear()
	showValues = bool(parent().par['Showvalues'] is not None and parent().par.Showvalues.eval())
	edge = me.fetch('barHeight')
	edgeRel = edge * netZoom

	for child in targetCOMP.children:

		if not child.expose:
			continue

		if not child.showDocked:
			continue

		opX = child.nodeX
		opY = child.nodeY
		opWidth = child.nodeWidth
		opHeight = child.nodeHeight

		x = (opX - x0) * netZoom
		y = (opY - y0) * netZoom
		width = opWidth * netZoom
		height = opHeight * netZoom

		# off screen even at the tallest bars (10x, border 11): skip before
		# reading any cook time
		reach = edgeRel * 10 + 11
		if x + width + reach < 0 or x - reach > netWidth or 		   y + height + reach < 0 or y - reach > netHeight:
			continue

		name = child.name
		isCOMP = int(child.family == 'COMP')
		isTOP = int(child.family == 'TOP')

		cooking = int(child.cookedThisFrame or child.cookedPreviousFrame)
		cookTime = _cookTimeOf(child)
		childrenCooking = int(child.childrenCookAbsFrame >= absTime.frame - absTime.step)
		childrenCookTime = child.childrenCookTime + child.childrenGPUCookTime

		current = child.current
		selected = child.selected
		border = 2
		if current: border = 11
		elif selected: border = 4


		outsideTopBar = False
		cookLevel = cookTime
		if cookLevel < 1: cookLevel = 1
		if cookLevel > 10: cookLevel = 10
		edgeRelLevel = edgeRel * cookLevel
		if x + width + border < 0 or x - border > netWidth or\
		   y + height + border + edgeRelLevel < 0 or y + height + border > netHeight:
			outsideTopBar = True

		outsideBottomBar = True
		if isCOMP:
			outsideBottomBar = False
			childrenCookLevel = childrenCookTime
			if childrenCookLevel < 1: childrenCookLevel = 1
			if childrenCookLevel > 10: childrenCookLevel = 10
			childrenEdgeRelLevel = edgeRel * childrenCookLevel
			if x + width + border < 0 or x - border > netWidth or\
			   y - border < 0 or y - border - childrenEdgeRelLevel > netHeight:
				outsideBottomBar = True

		if outsideTopBar and outsideBottomBar:
			continue

		# FNSTools: GPU memory only for operators in view, and a COMP's
		# total from TD's own childrenGPUMemory() (OP Class). The Python
		# walk this replaces visited every nested operator every frame:
		# 7.5 ms against 0.9 ms over /FNSTools, with identical totals.
		gpuMemory = child.gpuMemory if isTOP else 0
		childrenGpuMemory = child.childrenGPUMemory() if isCOMP else 0

		tableRowVals =[name, x, y, width, height, border, isCOMP, cooking, cookTime, childrenCooking, childrenCookTime, gpuMemory, childrenGpuMemory]
		tableRow = [str(val) for val in tableRowVals]

		opDistX = opX + opWidth / 2 - netX
		opDistY = opY + opHeight / 2 - netY
		opDist = tdu.Vector(opDistX, opDistY, 0).length()
		tableRowDistDict = {
			'tableRow': tableRow,
			'opDist': opDist,
			'value': (child.id, x, y, width, height, border,
					  cookTime + (childrenCookTime if isCOMP else 0),
					  childrenGpuMemory if isCOMP else gpuMemory,
					  childrenCooking if isCOMP else cooking),
		}

		added = False
		for i in range(len(tableRowsDistDict)):
			if tableRowsDistDict[i]['opDist'] > opDist:
				tableRowsDistDict.insert(i, tableRowDistDict)
				added = True
				break
		if not added:
			tableRowsDistDict.append(tableRowDistDict)


	maxOPs = parent().par.Maxops
	tableRowsDistDictCropped = tableRowsDistDict[:maxOPs]
	tableRows = [tableRowDistDict['tableRow'] for tableRowDistDict in tableRowsDistDictCropped]
	tableText += '\n' + '\n'.join(['\t'.join(tableRow) for tableRow in tableRows])

	op('table_op_info').clear()
	op('table_op_info').text = tableText

	if showValues:
		_writeValues([r['value'] for r in tableRowsDistDictCropped],
					 float(view['pixelsPerPoint']) or 1.0, edgeRel, frame)
