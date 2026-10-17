
'''Info Header Start
Name : QuickmarkStorageExt
Author : Dan@DAN-4090
Saveorigin : FNSTools_PRIV.toe
Saveversion : 2025.33070
Info Header End'''
### Code and idea from Alex Guevara
### Modified by Function Store

import json
from datetime import datetime
from TDStoreTools import StorageManager

TDF = op.TDModules.mod.TDFunctions

def fnsLog(*args, level='INFO'):
    """Log via the central FNSTools logger (op.FNS 'logger'); silent no-op when
    the logger is absent (standalone installs) or its Active par is off."""
    try:
        _logger = op.FNS.op('logger')
        if _logger and _logger.par.Active.eval():
            _logger.Log(*args, level=level)
    except Exception:
        pass




FNSCommand = next(d for d in me.docked if 'ExtUtils' in d.tags).mod('FNSCommand') # import

class QuickmarkStorageExt:
    """Quickmarks, stored on a custom parameter sequence.

    The store used to be a StorageManager, which had two costs: storage does
    not roam with the toolkit's config and is not visible or editable in the
    UI, so a mark could never carry a NAME the user could read or change. The
    sequence fixes both -- custom parameters travel with the project, roam
    through the config host's pars rail, and each block's Name is free text.

    Block N is the slot reached by ctrl+N, so the first ten line up with the
    hotkeys. The sequence may hold more; those are reachable by command.

    The legacy storage is still declared and is read once by the migration,
    then left alone as a backup. Nothing reads it afterwards.
    """

    SLOTS = 10

    def __init__(self, ownerComp):
        # The component to which this extension is attached
        self.ownerComp = ownerComp

        # legacy store -- migration source only, see _migrateFromStorage
        storedItems = [{'name': f'Quickmark{i}', 'default': None} for i in range(self.SLOTS)]
        self.stored = StorageManager(self, ownerComp, storedItems)

        self._migrateFromStorage()
        self._listSig = None
        self._pinsText = None
        self._rectsSig = None
        self._ensureOverlayPars()
        fnsLog('QuickMarks: init')

    def onInitTD(self):
        # The slim ExtUtils carries no announcer, so this tool registers its
        # quick-launch commands itself: deferred past the registry's /sys
        # promotion and this module's own compile.
        run('args[0]._announceCommands()', self, delayFrames=60, delayRef=op.TDResources)
        # past the overlay registry's /sys promotion
        run('args[0].valid and args[0].ext.QuickmarkStorageExt.syncOverlay()', self.ownerComp,
            delayFrames=90, delayRef=op.TDResources)

    def _announceCommands(self):
        FNSCommand.announce(self.ownerComp)

    def custom_print(self, message):
        # Prints a message to the status bar and the console
        current_time = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"{current_time} {message}"

        ui.status = formatted_message
        fnsLog(f'QuickMarks: {message}')

    ### slot addressing ###

    def _slotIndex(self, slot):
        """Slot index from any of 3, '3' or 'Quickmark3'.

        The hotkey path builds 'Quickmark3' while the registered commands pass
        a bare int; before this they addressed different keys entirely, so a
        mark set by hotkey was invisible to GoToMark.
        """
        text = str(slot).strip()
        if text.startswith('Quickmark'):
            text = text[len('Quickmark'):]
        try:
            return max(0, int(text))
        except ValueError:
            return 0

    def _block(self, slot):
        """Sequence block for a slot, growing the sequence to reach it."""
        index = self._slotIndex(slot)
        seq = self.ownerComp.seq.Mark
        if index >= seq.numBlocks:
            seq.numBlocks = index + 1
        return seq[index]

    def _defaultName(self, network_path):
        """A readable label for a freshly stored mark: the shortest trailing
        piece of its path that no OTHER stored mark's network also ends with,
        so three nested base1 networks come out as base1, base1/base1 and
        base7/base1/base1 instead of the same word three times."""
        if not network_path:
            return ''
        parts = [x for x in network_path.strip('/').split('/') if x]
        if not parts:
            return '/'
        others = []
        for mark in self.Marks():
            net = (mark.get('network') or '').strip('/')
            if net and net != network_path.strip('/'):
                others.append(net.split('/'))
        for k in range(1, len(parts) + 1):
            suffix = parts[-k:]
            if not any(o[-k:] == suffix for o in others):
                return '/'.join(suffix)
        return '/'.join(parts)

    ### store / retrieve ###

    def StoreQuickmark(self, key):
        """Store the current pane's network, current operator, position and zoom under a slot key."""
        # Get current pane details and store it
        current_pane = ui.panes.current
        # Workaround to get precise position and zoom of the network
        quickmark_value = {
            'current_network': current_pane.owner.path,
            'current_child': current_pane.owner.currentChild.path if current_pane.owner.currentChild else None,
            'x': current_pane.x,
            'y': current_pane.y,
            'zoom': current_pane.zoom
        }
        # the area the mark saved, in network units: drawn as its outline
        zoom = current_pane.zoom or 1.0
        quickmark_value['w'] = (current_pane.topRight.x - current_pane.bottomLeft.x) / zoom
        quickmark_value['h'] = (current_pane.topRight.y - current_pane.bottomLeft.y) / zoom
        block = self._block(key)
        block.par.Data = json.dumps(quickmark_value)
        # only auto-name an unnamed slot -- never overwrite the user's label
        if not str(block.par.Name.eval()).strip():
            block.par.Name = self._defaultName(quickmark_value['current_network'])
        self.custom_print(f"QuickMarks {self._label(key)} is set to: {quickmark_value['current_network']}")

    def UnstoreQuickmark(self, key):
        """Clear a slot's mark and name."""
        # Unstores the quickmark specified by the key
        block = self._block(key)
        label = self._label(key)
        block.par.Data = ''
        block.par.Name = ''
        self.custom_print(f"QuickMarks {label} unstored")

    def RetrieveQuickmark(self, key):
        """Jump the current pane to a stored mark (network, current operator, position, zoom); returns the mark."""
        # Get the quickmark from the sequence block
        quickmark = self.GetQuickmark(key)
        if quickmark and 'current_network' in quickmark:
            target = op(quickmark['current_network'])
            if target is None or not target.isCOMP:
                self.custom_print(f"QuickMarks {self._label(key)}: stored network {quickmark['current_network']} no longer exists")
                return quickmark
            pane = ui.panes.current
            pane.owner = target
            if 'current_child' in quickmark:
                child_op = op(quickmark['current_child'])
                if child_op:
                    child_op.current = True
                    child_op.selected = True

            view = (quickmark.get('x', 0), quickmark.get('y', 0), quickmark.get('zoom', 1))
            self._applyView(pane, view)
            # The editor can take the network switch late (measured: with
            # the UI busy, view writes made right after it landed on the
            # network being LEFT, and the new one opened at its own last
            # view), so the jump sometimes needed a second press
            # (2026-10-16; the original called this twice for it). Check
            # and re-apply over the next frames until the view holds.
            self._watchView(pane.id, target.path, view, self.VIEW_TRIES, 0)

            self.custom_print(f"QuickMarks Jump to {self._label(key)}")
        return quickmark

    VIEW_TRIES = 10         # frames a jump keeps checking its view
    VIEW_SETTLED = 2        # frames the view must hold before it stops

    @staticmethod
    def _applyView(pane, view):
        pane.x, pane.y, pane.zoom = view

    @staticmethod
    def _viewIs(pane, view):
        x, y, zoom = view
        return (abs(pane.x - x) < 0.5 and abs(pane.y - y) < 0.5
                and abs(pane.zoom - zoom) < 1e-4)

    def _watchView(self, pane_id, path, view, tries, held):
        run('args[0].valid and args[0].ext.QuickmarkStorageExt.settleView(*args[1:])',
            self.ownerComp, pane_id, path, view, tries, held,
            delayFrames=1, delayRef=op.TDResources)

    def settleView(self, pane_id, path, view, tries, held):
        """Wiring: one frame of a jump's check. Applies the stored view once
        the pane really shows the mark's network, and stops when it has held
        for VIEW_SETTLED frames, after VIEW_TRIES, or when the pane is gone
        or the user has moved on (a manual pan inside the window is
        overridden for at most VIEW_TRIES frames)."""
        pane = next((p for p in ui.panes if p.id == pane_id and p.open), None)
        if pane is None or tries <= 0:
            return
        if pane.owner is not None and pane.owner.path == path:
            if self._viewIs(pane, view):
                held += 1
                if held >= self.VIEW_SETTLED:
                    return
            else:
                held = 0
                self._applyView(pane, view)
        self._watchView(pane_id, path, view, tries - 1, held)

    def GetQuickmark(self, key):
        """The stored dict for a slot, or None. Never navigates."""
        raw = str(self._block(key).par.Data.eval()).strip()
        if not raw:
            return None
        try:
            return json.loads(raw)
        except ValueError:
            fnsLog(f'QuickMarks: slot {self._slotIndex(key)} holds unreadable data',
                   level='WARNING')
            return None

    def GetName(self, key):
        """The user's label for a slot, empty when unset."""
        return str(self._block(key).par.Name.eval()).strip()

    def SetName(self, key, name):
        """Rename a slot. Does not touch where it points."""
        self._block(key).par.Name = str(name)
        self.custom_print(f"QuickMarks slot {self._slotIndex(key)} named '{name}'")

    def _label(self, key):
        """'3' or '3 (my label)' -- for status messages."""
        index = self._slotIndex(key)
        name = self.GetName(key)
        return f'{index} ({name})' if name else str(index)

    def Marks(self):
        """Every populated slot as {index, name, network}."""
        out = []
        seq = self.ownerComp.seq.Mark
        for i in range(seq.numBlocks):
            data = self.GetQuickmark(i)
            if data:
                out.append({'index': i, 'name': self.GetName(i),
                            'network': data.get('current_network')})
        return out

    ### the overlay: a mark list and pins (FNS_OverlayRegistry) ###
    #
    # docs/NetworkOverlayRegistry.md. The list is an interactive widget of the
    # registry: the stored marks, the one for the network you are in
    # highlighted, a click jumps there. The pins are this tool's layer
    # (null_pins_layer, through the FNS_OverlayRegistry host): a label at each
    # mark's saved view centre while you are in its network. Both are rewritten
    # only when something they show has changed.

    LIST_CANONICAL = 'QuickMarks'
    LIST_ORDER = 150        # under CookBar's Top List (100) in a shared corner
    LAYER_ACTIVE_EXPR = 'me.parent().par.Active and me.parent().par.Showpins'
    OVERLAY_SHORTCUT = 'alt.shift.m'
    FRAME_GATE = ("parent().par.Active and ((parent().par.Showpins and "
                  "(parent().par['Ovdisplayed'] is None or parent().par.Ovdisplayed)) "
                  "or parent().par.Showlist)")
    KEYBOARD_SHORTCUTS_EXPR = "parent().par.Shortcuts + ' ' + parent().par.Overlayshortcut"
    LIST_MARGIN = 12
    LIST_ROWS = 10
    ROW_H = 18
    HEAD_H = 22

    def _ensureOverlayPars(self):
        """Get-or-create the overlay pars on the Custom page, appended after
        what is there. Schema re-applied every init; values are the user's."""
        c = self.ownerComp
        page = next((pg for pg in c.customPages if pg.name == 'Custom'), None)
        if page is None:
            return

        def ensure(name, style, label, default, **attrs):
            par = c.par[name]
            if par is None:
                par = getattr(page, 'append' + style)(name, label=label)[0]
                for k in ('menuNames', 'menuLabels'):
                    if k in attrs:
                        setattr(par, k, attrs[k])
                par.val = default
            for k, v in attrs.items():
                setattr(par, k, v)
            par.default = default
            return par

        ensure('Showlist', 'Toggle', 'Mark List', False, startSection=True,
               help='Show your marks in a corner of the network editor while QuickMarks is '
                    'active: the one for the network you are in is highlighted, and a click '
                    'jumps to a mark like Ctrl+number.')
        ensure('Listcorner', 'Menu', 'List Corner', 'topleft',
               menuNames=['topleft', 'topright', 'bottomleft', 'bottomright'],
               menuLabels=['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right'],
               help='Which corner of the network editor the mark list sits in.')
        ensure('Listmargin', 'Int', 'List Margin', self.LIST_MARGIN, min=0, max=400,
               clampMin=True, normMin=0, normMax=100,
               help='How far the mark list sits from the edges of the network editor, and '
                    'from any other tool\'s widget before it in the same corner, in screen points.')
        ensure('Listorder', 'Int', 'List Order', self.LIST_ORDER, min=0, max=1000,
               clampMin=True, normMin=0, normMax=300,
               help='The mark list\'s place among the widgets in the same corner: lower sits '
                    'nearer the corner. The Overlay tab in FNS_Hub sets it when you drag.')
        margin, order = c.par['Listmargin'], c.par['Listorder']
        if margin is not None and order is not None and order.order != margin.order + 0.25:
            order.order = margin.order + 0.25
        ensure('Showpins', 'Toggle', 'Pins', False,
               help='While QuickMarks is active, outline the area each mark saved, with its '
                    'number and name, in the network you are viewing.')
        ensure('Listcollapsed', 'Toggle', 'Mark List Collapsed', False,
               help='Fold the mark list to its title row. The arrow at the right of the '
                    'title row does the same.')
        ensure('Overlayshortcut', 'Str', 'Overlay Hotkey', self.OVERLAY_SHORTCUT,
               help='Hotkey that shows or hides the mark list and the outlines together. '
                    'Your marks and Ctrl+number keep working while they are hidden.')
        # One Keyboard In for every QuickMarks hotkey, following the pars (it
        # had been left holding a constant copy of Shortcuts, so a rebind
        # never reached it; /fns-hotkey-conformance).
        kbd = c.op('keyboardin1')
        if kbd is not None:
            want = self.KEYBOARD_SHORTCUTS_EXPR
            sp = kbd.par.shortcuts
            if sp.mode != ParMode.EXPRESSION or sp.expr != want:
                sp.expr = want
                sp.mode = ParMode.EXPRESSION
        # The pins layer draws while QuickMarks is on AND Pins is: the
        # overlay host's Layer Active, the tool's half of the layer's
        # visibility (docs/OverlayManager.md). Written only when different.
        # execute_overlay runs only while something of QuickMarks would
        # draw: Active, and the pins shown (Pins and the Overlay tab's Show)
        # or the mark list on (owner, 2026-10-12). It had run every frame.
        ex = c.op('execute_overlay')
        if ex is not None:
            ap = ex.par.active
            if ap.mode != ParMode.EXPRESSION or ap.expr != self.FRAME_GATE:
                ap.expr = self.FRAME_GATE
                ap.mode = ParMode.EXPRESSION
        host = c.op('FNS_OverlayRegistry')
        la = host.par['Layeractive'] if host is not None else None
        if la is not None and (la.mode != ParMode.EXPRESSION or la.expr != self.LAYER_ACTIVE_EXPR):
            la.expr = self.LAYER_ACTIVE_EXPR
            la.mode = ParMode.EXPRESSION

    def _parOn(self, name):
        par = self.ownerComp.par[name]
        return par is not None and bool(par.eval())

    def syncOverlay(self):
        """Register the mark list with the overlay registry for as long as
        QuickMarks exists, saying whether it shows: Mark List is the user's
        switch, Active the tool's. The registry places it only with both, and
        the Overlay tab in FNS_Hub lists it either way (docs/OverlayManager.md)."""
        reg = getattr(op, 'FNS_OVERLAYREGISTRY', None)
        if reg is None or not hasattr(reg, 'RegisterPanelWidget'):
            return
        c = self.ownerComp
        panel = c.op('widget_marks')
        if panel is None:
            reg.UnregisterPanelWidget(self.LIST_CANONICAL)
            return
        active, shown = self._parOn('Active'), self._parOn('Showlist')
        if active and shown:
            self._listSig = None
            view = reg.View() if hasattr(reg, 'View') else {}
            net = view.get('network')
            self._refreshList(net.path if net is not None else '')
        order = c.par['Listorder']
        reg.RegisterPanelWidget(panel, self.LIST_CANONICAL,
                                anchor=str(c.par.Listcorner.eval()),
                                order=int(order.eval()) if order is not None else self.LIST_ORDER,
                                margin=int(c.par.Listmargin.eval()),
                                shown=shown, active=active, tool=c,
                                pars={'show': 'Showlist', 'corner': 'Listcorner',
                                      'margin': 'Listmargin', 'order': 'Listorder'})

    def onOverlayFrame(self):
        """Every frame while QuickMarks is active (execute_overlay): keep the
        list's highlight and the pins in step with the view."""
        if not self._parOn('Active'):
            return
        reg = getattr(op, 'FNS_OVERLAYREGISTRY', None)
        if reg is None or not hasattr(reg, 'View'):
            return
        view = reg.View()
        net = view['network']
        path = net.path if net is not None else ''
        if self._parOn('Showlist'):
            self._refreshList(path)
        if self._parOn('Showpins'):
            self._writePins(view, path)

    def _refreshList(self, path):
        """Write the list rows when the marks or the viewed network changed."""
        panel = self.ownerComp.op('widget_marks')
        if panel is None:
            return
        marks = self.Marks()[:self.LIST_ROWS]
        collapsed = self._parOn('Listcollapsed')
        missing = {m['index']: op(m['network'] or '') is None for m in marks}
        sig = (path, collapsed, tuple((m['index'], m['name'], m['network'], missing[m['index']])
                                      for m in marks))
        if sig == self._listSig:
            return
        self._listSig = sig
        rows = []
        for m in marks:
            net = m['network'] or ''
            label = m['name'] or (net.strip('/').split('/')[-1] if net else '?')
            if missing[m['index']]:
                label += '   (missing)'
            rows.append((m['index'], '%d   %s' % (m['index'], label), net == path,
                         missing[m['index']]))
        if not rows:
            rows = [(None, 'No marks yet: Ctrl+Alt+number', False, True)]
        header = panel.op('header')
        if header is not None:
            title = 'QuickMarks (%d)' % len(marks) if collapsed else 'QuickMarks'
            if header.par.text.eval() != title:
                header.par.text = title
        fold = panel.op('btn_collapse')
        if fold is not None:
            # Material Design Icons chevrons (the toolbar's icon font): the
            # text font has no \u25b8/\u25be and drew a missing-glyph box
            glyph = chr(0xF0142) if collapsed else chr(0xF0140)
            if fold.par.text.eval() != glyph:
                fold.par.text = glyph
        shown = 0 if collapsed else len(rows)
        for i in range(self.LIST_ROWS):
            row = panel.op('row%d' % i)
            if row is None:
                continue
            if i < shown:
                slot, text, here, gone = rows[i]
                row.par.display = True
                if row.par.text.eval() != text:
                    row.par.text = text
                row.par.bgalpha = 0.16 if here else 0
                row.par.fontalpha = 0.45 if gone else 1
                row.store('slot', -1 if slot is None else slot)
            else:
                row.par.display = False
                row.store('slot', -1)
        height = self.HEAD_H + shown * self.ROW_H + (4 if shown else 2)
        if panel.par.h.eval() != height:
            panel.par.h = height

    def onMarkRowClick(self, row):
        """A list row was clicked (widget_marks/click_rows): jump to its mark."""
        slot = row.fetch('slot', -1, search=False)
        if slot is None or int(slot) < 0:
            return
        self.RetrieveQuickmark(int(slot))

    def onMarkRowRightClick(self, row):
        """A list row was right-clicked: rename its mark in TD's PopDialog
        (non-blocking), the current name as the default."""
        slot = row.fetch('slot', -1, search=False)
        if slot is None or int(slot) < 0:
            return
        slot = int(slot)
        dialog = getattr(op.TDResources, 'PopDialog', None)
        if dialog is None:
            return
        dialog.OpenDefault(text='Name for mark %d' % slot, title='QuickMarks',
                           buttons=['OK', 'Cancel'], callback=self._onRenameDialog,
                           details={'slot': slot}, textEntry=self.GetName(slot),
                           escButton=2, enterButton=1)

    def _onRenameDialog(self, info):
        if info.get('buttonNum') != 1:
            return
        slot = (info.get('details') or {}).get('slot')
        if slot is None:
            return
        self.SetName(slot, str(info.get('enteredText', '')).strip())
        self._listSig = None

    def onCollapseClick(self):
        """The arrow at the right of the list's title row: fold or unfold."""
        par = self.ownerComp.par['Listcollapsed']
        if par is not None:
            par.val = not par.eval()

    def _paneSizePx(self):
        pane = ui.panes.current
        if pane is None or pane.type != PaneType.NETWORKEDITOR:
            pane = next((p for p in ui.panes if p.type == PaneType.NETWORKEDITOR), None)
        if pane is None:
            return 1600.0, 900.0
        return (pane.topRight.x - pane.bottomLeft.x), (pane.topRight.y - pane.bottomLeft.y)

    def _writePins(self, view, path):
        """table_pins: one label per mark of the viewed network whose saved
        view centre is inside the overlay, in layer pixels."""
        t = self.ownerComp.op('table_pins')
        glsl = self.ownerComp.op('glsl_outlines')
        if t is None:
            return
        lines = ['x\ty\ttext']
        rects = []
        if path:
            upp = max(float(view['unitsPerPixel']), 1e-6)
            ppp = max(float(view.get('pixelsPerPoint', 1.0)), 1e-6)
            x0, y0 = float(view['x0']), float(view['y0'])
            w, h = float(view['width']), float(view['height'])
            pane_w = pane_h = None
            seq = self.ownerComp.seq.Mark
            for i in range(seq.numBlocks):
                data = self.GetQuickmark(i)
                if not data or data.get('current_network') != path:
                    continue
                zoom = float(data.get('zoom', 1) or 1)
                aw, ah = data.get('w'), data.get('h')
                if aw is None or ah is None:
                    # a mark from before areas were stored: the area the
                    # current pane would show at the saved zoom
                    if pane_w is None:
                        pane_w, pane_h = self._paneSizePx()
                    aw, ah = pane_w / zoom, pane_h / zoom
                left = (float(data.get('x', 0)) - float(aw) / 2 - x0) / upp
                bottom = (float(data.get('y', 0)) - float(ah) / 2 - y0) / upp
                rw, rh = float(aw) / upp, float(ah) / upp
                if left > w or bottom > h or left + rw < 0 or bottom + rh < 0:
                    continue
                if len(rects) < self.LIST_ROWS:
                    rects.append((left, bottom, rw, rh))
                name = self.GetName(i)
                text = ('%d  %s' % (i, name)) if name else str(i)
                pad = 8 * ppp
                lines.append('%.1f\t%.1f\t%s' % (max(pad, left + pad),
                                                  min(h - pad, bottom + rh - pad), text))
        text = '\n'.join(lines)
        if text != self._pinsText:
            self._pinsText = text
            if t.text != text:
                t.text = text
        sig = tuple(tuple(round(v, 1) for v in r) for r in rects)
        if glsl is not None and sig != self._rectsSig:
            self._rectsSig = sig
            for i in range(self.LIST_ROWS):
                r = rects[i] if i < len(rects) else (0.0, 0.0, 0.0, 0.0)
                for axis, v in zip('xyzw', r):
                    par = glsl.par['vec%dvalue%s' % (i + 1, axis)]
                    if par is not None:
                        par.val = v
            count = glsl.par['vec0valuex']
            if count is not None:
                count.val = len(rects)

    # value changes on the overlay pars (parexec_overlay)

    def _onActiveValueChange(self, par, prev):
        self.syncOverlay()

    def _onShowlistValueChange(self, par, prev):
        self.syncOverlay()

    def _onListcornerValueChange(self, par, prev):
        self.syncOverlay()

    def _onListmarginValueChange(self, par, prev):
        self.syncOverlay()

    def _onListorderValueChange(self, par, prev):
        self.syncOverlay()

    def _onListcollapsedValueChange(self, par, prev):
        self._listSig = None

    ### migration ###

    def _migrateFromStorage(self):
        """Copy legacy StorageManager slots into the sequence, once.

        Guarded by the Migrated par so it cannot run twice, and it never
        overwrites a block that already holds data. The old storage is left
        untouched afterwards as a backup.
        """
        try:
            if self.ownerComp.par.Migrated.eval():
                return
        except AttributeError:
            return          # sequence/par set not present yet
        moved = 0
        for i in range(self.SLOTS):
            old = self.stored.get(f'Quickmark{i}', None)
            if not old or 'current_network' not in old:
                continue
            block = self._block(i)
            if str(block.par.Data.eval()).strip():
                continue    # never clobber a mark already on the sequence
            block.par.Data = json.dumps(old)
            if not str(block.par.Name.eval()).strip():
                block.par.Name = self._defaultName(old.get('current_network'))
            moved += 1
        self.ownerComp.par.Migrated = True
        fnsLog(f'QuickMarks: migrated {moved} mark(s) from storage to the Mark sequence')

    ### hotkeys ###

    def HandleShortcut(self, shortcutName):
        """Called by the hotkey watcher with the pressed combo: recall, store or clear the slot the digit names, toggle the overlay, or toggle Active."""
        if self._isOverlayShortcut(shortcutName):
            self.ToggleOverlay()
            return
        # Extract the key number from the shortcutName
        key_number = shortcutName.split('.')[-1]
        if shortcutName == 'ctrl.alt.shift.0':
            parent().par.Active = not parent().par.Active
            self.custom_print(f"QuickMarks Active is now set to: {parent().par.Active}")

        elif shortcutName.startswith('ctrl.') and 'alt.' not in shortcutName and 'shift.' not in shortcutName:
            if parent().par.Active:
                # Once: RetrieveQuickmark re-applies the view a frame later
                # itself, which is what the doubled call here used to cover.
                self.RetrieveQuickmark(key_number)

        # For storing the quickmark with 'ctrl.' but not 'ctrl.alt.' or 'ctrl.0'
        elif shortcutName.startswith('ctrl.alt.') and 'shift.' not in shortcutName and key_number in [str(i) for i in range(1, 10)]:
            self.StoreQuickmark(key_number)

        # For unstoring the quickmark with 'ctrl.alt.'
        elif 'ctrl.' in shortcutName and 'alt.shift.' in shortcutName and key_number in [str(i) for i in range(1, 10)]:
            self.UnstoreQuickmark(key_number)

    ### FNS_CommandRegistry (quick-launch commands) ###

    @FNSCommand.fns_command(label='Go to quickmark')
    def GoToMark(self, slot: int):
        """Jump to the quickmark stored in the given slot."""
        self.RetrieveQuickmark(slot)
        return {'ok': True, 'slot': self._slotIndex(slot), 'name': self.GetName(slot)}

    @FNSCommand.fns_command(label='Store quickmark', context='network')
    def StoreMark(self, slot: int):
        """Store the current network location in the given slot."""
        self.StoreQuickmark(slot)
        return {'ok': True, 'slot': self._slotIndex(slot), 'name': self.GetName(slot)}

    @FNSCommand.fns_command(label='Clear quickmark')
    def ClearMark(self, slot: int):
        """Clear the quickmark stored in the given slot."""
        self.UnstoreQuickmark(slot)
        return {'ok': True, 'slot': self._slotIndex(slot)}

    @FNSCommand.fns_command(label='Name quickmark')
    def NameMark(self, slot: int, name: str = ''):
        """Set the label shown for a quickmark slot."""
        self.SetName(slot, name)
        return {'ok': True, 'slot': self._slotIndex(slot), 'name': self.GetName(slot)}

    @FNSCommand.fns_command(label='List quickmarks')
    def ListMarks(self):
        """List every populated quickmark slot with its name and network."""
        return {'ok': True, 'marks': self.Marks()}

    @FNSCommand.fns_command(label='Toggle QuickMarks', state='Active')
    def ToggleActive(self):
        """Enable or disable QuickMarks."""
        self.ownerComp.par.Active = not self.ownerComp.par.Active.eval()
        return {'ok': True, 'active': bool(self.ownerComp.par.Active.eval())}

    @FNSCommand.fns_command(label='Toggle QuickMarks overlay', state={'method': 'OverlayShown'})
    def ToggleOverlay(self):
        """Show or hide the mark list and the outlines; marks and Ctrl+number keep working."""
        show = not self.OverlayShown()
        for name in ('Showlist', 'Showpins'):
            par = self.ownerComp.par[name]
            if par is not None:
                par.val = show
        return {'ok': True, 'shown': show}

    def OverlayShown(self):
        """True while the mark list or the outlines are switched on."""
        return self._parOn('Showlist') or self._parOn('Showpins')

    def _isOverlayShortcut(self, shortcutName):
        """The Keyboard In names a shortcut as it was written; compare the
        parts, so 'shift.alt.m' and 'alt.shift.m' are the same key."""
        par = self.ownerComp.par['Overlayshortcut']
        if par is None:
            return False

        def parts(text):
            return frozenset(str(text).lower().replace('+', '.').split('.'))
        target = parts(shortcutName)
        return any(parts(combo) == target for combo in str(par.eval()).split())
