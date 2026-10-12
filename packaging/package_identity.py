"""Package identity stamped into every shipped artifact (docs/StandaloneTakeover.md).

The COMP name is a weak identity: a browser names a second download
`CustomParTools (1).tox`, TouchDesigner renames a drop into a network that
already holds one to `CustomParTools1`, and users rename. So the release step
stamps two things onto the ARTIFACT copy (build_manifest.ScrubArtifact),
never the live master:

  Pkgname        on the package's top-level FNS_About, beside Pkgversion, on
                 an internal page (never `To Deploy`, so FNS_About's Deploy
                 pulse does not mirror it onto the tool's About page). The
                 catalog name, FNS_ prefix included.
  <FNS:GLOBAL>   a tag on the root COMP of a global tool: one that lands in
                 the toolkit, is no FNS family member and is not core. The
                 form is TDFam's (`<FAM:FNS>`, `<TYPE:...>`); FNS as the key
                 keeps ours apart from TDFam's.

The updater reads both (FNS_Updater): Pkgname to match a renamed copy, the tag
to find standalone copies of global tools anywhere in a project.

Plain Python with no TD globals, loaded by path; tested by
tests/test_standalone_takeover.py.
"""

GLOBAL_TAG = '<FNS:GLOBAL>'
NAME_PAR = 'Pkgname'
IDENTITY_PAGE = 'Identity'
ABOUT = 'FNS_About'
GUARD = 'fns_standalone_guard'

# One line on a global tool's root COMP, for whoever reads the network
# without the toolkit's README beside it: a standalone copy, read by a person
# or an agent (get_op returns the comment). Kept to one line because TD shows
# the comment on the node; a tool's own comment (credits included: midiMapper
# and oscMapper carry Alpha Moonbase's) follows it, never replaced.
NOTICE = ('FNSTools tool: replaced whole on update; change it through its '
          'parameters. functionstore.tools/llms.txt')

# The step-aside a global tool carries (Execute DAT, Create on). Create fires
# when the component is loaded, pasted or the project starts (Execute DAT
# docs). It only releases the Global OP Shortcut: turning the copy's cooking
# off would also silence its hotkeys, but measured on TD 2025.33070 a DAT
# inside a COMP with cooking off never gets onCreate, so a copy switched off
# could never switch itself back on where no toolkit copy exists.
GUARD_TEXT = '''# Stamped by the FNSTools release (docs/StandaloneTakeover.md).
#
# If this project's FNSTools toolkit (op.FNS) already holds %(name)s, this
# copy is a standalone download beside it. TouchDesigner gives a Global OP
# Shortcut to its FIRST holder, so this copy releases its own and the
# toolkit's calls keep reaching the managed copy. The shortcut is remembered
# and put back wherever no toolkit copy exists, so a project carried to a
# machine without FNSTools works as before. The FNSTools console offers to
# take this copy over (Updates).
PACKAGE = %(name)r
KEY = 'fns_standalone_guard'


def onCreate():
	# deferred: on project start the toolkit may load after this copy
	run(_settle, parent().path, delayFrames=30, delayRef=op.TDResources)
	return


def _managedCopy(comp):
	root = getattr(op, 'FNS', None)
	if root is None or comp.path == root.path or comp.path.startswith(root.path + '/'):
		return None
	for c in root.children:
		if c.family != 'COMP' or c.id == comp.id:
			continue
		about = c.op('FNS_About')
		p = getattr(about.par, 'Pkgname', None) if about is not None else None
		if c.name == PACKAGE or (p is not None and str(p.eval()) == PACKAGE):
			return c
	return None


def _settle(path):
	comp = op(path)
	if comp is None:
		return
	held = comp.fetch(KEY, None, search=False)
	# no tag: someone took it off to keep this copy as their own (the
	# FNSTools guide's opt-out), so this guard stands down
	managed = _managedCopy(comp) if '<FNS:GLOBAL>' in comp.tags else None
	if managed is not None:
		if held is None:
			comp.store(KEY, str(comp.par.opshortcut.eval()))
		if str(comp.par.opshortcut.eval()):
			comp.par.opshortcut = ''
			# TD leaves its "Multiply defined Global OP Shortcut" error on
			# this copy after the shortcut is gone (measured); clear it
			comp.clearScriptErrors()
		# this copy's registry hosts registered under the SAME canonical
		# names as the toolkit copy's, taking its toolbar button and
		# settings entry over (measured); point them home again
		for h in managed.findChildren(type=COMP, key=lambda c: hasattr(c.par, 'Register')
				and hasattr(c.par, 'Regstatus')):
			h.par.Register.pulse()
		debug('%%s at %%s is a standalone copy beside FNSTools (%%s): its shortcut '
			  'is released. Take it over from the FNSTools console, Updates.'
			  %% (PACKAGE, comp.path, managed.path))
	elif held is not None:
		comp.par.opshortcut = held
		comp.unstore(KEY)
'''


def IsGlobal(placement, family, kind):
    """A global tool exists once per project: it lands in the toolkit
    (placement absent or 'toolkit'), is no family member, and is not core
    (core packages are embedded by developers and settle duplicates
    through the registries' own newest-wins)."""
    return ((placement or 'toolkit') == 'toolkit' and not family
            and str(kind or 'tool') != 'core')


def _namePar(about):
    """Get-or-create `Pkgname` on `about`, on the internal Identity page."""
    p = getattr(about.par, NAME_PAR, None)
    if p is None:
        page = next((pg for pg in about.customPages if pg.name == IDENTITY_PAGE), None)
        if page is None:
            page = about.appendCustomPage(IDENTITY_PAGE)
        p = page.appendStr(NAME_PAR, label='Package Name')[0]
        p.help = ('The catalog name of the package this component ships as. '
                  'Stamped at release; the updater matches on it, so a '
                  'renamed copy is still recognised.')
    return p


def _guard(comp, name, execute_type):
    """Get-or-replace the step-aside Execute DAT at the bottom left of the
    tool's network."""
    old = comp.op(GUARD)
    if old is not None:
        old.destroy()
    kids = comp.children
    d = comp.create(execute_type, GUARD)
    d.text = GUARD_TEXT % {'name': name}
    d.par.create = True
    d.nodeX = min([int(k.nodeX) for k in kids] or [0])
    d.nodeY = min([int(k.nodeY) for k in kids] or [0]) - 300
    if 'PACKAGE = %r' % name not in d.text or not d.par.create.eval():
        raise RuntimeError('%s did not stamp onto %s' % (GUARD, comp.path))
    return d


def Stamp(comp, name, is_global, execute_type=None):
    """Stamp `comp` (an artifact copy) with its package identity, and a
    global tool with its step-aside guard when `execute_type` (TD's
    executeDAT, passed by the caller) is given. Returns what was stamped;
    raises when the stamp did not hold."""
    out = {}
    about = comp.op(ABOUT)
    if about is not None:
        p = _namePar(about)
        p.expr = ''
        p.val = name
        p.readOnly = True
        if str(p.eval()) != name:
            raise RuntimeError('Pkgname did not stamp onto %s' % about.path)
        out['pkgname'] = name
    if is_global:
        comp.tags.add(GLOBAL_TAG)
        if GLOBAL_TAG not in comp.tags:
            raise RuntimeError('%s did not stamp onto %s' % (GLOBAL_TAG, comp.path))
        out['tag'] = GLOBAL_TAG
        if execute_type is not None:
            out['guard'] = _guard(comp, name, execute_type).name
        own = str(getattr(comp, 'comment', '') or '')
        if not own.startswith(NOTICE):
            comp.comment = NOTICE + ('\n' + own if own else '')
        out['comment'] = NOTICE
    else:
        comp.tags.discard(GLOBAL_TAG)
        old = comp.op(GUARD)
        if old is not None:
            old.destroy()
    return out


def ReadName(comp):
    """The package a COMP ships as: FNS_About.Pkgname, then the COMP's own
    Pkgname, else None. Callers fall back to the COMP name."""
    about = comp.op(ABOUT) if hasattr(comp, 'op') else None
    for holder in (about, comp):
        p = getattr(holder.par, NAME_PAR, None) if holder is not None else None
        if p is not None:
            v = str(p.eval() or '').strip()
            if v:
                return v
    return None
