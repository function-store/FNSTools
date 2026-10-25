---
package: ChopProcess
summary: 'Shapes channels in one node: limit, remap between ranges with an exponent curve, zero at the bottom, lag, and an optional speed mode that turns the result into a running total. An alternative for the Math CHOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Turning a fader into a speed
    anchor: turning-a-fader-into-a-speed
  - name: Input and output
    anchor: input-and-output
feature_list:
  - name: Limit and remap with a curve
    anchor: how-to-use-it
    does: 'Limits incoming values to a range and remaps that range onto another through an exponent curve.'
  - name: Zero Below
    anchor: how-to-use-it
    does: 'Makes the bottom of the input range output 0, so a fader switches fully off at its lowest point yet starts usefully once moved.'
  - name: Lag smoothing
    anchor: how-to-use-it
    does: Glides toward new values with a lag.
  - name: Speed mode
    anchor: turning-a-fader-into-a-speed
    does: 'Treats the result as a speed and outputs its running total, which can be clamped, looped or bounced between limits.'
  - name: Shape a whole fader bank in one node
    anchor: how-to-use-it
    does: 'Every input channel goes through the same chain, so one node shapes a whole fader bank; with nothing connected, the Value parameter is processed.'
  - name: Replace a Math CHOP
    anchor: how-to-use-it
    does: 'Create a Math CHOP with the alternatives shortcut held and ChopProcess is offered in its place, wired into the same spot.'
---

## Why use it

A controller value is rarely ready to use as it arrives. A MIDI fader sends 0
to 1 when you need 0 to 360 degrees, its response feels wrong at one end, and
its steps show up as jumps on screen. So after almost every controller you
build the same chain: a Limit CHOP, a Math CHOP to remap, a Lookup or a
Function CHOP for the curve, a Lag or Filter CHOP to smooth it.

ChopProcess is that chain in one node. Every channel of the input goes
through it, so one node shapes a whole fader bank.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. Or create a Math
   CHOP with the alternatives shortcut held, pick ChopProcess, and it lands in
   that spot with the wiring kept.
2. Wire your controller into it: a MIDI In CHOP, an OSC In CHOP, a Select CHOP
   holding the faders you want.
3. Set **From Range** to what the controller sends and **To Range** to what
   you need, for example 0 to 1 onto 0 to 360 for a rotation.
4. To keep values inside the range, set **Type** to clamp. Loop wraps them
   round and zigzag bounces them back.
5. Shape the response with **Exponent Value**. Above 1 the curve eases in, so
   the bottom of the fader gets the fine control; below 1 it eases out.
6. Smooth it with **Lag**, in seconds.

A few more things people reach for:

- **A fader that switches something fully off.** With Type on clamp, switch on
  **Zero Below** and the bottom of the input range outputs 0, even when the
  output range starts higher. The fader still starts from a useful value as
  soon as it moves: handy for a layer's opacity, off at the bottom and visible
  from the first nudge.
- **Your own channel names.** **Name** renames the output channels, one name
  per channel or a pattern like `chan[1-4]`.
- **No input at all.** With nothing wired in, ChopProcess processes its own
  **Value**, so it can shape a single value you type or reference there.

## Turning a fader into a speed

Switch on **Is Speed** and the processed value is treated as a speed: the
output is its running total, so a fader held above zero keeps the value
moving, and bringing the fader back to zero leaves the value where it got to.

- Map the fader onto -1 to 1 with **To Range**, and the centre holds the
  value still while either side runs it down or up.
- **Limit Type** decides what happens at **Minimum** and **Maximum**: clamp
  stops there, loop wraps around, zigzag bounces back. Loop between 0 and 1
  gives a phase that keeps cycling at the fader's speed.
- **Reset Pulse** sends the total back to **Reset Value** once; **Reset**
  holds it there while on.

## Input and output

- **in1** (CHOP): the channels to process. With nothing connected, the Value parameter is processed instead.
- **out1** (CHOP): the processed channels.
