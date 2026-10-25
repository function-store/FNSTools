---
package: SeqMod
summary: 'Watches a sequence of parameters on any COMP and tells you when blocks come and go: name the target and the sequence, and the block parameters are published as one list, with a callback per added or removed block.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Callbacks
    anchor: callbacks
feature_list:
  - name: Follow a sequence's blocks
    anchor: how-to-use-it
    does: 'Point it at a COMP and name the sequence, and the list of block parameters stays current as the sequence grows and shrinks.'
  - name: Publish the block parameters
    anchor: how-to-use-it
    does: 'Publishes the block parameters as name patterns in ParNames and as a table on out1, ready for a Parameter DAT, a UI builder or a script.'
  - name: Add and remove callbacks
    anchor: callbacks
    does: Create Callbacks makes a DAT whose OnAddBlock and OnRemoveBlock hooks run once per block; errors are reported on SeqMod itself.
    authors: true
---

## Why use it

Sequence parameters, the `Items0name`, `Items1name`, ... blocks TouchDesigner
grows and shrinks, are awkward to drive from outside. The names change with
the count, and nothing tells you when a block appears. Build a control panel
with a row per block of another COMP's sequence, and you need both: the
current list of block parameters, and a signal when one is added or removed.

SeqMod sits beside the COMP that owns the sequence and keeps that list
current. It publishes the block parameters as **ParNames** and as a table on
`out1`, and fires a callback for every block added or removed. Wire it to a
replicator, a UI builder or your own script and the sequence becomes something
you can react to.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog, where it is called
   Seq Mod. It is a member of the [FNS operator family](/docs/fns-opfamily/)
   and lands as one node.
2. Set **COMP** to the component that owns the sequence. References resolve
   from SeqMod itself: a bare name such as `geo1` is a sibling of SeqMod, `..`
   (the default) is the network SeqMod sits in, and something inside SeqMod
   needs `./name`.
3. Set **Seq Name** to the part of the parameter names before the block index:
   `Items` for `Items0name`, `Items1name` and so on. Empty publishes nothing.
4. Read the result. **ParNames** lists every block parameter as a pattern,
   `Items*name Items*level`, and is republished whenever blocks are added or
   removed. `out1` carries the same as a table: a row per block parameter,
   such as `Items_name`, followed by its value in each block.

**ParNames** is written for the Parameters field of a Parameter DAT, which is
how SeqMod builds `out1` itself. Reference it from your own Parameter DAT, for
example with the expression `op('seqMod1').par.Parnames`, and that DAT follows
the sequence as it changes.

From Python, the placed SeqMod also exposes `Comp` (the target COMP), `Seq`
(the watched sequence, or `None` while either parameter is unset) and
`SeqParNames`, the dependable behind **ParNames**.

## Callbacks

Press **Create Callbacks** to get an editable callbacks DAT; **Callbacks** is
pointed at it. Until then SeqMod uses a built-in template that does nothing.
The DAT reference follows the same rule as **COMP**: a bare name is a sibling
of SeqMod, a DAT inside it needs `./name`.

The DAT has two hooks, called once per block:

- `OnAddBlock(seqBlock)`: a block was added; `seqBlock` is the new block. When
  several arrive at once, it runs for each, lowest index first.
- `OnRemoveBlock(seqBlock_idx)`: a block was removed; you get the index it had,
  since the block itself is gone. Several at once run from the highest index
  down.

```python
def OnAddBlock(seqBlock):
	debug(f'block {seqBlock.index} added on {seqBlock.owner.path}')

def OnRemoveBlock(seqBlock_idx):
	debug(f'block {seqBlock_idx} removed')
```

Retargeting the tool to another COMP or sequence does not fire them. Errors
raised inside a callback are reported on SeqMod itself.
