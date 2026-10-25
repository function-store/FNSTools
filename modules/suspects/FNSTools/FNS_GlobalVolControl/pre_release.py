# Embody/PI pre_release hook

# --- ToolbarRegistry host scrub (auto-added) ---
# Shipped tools must not carry in-project registry cloning; the dev
# project's registry healing re-asserts it locally after a release.
for _reg in me.parent().findChildren(name='ToolbarRegistry*', maxDepth=1):
	try:
		_reg.par.clone = ''
	except Exception:
		pass

exec(open('packaging/pre_release_common.py').read())  # generic FNS strip (Version Ctrl / vc_data)

# --- ships at full volume, unmuted (owner, 2026-10-20) ---
# The live tool holds the author's session level and mute, and execute1
# pushes them into ui.masterVolume on project start, so a muted export
# silences every fresh install (v3.2.75's staged artifact carried Volume
# 0.49 and Mute on). The staged copy is not cooking: .val only.
for _name, _shipped in (('Volume', 1.0), ('Mute', False)):
	_p = me.parent().par[_name]
	if _p is not None:
		_p.val = _shipped
