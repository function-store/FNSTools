---
package: FNS_OpMenuRegistry
summary: 'OP Create dialog surface registry: search words, row decorations, right-click items, filter stages, op alternatives. The raw master, promoted to /sys.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: What tools contribute
    anchor: what-tools-contribute
  - name: For tool authors
    anchor: for-tool-authors
feature_list:
  - name: Shared OP Create dialog surface
    anchor: why-use-it
    does: 'Arbitrates between the tools that change the OP Create dialog, and the dialog goes back to stock when those tools are removed.'
  - name: Arrange contributions in Hub
    anchor: how-to-use-it
    does: 'Hub''s OpMenu tab reorders what the tools add to the dialog and switches any contribution off without uninstalling its tool.'
  - name: Replace a stock operator with an alternative
    anchor: how-to-use-it
    does: 'Create a stock operator type with the alternatives shortcut held and installed alternatives are offered; one is placed with its wiring restored, several open a picker.'
  - name: Alternatives from the store
    anchor: how-to-use-it
    does: 'Alternatives from tools downloaded to your store but not in the project are offered below a divider and placed from disk; >> marks such types.'
  - name: Search word contributions
    anchor: what-tools-contribute
    does: 'Tools add extra words that match an operator type, so searching music finds Audio File In.'
    authors: true
  - name: Row decorations
    anchor: what-tools-contribute
    does: 'Tools relabel rows in the operator list, such as the >>> OpTemplates puts beside every type you have a template for.'
    authors: true
  - name: Right-click menu items
    anchor: what-tools-contribute
    does: 'Tools add entries after TouchDesigner''s own three in the dialog''s right-click menu, such as OpTemplates'' Edit Templates.'
    authors: true
  - name: Filter-chain stages
    anchor: what-tools-contribute
    does: 'Tools splice Script DATs into the operator list''s filter chain to filter or rewrite the list itself.'
    authors: true
  - name: Panel injection
    anchor: what-tools-contribute
    does: 'Tools wire Panel COMPs into the dialog at a named anchor.'
    authors: true
  - name: Callbacks DAT inside each tool
    anchor: for-tool-authors
    does: 'A tool''s whole contribution is one opmenu_callbacks DAT inside the tool, so its menu behaviour travels in its own .tox.'
    authors: true
---

## Why use it

The OP Create dialog, where you pick every operator you add to a network, is a
single piece of TouchDesigner's UI that several tools want to change at once.
[OpMenuMods](/docs/fns-opmenumods/) adds search words and Greg Hermanovic's IO
filters to it, [OpTemplates](/docs/fns-optemplates/) marks the operator types
you have a template for and adds an *Edit Templates...* item, and any tool can
offer itself as an alternative to a stock operator. If each of them patched
the dialog on its own, they would overwrite each other's changes, the last one
installed would win, and removing a tool would leave its patches behind.

OpMenuRegistry is where those changes meet. Each tool contributes, the
registry combines the contributions and applies them, and when the tools are
removed the dialog goes back to stock.

## How to use it

The registry is part of the toolkit's core and installs with it. What you see
depends on which tools you have: words that find an operator under a name of
your own, the `>>>` beside types with a template, IO filter buttons at the top
right of the dialog, extra items when you right-click a row.

- **To reorder or switch off a contribution**, open the **OpMenu** tab of
  [Hub](/docs/fns-hub/) (left-click the **FNS** button in the main-menu bar).
  Switching one off keeps its tool installed.
- **To use an alternative**, create a stock operator type with the
  alternatives shortcut held: `Ctrl+Alt` by default (`Cmd+Ctrl` on macOS), set
  by **Alternatives Shortcut** on the registry's Alternatives page. Without the
  keys the operator is created as normal. With them, every alternative any
  installed tool declared for that type is offered: a single one is placed in
  the fresh operator's spot with its wiring restored, several open a picker.
- **Tools you have downloaded but not added to the project** are offered too,
  below a divider, and placed from disk when you pick them. In the operator
  list, `>>>` marks a type with an alternative in the project and `>>` one
  whose only alternatives are in the store.

## What tools contribute

Six kinds of contribution, and the code for every one of them lives in the
publishing tool, in a callbacks DAT that tool owns. The registry holds only a
reference to it, so it never names a tool, and a tool's menu behaviour
travels inside its own `.tox`.

- **Search words**: extra words that match an operator type, so `music` finds
  Audio File In. OpMenuMods' custom search keywords work this way.
- **Row decorations**: relabel a row, such as the `>>>` that OpTemplates puts
  beside every type you have a template for.
- **Right-click menu items**: entries appended after TouchDesigner's own three
  (Help, Python Help, Operator Snippets), such as OpTemplates' *Edit
  Templates...*.
- **Filter-chain stages**: Script DATs spliced into the operator list's filter
  chain to filter or rewrite the list itself. Greg Hermanovic's IO filters in
  OpMenuMods are the worked example.
- **Panels**: Panel COMPs wired into the dialog at a named anchor.
- **Alternatives**: a tool, or a library of chains, that stands in for a stock
  operator type. OpTemplates is the first contributor.

## For tool authors

A tool contributes through one registry host and one callbacks DAT, however
many kinds of contribution it makes:

1. Put an OpMenuRegistry host in your tool (copy one from a shipped tool, or
   `op.FNS.op('FNS_OpMenuRegistry').StampHost(tool, canonical_name='MyTool')`).
   Leave **Widget COMP** on the tool (`..`, the default) and set **Canonical
   Name**.
2. Press **Create Callbacks**. It puts an `opmenu_callbacks` DAT into your tool
   from the registry's template and points **Callback DAT** at it. Pressing it
   again adopts the existing DAT and never overwrites it.
3. Fill in the hooks you want and switch on **Auto-register**.

The pulse is also promoted onto the tool's own **Registry** page, so the whole
setup works without opening the host.

Every hook is optional. The registry checks which ones the DAT defines and
uses those; as the template ships, each returns empty and the tool contributes
nothing. `me.parent()` is your tool, so resolve everything from there, never
by absolute path.

| Hook | Returns | When |
|---|---|---|
| `onSearchWords()` | `{opType: [word, ...]}` | merged into the dialog's search |
| `onDecorateLabel(opType, label)` | a new label, or `None` | once per visible row, per cook: keep it cheap |
| `onMenuItems()` | `[label, ...]` | appended after TouchDesigner's own three items |
| `onMenuItem(label, opType)` | nothing | one of your items was clicked |
| `onChainNodes()` | `[scriptDAT, ...]` | stages spliced into the operator list's filter chain, in order |
| `onPanels()` | `[(comp, anchor_name), ...]` | panels injected into the dialog, wired to `anchor_name` |
| `onAlternatives()` | `{opType: [alternative, ...]}` | offered when that type is created with the shortcut held |

```python
def onSearchWords():
	return {'noiseTOP': ['grain', 'fractal', 'perlin']}

def onAlternatives():
	# a key may name several types, separated by spaces
	return {'moviefileinTOP ndiinTOP': [{'label': me.parent().name,
	                                     'source': me.parent(),
	                                     'help': 'One line on what it does.'}]}
```

An alternative is `{'label': str, 'source': OP, 'help': str}`. A COMP source
is placed whole, as one node, wired through its In and Out operators; add
`'unpack': True` to copy its children out instead, for a library base that
holds a chain. A bare operator is accepted, labelled with its name, and
unpacks. A tool whose shipped set can differ from its active one, such as a
library the user edits, can also define `onShippedAlternatives()` in the same
shape to name what ships in its `.tox`.

A panel needs an anchor: without one it drops out of the dialog's layout and
stays invisible. `searchpanel` puts it beside the search field. For a single
panel there is a zero-code path: set **Panel** and **Panel Anchor** on the
host and leave the callbacks DAT out. It adds to whatever `onPanels()`
returns.

**Live toggles.** Returning an empty list or dict withdraws a contribution,
and the registry removes whatever it had injected for it. To make one
conditional, decide it in your callbacks (it is your tool's decision) and
call `op.FNS_OPMENUREGISTRY.Resync()` when the condition changes. A hook that
raises is contained: it is reported with `debug()`, skipped, and the dialog
keeps working.
