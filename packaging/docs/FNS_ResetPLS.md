---
package: FNS_ResetPLS
summary: YouTube breakdown
features:
  - name: Global ResetPLS
    anchor: global-resetpls
    icon: ResetPLS.png
feature_list:
  - name: Reset everything at once
    anchor: global-resetpls
    does: 'Pulses resetpulse and similar parameters on every operator the search finds, from the Reset pulse or the hotkey.'
  - name: Search root and depth
    anchor: conf
    does: 'Root sets where the search starts, and Limit Depth with Depth caps how far down it reaches.'
  - name: Exceptions
    anchor: conf
    does: 'Except lists operators to skip, and Exceptions Limit also excludes everything under an excepted COMP.'
  - name: Reset on startup
    anchor: conf
    does: Reset On Startup pulses Reset automatically when the project starts.
  - name: Operator type toggles
    anchor: top-chop-sop-comp
    does: 'Toggles per TOP, CHOP, SOP and COMP type choose which operators are reset, with Enable/Disable All to set them together.'
  - name: Custom reset parameter names
    anchor: top-chop-sop-comp
    does: 'COMPs and Script operators are reset through parameters named Reset or Resetpulse, and Edit Custom Reset Pars adds more names.'
  - name: Reset the timeline
    anchor: misc
    does: Reset Timeline also sends the root timeline to the frame set in Reset Frame.
  - name: onReset callback
    anchor: misc
    does: 'Create Callbacks makes a text DAT for an onReset script, which runs on every reset while Callback is on.'
  - name: Static pattern exceptions
    anchor: misc
    does: 'Static Exceptions holds pattern match strings, prefixed with ^, for components that should always be excluded.'
---

## Global ResetPLS

[YouTube breakdown](https://youtu.be/G25n1DAI2pM)

This component takes care of all your reset needs, pulsing all `resetpulse` or similar parameters of operators included in search.
You can enable or disable certain operator types (hope I didn't forget any). No more dragging a Keyboard In CHOP all across your networks!
You can also specify exceptions and whether those exceptions block further resets down the line (only relevant for COMPs).

It is bound to `Ctrl+0` hotkey (which I have bound to one of my mouse buttons as well).

### Conf

- **Root:** where opfindDAT should start the search
- **Limit Depth:** enable limit how far opfind should search
- **Depth:** maximum depth of limit
- **Except:** list of opeartor exceptions the search should ignore.
- **Exceptions Limit:** only relevant for baseCOMP that are listed as Exception. If enabled all further operators under are also excluded. 
- **Enable/Disable All OPtypes:** sets the state of all operator type toggles
- **Reset On Startup:** pulses `Reset` automatically when the project starts
- **Reset:** pulses reset parameter for all included operators

### TOP, CHOP, SOP, COMP

- Individual toggles enabling/disabling certain operator types (only ones relevant for resetting listed)
- **For COMP operators and Script TOP/CHOP/SOP/DAT:** the component assumes a pulse parameter named `Reset` or `Resetpulse`. The list of assumed parameters can be edited under the `Misc` parameter tab, clicking the pulse `Edit Custom Reset Pars`

### Misc

- **Reset Timeline:** if enabled resets root timeline to the frame specified in `Reset Frame`
- **Reset Frame:** which frame to reset to if `Reset Timeline` is enabled
- **Callback:** toggles executing a custom callback on reset
- **Create Callbacks:** create a text DAT next to this component where you can define an `onReset` script
- **Callbacks:** location of the callback script (points to the default script by default)
- **Static Exceptions:** you should list all pattern match strings here you want to exclude.
  - A use-case for this is some common custom components such as the already present `colour_lovers_picker`. You must prepend your string with a `^`.
  - After adding more rows to this list you should re-save the component either as external tox or into your palette.
- **Edit Custom Reset Pars:** list of parameter names assumed to be present in **Base, Container, Script TOP/CHOP/SOP/DATs** for the purpose of resetting. You can add more rows.
