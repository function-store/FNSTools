# Generic FNS pre-release strip -- exec'd by every package's `pre_release`
# hook (a one-liner stamped on all 39 packages):
#
#     exec(open('packaging/pre_release_common.py').read())
#
# Runs on the STAGED COPY in /sys/quiet (extensions not initialized there;
# par/table edits only), so the live component is never touched. Exports
# only ever happen from the source checkout, so the relative open() always
# resolves.
#
# Private Investigator's apparatus is authoring-side only: the `Version
# Ctrl` page fronts `vc_data`, and both describe THIS checkout's save
# history, not the artifact. `Pkgversion` (About page) is the shipped
# version story; a second, stale one would just invite confusion.
#
# Pars are destroyed BEFORE their page: TD relocates a destroyed page's
# surviving pars onto another page instead of deleting them.

_c0 = me.parent()

# --- Envoy's bot never ships ------------------------------------------------
# Envoy draws its bot as envoy_bot_* annotate COMPs into whatever network a
# pane has open, and a tox saved while a pane showed the tool carries all
# of them (ComplexOp's first save did, 2026-09-23). The three sequencer
# hooks stripped them one by one; this is the fleet-wide backstop.
for _bot in _c0.findChildren(name='envoy_bot*', includeUtility=True):
    try:
        _bot.destroy()
    except Exception:
        pass

# --- in-network loggers ship empty ----------------------------------------
# ColorUI, HotkeyManager and PasteFromClipboard carry a Logger COMP that
# keeps its lines in a `logs` table inside the tool: v3.2.69's artifacts
# shipped 20, 100 and 8 lines from the author's machine (2026-10-12). Only
# the header row stays.
for _lg in _c0.findChildren(name='Logger', type=COMP, includeUtility=True):
    try:
        if _lg.par['ext0name'] is None or str(_lg.par.ext0name.val) != 'Logger':
            continue
        _t = _lg.op('logs')
        if _t is not None and _t.isTable and _t.numRows > 1:
            _head = [_c.val for _c in _t.row(0)]
            _t.clear()
            _t.appendRow(_head)
    except Exception:
        pass

# --- the network notes stay in the dev tree -------------------------------
# Annotations are the author's notes on the network (222 across 42
# packages, 2026-10-12): none drew anything a user needs, and a few landed
# in releases with errors. A release carries only the licence notes, which
# license_notices.Stamp adds to the exported copy AFTER this hook, and any
# annotation an operator points at through a parameter (PaneTypeRegistry's
# md viewer renders its annotate1 through Annotateop). `.val` only, matched
# as a path from the parameter's owner: nothing is evaluated on the staged
# copy, and op() would not do, since it never finds a utility operator and
# these notes are utility operators.
_notes = _c0.findChildren(type=annotateCOMP, includeUtility=True)
if _notes:
    _refs = []
    for _o in [_c0] + _c0.findChildren(includeUtility=True):
        for _p in getattr(_o, 'customPars', ()):
            try:
                if _p.style in ('OP', 'COMP') and str(_p.val or '').strip():
                    _refs.append((_o, str(_p.val).strip()))
            except Exception:
                pass

    # Lenient on purpose: a COMP's OP parameter resolves a bare name as its
    # sibling (md's 'annotate1'), so a note is kept when its name is the
    # reference's last segment and it sits in, beside or just above the
    # parameter's owner. Keeping a note too many costs nothing.
    def _isReferenced(_a):
        for _o, _ref in _refs:
            if not _o.valid:
                continue    # an operator inside a note already deleted
            if _ref == _a.path:
                return True
            if _ref.rstrip('/').split('/')[-1] != _a.name:
                continue
            try:
                _near = [_o, _o.parent(), _o.parent(2)]
            except Exception:
                _near = [_o]
            if any(_n is not None and _a.parent() == _n for _n in _near):
                return True
        return False

    for _a in _notes:
        # deleting one note deletes any note inside it, still in the list
        if not _a.valid:
            continue
        if _a.name.startswith('fns_license') or _isReferenced(_a):
            continue
        try:
            _a.destroy()
        except Exception:
            pass

# --- retire root-panel bindings from the artifact ------------------------
# Authored tools bind pars to hand-made control pars on the toolkit ROOT
# (parent.FNS.par.*). No install target has those pars, so shipped binds
# dangle and every install cooks with errors. Freeze them to their stored
# constant: the ConfigRegistry settings UI is the control surface installs
# get instead.
#
# DELIBERATELY `.val`, never `.eval()`: evaluating a dangling reference on
# the same-frame staged copy aborts the whole hook run at a level no
# `except` in this file can catch (cost a day -- v2.12.1 shipped three
# stale artifacts because of it). The stored constant is also the better
# value: it is the authored default, not whatever the author's live root
# panel happened to be set to at export time.
for _c in [_c0] + _c0.findChildren(type=COMP):
    for _p in _c.customPars:
        try:
            _bound = _p.bindExpr and 'parent.FNS' in _p.bindExpr
            _exprd = (_p.mode == ParMode.EXPRESSION and _p.expr
                      and 'parent.FNS' in _p.expr)
            if not (_bound or _exprd):
                continue
            _v = _p.val
            _p.mode = ParMode.CONSTANT
            _p.val = _v
        except Exception:
            pass

# --- no shipped web server listens beyond loopback ------------------------
# A Web Server DAT with a BLANK Local Address listens on EVERY interface
# (Derivative: "When left blank, the Web Server DAT will listen on all
# interfaces"). Every server in this toolkit builds 127.0.0.1 URLs and has no
# authentication, so a blank value shipped an unauthenticated surface to the
# whole LAN. The owning extensions now re-assert this at ensure/Configure
# time; this is the backstop that makes it true of the ARTIFACT regardless of
# which code path created the DAT, or how old the staged copy's server is.
for _ws in _c0.findChildren(type=webserverDAT):
    try:
        _p = _ws.par.localaddress
        if _p.mode != ParMode.CONSTANT:
            _p.mode = ParMode.CONSTANT
        _p.val = '127.0.0.1'
    except Exception:
        pass

for _t in _c0.findChildren(name='vc_data', type=tableDAT):
    try:
        _t.destroy()
    except Exception:
        pass

# --- FNS_About.Owner names the COMP it sits in, never a dev-project path --
# FNS_About copies are stamped, not cloned (every one has an empty clone
# master), and 56 of 57 in the dev project carry Owner as a CONSTANT -- 20
# of them the absolute path of the tool inside THIS checkout. Nothing in the
# toolkit reads Owner any more (the retired stub generator did), but a
# constant absolute path warns "Invalid path" in any project where the tool
# lands elsewhere: the launcher's carried registries, a renamed toolkit
# root, a `placement: root` package. Ship it as the expression that is true
# everywhere. The dev copies were swept to the same expression on 2026-10-21
# (with Enable Cloning switched off: they clone nothing, and a custom-par write
# on a cloning COMP with an empty Clone par has crashed TD natively); this
# stays as the backstop for any copy stamped from an older master.
for _fa in _c0.findChildren(name='FNS_About', type=COMP):
    _p = getattr(_fa.par, 'Owner', None)
    if _p is None:
        continue
    try:
        # the constant survives the switch to EXPRESSION and ships as bytes:
        # the dev path is gone only once the value itself is blanked
        _p.val = ''
        _p.expr = 'parent()'
        _p.mode = ParMode.EXPRESSION
    except Exception:
        pass

# --- clone links into the toolkit ship frozen --------------------------------
# A released copy runs what it shipped with (docs/RegistryHostsFrozen.md). A
# registry host's clone is `op.FNS.op('FNS_<X>Registry') if hasattr(op, 'FNS')
# else None`, ExtUtils clones `../FNS_CustomParTools/...`: in a user's project
# both tie the copy to whatever master is installed, and a host raised
# "Operator /FNSTools has been deleted" on every evaluation once the root was
# removed (2026-10-21). Only five tools' hooks scrubbed it; now every artifact
# does. Clones of TouchDesigner's own components (op.TDResources, op.TDTox,
# op.TDAnnotate, ...) are its palette convention and stay.
for _cc in [_c0] + _c0.findChildren(type=COMP, includeUtility=True):
    try:
        _cp = _cc.par['clone']
        if _cp is None:
            continue
        _ct = _cp.expr if _cp.mode == ParMode.EXPRESSION else str(_cp.val)
        if not _ct:
            # a registry host whose own tool hook already cleared the clone
            # (TimelineTools, GlobalVolControl, PreviewPanel do `clone = ''`)
            # still ships with cloning ON and nothing to clone -- the state
            # that crashed TD natively (2026-10-11). Hosts carry Regstatus.
            if _cc.par['Regstatus'] is not None and _cc.par.enablecloning.eval():
                _cc.par.enablecloning = False
            continue
        if _ct.lstrip().startswith('op.TD'):
            continue
        if 'op.FNS' in _ct or 'FNS_' in _ct or '/FNSTools' in _ct:
            _cp.mode = ParMode.CONSTANT
            _cp.val = ''
            _cc.par.enablecloning = False
    except Exception:
        pass

# --- logger FIFOs ship empty ------------------------------------------------
# The kindergaertner/callbackManager and stubser loggers keep their lines in a
# FIFO DAT under a `logger*` COMP: the fleet audit of 2026-10-21 found 2023-24
# lines naming the author's old /FunctionStore_tools root in AutoRes,
# AutoCombine, OpTemplates, CustomParTools and VSCodeTools artifacts.
for _ff in _c0.findChildren(type=fifoDAT, includeUtility=True):
    try:
        if _ff.parent().name.startswith('logger'):
            _ff.clear()
    except Exception:
        pass

# --- scrub baked log data from vendored ExtUtils copies -------------------
# The QuickExt stub machinery (ExtUtils/extStubser) rides inside FNS_About
# and registry hosts across the fleet, and its logger tables still carry
# 2024 log lines from the author's 2023 project -- dead bytes in every
# artifact and a checkout-path leak. Clear them on the staged copy.
for _d in _c0.findChildren(type=DAT):
    try:
        if 'extStubser' in _d.path and _d.name in ('out1', 'logger'):
            _d.clear()
    except Exception:
        pass

# --- console exposure ships DORMANT; the install rail enables it ----------
# A tool that contributes an FNS_Console tab carries a console host. A
# registry host bootstraps its own /sys global in a bare project -- right for
# a toolbar button (it adds capability), wrong for the console, whose
# exposure REMOVES a local surface: the host switches the tool's own web
# render off once the console serves the page. Shipped with Expose on, a
# standalone ColorUI drop would raise a console nobody asked for and kill
# its own panel.
#
# So every artifact ships with Expose off, and ONE artifact serves both
# regimes: a standalone drop stays in local mode; a toolkit install flips
# Expose on as it lands the package (InstallerExt.ExposeConsoleHosts). The
# flag lives on the tool's Registry page, which the config registry
# persists, so after that first decision the user's own choice roams and
# survives updates. Rule, for any future surface with the same property:
# a host whose exposure takes a local surface away ships dormant and is
# enabled by the install rail, never by bootstrapping itself.
for _c in [_c0] + _c0.findChildren(type=COMP):
    _host = _c.op('FNS_Console') if _c.name != 'FNS_Console' else None
    if _host is None:
        continue
    for _owner, _name in ((_c, 'Csautoregister'), (_host, 'Autoregister')):
        _p = getattr(_owner.par, _name, None)
        if _p is None:
            continue
        try:
            if _p.mode != ParMode.CONSTANT:
                _p.mode = ParMode.CONSTANT
            _p.val = False
        except Exception:
            pass

for _c in [_c0] + _c0.findChildren(type=COMP):
    for _pg in list(_c.customPages):
        if _pg.name != 'Version Ctrl':
            continue
        for _p in list(_pg.pars):
            try:
                _p.destroy()
            except Exception:
                pass
        try:
            _pg.destroy()
        except Exception:
            pass

# --- About is the last custom page ----------------------------------------
# With Version Ctrl gone, About closes the parameter dialog: the tool's own
# pages first, credit and version last. Pages land in creation order, so one
# added after About while authoring rode into the artifact ahead of it
# (measured 2026-10-01: FNS_OpSequencer shipped About before Easing,
# FNS_OpMenuRegistry before Alternatives). The other pages keep their order.
# Plain loops: this file runs under exec(), where a comprehension cannot see
# the script's own names.
for _c in [_c0] + _c0.findChildren(type=COMP):
    _names = []
    for _pg in _c.customPages:
        _names.append(_pg.name)
    if 'About' not in _names or _names[-1] == 'About':
        continue
    _order = []
    for _n in _names:
        if _n != 'About':
            _order.append(_n)
    _order.append('About')
    try:
        _c.sortCustomPages(*_order)
    except Exception as _e:
        try:
            op.Embody.Log('pre_release: could not move About last on %s: %s' % (_c.path, _e), 'WARNING')
        except Exception:
            pass

# --- a tool opens on its FIRST custom page --------------------------------
# The page a parameter dialog opens on is whatever the AUTHOR last clicked,
# and it rides into the artifact like any other live state: measured
# 2026-09-18, FNS_ColorUI shipped opening on `Registry` when its first custom
# page is `ColorUI`. Runs LAST, after the Version Ctrl page is destroyed --
# destroying the current page is exactly what would leave this dangling.
try:
    _pages = list(_c0.customPages)
    if _pages:
        _c0.currentPage = _pages[0]
except Exception:
    pass

# --- no artifact ships the author's atmosphere ----------------------------
# A package whose ROOT is a real object (a Camera COMP, a Geometry COMP) has
# every built-in of that operator in the artifact, and those are SCENE state,
# not package content. FNS_CamSequencer shipped fog 'linear' with fognear 700
# and fogfar 5200 straight out of the author's project, so every install
# arrived with atmosphere on a camera nobody asked to be foggy (reported by a
# user, 2026-09-18).
#
# Fog only, deliberately. A blanket reset of built-ins would be the wrong
# cure: a panel COMP's size, a TOP's resolution and a camera's projection are
# all things a tool legitimately authors. Fog is the one that is never the
# tool's business. Anything else per-package, in that package's own hook.
for _c in [_c0] + _c0.findChildren(type=COMP):
    _p = getattr(_c.par, 'fog', None)
    if _p is None:
        continue
    try:
        if _p.mode != ParMode.CONSTANT:
            _p.mode = ParMode.CONSTANT
        _p.val = _p.default
    except Exception:
        pass

# --- no artifact ships a config-file override -----------------------------
# Configfile (Config page, every ConfigRegistry master and host) redirects the
# aggregated settings JSON away from <palette>/FNSTools/config. The author's
# development project points its master at FNStools_config.dev.json so its
# settings stop roaming into every project where the toolkit is merely USED
# (owner, 2026-09-30). That value must never leave the dev checkout: shipped
# in FNS_ConfigRegistry it would move every user's settings to a file named
# for a development setup, and StampHost copies the master, so a host stamped
# inside the dev project would carry it into whichever package received it.
# Reset to the default on the staged copy, wherever it appears. Empty is the
# only value a user install should ever arrive with.
for _c in [_c0] + _c0.findChildren(type=COMP):
    _p = getattr(_c.par, 'Configfile', None)
    if _p is None:
        continue
    try:
        # CONSTANT mode alone is not enough: TD keeps the expression text
        # on the par, dormant, and one click on the expression toggle in a
        # user's parameter dialog would bring the dev path back. Measured on
        # an export read-back, 2026-09-30. Clear the text, then pin the value.
        _p.expr = ''
        _p.mode = ParMode.CONSTANT
        _p.val = _p.default
    except Exception:
        pass

# --- no artifact ships a development twin folder --------------------------
# The development project keeps its user data in `_dev` twins of the
# palette folders it would otherwise share with the projects where the
# toolkit is merely used: OpTemplates_dev/ for the template library,
# tables_dev/ for the hotkey table (owner, 2026-09-30; docs/ConfigScope.md).
# Those paths live in DAT `file` expressions and in the OpTemplates base's
# `externaltox`, and a shipped one would send every user's edits to a folder
# named for a development setup. Rewrite any `/FNSTools/<name>_dev/` back to
# `/FNSTools/<name>/` on every operator in the package, DATs included, which is
# why this walks all children and not just COMPs. ExternalTables keeps the
# folder as a bare `FNSTools/tables_dev` in its Foldername par, with no slash
# on either side, so the match ends at a slash OR the end of the value (and a
# name that merely starts with `_dev`, like `tables_devices`, is left alone).
import re as _re
_DEV_TWIN = _re.compile(r'FNSTools/([A-Za-z0-9]+)_dev(?=/|$)')
for _o in [_c0] + _c0.findChildren():
    for _pn in ('file', 'externaltox', 'folder', 'Foldername'):
        _p = getattr(_o.par, _pn, None)
        if _p is None:
            continue
        try:
            if _p.mode == ParMode.EXPRESSION and _DEV_TWIN.search(_p.expr or ''):
                _p.expr = _DEV_TWIN.sub(r'FNSTools/\1', _p.expr)
            elif _p.mode == ParMode.CONSTANT and _DEV_TWIN.search(str(_p.val)):
                _p.val = _DEV_TWIN.sub(r'FNSTools/\1', str(_p.val))
        except Exception:
            pass

# --- Embody's recovery breadcrumbs never ship -------------------------------
# Embody stamps `_tdn_rel_path` (and the pending-restore markers) into the
# storage of every COMP it externalizes as TDN, and storage rides inside the
# tox. Tools ported from a project that externalized them that way arrive
# carrying one on most of their COMPs (128 under /FNSTools on 2026-10-09,
# cleared then). In an install they point at files that do not exist. Literal
# keys: unstore() globs.
for _o in [_c0] + _c0.findChildren(includeUtility=True):
    try:
        for _k in ('_tdn_rel_path', '_pending_tox_restore', '_pending_tdn_restore'):
            if _k in _o.storage:
                _o.unstore(_k)
    except Exception:
        pass

# --- no artifact ships the network overlay ----------------------------------
# FNS_OverlayRegistry shows its composite through one utility annotation in
# the network you are viewing (docs/NetworkOverlayRegistry.md). A package
# exported while you viewed its own network would carry it; it is tagged, so
# it goes here wherever it sits.
for _ov in _c0.findChildren(tags=['fns_network_overlay', 'fns_network_overlay_widget'], includeUtility=True):
    try:
        _ov.destroy()
    except Exception:
        pass

# --- no artifact ships a drag-in path to the author's disk ------------------
# Dropping a .tox file into TouchDesigner writes TD's drag-in expression,
# `me.parent().fileFolder + '/' + '<relative path to the dropped file>'`, into
# the new COMP's externaltox. Switched to Constant later, the text stays on the
# par, dormant, and the portable export only blanks the VALUE of a nested
# externaltox, so the author's folder layout rode into the artifacts:
# '../../../../../../Users/<author>/Downloads/QuickParCustom.tox' in CustomParTools,
# '../Downloads/webBrowser.tox' in ColorUI, a personal palette folder in
# PreviewPanel, two Downloads paths in OpFamily (sweep of packaging/dist,
# 2026-10-18). Clear the text wherever it is dormant. A live expression is a
# binding the export handles; `parent.sys.fileFolder` (TD's own palette) names
# no machine and is left alone.
_DRAG_IN = _re.compile(r"me\.parent\(\)\.fileFolder\s*\+\s*'/'\s*\+")
for _c in _c0.findChildren(type=COMP):
    _p = getattr(_c.par, 'externaltox', None)
    if _p is None:
        continue
    try:
        if _p.mode != ParMode.CONSTANT or not _DRAG_IN.search(_p.expr or ''):
            continue
        _v = _p.val
        _p.expr = ''
        _p.mode = ParMode.CONSTANT
        _p.val = _v
    except Exception:
        pass

# --- registration readouts ship blank ---------------------------------------
# RegistryBase writes 'Registered: X -> /FNSTools/X/...' into each tool's
# Cfregstatus, Tbregstatus, Hbregstatus (one per registry prefix) and every
# host's Regstatus, and that text is the DEV project's paths, some of them
# from projects that no longer exist ('/FunctionStore_tools_2025/...'). It is
# rewritten on the first registration in an install, so the artifact carries
# the default. A host's Regstatus is BOUND to its tool's readout; the bind
# stays, only the constant stored under it is reset. On a bound par a `.val`
# write does not reach that constant (measured TD 2025.33070: the par stays in
# Bind mode with the old text), so it goes Constant, takes the default, and
# goes back to Bind, which keeps its bind expression.
for _c in [_c0] + _c0.findChildren(type=COMP):
    for _p in _c.customPars:
        if not _p.name.lower().endswith('regstatus'):
            continue
        try:
            if _p.mode == ParMode.EXPRESSION or _p.val == _p.default:
                continue
            _bound = _p.mode == ParMode.BIND
            _p.mode = ParMode.CONSTANT
            _p.val = _p.default
            if _bound:
                _p.mode = ParMode.BIND
        except Exception:
            pass

# --- shipped surface layout is the authored default, not the live one ------
# A tool's place on the toolbar, navbar, main menu, op menu, pane-type menu
# and hub tabs lives in its own surface pars (Tbmenuorder, Hbtaborder, ...),
# and the Hub configurators keep TD's built-ins, dividers and groups in
# their `state` tables. The author arranges those like any user, and every
# drag wrote straight into the tox: v3.2.67 shipped the author's personal
# group, anchored on two tools outside the starter set, and two tools tied
# at one toolbar slot. What ships is packaging/surface_defaults.json, which
# changes only when the author takes a snapshot (packaging/surface_defaults.py,
# docs/ShippedSurfaceDefaults.md). Deliberately NOT wrapped in a try: a file
# naming a par the package no longer has must fail this export, not ship the
# author's arrangement silently.
_sd = {}
exec(open('packaging/surface_defaults.py').read(), _sd)
_sd['Apply'](_c0, _sd['Load']())

