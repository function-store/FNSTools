---
package: FNS_CommandKit
summary: 'Drop-in kit that lets any component publish commands to every palette that serves them: the CommandPalette inside TouchDesigner and the TDXL launcher''s.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: How the command pieces fit
    anchor: how-the-command-pieces-fit
  - name: Marking methods with the decorator
    anchor: marking-methods-with-the-decorator
  - name: Declaring commands without imports
    anchor: declaring-commands-without-imports
  - name: 'Ids, handlers and limits'
    anchor: ids-handlers-and-limits
  - name: What the kit does on load
    anchor: what-the-kit-does-on-load
  - name: Checking it worked
    anchor: checking-it-worked
feature_list:
  - name: Publish commands from any component
    anchor: how-to-use-it
    does: Drop the kit in as a direct child and the methods you mark appear in the CommandPalette and the TDXL launcher.
    authors: true
  - name: Safe without a registry
    anchor: why-use-it
    does: 'With no command registry in the session nothing happens and nothing errors, so the component works the same for people without the palette.'
    authors: true
  - name: Decorator for command methods
    anchor: marking-methods-with-the-decorator
    does: 'The fns_command decorator derives label, help and prompted parameters from the method name, docstring and signature; Literal hints become menus.'
    authors: true
  - name: 'Context, state and identity options'
    anchor: marking-methods-with-the-decorator
    does: 'Decorator extras set a context for greying out, a live state chip, surface, capability, hidden, and a canonical identity shared across packages.'
    authors: true
  - name: Declare commands without imports
    anchor: declaring-commands-without-imports
    does: 'Promote an FnsCommands() method that returns a spec list, with no imports at all: id, label, method, help, prompted params and every decorator extra as plain dict keys.'
    authors: true
  - name: Announces on load
    anchor: what-the-kit-does-on-load
    does: 'Once the component declares a command the kit tags it and registers it, so a registry that arrives later still finds it; nothing to unregister.'
    authors: true
  - name: Check that commands arrived
    anchor: checking-it-worked
    does: 'Three reads tell you whether your commands are served, and a short ladder says what to look at when one is missing.'
    authors: true
  - name: Announce again after changes
    anchor: how-to-use-it
    does: Call Announce() to republish the component after its command set changes at runtime.
    authors: true
  - name: Tell placed copies apart
    anchor: ids-handlers-and-limits
    does: Promote FnsInstance() and FnsToolName() so palettes distinguish multiple copies and favourites reach all of them (FNS_CommandRegistry 3.2.1 or newer).
    authors: true
---

## Why use it

Say your component has a few actions worth a keystroke: toggle its overlay,
set the tempo, clear a buffer. Today you reach them by opening the component
and hunting for the pulse, or by wiring a Keyboard In CHOP for each one. A
command palette would be quicker, but you would not want your component to
depend on one, or to break for someone who has never installed it.

CommandKit puts your component's commands in every palette that serves the
command registry, the [CommandPalette](/docs/fns-commandpalette/) inside
TouchDesigner and [TDX Launcher Ultra](https://launcher.functionstore.xyz)'s
(`>` / `?` in both), without your component having to know anything about
the registry. Drop this COMP inside your component, mark the methods you want
exposed, and they show up.

It is **guarded throughout**: when no registry is in the session, nothing
happens and nothing errors. A component carrying the kit works exactly the
same for someone who never installs the palette or the launcher.

## How to use it

1. Drag the COMP in as a **direct child** of your component's root.
2. Mark your commands, with the
   [decorator](#marking-methods-with-the-decorator) or with an
   [explicit spec](#declaring-commands-without-imports).
3. That is all. The kit announces your component on load, once you actually
   declare something.
4. Open the palette and type `#` followed by your component's name: its
   commands list under it.

If your command set changes while TouchDesigner is running, call
`op('FNS_CommandKit').Announce()` to publish the new set.

Components inside the FNS toolkit do not need this kit: they carry the same
module in their ExtUtils and announce themselves. This is for everything
else.

## How the command pieces fit

This kit is the authoring half of a four-piece system. The other three are
installed separately, and none of them is required for a component that
carries the kit.

| Piece | Role | Where it lives |
|---|---|---|
| **CommandKit** (this page) | Lets any component publish commands: mark a method, or declare a spec | A direct child of your own component. FNS tools carry the same module in their ExtUtils and announce themselves, so they never need the kit |
| [CommandRegistry](/docs/fns-commandregistry/) | Collects every command tools declare, plus TouchDesigner's own, and serves one list to whatever can run them | A core package promoted to `/sys`, installed with the toolkit's core; the launcher's companion carries the same copy |
| [CommandPalette](/docs/fns-commandpalette/) | A consumer inside TouchDesigner: a hotkey, a ranked list, Enter runs the command | Installed like any tool |
| [TDX Launcher Ultra](https://launcher.functionstore.xyz) | A consumer outside TouchDesigner: its tray palette lists the same commands under `>` and `?` and runs them in the session you summoned it over | A separate desktop app with its own releases |

Your component talks to the registry only, through this kit, and only when
one is present. The consumers read from the registry, so a command you
declare once appears in both without you knowing either exists. Favourites,
hidden commands and presets are one machine-wide file that the palette and
the launcher both read and write, keyed by tool name and command id, so a
star in one is a star in the other; query history stays per consumer.

## Marking methods with the decorator

The decorator derives everything it can from your code:

```python
FNSCommand = op('FNS_CommandKit').mod('FNSCommand')  # import

class MyToolExt:
    @FNSCommand.fns_command(help='Set the project tempo')
    def SetBpm(self, bpm: float = 120, sync: bool = False):
        ...
```

The label comes from the CamelCase name, the help from the docstring's first
line, and the prompted parameters from the signature: type hints become
styles, `typing.Literal[...]` becomes a menu, and a parameter with no default
is required.

Extras: `fns_command(label=…, help=…, hidden=True, params=[…])`, plus:

- `context=`: what the command acts on, so a palette can grey it out when
  that subject is absent;
- `state=`: a live value to show as a chip;
- `surface=` and `capability=`: where and how a consumer may present it;
- `canonical=`: a cross-package identity for a command another package might
  ship too; the newest package wins.

The [registry page](/docs/fns-commandregistry/#what-a-command-carries)
explains each.

## Declaring commands without imports

For a component that would rather not import anything, or whose command set
is built at runtime, promote a `FnsCommands()` method that returns the same
information as a list of dicts. The kit prefers this method when both it and
decorated methods are present.

```python
class MyToolExt:
    def FnsCommands(self):
        return [
            {'id': 'toggle', 'label': 'Toggle overlay',
             'help': 'Show or hide the overlay', 'method': 'Toggle'},
            {'id': 'set_bpm', 'label': 'Set BPM', 'method': 'SetBpm',
             'help': 'Set the project tempo',
             'params': [
                 {'name': 'bpm', 'label': 'BPM', 'style': 'float',
                  'required': True, 'default': 120},
                 {'name': 'sync', 'label': 'Resync clips', 'style': 'toggle',
                  'default': False},
             ]},
        ]

    def Toggle(self): ...
    def SetBpm(self, bpm=120.0, sync=False): ...
```

| Key | Required | Meaning |
|---|---|---|
| `id` | yes | Unique within your component: letters, digits, `_` and `-`, up to 48 characters. Permanent once shipped (see the rules below) |
| `label` | yes | What the user reads, up to 80 characters |
| `method` | yes | A **promoted** (uppercase) method on your component |
| `help` | no | The one-line subtitle under the label |
| `params` | no | The arguments a palette prompts for, in order (table below) |
| `args`, `kwargs` | no | Values baked into every call |
| `hidden` | no | Off the default listings until the user opts in; an advanced command, not a secret |

Every decorator extra is a key here too: `context`, `state`, `surface`,
`capability` and `canonical` take the same values. Do not set `builtin`; it
marks TouchDesigner's own commands.

Each `params` entry describes one keyword argument:

| Key | Required | Meaning |
|---|---|---|
| `name` | yes | The keyword your method receives |
| `style` | no | `str` (default), `int`, `float`, `toggle` or `menu` |
| `label` | no | The prompt's label, defaults to the name |
| `required` | no | Refuse the run when no value arrives |
| `default` | no | Used when the user types nothing |
| `menu` | with `menu` | The legal values, up to 16 |
| `help` | no | A one-line hint shown while prompting |
| `current` | no | Where the live value lives, `'Parname'` or `{'method': 'GetX'}`, so the prompt opens pre-filled |

Values cross as text and arrive at your method coerced to the declared
style; a bad value or a missing required parameter refuses the run before
your method is called.

## Ids, handlers and limits

- **Command ids are permanent.** Favourites, hidden flags and presets in
  both palettes key on `tool#id`, and the id derives from the method name, so
  renaming a shipped method, or the component, orphans all of them. Treat
  every shipped id as public API.
- Handlers run **synchronously on the main thread**. Return quickly and kick
  long work off with `run(..., delayFrames=1)`.
- A handler may return nothing, a JSON-serializable value, or a dict. A dict
  with `ok: False` marks the run failed in the palette's footer; nothing
  raises into the palette.
- Caps: 24 commands per component, 6 parameters per command, 16 entries per
  menu.
- **Placed more than once?** Promote `FnsInstance()` returning a short label
  for each copy, and `FnsToolName()` returning one shared name when the copies'
  COMP names differ. Palettes then tell the copies apart, and favourites reach
  all of them. Needs FNS_CommandRegistry 3.2.1 or newer; older registries
  ignore both.

## What the kit does on load

The kit holds the authoring module (`FNSCommand`), a small announcer and a
README with the same recipe as this page. The announcer looks at the
component it sits in a moment after load. Once that component declares a
command, by decorator or by `FnsCommands()`, the announcer tags it
`fnscommands` and registers it with the registry in the session, if there is
one. The tag is what a registry that arrives later, or is replaced by a newer
version, uses to find your component again, so load order never matters.

A component that declares nothing is left alone: no tag, no registration.
Nothing is unregistered when the component is removed; the registry drops
owners that no longer resolve. Changing the command set while running needs
one call, `op('FNS_CommandKit').Announce()`, which registers the new set in
place of the old.

## Checking it worked

Open the palette and type `#` followed by your component's name: its
commands list under it. Without a palette, three reads from the Textport say
the same:

```python
op.FNS_COMMANDREGISTRY                        # None means no registry in this session
'fnscommands' in op('/path/to/MyTool').tags   # True once the kit has announced it
[c for c in op.FNS_COMMANDREGISTRY.Commands() if c['path'] == op('/path/to/MyTool').path]
```

When a command is missing, look in this order:

1. No registry in the session. Install the toolkit's core, or run the
   launcher, which carries one. Without a registry nothing surfaces, by
   design.
2. The method is not promoted (its name must start with a capital letter),
   or the extension does not compile.
3. The tag is missing: the announcer did not see a command at load. Call
   `op('FNS_CommandKit').Announce()` and read what it returns.
4. The row is there but stale after an edit: `Announce()` again.
   Reinitialising the extension does not re-register on its own.
