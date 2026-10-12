# Embody pre_release hook -- runs on the STAGED COPY in /sys/quiet before
# the portable tox is written (extensions NOT initialized there; direct
# par/storage edits only). Scrubs all host and overlay state so the released
# OverlayRegistry ships inactive: it installs/updates the /sys global on
# first load and draws nothing until a tool registers a layer.
# args[0] = resolved save path.

comp = me.parent()

# StorageManager keeps its items inside one container key; the overlay's
# last network path is per session.
for key in ('OverlayRegistryExtStored', 'PaneRegistry', 'HostCanonical', 'overlay_path', 'widgets'):
	if key in comp.storage:
		comp.unstore(key)

# hosts ship with Registration pars BOUND to the tool's Registry page;
# the staged copy has no tool above it -- unbind before scrubbing
# Layer Active stays an expression: it is the tool's own on/off, and a
# constant would freeze a shipped tool's layer on or off for good
# (docs/OverlayManager.md, found on the first local release, 2026-10-12).
for _page in comp.customPages:
	if _page.name == 'Registration':
		for _p in _page.pars:
			if _p.name == 'Layeractive':
				continue
			try:
				_p.mode = ParMode.CONSTANT
			except Exception:
				pass

p = comp.par
p.Autoregister = False
p.Canonicalname = ''
p.Regstatus.val = ''
p.Comp = '..'
if p['Layer'] is not None:
	p.Layer = ''
p.Menuorder = -1
p.Displayed = True
p.Callback = ''
p.Promotepars = False  # shippers may opt out per-tool; the bare registry ships with the default
p.opshortcut = ''
p.clone = ''  # never ship with in-project cloning on

# the overlay's per-session state: no layer selects, the frame driver off,
# the View page at rest
for _o in comp.ops('layer_*'):
	_o.destroy()
_frame = comp.op('execute_frame')
if _frame is not None:
	_frame.par.active = False
for _name, _value in (('Viewx0', 0.0), ('Viewy0', 0.0), ('Viewx1', 1.0), ('Viewy1', 1.0),
					  ('Resolutionw', 8), ('Resolutionh', 8), ('Unitsperpixel', 1.0),
					  ('Pixelsperpoint', 1.0), ('Zoom', 1.0), ('Network', '')):
	_vp = comp.par[_name]
	if _vp is not None:
		_vp.val = _value

# The generic FNS strip runs LAST (packaging/pre_release_common.py).
exec(open('packaging/pre_release_common.py').read())
