---
package: FNS_CommandPalette
summary: 'A command palette inside TouchDesigner: every command your FNS tools declare, plus TouchDesigner''s own palette components, ranked by what you are looking at.'
features:
  - name: CommandPalette
    anchor: commandpalette
  - name: How the pieces fit
    anchor: how-the-command-pieces-fit
  - name: Prefixes
    anchor: prefixes
  - name: Commands tab
    anchor: commands-tab
  - name: Hotkey and persistence
    anchor: hotkey-and-persistence
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
  - name: Palette over the current network
    anchor: commandpalette
    does: 'Opens a small window over the network you are in with one input, a ranked list and a footer saying what Enter will do.'
  - name: Context-aware ranking
    anchor: commandpalette
    does: 'Commands whose context matches where you were rank first: the parameter under the mouse, then the current or selected operator, then the network.'
  - name: Typo-tolerant word matching
    anchor: commandpalette
    does: 'Every typed word must hit; strict matches rank first, then initials, typos and letters in order, with British and American spellings treated alike.'
  - name: Find a command by what it does
    anchor: commandpalette
    does: 'A word also matches a command''s help line and its tool''s description and documentation, so copy finds PasteFromClipboard, and the row says why it matched.'
  - name: Step through command parameters
    anchor: commandpalette
    does: 'Enter on a command that declares parameters walks them one at a time, as filtered pick rows for menus or text fields showing type and default.'
  - name: Place palette components
    anchor: palette-components
    does: 'TouchDesigner''s palette components, your own folders included, load into the network attached to the mouse for placing, or can be dragged into any pane.'
  - name: Scoping prefixes
    anchor: prefixes
    does: 'A leading character scopes the list: `>` for commands with TouchDesigner built-ins, `?` for tool commands, `=` for components, `#` for one tool''s commands.'
  - name: Navigate the network
    anchor: prefixes
    does: 'Typing `/`, `./` or `../` browses networks from the root, from where you came, or up a level, drilling in with Right and out with Left.'
  - name: Stars and hidden commands
    anchor: prefixes
    does: 'Ctrl+D stars a command or component so it leads its tier; Ctrl+H hides a command, which the Commands tab can show again.'
  - name: Query history
    anchor: prefixes
    does: Alt+Up and Alt+Down cycle through the queries you have run before.
  - name: Install tools from the palette
    anchor: prefixes
    does: 'A tool not in the project but installable shows as an Install entry; Enter installs it, downloading it first when needed.'
  - name: Rank by usage
    anchor: prefixes
    does: 'Commands you run often rank higher, the lift fading over a couple of weeks unused and only breaking ties; launcher quick-launch runs count too.'
  - name: Command presets
    anchor: prefixes
    does: 'Alt+S saves a command, with any parameter values entered so far, as a named preset that runs on Enter without prompting.'
  - name: Commands per tool copy
    anchor: prefixes
    does: 'When a tool is placed more than once, each copy''s commands carry its searchable label, and a preset saved from one runs on that copy only.'
  - name: Commands tab in Hub
    anchor: commands-tab
    does: 'Lists every registered command, hidden ones included, with Star and Hidden toggles, a filter, Refresh, Open palette and Clear usage.'
  - name: Rebindable hotkey and roaming favourites
    anchor: hotkey-and-persistence
    does: 'The hotkey is managed in HotkeyManager, and favourites, presets, hidden commands and history persist through ConfigRegistry globally or per project.'
  - name: Call extension methods
    anchor: prefixes
    does: 'The `~` prefix lists public methods of promoted extensions on the subject COMP, completes them in the input and calls them with typed arguments.'
    authors: true
---

## CommandPalette

Press the hotkey (`ctrl.shift.p` by default) and a small window opens over the
network you are in: one input, a ranked list, and a footer that always says
what Enter will do to the row you are on. Type to filter, Up and Down to move,
Enter or a click to act, Esc to close. Clicking anywhere else closes it too.

The list is fed by [CommandRegistry](/docs/fns-commandregistry/): every
command any installed FNS tool declares, without the tools knowing this
palette exists. A component of your own publishes its commands the same way
by carrying [CommandKit](/docs/fns-commandkit/), and
[TDX Launcher Ultra](https://launcher.functionstore.xyz) lists the same
commands outside TouchDesigner; [how the pieces fit](#how-the-command-pieces-fit)
is below. TouchDesigner's own palette components are in the same list,
read from the Palette Browser's model, so your own palette folders are
included; Enter on one places it into the network you came from, right of
everything and selected.

Ranking cares about **where you were when you opened it**. The palette takes a
snapshot of your context before its window can take focus, and a command
whose context that snapshot satisfies ranks first, most specific first: a
command about the parameter under your mouse, then one about the current or
selected operator, then one about the network, then general commands, then
components. A command whose context is missing is dimmed and
refused. Badges are coloured by kind, and context commands carry
a small `par` / `op` / `net` tag so the reason for a row's rank is visible.

Once you type, the words you typed decide the order and the context only
breaks ties. Every word must hit, and a hit is read as strictly as it can be:
the whole title, its start, the start of a word in it, anywhere in it, then
the looser readings that only fill in below those, initials (`mfo`), a typo
of a word (`opne ext`, `nosie`; one slip for words of four to seven letters,
two from eight) and last the letters in order (`tmln`). Spellings either side
of the Atlantic are the same word (`randomise` finds Randomize). A hit in the
title ranks above the same hit in a tool name, and the file path of a
component only counts when the word is literally in it. The letters-in-order
reading only fills the list when nothing matched more strictly, so `delete`
is not answered by a component whose long name happens to hold those letters.

A command also answers to **what it does**: a word of three letters or more
that starts a word of its help line, of its tool's description or of the
main words of its tool's documentation finds it, ranked under the same word
in a title or tool name. `copy` finds PasteFromClipboard, `bookmark` finds
QuickMarks. Such a row says why it is there (`in docs: copy`, `in help:
image`), and at most two commands of one tool are listed for a documentation
word, since that word belongs to the whole tool. The description and
documentation words come from the store manifest the updater downloads, so
they are there once the updater has checked the store at least once.

Enter on a command that declares parameters walks them one at a time. A menu parameter becomes pick rows filtered as you type, the rest a
text field whose placeholder names the parameter, its type and its default.
Enter accepts (empty keeps the default), Left steps back a parameter, Esc
backs out to the list.

### Palette components

TouchDesigner's own palette components are rows like any other, tagged `TOX`. Choosing one (Enter, or a click) loads it into the network the palette was opened over and **hands it to your mouse**, exactly like a new operator from the OP Create dialog: move it where you want and click to place. You can also **press a row and drag it** into any network pane, the gesture TouchDesigner's own Palette browser uses. Derivative's built-in components ship as bundles (the component, its icon and its help text in one wrapper); the palette unwraps them either way, so what lands in your network is the component itself.

## How the command pieces fit

This palette is one of two consumers of a four-piece system. It never talks
to a tool directly: it asks the registry for the list and hands a chosen
command back to it to run.

| Piece | Role | Where it lives |
|---|---|---|
| **CommandPalette** (this page) | A consumer inside TouchDesigner: a hotkey, a ranked list, Enter runs the command | Installed like any tool |
| [CommandRegistry](/docs/fns-commandregistry/) | Collects every command tools declare, plus TouchDesigner's own, and serves one list to whatever can run them | A core package promoted to `/sys`, installed with the toolkit's core; the launcher's companion carries the same copy |
| [CommandKit](/docs/fns-commandkit/) | Lets any component of your own publish commands: mark a method, or declare a spec | A direct child of that component. FNS tools carry the same module in their ExtUtils and announce themselves, so they never need the kit |
| [TDX Launcher Ultra](https://launcher.functionstore.xyz) | The other consumer, outside TouchDesigner: its tray palette lists the same commands under `>` and `?` and runs them in the session you summoned it over | A separate desktop app with its own releases |

Without the registry the palette still opens and still places
TouchDesigner's palette components, with no tool commands to list. Favourites,
hidden commands and presets are one machine-wide file that this palette and
the launcher both read and write, keyed by tool name and command id, so a
star in one is a star in the other; the query history stays per consumer.
The [Commands tab](#commands-tab) in Hub is where that curation is managed
from inside TouchDesigner.

## Prefixes

A leading character scopes the query. With nothing typed the footer shows
them.

| Prefix | Scope |
|---|---|
| `>` | Commands only: your tools' commands first, then TouchDesigner's own built-in commands, badged `TD` |
| `?` | Tool commands only, built-ins left out |
| `=` | Components only |
| `/`, `./`, `../` | Navigate the network: `/` is the root, `.` or `./` is where you came from, each `..` goes up a level |
| `~` | Public methods of the promoted extensions on the selected COMP, else the current one, else the network you came from |
| `#` | One tool's commands: `#` lists the tools, `#QuickMarks ` lists that tool's commands. A word that is not in a tool's name finds the tools whose description or documentation has it: `#copy` |

Navigation and tool rows drill in with Right and back out with Left, keeping
whichever convention you are typing in.

**Methods complete before they run.** Enter (or a click, or Right) on a method
row fills the input with `~SetLevel ` and leaves the palette open, so you can
type the arguments; Enter again calls it. **Tab** only ever completes, never
runs, and the footer shows what it would give you.

**Scope to one extension.** `~ext.` lists the extensions on the subject COMP,
and `~ext.MyExt.` or the shorter `~MyExt.` lists that one's members. Addressed
this way the list is everything not starting with an underscore, lowercase
members included: reaching a member through `.ext.MyExt` does not require it to
be promoted, so the lowercase wiring tier is callable here even though the COMP
does not expose it. The name is the Extension Name parameter when one is set and
the class name when it is not, which is what `.ext.` resolves by either way. A method runs through the COMP, so the palette can only
call what the COMP itself exposes, and one whose required arguments are still
missing is refused with the footer saying how many it needs.

Ctrl+D stars the selected command or component; starred rows lead within
their tier. Ctrl+H hides the selected command from the palette; the Commands
tab shows it again. Alt+Up and Alt+Down cycle the queries you have run
before.

Right-click a row for its menu: Run, Star or Unstar, Hide (Delete preset on
a preset), and, with FNS_RadialMenu installed, Add to radial menu, which puts
the command in the first empty slot of the radial menu's main wheel.

**Only what can run.** A tool that is bypassed or has cooking off does not
offer its commands until it is back on. A tool that is not in the project but
that you can install shows as **Install <tool>** with an `INSTALL` badge;
Enter installs it, downloading it first when needed.

**Rank by usage.** Commands you run often rank higher, on by default. The
lift fades over a couple of weeks of not using a command, and it only breaks
ties between similar matches: a better match or a starred row still wins.
Runs from the TDXLU launcher's quick launch count too. Turn it off with
**Rank By Usage** on the tool's Palette page; your runs are still recorded,
so turning it back on picks up where you left off.

**Presets.** Alt+S saves the selected command under a name of your own. Press
it in the middle of a parameter walk and the values entered so far are baked
in, the rest taking their defaults, so `Set volume` with `level=0.5` becomes a
one-keystroke row. Presets show a `PRESET` badge, rank just above the command
they wrap, run on Enter without prompting, and can be starred. A preset over a
hidden command still runs, since saving it was the opt-in. Ctrl+H on a preset
deletes it.

**Tools with several copies.** When a tool is placed more than once, each
copy's commands carry its label, as in `Freeze scope · Main out` and
`Freeze scope · Preview`, and the label is searchable. A preset saved from one
of those rows runs on that copy only; a preset over the command itself lists
once per copy. Stars and hidden flags cover the command on every copy.

## Commands tab

The palette contributes a **Commands** tab to [Hub](/docs/fns-hub/):
every registered command, hidden ones included, with its tool and context.
Click **Star** to star it and **Hidden** to hide or show it; your choice
beats the tool's own default in both directions. A filter field narrows the
list, Refresh rebuilds it, and Open palette does what the hotkey does. Clear
usage forgets the palette's run history; the launcher's history still counts
until you clear it there.
TouchDesigner's built-in commands show `built-in` in their Context cell.

## Hotkey and persistence

The hotkey lives on the tool's `Hotkey` parameter, so
[HotkeyManager](/docs/fns-hotkeymanager/) lists it, checks it for
conflicts and rebinds it. Which display the window opens on is set by the
window placement parameters on the same page.

Favourites, presets and hidden commands are keyed by tool and command id,
the same identity the launcher's tray app uses, so they survive a tool moving
in the network. They and the query history persist through
[ConfigRegistry](/docs/fns-configregistry/), so under global scope they
follow you between projects and under project scope they stay in the `.toe`.
