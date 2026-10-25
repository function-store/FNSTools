---
package: FNS_CustomParTools
summary: This button is a quick way to manipulate Custom Parameters of a parent component.
features:
  - name: Why use it
    anchor: why-use-it
    icon: CustomParTools.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Promoting parameters
    anchor: promoting-parameters
  - name: CustomParCustomize
    anchor: customparcustomize
  - name: Other button actions
    anchor: other-button-actions
  - name: The path bar
    anchor: the-path-bar
  - name: QuickParCustom
    anchor: quickparcustom
  - name: Parameter and editor hotkeys
    anchor: parameter-and-editor-hotkeys
  - name: QuickExt
    anchor: quickext
  - name: CustomParHelper
    anchor: customparhelper
  - name: NoNode
    anchor: nonode
  - name: Switching parts off
    anchor: switching-parts-off
feature_list:
  - name: Promote by drop
    anchor: promoting-parameters
    does: 'Drop a parameter on the button or on a parent in the path bar and it becomes a custom parameter there, bound back to the original.'
  - name: Customise as you promote
    anchor: customparcustomize
    does: 'Hold `Ctrl` while dropping to set the name, label, range, clamping and default before the parameter is created.'
  - name: Menu parameter from a table
    anchor: promoting-parameters
    does: 'Drop a Table DAT and the parent gets a menu parameter that takes its entries from the table.'
  - name: Promote the hovered parameter
    anchor: quickparcustom
    does: '`Alt+X` promotes the parameter under the mouse and `Alt+\` opens it in the Component Editor, with nothing to select or drag.'
  - name: Clear dangling binds and expressions
    anchor: other-button-actions
    does: 'Switches parameters with a dangling bind or a failing expression back to constant and clears script errors, on the selected COMP and its immediate children.'
  - name: Add a parent shortcut
    anchor: other-button-actions
    does: 'Gives a COMP a parent shortcut from the button or quick-launch, starting from its name or the shortcut it already has.'
  - name: Internal OPs by drop
    anchor: other-button-actions
    does: 'A `Ctrl+Alt` drop adds an operator to the parent, or to a parent in the path bar, as an iop.'
  - name: Open parameters and the Component Editor
    anchor: parameter-and-editor-hotkeys
    does: 'Open the parameter dialog or the Component Editor for the selected operator or the current network''s COMP from the button, the keyboard or quick-launch.'
  - name: Create an extension in one click
    anchor: quickext
    does: 'QuickExt gives a COMP a Python extension with the starting code written, ExtUtils docked and the extension slot filled in.'
  - name: Switch parts off
    anchor: switching-parts-off
    does: 'Each part switches off on its own, and its button or pane-bar widget goes away with it.'
  - name: Parameters as extension properties
    anchor: customparhelper
    does: 'CustomParHelper gives an extension `self.evalSpeed` and `self.parSpeed` for every custom parameter.'
    authors: true
  - name: Callbacks by parameter name
    anchor: callbacks-by-name
    does: 'A method named `onParSpeed` runs when the Speed parameter changes, with matching names for pulses, parameter groups and sequences.'
    authors: true
  - name: Declare parameters in code
    anchor: declaring-parameters-in-code
    does: 'Helpers such as `CustomParHelper.Float` and `CustomParHelper.Menu` create custom parameters from `__init__`, with page, range and help text.'
    authors: true
  - name: Name your own handlers
    anchor: naming-the-handler-yourself
    does: '`@CustomParHelper.onPar(''Speed'')` binds any method to a parameter, and a mistyped parameter name is reported in the log.'
    authors: true
  - name: Execute callbacks without nodes
    anchor: nonode
    does: 'NoNode registers CHOP, DAT and parameter execute callbacks from extension code or from decorators on the methods, with no execute DATs in the network.'
    authors: true
  - name: Keyboard shortcuts from code
    anchor: registering-callbacks
    does: '`NoNode.RegisterKeyboardShortcut` binds a key such as `ctrl.k` to an extension method, and `DeregisterKeyboardShortcut` removes it.'
    authors: true
---

## Why use it

Promoting a parameter by hand takes a dozen clicks. You open the Component
Editor on the parent, pick a page, add a parameter of the right type, copy the
name, label and range across, then go back to the original and type a bind
expression that points up at it. A Transform's Translate is three of those, and
a control panel for a finished component is easily twenty.

Extensions are the same kind of chore. Each one starts with a text DAT, the
class skeleton and an extension slot filled in on the Component Editor. Every
custom parameter that should do something needs a Parameter Execute DAT with an
`if par.name == ...` branch, and watching a CHOP channel or adding a keyboard
shortcut brings another execute DAT. Before long the logic of one component is
spread over a dozen small DATs around its extension.

CustomParTools covers both ends. Drop a parameter on its button, or hover it and
press `Alt+X`, and it is promoted to the parent and bound back. One click gives a
COMP an extension with ExtUtils docked: CustomParHelper turns your custom
parameters into properties and callbacks named after them, and NoNode registers
execute callbacks and keyboard shortcuts from code, so the network holds the
extension and little else.

## How to use it

Once it is installed, the CustomParTools button
![](/docs/assets/icons/CustomParTools.png) sits on the toolbar and on every pane
bar. It works on the COMP whose network you are in, which this page calls the
parent. Pick the part for the job:

- **Move a parameter up to the parent:** drag it onto the button. See
  [Promoting parameters](#promoting-parameters).
- **Choose its name, range and default as you go:** hold `Ctrl` while you drop.
  See [CustomParCustomize](#customparcustomize).
- **Promote without dragging:** hover the parameter and press `Alt+X`. See
  [QuickParCustom](#quickparcustom).
- **Promote onto a COMP further up:** drop on that COMP in the path bar. See
  [The path bar](#the-path-bar).
- **Open parameters or the Component Editor:** click or right-click the button,
  or press `Shift+Alt+Q`. See [Other button actions](#other-button-actions) and
  [Parameter and editor hotkeys](#parameter-and-editor-hotkeys).
- **Tidy up a COMP copied from another project:** `Alt+click` the button. See
  [Other button actions](#other-button-actions).
- **Start an extension:** `Shift+Alt+click` the button. See [QuickExt](#quickext).
- **Write the extension:** [CustomParHelper](#customparhelper) handles your
  custom parameters and [NoNode](#nonode) handles execute callbacks and keyboard
  shortcuts.

## Promoting parameters

Drag a parameter from any operator's parameter window onto the button.
CustomParTools creates a matching custom parameter on the parent, carries the
value across, and binds the original to it. From then on you can change either
one and both follow.

- **To link it by expression:** hold `Shift` while you drop. The original gets an
  expression pointing at the promoted parameter. If you want that every time,
  switch **Ref/Bind** off; `Shift` then gives you a bind.
- **Where it lands:** on the custom page showing in the parent's parameter
  window. With a built-in page showing it goes on the first custom page, and a
  COMP with no custom pages gets a new page called Custom.
- **Names that are taken:** if the parent already has a parameter of that name,
  the new one gets a number on the end. A parameter that is already bound to the
  parent is not promoted a second time.
- **Expressions move up:** if the original was driven by an expression or a
  bind, it moves to the promoted parameter, rewritten so its references still
  reach the same operators from the parent. When a reference cannot be reached
  from there, the promoted parameter keeps the value and a warning is logged.
- **GLSL uniforms:** a vector uniform on a GLSL operator's Vectors page is named
  after the uniform, such as `uColor`.

Two other things can be dropped on the button:

- **A Table DAT** adds a menu parameter to the parent, named after the table,
  with the table as its menu source. With two columns the first gives the names
  and the second the labels; a first row headed `name` and `label` is read as
  headers.
- **A COMP** promotes all of its custom parameters to the parent and binds them,
  which is the quick way to wrap a finished component in another one.

[ExprHotStrings](/docs/fns-exprhotstrings/) uses the same promotion from inside a
parameter field you are typing in.

## CustomParCustomize

A plain promotion keeps the original's name and label. Often you want something
else: `Speed` for an LFO's Frequency, a range of 0 to 10, a default other than
the value it has right now. Hold `Ctrl` while dropping a parameter on the
button, or on a parent in the path bar, and a small dialog opens before anything
is created.

1. The name field opens with the original's name, capitalised. Type the name the
   custom parameter should get.
2. The label field opens with the original's label. Clear it and the original's
   label is used.
3. Slider-type parameters also get min and max fields, clamping tickboxes and a
   default. The range opens with the original's slider range; for a Switch's
   Index the max is already set to its number of inputs minus one.
4. `Tab` and `Shift+Tab` jump between the fields. OK promotes it.

## Other button actions

| On the button | What happens |
|---|---|
| Click | Opens the parent's parameters |
| `Shift+click` | Opens the selected operator's parameters |
| Right-click | Opens the parent's Component Editor |
| `Shift+right-click` | Opens the selected operator's Component Editor |
| `Alt+click` (`Cmd+click` on macOS) | Runs ClearPars on the selected COMP, see below |
| `Ctrl+Alt` drag an operator onto it (`Ctrl+Cmd` on macOS) | Adds the operator to the parent as an internal operator shortcut (iop) |
| `Ctrl+Shift+click` | Adds a parent shortcut to the parent |
| `Shift+Alt+click` (`Shift+Cmd+click` on macOS) | Adds an extension to the parent with [QuickExt](#quickext) |
| Middle-click | Collapses the selected nodes through [QuickCollapse](/docs/fns-quickcollapse/), when it is installed. Hold `Ctrl` or `Shift` to name the result first |

**ClearPars** is for a COMP you copied in from another project. It tends to
arrive with parameters bound to operators that do not exist here, or expressions
that raise. Select it and `Alt+click` the button: every parameter left in Bind
mode with no valid bind master, or in Expression mode with an expression that
currently raises, is switched to Constant, which drops the dangling bind or
expression. The COMP's script errors are cleared too. It covers the COMP and its
immediate children, annotations excluded, and it is one undo step.

The parent shortcut and the iop each ask for a name in a small dialog; the
parent shortcut starts from the COMP's name, or the shortcut it already has. Two
of these also run from quick-launch on the selected COMP: **Add parent
shortcut** and **Create extension on current**.

## The path bar

The path bar at the top of each pane lists the COMPs above the one you are in,
and CustomParTools makes each of them a drop target. It is the quickest way to
promote a parameter more than one level up.

- Drop a parameter on a parent to promote it there. Hold `Ctrl` to customise it
  first.
- Hold `Ctrl+Alt` (`Ctrl+Cmd` on macOS) and drop an operator to add it to that
  parent as an iop. The root `/` counts as a parent, so the root can get a
  shortcut too.
- Middle-click a parent to open its parameter window.
- Long middle-click a parent to open its customise window.

## QuickParCustom

Dragging a parameter onto a button means having both on screen. QuickParCustom
works on the parameter under the mouse: hover it in any parameter window and
press a key.

| Key | On the hovered parameter |
|---|---|
| `Alt+X` | Promotes it to the parent as a bind. If it is already promoted, opens the promoted parameter in the Component Editor |
| `Shift+Alt+X` | The same, with the promotion made as an expression |
| `Alt+\` | Opens it in the Component Editor: a COMP's own parameter on that COMP, an operator's promoted parameter on the COMP it was promoted to |
| `Ctrl+Alt+\` | Switches a promoted parameter between Bind and Expression, keeping what it points at |

The two promote keys follow **Ref/Bind** like the button does: switch it off and
`Alt+X` makes the expression and `Shift+Alt+X` the bind. A promotion is one undo
step, and a parameter driven by an export is left alone.

All four keys can be rebound on the Custom page of QuickParCustom and are listed
in [HotkeyManager](/docs/fns-hotkeymanager/). Its **Active** switch, also reached
as **Toggle QuickParCustom** in quick-launch, turns the whole thing off.

QuickParCustom was a separate package until 2026-08-24. It always needed
CustomParTools to do the promoting, so it now ships inside it.

## Parameter and editor hotkeys

Four keys for windows you open all day, also available from quick-launch:

| Key | Opens | Quick-launch |
|---|---|---|
| `Shift+Alt+Q` | the parameter dialog for the selected operator | **Open current COMP parameters** |
| `Ctrl+Alt+Q` | the parameter dialog for the COMP whose network is showing | **Open parent COMP parameters** |
| `Shift+Alt+W` | the Component Editor for the selected operator | **Customize current COMP** |
| `Ctrl+Alt+W` | the Component Editor for the COMP whose network is showing | **Customize parent COMP** |

On macOS, Alt is Option. The keys and the commands run the same code, and that
code calls only TouchDesigner itself, so they work whichever other packages you
have installed. Each key can be rebound on the Custom page or in
[HotkeyManager](/docs/fns-hotkeymanager/).

These four came over from the retired **MY_HOTKEYS** package. Their command ids
are unchanged (`opencurrentparameters`, `openparentparameters`,
`customizecurrentcomp`, `customizeparentcomp`), but they now belong to
CustomParTools, so launcher history, curation and presets that referenced
`MY_HOTKEYS#…` need re-pointing once.

## QuickExt

Setting up an extension by hand means a text DAT, the class skeleton, and an
extension slot on the Component Editor filled in with
`op('./MyExt').module.MyExt(me)`, Promote ticked and the extension initialised.
QuickExt does all of it in one step.

1. Go inside the COMP that should get the extension and `Shift+Alt+click` the
   CustomParTools button (`Shift+Cmd+click` on macOS). You can also long-click
   **Add** in the Extension section of the Component Editor and pick
   **QuickExt**, or select the COMP and run **Create extension on current** from
   quick-launch.
2. Type a name for the extension class. The dialog opens with `Ext`.
3. QuickExt creates a text DAT of that name to the left of the network, writes the
   starting code into it under your class name, docks an ExtUtils to it, puts it
   in the first free extension slot with Promote on, and initialises it. The COMP
   is also set to initialise its extensions on start.

The class it writes starts like this, with `onInitTD` and `onDestroyTD` stubs
below:

```python
class MyExt:
    def __init__(self, ownerComp):
        CustomParHelper.Init(self, ownerComp, enable_properties=True, enable_callbacks=True)
        self.ownerComp = ownerComp
```

ExtUtils carries the helpers your extension imports:
[CustomParHelper](#customparhelper) for custom parameters, [NoNode](#nonode) for
execute callbacks and keyboard shortcuts, and FNSCommand, which turns a promoted
method into a quick-launch command when you decorate it with
`@FNSCommand.fns_command`. The comment in the starting code explains it, and
[CommandRegistry](/docs/fns-commandregistry/) collects the commands for the
command palette.

> Keep `ExtUtils` docked to your extension DAT.

> Pro tip: set your IDE's Python interpreter to TouchDesigner's to get stubs and
> code suggestions. ExtUtils deploys its definitions automatically.

### Importing

The starting code imports CustomParHelper and FNSCommand with lines that look
complicated at first sight. You can ignore them, but do not remove them. Each
one finds the ExtUtils docked to your extension, or the one beside it when the
dock is missing, which keeps a cloned component working, and it avoids conflicts
when several extensions each have their own ExtUtils. NoNode takes the same kind
of line; add it when you want it:

```python
CustomParHelper: CustomParHelper = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('CustomParHelper').CustomParHelper # import
NoNode: NoNode = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('NoNode').NoNode # import
```

To see CustomParHelper and NoNode at work, download
[QuickExtTest.tox](https://github.com/function-store/FunctionStore_tools/blob/dev2023/modules/suspects/FunctionStore_tools_2023/QuickExtTest.tox)
and run it, or read its
[extension code](https://github.com/function-store/FunctionStore_tools/blob/dev2023/scripts/QuickExt/templates/ExtUtils/ExtTest.py).

## CustomParHelper

Inside a plain extension, reading a custom parameter is
`self.ownerComp.par.Speed.eval()`, and reacting to one takes a Parameter Execute
DAT that calls back into the class. CustomParHelper reads the COMP's custom
parameters when the extension starts and gives the extension a property for
each, then calls the method named after a parameter when that parameter changes
or pulses. It handles parameter groups (an XYZ or an RGB as one value) and
sequences, lets you choose which parameters and pages it covers, and can create
the parameters for you from code.

### Setting up CustomParHelper

QuickExt does this for you. By hand:

1. Dock ExtUtils to your extension DAT.
2. Import the class:

    ```python
    CustomParHelper: CustomParHelper = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('CustomParHelper').CustomParHelper # import
    ```

3. Initialise it in your extension's `__init__`:

    ```python
    CustomParHelper.Init(self, ownerComp)
    ```

The full signature, with every optional argument:

```python
CustomParHelper.Init(self, ownerComp, enable_properties: bool = True, enable_callbacks: bool = True, enable_parGroups: bool = True, enable_seq: bool = True, expose_public: bool = False,
      par_properties: list[str] = ['*'], par_callbacks: list[str] = ['*'],
      except_properties: list[str] = [], except_sequences: list[str] = [], except_callbacks: list[str] = [], except_pages: list[str] = [],
      enable_stubs: bool = False, general_callback_enable: bool = True,
      enable_parfields: bool = True)
```

- `enable_properties`: creates properties for custom parameters (default: True).
- `enable_callbacks`: creates callbacks for custom parameters (default: True).
- `enable_parGroups`: creates properties and methods for parameter groups
  (default: True).
- `enable_seq`: creates properties and methods for sequence parameters
  (default: True).
- `expose_public`: uses capitalised property and method names, `Par` and `Eval`
  in place of `par` and `eval`.
- `par_properties`: parameter names to create properties for. By default all of
  them.
- `par_callbacks`: parameter names to handle callbacks for. By default all of
  them.
- `except_properties`: parameter names to leave without a property.
- `except_callbacks`: parameter names to leave without callbacks.
- `except_pages`: parameter pages to leave out of both.
- `except_sequences`: sequence names to leave out of both.
- `enable_stubs`: does nothing any more (default: False). Stub generation was
  removed from ExtUtils, since the Stubser it carried was about 19 operators in
  every instance and nothing enabled it. The argument stays so existing calls
  keep working. Generate stubs through [VSCodeTools](/docs/fns-vscodetools/) or
  QuickExt, which carry their own (thanks to AlphaMoonbase.berlin for Stubser).
- `general_callback_enable`: enables the general callbacks that catch every
  parameter change (default: True).
- `enable_parfields`: creates any parameters the class declares before the
  reflection runs (default: True). Harmless for a class that declares none.

Keep each COMP's extension pointing at its own DAT, the way QuickExt sets it up
(`op('./MyExt').module.MyExt(me)`). The properties are set on the class, so two
COMPs sharing one extension module would end up reading each other's parameters.

### Declaring parameters in code

Optionally, declare your parameters in code and they get created:

```python
class MyToolExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp

        self.Speed = CustomParHelper.Float(ownerComp, 'Speed', default=1.0,
                                           min=0, max=10, page='Settings',
                                           help='Playback speed multiplier.')
        self.Mode  = CustomParHelper.Menu(ownerComp, 'Mode', ['fast', 'slow'],
                                          page='Settings',
                                          help='Which way the thing runs.')

        if ownerComp.par.Advanced.eval():            # conditionals work
            CustomParHelper.Int(ownerComp, 'Depth', default=3,
                                page='Settings', help='Recursion depth.')

        for name in ('Alpha', 'Beta'):               # so do loops
            CustomParHelper.Toggle(ownerComp, name, page='Flags',
                                   help='Flag %s.' % name)

        CustomParHelper.Init(self, ownerComp)
```

Each call creates the parameter and returns it, so you can use it on the next
line: `self.Speed.val = 5`. Declaring inside `__init__` is what makes
conditionals, loops and computed defaults ordinary Python, since the COMP exists
by then.

There is one helper per style: `Float` `Int` `Str` `Toggle` `Pulse` `Menu`
`StrMenu` `File` `Folder` `Header` `XYZ` `RGB` `RGBA` `OP` `COMP` `TOP` `CHOP`
`SOP` `DAT` `MAT`. The multi-member ones (`XYZ`, `RGB`, `RGBA`) return a ParGroup
and take either one value for every member or a sequence:
`default=(0.2, 0.4, 0.6)`.

Declaring is additive. CustomParHelper still reflects whatever parameters it
finds, so a tool that declares nothing behaves exactly as before, and you can mix
declared and hand-made parameters freely. There is no base class to inherit.

Declare before `CustomParHelper.Init`, so the new parameters get properties and
callbacks in the same pass. A parameter added by hand after `Init` has no
property until something refreshes it; a declared one cannot drift.

The `page` keyword names the page, `page='Settings'` above. It is the page name,
created if it does not exist, and it defaults to `'Custom'`. It is only used when
the parameter is created; an existing parameter is not moved.

Every other keyword is a TouchDesigner `Par` member, set straight through:
`default`, `label`, `help`, `readOnly`, `startSection`, `min`, `max`,
`clampMin`, `clampMax`, `normMin`, `normMax`, `menuNames`, `menuLabels`,
`order`. They keep TouchDesigner's own names; see the
[Par Class](https://docs.derivative.ca/Par_Class) for what each does and which
styles honour it.

If the parameter set never varies, you can declare on the class body and `Init`
creates them:

```python
class MyToolExt:
    Speed = CustomParHelper.ParFloat(default=1.0, page='Settings',
                                     help='Playback speed multiplier.')

    def __init__(self, ownerComp):
        CustomParHelper.Init(self, ownerComp)
```

This form cannot do conditionals or loops, and it cannot hand you the parameter,
because a class body runs before there is any COMP to create one on.
`self.Speed` still resolves to the real Par once `Init` has run, and raises a
message explaining itself if you touch it before that. Both forms use the same
code underneath, so they behave identically once the parameter exists.

Three things worth knowing:

- **A new parameter is seeded with its default; an existing one keeps its
  value.** The first time a declaration creates a parameter, it is set to the
  declared `default`. After that, re-initialising keeps the value and anything
  you changed in the Component Editor (label, help, range, default). Only the
  style, the menu entries and `readOnly` follow the code on every run. After
  changing a declaration, call `CustomParHelper.RefreshDeclared(self, ownerComp)`
  once to push its label, help, range and default to existing parameters, or pass
  `force=True` on a single declaration.
- **A style change is applied for you.** Declaring `ParStr` over an existing
  Float rebuilds the parameter and carries across its value, expression, bind
  expression and position on the page. The one thing that cannot survive is an
  export: that link belongs to the exporting CHOP and lives outside the
  parameter, so it is reported in the textport and you re-export it.
- **`help` is strongly expected but not enforced.** Leaving it out logs a warning
  and your extension keeps working. Fill it in: it is the tooltip your users get
  when they hover the parameter name.

### Reading and setting values

With `enable_properties` on (the default) there are two ways to reach a
parameter.

The eval properties are the simple way to read and set values:

```python
# Get value
value = self.evalMyparam
# Set value (always sets .val regardless of parameter mode)
self.evalMyparam = 5

# Parameter groups: get values
values = self.evalGroupXyz
# Set values (always sets .val for each parameter)
self.evalGroupXyz = [1, 2, 3]
```

The par properties hand you the parameter itself, for advanced control:

```python
# Get parameter object for advanced operations
self.parMyparam.expr = "op('something').par.value"
self.parMyparam.bindExpr = "op('other').par.value"
# Set value (only works in CONSTANT or BIND modes)
self.parMyparam = 5  # Ignored if parameter is in EXPRESSION mode

# Get parameter group for advanced operations
myGroup = self.parGroupXyz
# Set values (only works for parameters in CONSTANT or BIND modes)
self.parGroupXyz = [1, 2, 3]  # Only affects non-expression parameters
```

To expose them publicly, as `self.ParMyparam` in place of `self.parMyparam`, set
`expose_public=True` in `Init`.

### Callbacks by name

With `enable_callbacks` on (the default), CustomParHelper calls a method whose
name matches the parameter. Arguments can be left off from the right when you do
not need them.

```python
# a regular parameter changes (_par and _prev can be omitted)
def onPar<Parname>(self, _par, _val, _prev):

# a pulse parameter fires (_par can be omitted)
def onPar<PulseParname>(self, _par):

# a sequence's block count changes
def onSeq<SeqName>N(self, idx):

# a parameter inside a sequence block changes (_par and _prev can be omitted)
def onSeq<SeqName>N<Parname>(self, _par, idx, _val, _prev):

# a parameter group changes, with enable_parGroups on (_parGroup can be omitted)
def onParGroup<Groupname>(self, _parGroup, _val):
```

With `general_callback_enable` on (the default), two general callbacks catch
every change that has no specific callback:

```python
def onValueChange(self, _par, _val, _prev):
    # any parameter value change without a specific callback
    # _val and _prev can be omitted if not needed

def onPulse(self, _par):
    # any pulse without a specific callback
    # _par can be omitted if not needed
```

### Naming the handler yourself

Every callback above is found by its name. If you would rather name the method
for what it does, declare which parameter it handles:

```python
class MyToolExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        CustomParHelper.Init(self, ownerComp)     # harvests the declarations

    @CustomParHelper.onPar('Speed')
    def playbackSpeedChanged(self, _par, _val, _prev):
        ...

    @CustomParHelper.onPar('Reset')               # a Pulse parameter
    def clearEverything(self, _par):
        ...

    @CustomParHelper.onParGroup('Translate')
    def moved(self, _parGroup, _val):
        ...
```

There are six decorators, one per callback kind: `onPar` (value change, or pulse
for a Pulse parameter), `onParGroup`, `onSeq(sequence, par)`,
`onSeqBlock(sequence)`, and `onAnyValueChange()` and `onAnyPulse()` for the two
general callbacks.

`Init` harvests them, so there is no extra call and no change to your `Init`.
Signatures and arity are exactly as documented above: the decorator records which
parameter the method handles and returns the method untouched, so you can still
leave `_val` and `_prev` off the right.

Two things the naming convention cannot do:

- **A declaration that names a parameter you do not have is reported.** With the
  convention, a mistyped `onParSpeeed` is a method that never runs and never
  complains. A declaration is logged, so one bad declaration does not stop a
  tool loading.
- **A collision is reported too.** If the class already defines `onParSpeed` and
  another method declares `@onPar('Speed')`, the existing method wins and the
  declaration is reported as ignored, so nothing silently shadows working code.

Declared and conventionally named callbacks work side by side on the same
extension; use whichever reads better per parameter.

## NoNode

A Parameter Execute DAT for one parameter, a CHOP Execute for a trigger channel,
a Keyboard In with its callbacks for one shortcut: each is a node to create,
point at the right operator and keep in step with the extension that does the
real work. NoNode registers the same callbacks from your extension's code. The
network keeps only the extension and its ExtUtils, and every operator with a
registered callback is marked with a colour so you can see what is being
watched.

### Setting up NoNode

1. Dock ExtUtils to your extension DAT.
2. Import the class:

    ```python
    NoNode: NoNode = (next((d for d in me.docked if 'ExtUtils' in d.tags), None) or next((c for c in me.parent().children if 'ExtUtils' in c.tags), None)).mod('NoNode').NoNode # import
    ```

3. Initialise it in your extension's `__init__`, passing the COMP:

    ```python
    NoNode.Init(ownerComp, enable_chopexec=True, enable_datexec=True, enable_parexec=True, enable_keyboard_shortcuts=True)
    ```

### Registering callbacks

The event types are `NoNode.ChopExecType` (`OffToOn`, `WhileOn`, `OnToOff`,
`WhileOff`, `ValueChange`), `NoNode.DatExecType` (`TableChange`, `RowChange`,
`ColChange`, `CellChange`, `SizeChange`) and `NoNode.ParExecType`
(`ValueChange`, `OnPulse`). As with CustomParHelper, a callback can leave
arguments off the right side of its signature.

CHOP executions:

```python
NoNode.RegisterChopExec(NoNode.ChopExecType.ValueChange, chop_op, channel_name(s), self.on_value_change_function)
# callback signature: def on_value_change_function(self, channel: Channel, sampleIndex: int, val: float, prev: float):
# can omit parameters from the right side of the signature if not needed

NoNode.RegisterChopExec(NoNode.ChopExecType.OffToOn, chop_op, channel_name(s), self.on_activate_function)
# callback signature: def on_activate_function(self, channel: Channel, sampleIndex: int, val: float, prev: float):
# can omit parameters from the right side of the signature if not needed
```

DAT executions:

```python
NoNode.RegisterDatExec(NoNode.DatExecType.TableChange, dat_op, self.on_table_change_function)
# callback signature depends on the event type, eg.: def on_table_change_function(self, dat: DAT):

NoNode.RegisterDatExec(NoNode.DatExecType.CellChange, dat_op, self.on_cell_change_function)
# callback signature depends on the event type, eg.: def on_cell_change_function(self, dat: DAT, cells: list[Cell], prev: Cell):
```

Parameter executions:

```python
NoNode.RegisterParExec(NoNode.ParExecType.ValueChange, par_op, par_name, self.on_value_change_function)
# callback signature depends on the event type, eg.: def on_value_change_function(self, par: Par, val: float, prev: float):
# can omit prev, or use val only

NoNode.RegisterParExec(NoNode.ParExecType.OnPulse, par_op, par_name, self.on_pulse_function)
# callback signature: def on_pulse_function(self,par: Par):
# can omit par if not needed
```

Keyboard shortcuts:

```python
NoNode.RegisterKeyboardShortcut('ctrl.k', self.onKeyboardShortcut)
# callback signature: def onKeyboardShortcut(self):
```

Each has a matching call to remove it again:

```python
NoNode.DeregisterChopExec(NoNode.ChopExecType.ValueChange, chop_op, channel_name(s))
NoNode.DeregisterDatExec(NoNode.DatExecType.TableChange, dat_op)
NoNode.DeregisterParExec(NoNode.ParExecType.ValueChange, par_op, par_name)
NoNode.DeregisterKeyboardShortcut('ctrl.k')
```

To change the colour that marks watched operators:

```python
NoNode.SetMarkColor((r, g, b))
```

### Declaring callbacks on the method

The `Register*` calls above are one way to wire a callback. The other is to
declare it on the method itself and let NoNode collect them:

```python
class MyToolExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        NoNode.Init(ownerComp, enable_chopexec=True, enable_parexec=True)
        NoNode.HarvestCallbacks(self)          # registers everything below

    @NoNode.onChopExec(NoNode.ChopExecType.ValueChange, 'null_audio', 'chan1')
    def audioMoved(self, channel, sampleIndex, val, prev):
        ...

    @NoNode.onParExec(NoNode.ParExecType.ValueChange, 'null_hk', 'Shift')
    def shiftChanged(self, par, val, prev):
        ...

    @NoNode.onKeyboardShortcut('ctrl.k')
    def quickAction(self):
        ...
```

`@NoNode.onChopExec`, `@NoNode.onDatExec`, `@NoNode.onParExec` and
`@NoNode.onKeyboardShortcut` take the same arguments as their `Register*`
counterparts, minus the callback itself. Signatures are unchanged, and arity is
still inferred, so you can still drop arguments off the right.

Targets are strings, resolved when `HarvestCallbacks` runs, relative to the
extension's COMP. They cannot be `op()` calls: a class body is executed while
the class is being defined, long before any COMP exists to resolve against.
Leave out the owner on `onParExec` to watch your own COMP's parameter.

What this gives you over the `Register*` calls:

- **The binding is visible at the callback**, right where you read the handler,
  and the method name is yours to choose.
- **A target that does not resolve is reported.** A mistyped operator or
  parameter name in a `Register*` call gives a callback that never fires;
  `HarvestCallbacks` logs it, and raises nothing, so one bad declaration does
  not stop a tool from loading.
- **Re-harvesting rebuilds from scratch**, so a callback deleted from the code
  disappears with it and there is nothing stale to deregister.

Both styles work on the same extension, and neither needs the other:
`NoNode.Init` plus `HarvestCallbacks` is enough on its own, with no
CustomParHelper involved.

NoNode also works alongside CustomParHelper. The two watch through separate
execute DATs and do not read each other's state, so a COMP can use
CustomParHelper for its parameters and decorators for its callbacks. On the same
parameter both fire, though: an `onParSpeed` method and an `@onParExec`
decorator for `Speed` give you two callbacks, so pick one style per parameter.
Use the decorator when you want the handler's name free of the `onPar<Name>`
convention.

## Switching parts off

Each part of CustomParTools is a separate module, and the **Modules** page
switches each one on or off on its own. All nine ship on, and the settings are
kept through [ConfigRegistry](/docs/fns-configregistry/) like the rest of the
tool's parameters.

The nine fall into three groups:

- five that work through the button: **Parameter Promotion**, **QuickExt**,
  **QuickParent**, **ClearPars** and **IOP Promoter**;
- two on the pane bar: **Navbar Drag/Drop**, which takes the drops, and
  **Navbar Path Cell Click**, the middle-click on a parent in the path bar;
- two sets of keys: **QuickParCustom**, which is bound to QuickParCustom's own
  **Active** switch, and **Parameter/Editor Hotkeys**.

Switching a module off withdraws whatever it puts on screen:

- The two pane-bar modules each register their own widget, so turning one off
  removes that widget from every pane bar.
- The five button modules share the CustomParTools button. It leaves the pane
  bars and the toolbar only when all five are off, since any one of them still
  gives it something to do.
- The settings registration is never withdrawn. It puts nothing on screen, and
  it is what stores these toggles, so dropping it would discard the setting that
  asked for the drop.
