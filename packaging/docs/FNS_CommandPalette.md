---
package: FNS_CommandPalette
summary: 'A command palette inside TouchDesigner: every command your FNS tools declare, plus TouchDesigner''s own palette components, ranked by what you are looking at.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Finding commands
    anchor: finding-commands
  - name: Prefixes
    anchor: prefixes
  - name: Values and presets
    anchor: values-and-presets
  - name: Placing palette components
    anchor: placing-palette-components
  - name: Shaping the list
    anchor: shaping-the-list
  - name: Calling extension methods
    anchor: calling-extension-methods
  - name: How the pieces fit
    anchor: how-the-pieces-fit
hotkeys:
  - keys: Ctrl+Shift+P
    does: Open the palette over the network you are in
local_keys:
  - Ctrl+D
  - Ctrl+H
  - Alt+S
  - Alt+Up
  - Alt+Down
feature_list:
  - name: Find any command on one key
    anchor: how-to-use-it
    does: 'Opens over the network you are in with every command your FNS tools declare, TouchDesigner''s built-in commands and its palette components in one ranked list.'
  - name: Context-aware ranking
    anchor: finding-commands
    does: 'Commands about the parameter under your mouse, the selected operator or the current network come first.'
  - name: Typo-tolerant search
    anchor: finding-commands
    does: 'Initials, typos, letters in order and British or American spellings all find a command, with strict matches ranked first.'
  - name: Search by what a command does
    anchor: finding-commands
    does: 'A word from a command''s help or its tool''s documentation finds it, so `copy` finds PasteFromClipboard, and the row says why it matched.'
  - name: Actions first for words like copy
    anchor: action-words
    does: 'A word that starts command titles, such as copy, open or reset, lists the commands that start with it first, then components named with it.'
  - name: Scoping prefixes
    anchor: prefixes
    does: 'A leading character narrows the list to commands, tool commands, components or one tool''s commands.'
  - name: Navigate the network
    anchor: prefixes
    does: '`/` is the root, `./` where you came from and each `..` a level up; Right drills into a row and Left backs out.'
  - name: Step through a command's values
    anchor: values-and-presets
    does: 'A command that takes values asks for them one at a time: a menu as pick rows, anything else as a field naming its type and default.'
  - name: Presets that run on Enter
    anchor: presets
    does: '`Alt+S` saves a command with its values as a preset row, which runs on Enter without prompting.'
  - name: Place palette components
    anchor: placing-palette-components
    does: 'TouchDesigner''s palette components, your own folders included, land on your mouse ready to place, or drag into any pane.'
  - name: Stars and hidden commands
    anchor: shaping-the-list
    does: 'Star commands with `Ctrl+D` to lead their tier, and hide the ones you never use with `Ctrl+H`.'
  - name: Rank by usage
    anchor: shaping-the-list
    does: 'Commands you run often rank higher, the lift fading over a couple of weeks unused; Rank By Usage switches it off.'
  - name: Query history
    anchor: how-to-use-it
    does: '`Alt+Up` and `Alt+Down` cycle through the queries you have run before.'
  - name: Commands tab in Hub
    anchor: shaping-the-list
    does: 'Every registered command, hidden ones included, with Star and Hidden toggles shared with TDX Launcher Ultra.'
  - name: Install from the palette
    anchor: shaping-the-list
    does: A tool you can install but have not yet shows as an Install row; Enter installs it.
  - name: Call extension methods
    anchor: calling-extension-methods
    does: '`~` lists the public methods of a COMP''s extensions and calls them with the arguments you type.'
    authors: true
---

## Why use it

A project with a good set of tools installed has more actions than anyone can
keep on keys. FNS tools declare dozens of commands, TouchDesigner has its own
dialogs and menu items, and the Palette Browser holds a long list of
components. Each lives somewhere else: a toolbar button, a right-click menu, a
hotkey you set months ago, a palette folder you scroll through.

CommandPalette puts them behind one key. Press `Ctrl+Shift+P`, type a few
letters of what you want, press Enter. The list holds every command your FNS
tools declare, TouchDesigner's built-in commands and its palette components,
and it is ranked by what you were looking at when you pressed the key: a
command about the parameter under your mouse comes before one about the whole
network.

## How to use it

1. Press `Ctrl+Shift+P`. A small window opens over the network you are in:
   one input, a ranked list, and a footer that always says what Enter will do
   to the row you are on.
2. Type to filter. Up and Down move through the list, Enter or a click acts,
   and Esc closes the window. Clicking anywhere else closes it too.
3. A command that takes values asks for them one at a time
   ([Values and presets](#values-and-presets)). A palette component lands on
   your mouse, ready to click into place
   ([Placing palette components](#placing-palette-components)).

With nothing typed, the footer shows the [prefixes](#prefixes) that narrow the
list, such as `>` for commands only and `/` to browse the network.

Once the palette is part of your day:

- To keep a command you use all the time at the top, select it and press
  `Ctrl+D` to star it.
- To get a command you never use out of the way, press `Ctrl+H` to hide it.
  The Commands tab in Hub can show it again.
- To repeat a search, `Alt+Up` and `Alt+Down` cycle through the queries you
  have run before.
- To turn a command and its values into a single row, save it as a preset with
  `Alt+S`.
- Right-click a row for its menu: Run, Star or Unstar, Hide (Delete preset on a
  preset) and, with [RadialMenu](/docs/fns-radialmenu/) installed, Add to
  radial menu, which puts the command in the first empty slot of the radial
  menu's main wheel.
- To open the palette with another key, rebind **Hotkey** in
  [HotkeyManager](/docs/fns-hotkeymanager/), which lists it and checks it for
  conflicts. **Justify and Offset To...** and the other window placement
  parameters on the same page decide which display the window opens on.

## Finding commands

### What comes first

Before its own window takes focus, the palette takes a snapshot of where you
were. A command whose context that snapshot satisfies ranks first, most
specific first:

1. a command about the parameter under your mouse,
2. one about the current or selected operator,
3. one about the network,
4. general commands,
5. components.

A command whose context is missing is dimmed and refused. Badges are coloured
by kind, and context commands carry a small `par`, `op` or `net` tag, so you
can see why a row sits where it does.

### How typed words match

Once you type, your words decide the order and the context only breaks ties.
Every word must hit, and each hit is read as strictly as it can be. From
strictest to loosest:

1. the whole title, its start, the start of a word in it, anywhere in it;
2. initials (`mfo`);
3. a typo of a word (`opne ext`, `nosie`): one slip for words of four to seven
   letters, two from eight;
4. the letters in order (`tmln`).

Spellings either side of the Atlantic are the same word, so `randomise` finds
Randomize. A hit in the title ranks above the same hit in a tool name, and a
component's file path only counts when the word is literally in it. The
letters-in-order reading only fills the list when nothing matched more
strictly, so `delete` does not turn up a component whose long name happens to
hold those letters.

### Searching by what a command does

A command also answers to what it does. A word of three letters or more that
starts a word of its help line, of its tool's description or of the main words
of its tool's documentation finds it, ranked under the same word in a title or
tool name. `copy` finds PasteFromClipboard, `bookmark` finds QuickMarks. Such a
row says why it is there (`in docs: copy`, `in help: image`). A documentation
word belongs to the whole tool, so at most two commands of one tool are listed
for it.

The description and documentation words come from the store manifest that
[Updater](/docs/fns-updater/) downloads, so they are there once the updater
has checked the store at least once.

### Action words

Some words ask for something to do: `copy`, `open`, `reset`. The palette
learns them from the commands themselves. A word counts as an action when it
starts a command title (`Copy op path`, `Open Errors`) and also starts a help
line, or appears as copied, saving or tapped somewhere in the help and docs.
For an action word the list runs:

1. commands that start with it,
2. components named with it (`copy` lists Copy op path above CopyPars),
3. commands whose help or docs use it,
4. last, a title that only holds it as a thing (`Floating copy of pane`).

A component answers to an action word only through a strict hit, never by a
typo or letters in order, and `copy` also finds a help line that says copies or
copied. A word you are still typing (`cop`) only counts as an action once it is
whole. Every other word ranks as described above, and a new tool's commands
teach the palette new action words.

### Words that mean the same

A few words are treated as the same, and any of them finds the others in a
command title:

- add and install; remove and delete; open, show and view;
- randomize, scramble and shuffle; restore and revert; quit and exit; create
  and new; load and import;
- TouchDesigner's short names: op and operator, par and parameter, comp and
  component, plurals too.

`delete family` finds Remove Operator Family, `view bookmarks` finds Open
Bookmarks and `hovered parameter` finds LFO on hovered par. Such a row says why
(`delete as remove`) and ranks below every title holding the word you typed,
above help and docs hits. Only whole words count, so `ad` and `inst` match the
way any partial word does.

## Prefixes

A leading character scopes the query. With nothing typed, the footer shows
them.

| Prefix | Scope |
|---|---|
| `>` | Commands only: your tools' commands first, then TouchDesigner's own built-in commands, badged `TD` |
| `?` | Tool commands only, built-ins left out |
| `=` | Components only |
| `/`, `./`, `../` | Navigate the network: `/` is the root, `.` or `./` is where you came from, each `..` goes up a level |
| `~` | Public methods of the promoted extensions on the selected COMP, else the current one, else the network you came from ([Calling extension methods](#calling-extension-methods)) |
| `#` | One tool's commands: `#` lists the tools, `#QuickMarks ` lists that tool's commands |

Navigation and tool rows drill in with Right and back out with Left, keeping
whichever convention you are typing in. After `#`, a word that is not in any
tool's name finds the tools whose description or documentation has it, as in
`#copy`.

## Values and presets

Enter on a command that declares parameters walks them one at a time. A menu
parameter becomes pick rows filtered as you type; anything else gets a text
field whose placeholder names the parameter, its type and its default. Enter
accepts (empty keeps the default), Left steps back a parameter, Esc backs out
to the list.

### Presets

For a command you run with the same values again and again, save a preset.
Select the command and press `Alt+S` to save it under a name of your own. Press
it in the middle of a parameter walk and the values entered so far are baked
in, the rest taking their defaults, so `Set volume` with `level=0.5` becomes a
one-keystroke row.

- A preset shows a `PRESET` badge and ranks just above the command it wraps.
- Enter runs it without prompting.
- It can be starred.
- It still runs when its command is hidden, since saving it was the opt-in.
- `Ctrl+H` on a preset deletes it.

### Tools with several copies

When a tool is placed more than once, each copy's commands carry its label, as
in `Freeze scope · Main out` and `Freeze scope · Preview`, and the label is
searchable. A preset saved from one of those rows runs on that copy only; a
preset over the command itself lists once per copy. Stars and hidden flags
cover the command on every copy.

## Placing palette components

TouchDesigner's palette components are rows like any other, tagged `TOX`. They
are read from the Palette Browser's model, so your own palette folders are in
the list too. Type `=` first to see components only.

- Choose one with Enter or a click and it loads into the network the palette
  was opened over and is handed to your mouse, the way the OP Create dialog
  hands you a new operator: move it where you want and click to place it. If
  that pane has moved on to another network, the component stays to the right
  of everything in the network it loaded into, selected.
- Or press a row and drag it into any network pane, the gesture TouchDesigner's
  own Palette Browser uses.

Derivative's built-in components ship as bundles, with the component, its icon
and its help text in one wrapper. The palette unwraps them either way, so what
lands in your network is the component itself.

## Shaping the list

Starred rows (`Ctrl+D`, on a command or a component) lead within their tier,
and a hidden command (`Ctrl+H`) stays out of the palette until the Commands tab
shows it again. Two more things decide what the list offers:

- **Usage.** Commands you run often rank higher. The lift fades over a couple
  of weeks of not using a command, and it only breaks ties between similar
  matches: a better match or a starred row still wins. Runs from TDX Launcher
  Ultra's quick launch count too. Switch off **Rank By Usage** to stop it; your
  runs are still recorded, so switching it back on picks up where you left off.
- **Only what can run.** A tool that is bypassed or has cooking off does not
  offer its commands until it is back on. A tool you can install that is not in
  the project yet shows as an install row (Install QuickMarks, for example)
  with an `INSTALL` badge. Enter installs it, downloading it first when needed.

### The Commands tab

The palette adds a **Commands** tab to [Hub](/docs/fns-hub/). It lists every
registered command, hidden ones included, with its tool and context;
TouchDesigner's built-in commands show `built-in` in the Context cell.

- Click **Star** to star a command and **Hidden** to hide or show it. Your
  choice beats the tool's own default in both directions.
- A filter field narrows the list, Refresh rebuilds it, and Open palette does
  what the hotkey does.
- Clear usage forgets the palette's run history. The launcher's history still
  counts until you clear it there.

### Where your choices are kept

Stars, hidden commands and presets are keyed by tool name and command id, the
same identity [TDX Launcher Ultra](https://launcher.functionstore.xyz) uses, so
they survive a tool moving in the network. They live in one machine-wide file
that this palette and the launcher both read and write: a star in one is a
star in the other, in every project on the machine, whatever config scope the
project uses.

The query history is kept per consumer. It persists through
[ConfigRegistry](/docs/fns-configregistry/), so under global scope it follows
you between projects and under project scope it stays in the `.toe`.

## Calling extension methods

For tool authors, `~` gives you a way to call into an extension while you
build it, from the network you are in. It lists the public methods of the
promoted extensions on the selected COMP, else the current one, else the
network you came from.

- **Methods complete before they run.** Enter, a click or Right on a method row
  fills the input with, say, `~SetLevel ` and leaves the palette open for the
  arguments. Enter again calls it. Tab only ever completes, never runs, and the
  footer shows what it would give you.
- **Missing arguments are refused.** A method whose required arguments are
  still missing does not run, and the footer says how many it needs.
- **Scope to one extension.** `~ext.` lists the extensions on the subject COMP,
  and `~ext.MyExt.` or the shorter `~MyExt.` lists that one's members.

A plain `~Method` row runs through the COMP, so it offers what the COMP itself
exposes. Addressed through an extension, the list is everything not starting
with an underscore, lowercase members included: reaching a member through
`.ext.MyExt` does not require it to be promoted, so the lowercase wiring tier
is callable here even though the COMP does not expose it. The name is the
Extension Name parameter when one is set and the class name when it is not,
which is what `.ext.` resolves by either way.

## How the pieces fit

This palette is one of two consumers of a four-piece system. It gets its list
from the registry and hands a chosen command back to the registry to run, and
tools declare their commands there without knowing this palette exists.

| Piece | Role | Where it lives |
|---|---|---|
| **CommandPalette** (this page) | A consumer inside TouchDesigner: a hotkey, a ranked list, Enter runs the command | Installed like any tool |
| [CommandRegistry](/docs/fns-commandregistry/) | Collects every command tools declare, plus TouchDesigner's own, and serves one list to whatever can run them | A core package promoted to `/sys`, installed with the toolkit's core; the launcher's companion carries the same copy |
| [CommandKit](/docs/fns-commandkit/) | Lets any component of your own publish commands: mark a method, or declare a spec | A direct child of that component. FNS tools carry the same module in their ExtUtils and announce themselves, so they never need the kit |
| [TDX Launcher Ultra](https://launcher.functionstore.xyz) | The other consumer, outside TouchDesigner: its tray palette lists the same commands under `>` and `?` and runs them in the session you summoned it over | A separate desktop app with its own releases |

Without the registry the palette still opens and still places TouchDesigner's
palette components, with no tool commands to list. A component of your own
that carries CommandKit shows its commands here and in the launcher like any
FNS tool. The two consumers share stars, hidden commands and presets
([Where your choices are kept](#where-your-choices-are-kept)), and the
[Commands tab](#the-commands-tab) in Hub is where that curation is managed from
inside TouchDesigner.
