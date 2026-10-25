---
package: FNS_ResetPLS
summary: One key that resets every feedback loop, timer, counter and simulation in the project.
features:
  - name: Why use it
    anchor: why-use-it
    icon: ResetPLS.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Leaving things out
    anchor: leaving-things-out
  - name: Your own components
    anchor: your-own-components
feature_list:
  - name: Restart every feedback loop and timer at once
    anchor: how-to-use-it
    does: 'One press of `Ctrl+0`, the toolbar button or quick-launch pulses the reset of every matching operator in the project.'
  - name: Operator type toggles
    anchor: how-to-use-it
    does: 'Switch whole operator types in or out, from Feedback TOPs and Timer CHOPs to particle systems, solvers and MIDI In DATs.'
  - name: Startup reset
    anchor: how-to-use-it
    does: The project can reset itself once as it opens.
  - name: Rewind the timeline too
    anchor: how-to-use-it
    does: A reset can also send the root timeline back to a chosen frame.
  - name: Search only part of a project
    anchor: leaving-things-out
    does: 'Point the search at one component, and cap how deep it looks.'
  - name: Exclude operators by path
    anchor: leaving-things-out
    does: 'Leave named operators alone, with or without everything inside them.'
  - name: Exceptions by pattern
    anchor: leaving-things-out
    does: 'A pattern list such as `^*/presets*` for components that should never be reset; with Externalize Tables on, it follows you from project to project.'
  - name: Custom components join the reset
    anchor: your-own-components
    does: 'Your components and Script operators join the reset through a pulse named Reset or Resetpulse, and the list of names is yours to extend.'
  - name: Callback on every reset
    anchor: your-own-components
    does: 'Run your own Python on every reset, for anything a pulse cannot express.'
---

## Why use it

Anything in TouchDesigner that builds up over time needs a way back to the
start: feedback loops, trails, caches, counters, timers, particle systems.
While you build, that means clicking reset pulses one by one, or dragging a
Keyboard In CHOP into every network and wiring it to each reset parameter.
Neither scales. Once a project has a dozen of these spread across components,
you forget one, and the run-through starts with last night's trails still on
screen.

ResetPLS gives the whole project one reset button. Press `Ctrl+0` and it finds
every operator of the kinds you care about, wherever it sits, and pulses its
reset. There is nothing to wire, and operators you add later are included the
next time you press it.

## How to use it

1. Install it. Out of the box it searches the whole project and covers the
   operators people usually mean by "reset": Feedback and Cache TOPs, Movie File
   In, Timer, Count, LFO, Lag and Filter CHOPs, particle and spring systems,
   the physics solvers and MIDI In.
2. Press `Ctrl+0` (`Cmd+0` on macOS), click the ResetPLS button on the toolbar,
   or run **Reset all generators** from quick-launch.
3. To change which kinds of operators are included, right-click the toolbar
   button to open the parameters and switch types on or off on the TOP, CHOP,
   SOP, POP, DAT and COMP pages. **Enable All OPtypes** and **Disable All
   OPtypes** flip them all at once, which is handy when you only want two or
   three types.

A few habits that help in a show:

- Switch on **Reset On Startup** and the project resets itself once as it
  opens, so every run starts from the same place.
- A reset also sends the root timeline back to frame 1. If you only want the
  operators reset, switch off **Reset Timeline** on the Misc page, or pick
  another frame there.
- Bind `Ctrl+0` to a spare mouse button. It is the key you reach for most
  while tuning anything feedback based.

There is also a [video breakdown](https://youtu.be/G25n1DAI2pM) on YouTube.

## Leaving things out

Some things should survive a reset: a Record CHOP holding a take you want to
keep, a component that manages its own state, or a whole section of the
project you are not working on.

- **One operator or component:** add its path to **Except**. Several paths go
  in the same field, separated by spaces. Switch on **Exceptions Limit** to
  skip everything inside an excepted component as well.
- **Only part of the project:** set **Root** to the component that holds it.
  **Limit Depth** stops the search a set number of levels below Root, which also
  keeps it quick in a big project.
- **Never, in any project:** open **Static Exceptions** on the Misc page and add
  a pattern starting with `^`, for example `^*/presets*`. The list ships with a
  few entries for common components, and ResetPLS keeps itself out of its own
  reset the same way. With **Externalize Tables** on, the list is kept in a file
  and follows you from project to project; with it off, re-save the component
  after adding rows.

## Your own components

ResetPLS resets a component or a Script operator by pulsing a parameter named
`Reset` or `Resetpulse`. So to make one of your own components part of the
reset:

1. Give it a pulse parameter called `Reset`, and do whatever resetting means
   for that component when it fires.
2. Switch on its type on the COMP page (Base, Container and so on), or Script
   on the TOP, CHOP, SOP or DAT page.

If your components already use a different name, add it with **Edit Custom
Reset Pars** on the Misc page.

For anything a pulse cannot express, use the callback:

1. Press **Create Callbacks** on the Misc page. It puts a text DAT next to
   ResetPLS with an empty `onReset` function and points **Callbacks** at it.
2. Switch on **Callback**.
3. Fill in `onReset`. It runs on every reset.

```python
def onReset():
	# start the show from the first scene again
	op('/project1/switch_scenes').par.index = 0
	return
```
