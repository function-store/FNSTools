# Pre-release hook -- runs on the STAGED COPY before the portable tox is
# written (extensions NOT initialized there; direct par/storage edits only).
# args[0] = resolved save path.

exec(open('packaging/pre_release_common.py').read())  # generic FNS strip (Version Ctrl / vc_data)

_c = me.parent()

# The color overrides are this checkout's own palette: storage rides inside
# the tox, so without this a release ships whatever the author last saved
# (v3.2.68 carried 7 family colors, by luck TD's factory values). A user's
# own colors arrive through their config after the tool starts. Exact keys:
# unstore() globs.
for _k in ('colors', 'fam_colors'):
    if _k in _c.storage:
        _c.unstore(_k)
