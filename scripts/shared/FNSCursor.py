"""The mouse over a network editor, in network units, for the tools that
need it.

WHY THIS EXISTS
---------------
FNS_OverlayRegistry.Cursor() answers the same question, and a tool calling
it depends on the overlay registry package, which the manifest cannot
express: `requires` is derived from the registries a tool hosts, and a tool
that only reads the cursor hosts none. FNS_SpaceMaker cannot work without
the cursor, so it reads it from this file instead (owner, 2026-10-19;
docs/SpaceMaker.md). The code and its measurements are TDXCollab's
(CollabPaneSyncHandler._localCursor, 2026-10-15), by way of the registry;
the registry keeps its own copy until it moves to this file at its own
version.

THE CONTRACT
------------
networkPoint(mouseChop=None) -> (network COMP, x, y) in network units, or
None when the mouse is over no network editor of this TD's main window
(another app, a floating TD window, a second TD). Read on demand, never
polled. The current pane is tried first, then every open network editor.

Windows asks the OS (GetCursorPos, ScreenToClient against the main window,
DPI from GetClientRect over the content's width in points), which is current
even when the mouse has not moved. macOS reads a Mouse In CHOP the caller
passes in (output 'absolute': points, y up), minus ui.windowX/Y: IMPLEMENTED
BUT UNVERIFIED here, as in the registry. Positions are measured below each
pane's ~24 point path bar.
"""

import sys

# TD centres a network editor's view (pane.x, pane.y) on the network below the
# pane's path bar, which bottomLeft/topRight include: measured 2026-10-15 by
# TDXCollab from screenshots (Windows 125%, zoom 1 and 2; a Mac agreed).
PANE_BAR = 24.0		# points
_user32 = None


def _getUser32():
	"""user32 with the argtypes these calls need, in its own instance so they
	do not leak into other code using ctypes.windll.user32."""
	global _user32
	if _user32 is None:
		import ctypes
		from ctypes import wintypes
		user32 = ctypes.WinDLL('user32')
		user32.GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
		user32.WindowFromPoint.argtypes = [wintypes.POINT]
		user32.WindowFromPoint.restype = wintypes.HWND
		user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
		user32.GetAncestor.restype = wintypes.HWND
		user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
		user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
		user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
		user32.ScreenToClient.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
		_user32 = user32
	return _user32


def inWindow(mouseChop=None):
	"""The mouse over TD's main window as (x, y) in the panes' coordinates:
	DPI-scaled points from the window content's bottom-left. None when the
	mouse is somewhere else, or this platform cannot tell."""
	pane = next((p for p in ui.panes if p.topRight.u > 0), None)
	if pane is None:
		return None
	scaledWidth = pane.topRight.x / pane.topRight.u	# the content's width in points
	if sys.platform == 'win32':
		try:
			return _inWindowWin32(scaledWidth)
		except Exception:
			return None
	return _inWindowMouseIn(mouseChop)


def _inWindowWin32(scaledWidth):
	"""The window under the mouse must be this TD's main window: not another
	app, a floating TD window, or a second TD on the same machine."""
	import ctypes
	import os
	from ctypes import wintypes
	user32 = _getUser32()
	point = wintypes.POINT()
	if not user32.GetCursorPos(ctypes.byref(point)):
		return None
	window = user32.GetAncestor(user32.WindowFromPoint(point), 2)	# GA_ROOT
	pid = wintypes.DWORD()
	user32.GetWindowThreadProcessId(window, ctypes.byref(pid))
	title = ctypes.create_unicode_buffer(32)
	user32.GetWindowTextW(window, title, 32)
	if pid.value != os.getpid() or not title.value.startswith('TouchDesigner'):
		return None
	rect = wintypes.RECT()
	user32.GetClientRect(window, ctypes.byref(rect))
	user32.ScreenToClient(window, ctypes.byref(point))
	if rect.right <= 0:
		return None
	scale = rect.right / scaledWidth	# physical pixels per point
	return point.x / scale, (rect.bottom - point.y) / scale


def _inWindowMouseIn(mouse):
	"""macOS: a Mouse In CHOP's absolute position (points, y up from the
	primary monitor's bottom-left) minus where the window content starts.
	UNVERIFIED: see the module docstring."""
	if mouse is None or mouse.numChans < 2:
		return None
	return mouse[0].eval() - ui.windowX, mouse[1].eval() - ui.windowY


def networkPoint(mouseChop=None):
	"""(network COMP, x, y) for the network editor under the mouse, in
	network units, or None."""
	cursor = inWindow(mouseChop)
	if cursor is None:
		return None
	cx, cy = cursor
	for pane in [ui.panes.current] + list(ui.panes):
		if pane is None or pane.type != PaneType.NETWORKEDITOR or not getattr(pane, 'open', True):
			continue
		bl, tr = pane.bottomLeft, pane.topRight
		width, height = tr.x - bl.x, tr.y - bl.y - PANE_BAR	# the network, below the path bar
		px, py = cx - bl.x, cy - bl.y
		if not (0 <= px <= width and 0 <= py <= height) or pane.owner is None:
			continue
		zoom = pane.zoom or 1.0
		# pane.x/y is the network point at the centre of the network area
		return (pane.owner, pane.x + (px - width / 2) / zoom, pane.y + (py - height / 2) / zoom)
	return None
