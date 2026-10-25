---
package: FNS_ConfigRegistry
summary: 'There are a couple of components whose states/contents you''ll probably want to synchronize between your projects, such as OpTemplates, ExprHotStrings, or Global ResetPLS exceptions.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: The settings page
    anchor: the-settings-page
  - name: Where your settings are kept
    anchor: where-your-settings-are-kept
  - name: Making a tool remember its settings
    anchor: making-a-tool-remember-its-settings
feature_list:
  - name: Settings page for every tool
    anchor: the-settings-page
    does: 'OpenSettingsUI() opens one page, served by Console on localhost, listing every registered tool with its version and editable parameters.'
  - name: Sync settings across projects
    anchor: where-your-settings-are-kept
    does: 'Gathers every tool''s custom parameters, plus extra state from tools like OpTemplates, into one JSON file in the User Palette, outside the .toe.'
  - name: Automatic load and save
    anchor: where-your-settings-are-kept
    does: 'Each tool loads its section once per session, which can be turned off per tool; settings save on project pre-save and before an update.'
  - name: Save All and Load All
    anchor: how-to-use-it
    does: 'One pulse, or a quick-launch command, syncs every tool''s settings to or from the JSON file at once.'
  - name: Global or per project
    anchor: where-your-settings-are-kept
    does: 'Settings either roam through the one file to every project on the machine, or stay in the project file.'
  - name: Host copy per tool
    anchor: making-a-tool-remember-its-settings
    does: 'A tool persists its settings by carrying a small host copy, shown as its Registry page, which forwards to the single promoted /sys registry.'
    authors: true
---

## Why use it

Some of what you set up in the toolkit is worth keeping in every project:
your [OpTemplates](/docs/fns-optemplates/), your
[ExprHotStrings](/docs/fns-exprhotstrings/), the way you configured a tool
you use daily. TouchDesigner keeps parameter values in the `.toe`, so a
change made in one project is missing from the next one, and you end up
flipping the same toggles again.

For a tool author it is the same problem as a chore: every tool that wants
to remember its settings would need its own file, its own idea of when to
save, and its own way to survive an update.

ConfigRegistry does this once for the whole toolkit. It aggregates every
installed tool's custom parameters into **one JSON file** in your User
Palette, saves it when you save the project, and gives each tool its section
back when it loads. Your settings follow you across projects and stay out of
the `.toe`.

## How to use it

ConfigRegistry is one of the toolkit's **core** packages, always installed,
so there is nothing to add. Change a tool's settings as usual and save the
project; open another project and the tool comes up the way you left it.

- **To see every tool's settings in one place**, run **Open FNS settings**
  from quick-launch, or call `op.FNS_CONFIGREGISTRY.OpenSettingsUI()`. See
  [The settings page](#the-settings-page).
- **To carry a change into other projects right away**, pulse **Save All
  Now** (or run **Save all tool configs** from quick-launch). It is handy
  after a significant change. In the other project, **Load All Now**
  re-applies the file to every tool at once.
- **To keep one tool's settings with the project**, switch off **Auto-load**
  on that tool's Registry page, for example for a tool whose state should
  migrate with the project folder.
- **To keep everything with the project**, set the toolkit's Config Scope to
  project ([below](#where-your-settings-are-kept)).

## The settings page

`op.FNS_CONFIGREGISTRY.OpenSettingsUI()` shows every installed tool's
settings on one page. It is the toolkit's settings panel, the replacement for
the hand-authored control parameters that used to live on the toolkit root.
It lists every tool that is registered, with its version and its parameters,
and writing a value there goes through the same filters and persistence as
any other change, so the page and the components can never disagree. A
parameter driven by an expression or a bind is shown read-only.

The page's HTML holds no hardcoded list of tools or parameters. It asks the
registry what exists and renders that, which is why it is always correct for
the subset of tools you actually installed and never grows dead entries for
ones you removed. Each tool's `Registry` page is skipped; that is
registration plumbing.

The page is served by [Console](/docs/fns-console/), the toolkit's web front
and a core package of its own, on `127.0.0.1`, first free port in
**36710-36759**, only while you are looking at it. It opens in the toolkit
root's web panel when there is one, otherwise in your system browser. This
registry only answers the console's `/api/*` calls: `UiState`, `UiSet`,
`UiExport`, `UiImport`, `UiScope`. `op.FNS_CONFIGREGISTRY.OpenSettingsUI()`
still works; it forwards to `op.FNS_CONSOLE.Open()`.

## Where your settings are kept

The file is `FNSTools/config/FNStools_config.json` inside your **User
Palette** by default; **Config File** on the master overrides the location
per install. Each tool has its own section there, holding its custom
parameters plus optional extra state, for example from OpTemplates or
ExprHotStrings.

- **Loading:** each tool loads its own section once per session, about 30
  frames after it registers (**Auto-load**, on by default per tool).
- **Saving:** automatic on project pre-save, on the **Save All Now** pulse
  (on the master or forwarded from any host), and right before the updater
  replaces a package.

Whether the file is used at all is the **Config Scope**, which every copy
follows from the toolkit root's own Config Scope on its FNSTools page:

- **global**, the default: everything roams through the one file, shared by
  every project on the machine. The last save wins across projects.
- **project**: the file is never read and never written. The `.toe` holds the
  settings, and they travel with the project. A tool released on its own, in
  a project without the toolkit root, reads project.

The header of the settings page switches the scope too. Going from project
back to global asks first, because the next save would overwrite the shared
file: you can push this project's settings to it, adopt the shared settings,
or stay on project.

## Making a tool remember its settings

ConfigRegistry ships as its own package, promoted to `/sys` (global shortcut
`op.FNS_CONFIGREGISTRY`). Every tool that wants its settings to persist
carries a small **host** copy of it, visible as the tool's own `Registry`
page (the `Cf`-prefixed section; every control in it is listed under
[What it adds to a registered tool](#registry-section)).

Tools carry a host copy of the registry, but every host forwards to the
promoted `/sys` global, so there is exactly one source of settings however
many tools you have installed. Removing a tool's host means that tool's
settings stop syncing, and nothing else breaks.

For a component of your own, [ConfigHost](/docs/fns-confighost/) is the same
host as a standalone package: drop it in, give it a canonical name, and the
component's parameters join the file. Its page also shows how to save state
that is not a parameter.
