---
package: TopToMidi
summary: 'Samples an image at points you define and turns the pixel values into MIDI notes in a musical scale: index or value mapping, trigger gating and retrigger control, custom and MIDI-learned scales, output to a MIDI Out or Audio VST CHOP.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Your own scales and playing along
    anchor: your-own-scales-and-playing-along
  - name: Installing mingus
    anchor: installing-mingus
  - name: Inputs and outputs
    anchor: inputs-and-outputs
feature_list:
  - name: Sample an image at points
    anchor: how-to-use-it
    does: 'A SOP''s points or a TOP''s pixels say where the input image is read, and each sample point becomes a note.'
  - name: Index mode
    anchor: how-to-use-it
    does: 'Each sample point plays its own note whenever its pixel passes the threshold, so a pattern sweeping across the picture plays an arpeggio.'
  - name: Value mode
    anchor: how-to-use-it
    does: 'The pixel''s brightness picks the note, quantised to a number of steps.'
  - name: Scale mapping
    anchor: how-to-use-it
    does: 'Maps every note into a scale from a root note and octave, from major and minor to the church modes.'
  - name: Trigger gating
    anchor: how-to-use-it
    does: 'Gate lengths, a minimum sustain and a retrigger delay keep a busy picture from spraying notes.'
  - name: Custom scales
    anchor: your-own-scales-and-playing-along
    does: Type your own scales into a table and they join the Scale menu.
  - name: Learn a scale from a MIDI keyboard
    anchor: your-own-scales-and-playing-along
    does: 'With MIDI Scale Learn on, the notes you play one by one become the scale.'
  - name: Play along on a MIDI keyboard
    anchor: your-own-scales-and-playing-along
    does: 'With MIDI Live on, the scale follows the keys you hold, so you can duet with the picture.'
  - name: Send notes to MIDI Out or a VST
    anchor: how-to-use-it
    does: 'Sends the notes to a MIDI Out CHOP, an Audio VST CHOP or both, and outputs them as a CHOP for anything else.'
  - name: Sampling preview
    anchor: how-to-use-it
    does: 'Shows the sample points over the image in a window where you can drag, scale and reset them.'
  - name: Install the mingus dependency
    anchor: installing-mingus
    does: 'Install mingus writes a requirements file and hands it to the Python Environment Manager, which installs it into the linked environment in the background.'
---

## Why use it

Turning an image into music in TouchDesigner usually means a TOP to CHOP, some
maths to turn brightness into note numbers, a lookup that keeps those notes in
a key, and a CHOP Execute DAT that sends note-ons and note-offs without leaving
any hanging. Each part is simple. Together they are an afternoon, and the
note-off bookkeeping is where it tends to go wrong.

TopToMidi plays your visuals. You decide where the image is read, with a SOP's
points or a TOP's pixels, and every sample point becomes a note in the scale
you choose. The notes go to a MIDI Out CHOP, an Audio VST CHOP or both, and
also come out as a CHOP for anything else.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog and wire the image
   into its input.
2. Look at **Status** on the Setup page. Every scale except MIDI Scale needs
   the Python package mingus; if Status says it is missing, see
   [Installing mingus](#installing-mingus).
3. Set **Sampler** to a SOP or a TOP that says where to read the image, for
   example a Grid SOP for a regular grid of points. Many SOPs sit around the
   origin, and **Offset 0.5** moves them onto the image. Pulse **Sample
   Preview** to see the points over the picture and drag them into place.
4. Pick a **Mapping Mode**:
   - **Index**: each sample point plays its own note while its pixel passes
     **Threshold**, so a bright bar sweeping across a grid plays an arpeggio.
     **Steps** follows the number of points, so keep the count modest: MIDI
     has 128 notes.
   - **Value**: the brightness at each point picks the note, quantised to
     Steps. Two points with the same value play the same note. Keep
     **Re-Range** on in this mode.
5. Choose the music on the Scale page: **Scale**, **Key** and **Octave**. With
   more steps than the scale has notes, **Extend Mode** carries on into the
   octaves above.
6. Send the notes. Drop a MIDI Out CHOP beside the tool and name it in **MIDI
   Out CHOP**, or name an Audio VST CHOP in **VST CHOP** and switch on **VST
   Active**. Reference the CHOP itself, with no Null after it.

Notes are only worked out while a MIDI Out or VST CHOP is set or the outputs
are wired, so a copy with nothing attached does no note work.

A few things people adjust once it plays:

- **A busy picture sprays notes:** the Trigger Options on the Input page are
  for this. **Trigger Gate Length** makes a point stay above the threshold for
  a moment before its note starts, **Re-Trigger Delay** stops one note
  repeating too fast, and **Min Sustain Length** keeps short notes audible.
- **Velocity by pitch:** point **Keytrack Lookup** at a multi-sample CHOP and
  it sets how hard each note plays from its pitch.
- **A note hangs:** run **All Notes Off** from quick-launch. It sends a
  note-off for every note on the MIDI and VST outputs.

## Your own scales and playing along

- **Your own scale:** pulse **Edit Custom Scales**. A table opens where each
  column is one scale, its name on top and its notes below in standard
  notation, such as `C#3`. Your scales then show up in the **Scale** menu.
- **A scale from your keyboard:** set **Scale** to MIDI Scale, name a MIDI In
  CHOP in **MIDI In CHOP**, switch on **MIDI Scale Learn** and play the notes
  of the scale one by one.
- **Duet with the picture:** with **MIDI Live** on, the scale follows the keys
  you are holding right now, so the picture plays in whatever chord your hands
  are on. **Live Octave Offset** moves it above or below them, and **Sync
  Steps** matches the number of steps to the number of keys held (not
  available while Extend Mode is on).

MIDI learning runs only while a MIDI In CHOP is set.

## Installing mingus

Every scale except MIDI Scale is computed with the Python package mingus,
which TouchDesigner does not bundle. The tool ships its own pip requirements
file (the `requirements` DAT inside it) and installs it through TouchDesigner's
Python Environment Manager. The Setup page's **Status** says whether mingus is
available. When it is missing:

- With a Python vEnv or Conda environment linked through the Python
  Environment Manager, pulse **Install mingus**, or run **Install Mingus** from
  quick-launch. The tool writes `TopToMidi.requirements.txt` beside your .toe
  and hands it to the environment manager, which installs it into the linked
  environment in the background; Status reports the result. When the project
  has an environment context file, the requirements file is also registered in
  it, so a machine that opens the project with Auto Setup On Startup installs
  it on its own.
- With no environment, create one in the Python Environment Manager (palette:
  tdPyEnvManager), then pulse **Install mingus**. **Python Env Manager Help**
  opens its documentation.
- If you installed mingus some other way, pulse **Re-check**.

Nothing blocks TouchDesigner while this happens, and the tool never installs
anything until you ask. If Status says mingus is installed but this session
cannot see it yet, restart TouchDesigner.

## Inputs and outputs

- **in2** (TOP): the image to sample.
- **out_viz** (TOP): the sampling points drawn over the input.
- **out_sampled** (TOP) and **out_sampled_CHOP** (CHOP): the sampled values.
- **out_notes** (CHOP): the generated notes.
