---
package: oscMapper
summary: Simple OSC mapping tool by AlphaMoonbase.berlin.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Sending values back to the controller
    anchor: sending-values-back-to-the-controller
feature_list:
  - name: Learn-based OSC mapping
    anchor: how-to-use-it
    does: 'Drag parameters onto the mapper, switch on Learn and move a fader or knob to assign it.'
  - name: Mapping range
    anchor: how-to-use-it
    does: Set the min/max range a mapped control drives.
  - name: Send values back to the controller
    anchor: sending-values-back-to-the-controller
    does: 'Talkback sends values back out over OSC as they change, so a controller with motorised faders or LEDs can follow TouchDesigner.'
  - name: Listen and send per project
    anchor: how-to-use-it
    does: 'A new copy neither listens nor sends until you switch it on, and that choice stays with the project.'
---

## Why use it

A tablet running an OSC controller app, a phone, another machine with its own
patch: they all send named OSC addresses, and wiring one to a parameter by
hand means an OSC In CHOP, finding the right channel, rescaling it and
exporting it onto the parameter.

oscMapper, a simple OSC mapping tool by
[AlphaMoonbase.berlin](https://alphamoonbase.de/), learns the address for
you: drop a parameter, move the control, and it is mapped, each mapping with
its own range.

## How to use it

1. Open the **oscMapper** tab in [FNS_Hub](/docs/fns-hub/). Right-click the
   tab to configure the tool.
2. Switch on **Active**. A new copy does not listen until you do.
3. Set **Port** to the port your controller sends to. If several tools share
   that port, narrow **OSC Address Scope**; on a machine with several network
   cards, pick the **Local Address** to listen on.
4. Drag the parameters you want to control onto the mapper, switch on
   **Learn** and move a control. While Learn is on, the next address that
   arrives is assigned to every row still waiting, so drop one parameter at a
   time, or several to put them on one control. Switch **Learn** off when you
   are done.
5. Set each mapping's min and max. The 0 to 1 the controller sends is spread
   across that range.

- **To edit mappings by hand,** **Edit DAT** opens the table, one row per
  mapping. **Clear** deletes every mapping.
- **To keep mappings somewhere else,** point **Mappingtable** on the
  Repositorie page at another table, or press **Create** to make one.

The tool's settings, such as ports and addresses, persist and follow you
across projects through [ConfigRegistry](/docs/fns-configregistry/), like
every other tool; the `Registry` page on the component controls whether it
participates. Two things stay with the project: the mappings, and whether
this project listens and sends at all (**Active** and **Talkback Active**).

## Sending values back to the controller

A controller with motorised faders or LEDs can follow TouchDesigner, so a
value you change on screen shows up on the hardware too.

1. Switch on **Talkback Active**.
2. Set **Network Address** to the controller's IP, or leave it on localhost
   for an app on the same machine.
3. Set the talkback **Port** to the port the controller listens on. It is
   normally a different port from the one you receive on.

Each mapped parameter's value is then sent back on its address, scaled to 0
to 1.
