---
package: FNS_OpFamily
summary: 'The FNS tab in the OP Create dialog: an operator family whose members are FNS tools placed from the store as one node each, with stubs for projects that travel and in-place updates. Built with TDFam.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Where the operators come from
    anchor: where-the-operators-come-from
  - name: Stubs and updates
    anchor: stubs-and-updates
  - name: Credits
    anchor: credits
feature_list:
  - name: Create FNS tools from OP Create
    anchor: how-to-use-it
    does: 'Adds an FNS tab beside COMP, TOP, CHOP and the others; each entry places an FNS tool into the current network as one operator.'
  - name: Remove the FNS tab
    anchor: how-to-use-it
    does: 'Pick Tools, the FNS Tab in OP Create switch or Remove Operator Family take the tab away, the choice sticks, and the switch brings it back.'
  - name: Members mirrored from the store
    anchor: where-the-operators-come-from
    does: 'The tab lists exactly the members this machine''s store holds, kept in step by the updater, and the same folder shows up in the Palette.'
  - name: Replace a stock operator with a member
    anchor: where-the-operators-come-from
    does: 'A member can also be offered in place of a stock operator, such as Random when you create a Noise CHOP with the alternatives shortcut held.'
  - name: Stub operators for projects that travel
    anchor: stubs-and-updates
    does: 'Placed members become light placeholders that keep their wiring, position, retained parameters and state, and come back as the real operators wherever the family is installed.'
  - name: Update placed operators in place
    anchor: stubs-and-updates
    does: 'Upgrades every placed member to the newest version in the family folder, keeping its retained parameters and state.'
  - name: Sync, stub and update from quick-launch
    anchor: stubs-and-updates
    does: 'Stub, replace, update and resync from quick-launch without dialogs, for the whole project or only the network you are in.'
  - name: Manifest-declared retention
    anchor: stubs-and-updates
    does: Each member's manifest declares which parameters and which state survive a stub or an update.
    authors: true
---

## Why use it

Many FNS tools behave like operators: a Random CHOP, a scene changer, a
sequencer, PrismTOP. Each is a COMP with a network inside, and without help you
place one by finding its `.tox` and dragging it in. Every copy then stays the
version it was when you dropped it, and nothing keeps track of where the copies
went.

The operator family gives these tools their own **FNS** tab in the OP Create
dialog. Every entry reads as one operator: inputs on the left, outputs on the
right, its own parameters, placed into the network you are working in like any
stock type. Because the family knows every copy you placed, it can also update
them in place, or turn them into light stubs before a project travels.

## How to use it

1. Install a family operator. The installer adds the family with the first of
   its operators and removes it with the last. When you tick a family operator
   in Pick Tools, the selection bar shows **Add FNS tab to OP Create**; leave it
   ticked for the tab, or untick it to keep the operators in your palette only.
2. Open the OP Create dialog in any network and click the **FNS** tab.
3. Pick an operator. It lands in the network you are in as one node, ready to
   wire.

More than thirty tools are members, among them
[Random](/docs/fns-randomchop/), the scene changers, the sequencers,
[SeqMod](/docs/seqmod/), [PrismTOP](/docs/prismtop/) and
[ChopBank](/docs/chopbank/). A project without FNS operators has no FNS tab, no
family registry and no family folder.

To take the tab away, untick **FNS Tab in OP Create** on the FNSTools page of
the toolkit's parameters, untick the same switch in Pick Tools, or run **Remove
Operator Family** from quick-launch. The switch brings the tab back as long as
at least one family operator is installed. Your FNS tools stay installed either
way, and the choice sticks: installing another family operator, or setting up a
new project like the last one, keeps the tab off until you tick the switch
again.

## Where the operators come from

Members are the packages you already know, mirrored from the machine's store
into the family's operator folder, `FNSTools/FNS/` in your palette folder: one
tox per member under its plain name, with a manifest beside it. The same folder
shows up in TouchDesigner's own Palette as `FNSTools > FNS`.

The [FNS updater](/docs/fns-updater/) keeps that folder in step with the store.
Every install and update pass that leaves the store complete runs the sync, and
the family asks for one when it arrives in a project, so the FNS tab lists
every member the machine holds, and only those. **Sync Family From Store** runs
it by hand.

The store only holds the packages your account is entitled to. A Pro-tier
member therefore appears on the tab for Pro members and not for Base members,
with no extra gate anywhere. A member you never installed is still on the tab
once the store holds it, since the store is complete by default (see **Keep the
Whole Release in the Store** on the updater).

A member can also be an operator alternative: create a Noise CHOP with the
alternatives shortcut held and Random is offered. Two doors, one tox.

## Stubs and updates

A placed member stays the version it was placed at, and it needs the family
folder to exist. Two jobs follow from that:

- **Sending a project to a machine without the toolkit.** Run **Stub Family
  Operators** first. Each placed member becomes a light placeholder that keeps
  its wiring, position, retained parameters and retained state. On a machine
  with the family, **Replace Family Stubs** brings the real operators back from
  the family folder. A stub whose package that machine's store does not hold
  stays a stub, and the command tells you how many.
- **Bringing placed operators up to date.** **Update Family Operators**
  upgrades every placed member to the newest version in the family folder,
  applying each member's retained parameters and state. Members that are
  already current are left alone.

Which parameters and which state survive a stub or an update is declared per
member in its manifest.

These quick-launch commands act without dialogs and report what they did.
**Stub Family Operators**, **Replace Family Stubs** and **Update Family
Operators** can each be limited to the network you are looking at.

The Stubs page on this package's parameters has the same actions as pulses,
for every operator, one **Target Op**, everything inside a **Target Comp**, or
every placed operator of one **Target Type**. Those are TDFam's own buttons:
they ask before they act and report in dialogs, which suits a click and not a
script.

The toolkit's own copies of the members are never stubbed or updated this way,
by the commands or by the pulses: those copies belong to the FNS updater.

## Credits

The family is a TDFam family named `FNS`, coloured brick red
(0.569 0.265 0.188) and installed on project start. Its registry promotes
itself to `/sys` the way TDFam designs it.

Built with [TDFam](https://github.com/dotsimulate/TDFam) by Lyell Hintz
(dotsimulate) and Dan Molnar (Function Store), Apache-2.0. The licence and
notice ship inside the package.
