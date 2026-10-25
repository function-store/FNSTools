---
package: FNS_ConfigHost
summary: 'A standalone ConfigRegistry host: drop it into a component to give that component roaming settings.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Choosing the canonical name
    anchor: choosing-the-canonical-name
  - name: Roaming or per project
    anchor: roaming-or-per-project
  - name: Saving more than parameters
    anchor: saving-more-than-parameters
feature_list:
  - name: Roaming settings for any component
    anchor: how-to-use-it
    does: Drop it inside a component and that component's custom parameters are written into the shared settings file and restored on load.
  - name: Parameter and page exclusions
    anchor: how-to-use-it
    does: 'Name patterns, or whole parameter pages, stay out of what is saved, for parameters that must boot at their defaults.'
  - name: Registry page on the parent
    anchor: how-to-use-it
    does: 'The host''s key settings are mirrored onto the component as a Registry page, so it can be configured without opening the host.'
  - name: Edit on the settings page
    anchor: how-to-use-it
    does: 'With the toolkit installed, the component is listed on the FNS settings page beside every FNS tool, its parameters editable there.'
  - name: Named settings section
    anchor: choosing-the-canonical-name
    does: 'The canonical name is the section the settings are stored under, defaulting to the component''s name; renaming it orphans values saved under the old name.'
  - name: Global or per project
    anchor: roaming-or-per-project
    does: 'Follows the toolkit''s choice between one settings file shared by every project and settings kept in the .toe.'
  - name: Save and load callbacks
    anchor: saving-more-than-parameters
    does: 'onConfigSave and onConfigLoad save and restore anything JSON-serializable, such as table rows; a pulse writes the starter DAT.'
    authors: true
---

## Why use it

Say you built a component of your own, a MIDI mapper or a library of looks,
and you want the way you set it up to follow you into the next project.
TouchDesigner keeps its parameters in the `.toe`, so the usual answer is to
write your own save and load: a JSON file somewhere, code that decides when
to write it, and more code that puts the values back once the component has
finished initialising. Every component that does this ends up with its own
file and its own rules.

Every FNS tool that remembers its settings does so by carrying a small
**ConfigRegistry host**. This is that host on its own, so a component
outside the toolkit can have the same thing: its parameters are written into
the shared settings file and restored on load.

If you find an `FNS_ConfigHost` inside a component someone gave you, this is
what makes that component remember its settings.

## How to use it

1. Drag the COMP inside the component whose settings should roam. **Tool
   COMP** points at its parent by default, so it saves the component it sits
   in.
2. Give it a **Canonical Name**, the section its settings are stored under.
   Left empty, it uses the component's name. Choose it with care, see
   [below](#choosing-the-canonical-name).
3. Make sure **Auto-register** is on, so the component stays published while
   it exists, and **Auto-load**, so saved values come back when it registers.
4. Save the project. The component's custom parameters are written into the
   settings file, and in another project the same component gets them back
   shortly after it registers.

A few things people commonly adjust:

- **Parameters that must boot at their defaults**, an output toggle for
  example: list them in **Exclude Pars** as name patterns, like
  `Spoutactive Ndi*`, or leave whole pages out with **Exclude Pages**.
- **Configuring it from the component:** with **Promote Parameters** on, the
  host mirrors its key parameters onto the parent as a bound **Registry**
  page, so it can be configured without opening the host. Turn it off before
  shipping a tool that should not expose registry controls.
- **Editing the values from one page:** with the toolkit installed, the
  component is listed on the settings page (**Open FNS settings** in
  quick-launch) beside every FNS tool.

The host carries the same code as [ConfigRegistry](/docs/fns-configregistry/),
the registry that owns the settings file. Every copy forwards to one global
registry in `/sys`, `op.FNS_CONFIGREGISTRY`; if there is none yet, the first
copy to start becomes it.

## Choosing the canonical name

**Canonical Name is the key your settings are stored under.** Renaming it
orphans everything saved under the old name; the values remain in the file,
but the component stops seeing them. Choose it once, and pick a name no other
tool uses: the file holds one section per name.

## Roaming or per project

ConfigRegistry's scope decides whether settings roam across all your projects
or stay with one. The host's **Config Scope** follows the toolkit root's: in
global scope your component's section goes into the one file every project
on the machine shares, in project scope it stays in the `.toe`. In a project
without the toolkit root it reads project, so the settings are kept with that
project file. The [ConfigRegistry page](/docs/fns-configregistry/) has the
details.

## Saving more than parameters

Custom parameters are saved for you. State that lives outside parameters,
such as the rows of a table or a dict in storage, needs a callback:

1. Pulse **Create Callbacks**. It puts a `config_callbacks` DAT into your
   component from the registry's template and points **Callback DAT** at it.
   Pulsing it again adopts the existing DAT and never overwrites it.
2. Fill in the two functions. Both are optional; the registry uses what it
   finds.

```python
def onConfigSave():
	# keep the rows of a table that is not a parameter
	return {'rows': [[c.val for c in r] for r in me.parent().op('my_table').rows()]}

def onConfigLoad(data):
	t = me.parent().op('my_table')
	t.clear()
	for r in data.get('rows', []):
		t.appendRow(r)
```

- `onConfigSave()` returns a JSON-serializable dict (strings, numbers,
  booleans, `None`, lists and dicts), stored under your component's `state`
  key in the file. Return `{}` to save nothing extra. It runs on every save:
  the project's pre-save, the **Save All Now** pulse, and right before the
  updater replaces the toolkit.
- `onConfigLoad(data)` receives exactly what `onConfigSave` returned. It runs
  once per session after the component registers, with **Auto-load** on, and
  after the parameters have been applied; an explicit Load All runs it again.
- `me` is the callbacks DAT, so `me.parent()` is your component. Resolve
  everything from there, never from an absolute path or a global shortcut.
- A hook that raises is contained: the registry reports it with `debug()`,
  skips that state, and the file stays intact.
