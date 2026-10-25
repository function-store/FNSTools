---
package: FNS_Console
summary: 'The toolkit''s web front: one page served from inside your project, with a tab per concern: settings, install & remove, and whatever your tools contribute.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: How it runs
    anchor: how-it-runs
  - name: Contributing a tab
    anchor: contributing-a-tab
  - name: 'Worked example: ColorUI'
    anchor: worked-example-colorui
  - name: HTTP API
    anchor: http-api
  - name: Python API
    anchor: python-api
  - name: Developing on it
    anchor: developing-on-it
  - name: Troubleshooting
    anchor: troubleshooting
feature_list:
  - name: Settings for every tool on one page
    anchor: how-to-use-it
    does: 'Each installed tool appears as a card with its parameters grouped by page, with a jump list and a search across all of them.'
  - name: Open on any tab
    anchor: how-to-use-it
    does: 'Open Settings, Pick Tools and Open Console open it in Hub, the toolkit root''s panel or your system browser, and the tab sits in the address so a reload or a link keeps it.'
  - name: Install and remove
    anchor: how-to-use-it
    does: 'The installer''s picker in a tab: check a tool to install it, uncheck an installed one to remove it, and its settings are kept for next time.'
  - name: Updates in one list
    anchor: how-to-use-it
    does: 'Compares what you have installed with what the store publishes, shows each update''s notes, and applies one update or all of them.'
  - name: Community tools
    anchor: how-to-use-it
    does: 'Lists tools by other creators, and places some of them straight into the network you are working in.'
  - name: 'Config scope, global or project'
    anchor: how-to-use-it
    does: 'The Settings header switches your settings between global and project scope.'
  - name: Export settings
    anchor: how-to-use-it
    does: 'Writes every tool''s settings to one JSON file in the config folder and offers it as a download.'
  - name: Import settings
    anchor: how-to-use-it
    does: 'Applies a settings file to the tools you have now and keeps the sections for tools you install later.'
  - name: Show or hide tabs
    anchor: how-to-use-it
    does: 'The ⋯ button shows or hides each contributed tab, and the choice is saved on the tool that contributed it.'
  - name: Runs only while in use
    anchor: how-it-runs
    does: 'Served on 127.0.0.1 from inside your project; it starts when you open it and stops after ten idle minutes.'
  - name: Contribute a tab
    anchor: contributing-a-tab
    does: 'A stamped FNS_Console host publishes a tool''s own HTML page as a console tab, with an optional Python DAT answering its requests.'
    authors: true
  - name: Browser hand-off
    anchor: contributing-a-tab
    does: 'While a tool''s tab is exposed, the console switches the tool''s own web render off, and back on when the exposure ends.'
    authors: true
  - name: HTTP API
    anchor: http-api
    does: 'Routes on the console''s port list and show tabs, read and set settings, export and import them, and drive updates from another page.'
    authors: true
  - name: Python API
    anchor: python-api
    does: '`op.FNS_CONSOLE` opens and closes the console, lists and shows tabs, and registers a tab without a host.'
    authors: true
  - name: Hot-synced sources
    anchor: developing-on-it
    does: 'Disk edits to the externalized console sources reach the running console on its next request.'
    authors: true
---

## Why use it

An installed FNSTools carries dozens of tools, and each keeps its settings
on its own parameter pages, inside its own component. Changing how five of
them behave means finding five components and opening five parameter
windows. Adding a tool, removing one and checking for updates are separate
jobs again.

The console puts all of it on one page: every tool's settings in one
scrollable, searchable list, the install picker, the update list, and any tab
a tool contributes. It is served from inside your project on `127.0.0.1`,
only while you are looking at it. Each request goes to the component that
owns the answer, so the page always shows what the tools themselves hold.

## How to use it

1. Open it from the toolkit root's FNSTools parameter page: **Open Settings**
   lands on Settings, **Pick Tools** on Install & remove. The FNS button's
   right-click menu in [Hub](/docs/fns-hub/) has the same two entries, and
   the `FNS_Console` component itself has **Open Console**.
2. It shows in Hub's Console tab when the hub is installed, else in the
   toolkit root's web browser panel, else in your system browser. Inside
   TouchDesigner the page does everything it does in a browser, file
   dialogs included.
3. Pick a tab:
   - **Install & remove** is the installer's picker. Check tools to add
     them, uncheck installed ones to remove them, then review and apply. A
     removed tool's settings are kept for the next install. A badge counts
     the tools that are new since you last looked.
   - **Settings** lists every registered tool as a card with its parameters
     grouped by page, a jump list that follows your scrolling, and a search
     across all tools. A value you change is written through
     [ConfigRegistry](/docs/fns-configregistry/), so it persists and the page
     can never disagree with the component.
   - **Updates** compares what you have with what the store publishes, with
     each update's notes. **Check for updates** asks the store; **Update** or
     **Update all** applies. A standalone copy of a global tool gets a **Take
     over** button that shows what will happen first. It needs
     [Updater](/docs/fns-updater/) in the project.
   - **Community** lists tools by other creators, who make, maintain and
     support them, and places some of them straight into the network you are
     working in. FNSTools never updates those.
   - Tabs that tools contribute, such as ColorUI's, sit after a divider.

A few things people adjust:

- **Settings for this project only:** the Settings header switches the
  **scope** between global and project. [ConfigRegistry](/docs/fns-configregistry/)
  explains the two.
- **Moving your settings to another machine:** **Export** writes
  `<config dir>/exports/FNStools_config_<stamp>.json` and offers it as a
  download. **Import** applies a document to the tools you have now and keeps
  the sections for tools you install later.
- **Fewer tabs:** the **⋯** button at the end of the tab bar lists every
  contributed tab, hidden ones included, with a checkbox each. Your choice is
  written to the contributing tool's **Shown in Console** parameter, so it
  stays with the tool and roams with its settings. The built-in tabs are
  always shown.
- **Keeping a tool in its own panel:** switch off **Expose to Console** on
  the tool's Registry page. It contributes no tab and its own panel works as
  before.
- **Linking to a tab:** the tab you are on is in the address (`#settings`,
  `#tools`, `#updates`, `#t-<name>`), so a reload keeps it and a link can open
  a tab directly. Hub's Console tab reopens on the tab you were last on.

## How it runs

`FNS_Console` is a registry in the FNS sense: it sits on `RegistryBase` like
the toolbar, navbar and config registries.

- The in-project master `FNSTools/FNS_Console` promotes a global copy to
  `/sys/FNS_Registries/FNS_Console`, reachable as `op.FNS_CONSOLE`. The global
  owns the API; the master and every host forward to it.
- The surface is the server. The global owns a Web Server DAT
  (`console_server`) that is created on demand, bound to the first free port
  in **36710-36759**, switched on by `Open`, and switched off after **ten
  minutes** without a request. While someone has used the mouse or keys on
  the page in the last two minutes, the page pings once a minute. The server
  is never saved into the `.toe` or any package, since `/sys` is rebuilt on
  every project open, and several open projects each run their own console
  on their own port.
- Everything is `127.0.0.1` only. The server's Local Address is pinned to
  loopback every time the console checks it, because a Web Server DAT with a
  blank address listens on every interface, venue wifi included.
- The page (`console_page`) and the request dispatcher
  (`console_server_callbacks`) ride along from the master; the global pulls
  them from the master if a promoted copy predates them.
- Routing: `/api/*` settings calls go to `FNS_ConfigRegistry`'s `Ui*`
  methods (the paths are the registry's original ones; the TDXLPP launcher
  reads `/api/state` and `/api/set`); `/api/updates*` goes to `FNS_Updater`;
  `/tools` and the picker's routes go to `FNS_Installer.ServeRequest`;
  `/t/<tab>/...` goes to the tool that contributed the tab. Without the
  config package the Settings tab says so, and the Install and Updates tabs
  do the same without an installer or updater.
- The root's `webBrowser` panel draws the console inside TouchDesigner
  (Hub's Console tab mirrors it), and it renders only while someone can see
  it: its own *Render Only While Window Open* and *Render Only While Viewer
  Active* watchers follow the floating window and the node's viewer, and the
  console, or Hub while its Console tab is shown, holds it on. Closed, its
  Web Render cooks nothing.

## Contributing a tab

A tool contributes a tab the same way it contributes a toolbar button or its
settings: it carries a stamped `FNS_Console` host. What it contributes is a
web re-expression of what it owns (tables, parameters, state), talking to the
same extension its panel talks to. A TouchDesigner panel itself cannot be
embedded in a browser.

1. Put the tab's HTML in a text DAT inside the tool. If the page needs to talk
   to TouchDesigner, add a Python DAT defining `onConsoleRequest` (below).
2. Stamp a host into the tool. The master does the copy safely:

   ```python
   op.FNS.op('FNS_Console').ext.ConsoleRegistryExt.StampHost(
       op.FNS.op('MyTool'), canonical_name='MyTool', autoregister=True,
       par_values={'Tabpage': 'my_page', 'Tabapi': 'my_api',
                   'Tablabel': 'My Tool', 'Taborder': 30})
   ```

3. On the host's Registration page, **Tab Page** names the HTML DAT and
   **Tab API** the Python DAT. Use sibling names: an OP parameter resolves
   from the host's parent network, which is the tool, so write `my_page`,
   not `../my_page` (that looks one level too high).
4. **Canonical Name** sets the tab's path, `/t/<name>/`; empty uses the
   tool's name. It must be URL-safe (letters, digits, `_`, `-`) and must not
   be a built-in's name (`tools`, `settings`, `updates`, `community`).
5. **Tab Label** is what the bar shows. Contributed tabs always sit after the
   built-ins, sorted by **Tab Order** (50 by default) and then by label.
6. With **Expose to Console** on, the host publishes the tab while the
   component exists and re-publishes itself on every start. **Register**
   publishes once regardless. If the tab does not appear, **Registration
   Status** says why.

The host mirrors Expose to Console, Register, Registration Status, Shown in
Console, Tab Label and Tab Order onto the tool's own **Registry** page (prefix
`Cs`), so a tool like ColorUI exposes, hides or goes local-only from its own
parameters without anyone opening the host.

### Writing the page

- **Keep it self-contained.** Inline your CSS and JS. The one shared asset is
  `/base.css`, the console's own palette and components: link it with
  `<link rel="stylesheet" href="/base.css">` and build on its `var(--bg)`,
  `var(--accent)`, `.btn` and `.chip`. A page that must also run outside the
  console, as ColorUI's own Web Render does with no server behind it, inlines
  a copy of that block.
- **Use relative URLs.** They resolve under `/t/<name>/`, so `fetch('api/x')`
  reaches your API. A root-relative `/api/...` reaches the console's own API.

### The API DAT

One function:

```python
def onConsoleRequest(action, method, body):
    """action = the path after /t/<name>/api/, method = 'GET'|'POST',
    body = parsed JSON of a POST, else None. Return anything JSON-able."""
```

Returning `None` answers `{"ok": true}`. An exception answers status 500 with
`{"ok": false, "why": "<the message>"}`, so the page can show the reason.

### The tool's own browser

If the tool's panel is a Web Render of the same page, name it on **Local
Browser**. While the tab is exposed the console serves the page and switches
that browser's `Active` off, since a renderer nobody looks at would keep a CEF
process and a texture alive. It switches `Active` back on when the exposure
ends: Expose off, a failed registration, or the host removed. A tool that
wants finer control implements `OnConsoleExposure(exposed)` on its extension;
the host then calls that and leaves `Active` alone.

### Registering without a host

From your own extension:

```python
op.FNS_CONSOLE.RegisterTab(comp, 'MyTool', page=op('my_page'),
                           api_dat=op('my_api'), label='My Tool', order=30)
```

A direct registration is ephemeral, because the global is rebuilt on every
open: re-register on your `onStart`. A host re-publishes itself.

### Shipped dormant, enabled by the install

Every tool artifact ships with **Expose to Console** off, and the toolkit's
installer turns it on as it lands the package. One artifact therefore serves
two lives:

| How the tool arrived | Console exposure | Its own panel |
|---|---|---|
| dropped into a project on its own (a standalone plugin) | off; nothing raises a console | works as always |
| installed by `FNS_Installer` (bootstrap, picker, Textport rail) | **on**, flipped once at install | off while exposed; the console is the UI |
| updated by `FNS_Updater` | untouched; your choice persists | follows your choice |

It ships off because a registry host bootstraps its own `/sys` global when
none exists. That suits a toolbar button, which adds a capability, and does
harm in the console, whose exposure takes a local surface away: a standalone
ColorUI shipped exposed would raise a console nobody asked for and switch off
its own panel. The rule for any future surface like this: a host whose
exposure takes a local surface away ships dormant, and only the install rail
enables it.

The config registry persists Expose to Console, so after the install's one
decision your choice roams across projects and survives updates. A package
dragged into a project by hand arrives in local mode; switch Expose on from
the tool's page.

## Worked example: ColorUI

ColorUI's panel already is a web page (`webui_html`, rendered in its own Web
Render browser, talking to TouchDesigner through `document.title` rewrites up
and `executeJavaScript` down). Its console tab is the same page with a second
transport, picked at load:

```js
const SERVED = /^https?:$/.test(location.protocol);
const Bridge = SERVED ? HttpBridge : TitleBridge;   // same post()/ack() surface
```

Served, `HttpBridge` POSTs every command to `api/cmd` and gets the fresh state
back, and polls `api/state` every two seconds so edits made in the in-TD panel
show up. The extension side is two methods over the code the panel already
used:

```python
def ConsoleState(self):
    return {'ok': True, 'state': self._statePayload()}

def ConsoleCommand(self, msg):
    if not isinstance(msg, dict):
        return {'ok': False, 'why': 'command must be a JSON object'}
    self._toast_sink = []            # toasts a command raises ride back
    try:
        self._dispatch(msg)          # the title bridge's vocabulary
    except Exception as e:
        toasts, self._toast_sink = self._toast_sink, None
        return {'ok': False, 'why': str(e), 'toasts': toasts}
    toasts, self._toast_sink = self._toast_sink, None
    return {'ok': True, 'state': self._statePayload(), 'toasts': toasts}
```

and the whole `console_api` DAT:

```python
def onConsoleRequest(action, method, body):
    ext = parent.ColorUI.ext.ExtColorUI
    if action == 'state':
        return ext.ConsoleState()
    if action == 'cmd' and method == 'POST':
        return ext.ConsoleCommand(body)
    return {'ok': False, 'why': 'unknown action: %s %s' % (method, action)}
```

Host parameters: Tab Page `webui_html`, Tab API `console_api`, Local Browser
`webBrowser`, label `ColorUI`, order 20.

ColorUI also keeps its renderer off whenever nobody can see it. A Panel
Execute DAT (`watch_viewer`) on the panel value `winopen` (1 while the panel
is open as a floating window) feeds `SyncLocalBrowser`, whose single rule is:
Active = shown in Hub, or the viewer open and the page not served by the
console. The console's hand-off (`OnConsoleExposure`), Hub's
(`OnHubExposure`) and the Expose parameter all call that rule, so there is one
owner and no flicker. With the viewer closed the Web Render cooks nothing;
*Open UI* opens the console's tab while the page is served, else the panel.

## HTTP API

All on the console's port, `127.0.0.1` only.

| Route | Method | Answers with |
|---|---|---|
| `/` | GET | the console page |
| `/base.css` | GET | the console's shared styles, for contributed tabs to link |
| `/api/tabs` | GET | `{ok, tabs:[{name, label, order, builtin, displayed, url?, api?, source?}]}`; hidden contributions included |
| `/api/tabs/display` | POST `{name, displayed}` | `{ok, name, displayed, persisted}`; built-ins refuse |
| `/api/view` | POST `{name}` | remembers the tab the reader is on, so the hub reopens there |
| `/api/state` | GET | every registered tool with its exposed parameters (+ `scope`, `project`, `installer`) |
| `/api/set` | POST `{tool, par, value}` | `{ok, val}`, validated against what `/api/state` exposes |
| `/api/export` | GET | `{ok, document, tools, saved_to}`; the document is also written to `<config dir>/exports/` |
| `/api/import` | POST (a config document) | `{ok, applied:[...], deferred:[...], scope}` |
| `/api/scope` | GET / POST `{value, mode}` | `{ok, scope}`; `global` requires `mode` `push` or `adopt` |
| `/api/updates` | GET | the Updates tab's rows with release notes, and whether a check or an update is running |
| `/api/updates/check` | POST | starts a store check (manifest only) |
| `/api/updates/apply` | POST `{names}` | updates the named packages, or everything that differs when empty |
| `/api/updates/status` | GET | the running pass: stage, the updater's narration, and the results once settled |
| `/api/updates/takeover` | POST `{path, confirm}` | brings a standalone copy of a global tool under the toolkit: the plan first, the move once confirmed |
| `/tools`, `/manifest.js`, `/selection`, `/status`, `/install` and the rest of the picker's routes | any | forwarded to `FNS_Installer` |
| `/t/<name>/` | GET | the contributed tab's page |
| `/t/<name>/api/<action>` | GET / POST | the tab's `onConsoleRequest` |

## Python API

On `op.FNS_CONSOLE` (any host or the master forwards):

```python
op.FNS_CONSOLE.Open()                 # Install & remove, the first tab
op.FNS_CONSOLE.Open(tab='settings')   # Settings
op.FNS_CONSOLE.Open(tab='ColorUI')    # a contributed tab, by canonical name
op.FNS_CONSOLE.Open(panel=False)      # force the system browser
```

| Call | Does |
|---|---|
| `Open(tab=None, panel=True)` | serve and show; returns `{ok, url, shown}`, where `shown` is `hub`, `panel` or `browser` |
| `Serve(tab=None)` | serve without showing; returns the URL, or `None` when no server can start |
| `Close()` | stop serving now |
| `Url()` | the URL while serving, else `None` |
| `Tabs(include_hidden=False)` | the ordered tab list; hidden contributions only when asked |
| `SetTabDisplayed(canonical, displayed)` | show or hide a contribution, written back to its host's Shown in Console |
| `RegisterTab(comp, canonical, page=None, api_dat=None, label='', order=50, displayed=True)` / `UnregisterTab(canonical)` | contributions without a host |
| `ServeTab(canonical, subpath='', method='GET', body=None)` | what the dispatcher calls for `/t/...` |
| `StampHost(target_comp, canonical_name=None, autoregister=True, promote_pars=True, par_values=None)` | on the master: copy a configured host into a tool |
| `UiUpdates()`, `UiUpdatesCheck()`, `UiUpdatesApply(names=None)`, `UiUpdatesStatus()`, `UiUpdatesTakeOver(path=None, confirm=False)` | what the `/api/updates*` routes call |

`op.FNS_CONFIGREGISTRY.OpenSettingsUI(tab, panel)` still works; it forwards
here.

## Developing on it

- Sources are Embody-externalized under `modules/suspects/FNSTools/FNS_Console/`
  (`ConsoleRegistryExt.py`, `console_server_callbacks.py`, `console_page.html`,
  `pre_release.py`). A disk edit hot-syncs into the master and into the `/sys`
  global (its DATs keep the file binding), so the running console picks it up
  on the next request; reload the page.
- Structural changes under `FNSTools` (a new host, a new DAT) must be
  persisted the project's way or a reload reverts them: `pi.Add` for new
  components, `pi.Save` on the changed suspects, `pi.Save(op.FNS)` last, then
  save the project.
- Promoted globals live in `/sys/FNS_Registries`. A `findChildren` from `/`
  does not descend there; search that container explicitly.
- The pre-release hook scrubs registration state, the shortcut, cloning, the
  external-tox binding and any server DAT, so a shipped `FNS_Console` is inert
  until it promotes in the user's project.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| "no free port in 36710-36759" | fifty consoles are open, or that block is reserved on the machine (`netsh interface ipv4 show excludedportrange protocol=tcp`); close some, or change `UI_PORTS` in `ConsoleRegistryExt` |
| The page stops answering after a while | the server stops after ten minutes with nobody using the page, as designed; open the console again |
| Settings tab says the config package is missing | `FNS_ConfigRegistry` is not installed or not yet promoted |
| Install tab says there is no installer | the project has no `FNS_Installer`; drop in the bootstrap or the bare installer |
| Install tab shows **Locked (source checkout)** | you are in the toolkit's own source root, where removing a tool would remove an authored master; point *Install Into* at a scratch container |
| Updates tab says there is no updater | the project has no `FNS_Updater`; updates need the toolkit root with its updater |
| A contributed tab is missing | the host's **Registration Status** says why: no page DAT, a name that is not URL-safe, or a name clashing with a built-in. Remember sibling names for the DAT parameters |
| A tab's `fetch('/api/...')` hits the wrong thing | root-relative paths reach the console; use a relative `api/...` |
| A Register pulse "did nothing" in a script | parameter callbacks fire at frame end; read the status on the next frame |
