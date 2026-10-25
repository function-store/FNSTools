---
package: FNS_OpTemplates
summary: Keep your own versions of operators, chains and small networks, and put one down whenever you create that operator type.
features:
  - name: Why use it
    anchor: why-use-it
    icon: OpTemplates.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Building templates
    anchor: building-templates
  - name: Whole networks as templates
    anchor: whole-networks-as-templates
  - name: Placing into a connection
    anchor: placing-into-a-connection
  - name: Where your library lives
    anchor: where-your-library-lives
  - name: Upgrading from an older FNSTools
    anchor: upgrading-from-an-older-fnstools
  - name: Known issues
    anchor: known-issues
feature_list:
  - name: Template by drag and drop
    anchor: how-to-use-it
    does: Drop an operator set up the way you like onto the toolbar icon and it becomes a template for its type.
  - name: Place a template on create
    anchor: how-to-use-it
    does: 'Hold the alternatives shortcut (`Ctrl+Alt` by default) while placing an operator marked >>> in the OP Create dialog, and your template goes down in its place with the wiring kept.'
  - name: Variants of one operator type
    anchor: building-templates
    does: Keep as many named variants of one operator type as you like and pick one from a menu as you place it.
  - name: Operator chains as templates
    anchor: building-templates
    does: 'Operators wired after the template operator are placed together with it, such as the shipped LFO, Math and Null.'
  - name: Network snippets as templates
    anchor: whole-networks-as-templates
    does: 'A Base COMP in the type''s template holds a whole network, such as a Render TOP with its geometry, camera and light, placed as one template.'
  - name: Substitute a COMP for the operator
    anchor: whole-networks-as-templates
    does: 'A Base COMP inside a snippet''s Base COMP makes the template land as that COMP.'
  - name: Insert into a connection
    anchor: placing-into-a-connection
    does: 'Templates, chains and networks drop into an existing wire, with In and Out operators marking where a network connects.'
  - name: Shared alternatives menu
    anchor: how-to-use-it
    does: 'Other tools that offer themselves for the same operator type are listed beside your templates, with tools from your store below a divider.'
  - name: Global or per-project library
    anchor: where-your-library-lives
    does: 'Keep one library for every project on the machine or one inside the project file, or follow the toolkit''s Config Scope.'
  - name: Push project templates to global
    anchor: where-your-library-lives
    does: 'Push To Global copies the project set to the global file whenever you like, asking first when the file exists.'
  - name: Save the templates
    anchor: where-your-library-lives
    does: 'Under global scope, middle-click the toolbar icon or press Save Templates; under project scope, saving the project saves them.'
  - name: Open the library
    anchor: how-to-use-it
    does: 'Left-click the toolbar icon, or run Open templates from quick-launch, to browse or edit the library in a floating network editor.'
  - name: Edit one type's templates
    anchor: how-to-use-it
    does: 'Right-click a type in the OP Create dialog and pick Edit Templates... to work on its templates.'
  - name: Starter set
    anchor: why-use-it
    does: Ships with templates for 18 operator types to start from.
  - name: Library kept across upgrades
    anchor: upgrading-from-an-older-fnstools
    does: 'On the first start after an upgrade it finds the newest library you saved under an older name, and keeps the file it replaces beside it.'
---

## Why use it

Most operators get the same first edits every time you create them. A Noise
TOP gets its resolution and period changed, an LFO CHOP gets a Math and a Null
after it, a Trigger CHOP gets the envelope you always use. A Render TOP is the
worst case: it does nothing until you have also made a Geometry COMP, a camera
and a light and wired them in. TouchDesigner starts you from factory defaults
every time, so you redo that work, or keep a stash of components around to
copy from.

OpTemplates keeps your versions. Store an operator, a chain or a small network
as a template for its type, and the next time you create that type with the
alternatives shortcut held, your template is put down in its place, wired the
way the new operator was. It ships with a starter set for 18 operator types,
the Render TOP among them.

## How to use it

1. Set an operator up the way you want new ones to start, and drag it onto the
   ![](/docs/assets/icons/OpTemplates.png) icon in the toolbar. It is stored
   as a template for its type.
2. Middle-click the icon to save the templates. It asks first, because saving
   overwrites what was saved before.
3. Open the OP Create dialog. Every type that has a template shows `>>>` after
   its name.
4. Click that type to start placing it, then hold `Ctrl+Alt` (`Ctrl+Cmd` on
   macOS) as you click in the network to put it down.
5. With one template for the type, it replaces the new operator straight away.
   With several, a menu lists them by name, each followed by `(OpTemplates)`;
   pick one.

Placing is done by [OpMenuRegistry](/docs/fns-opmenuregistry/), which offers
an alternative for every tool that declares one; OpTemplates hands it your
library. So the menu can hold more than your templates: a tool that offers
itself for the type you are placing is listed beside them, and a tool you
downloaded to your store without installing it is listed below a divider. A
`>>` mark beside a type (where you would expect `>>>`) means its only
alternatives are in the store.

A few things people adjust:

- **Browse or edit the library by hand:** left-click the toolbar icon, or run
  **Open templates** from quick-launch. The library opens in a floating
  network editor. Right-click the icon for the tool's parameters.
- **Work on one type's templates:** right-click the type in the OP Create
  dialog and pick **Edit Templates...**.
- **Throw away edits you have not saved:** press **Refresh Templates**.
- **A different shortcut:** set **Alternatives Shortcut** on the Alternatives
  page of FNS_OpMenuRegistry. OpTemplates' own **Keys** parameter only mirrors
  it and is read-only.

## Building templates

The library holds one Base COMP per operator type, named after the type as
TouchDesigner spells it (its `OPType`): `triggerCHOP` for the Trigger CHOP,
`noiseTOP` for the Noise TOP. Everything inside that Base COMP is a template
for the type. Dropping an operator on the toolbar icon creates it for you,
**Edit Templates...** creates it and opens it, and you can also create and
name one by hand in the library.

- **Several per type.** Put as many operators of the type inside as you like.
  The menu shows each one by its name, so name them for what they are:
  `trigger_decay`, `trigger_sustain`.
- **Chains.** Wire more operators after the template operator and they are
  placed together with it. The shipped LFO CHOP template is an LFO, a Math and
  a Null.
- **Bypass them.** It is worth bypassing template operators, or switching off
  cooking on their Base COMP, to avoid performance issues or errors. Placed
  copies come out un-bypassed with cooking on.

## Whole networks as templates

A snippet is a network placed as one template. Put down a Render TOP and get
the Geometry COMP, camera and light with it, or anything else you build.

1. Inside the type's Base COMP (say `renderTOP`), create another Base COMP.
   Its name is what the menu shows.
2. Build the network inside it. Everything in it is copied out when the
   template is placed.
3. If the snippet should sit in a chain, add an In and an Out operator to its
   Base COMP, wired to the operators that take the incoming and outgoing
   connections. Without them the tool has to guess, and can guess wrong.

To swap the operator for a component, put a Base COMP inside the snippet's
Base COMP: the template then lands as that COMP.

The first operator of a chain or snippet lands where you clicked, and the rest
keeps its layout to the right of it.

## Placing into a connection

Templates, chains and snippets can be placed on their own or inserted into an
existing connection, and the wires are restored onto the template:

- In a snippet with In and Out operators, the incoming wire goes to what the
  In feeds, and the outgoing wire leaves from what feeds the Out.
- Without them, the operator of the placed type that has no inputs takes the
  incoming wire, and the operator at the end of the chain takes the outgoing
  one.
- If a chain has several parallel dead ends, which one becomes the output is
  more or less random. Most templates have one end, so this rarely matters.

## Where your library lives

One library is active at a time, and **Library Scope** says where it lives:

- **Global**, the historical default: one `.tox` in your user palette folder,
  under `FNSTools/OpTemplates/`, shared by every project on this machine.
  Saving writes that file.
- **Project**: a component named `OpTemplatesLibrary` at the network root, next
  to the FNSTools container. It saves with the project file and stays through
  toolkit updates, because it lives outside the tool.
- **Follow config scope**, the default: global or project, whatever the
  toolkit's **Config Scope** says, so a project-scoped install keeps its
  templates in the project with no second decision.

How you save follows the scope. Under global scope, middle-click the toolbar
icon or press **Save Templates**. Under project scope, saving the project
saves the templates.

A library that does not exist yet is created from the set loaded at that
moment; the templates that ship with the tool are only that starting point.
Switching scope never overwrites anything by itself: it loads what is there, or
creates it. Switching from project to global while both a project library and
a global file exist asks what to do with the project set: push it to the
global file, adopt the global set as it is, or stay on project. **Push To
Global** does the same push whenever you like, asking first when the file
exists. That is how a set you built in one project becomes the one every
project loads.

**Templates** shows the library the scope resolved to and is read-only. The
former Advanced mode, where you pointed the tool at any Base COMP in the
project, is retired; a component it pointed at is adopted as the project
library on the first start after upgrading.

## Upgrading from an older FNSTools

Your templates come along on their own. On the first start, the toolkit
renames the old `FNStools_ext` palette folder to `FNSTools`, and OpTemplates
loads your library from `FNSTools/OpTemplates/`. Before it would ever create a
library from the shipped templates, it looks for one you already have and uses
the most recently saved of:

- the `_2023` copy that TouchDesigner 2023 saved to (`OPTemplates1_2023.tox`),
- an `OPTemplates2.tox` or higher, which the old Create New choice made,
- a copy the folder migration set aside in `FNSTools/legacy_FNStools_ext/`.

This check also runs once on a machine that already has a library, so a newer
set saved under one of those names still wins. Whatever it replaces is kept
beside it as `OPTemplates1.before-adopt.tox`, and the textport log names the
file it adopted.

Two older setups are not found automatically, because they left no file:

- **Templates you never saved.** The old tool wrote the palette file only when
  you saved the templates by middle-clicking the toolbar icon. Edits you only
  saved with the project live in that project's copy of OpTemplates.
- **External turned off.** With it off, the templates lived only in the
  project.

For either, open the old project, copy the templates Base COMP out of the old
OpTemplates, and save it as `OPTemplates1.tox` in your palette's
`FNSTools/OpTemplates/` folder (right-click the COMP, Save Component .tox).
Then restart the project.

Since 3.1, placing is done by OpMenuRegistry, so the two packages go together.
OpTemplates 3.1 places nothing under an older OpMenuRegistry, because the
watcher moved out of OpTemplates. OpMenuRegistry is a core package, so a normal
install or update has both. If you had changed **Keys** before upgrading, your
shortcut was carried onto the registry's **Alternatives Shortcut** the first
time the new version started, so it keeps working. Your library files,
**Edit Templates...** and the quick-launch commands work as before.

## Known issues

- Creating an operator by typing its type in full and pressing Enter does not
  give you the chance to place a template.
- Relative operator references in parameters can break because of naming
  conflicts.
- Template libraries saved by versions before 3.1 may carry `TEMPLATE_ROOT`,
  `TEMPLATE_IN` or `TEMPLATE_OUT` tags on their operators, left behind by
  earlier placements. They are harmless and are cleaned off as those templates
  get placed again.
