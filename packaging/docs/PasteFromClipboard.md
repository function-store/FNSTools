---
package: PasteFromClipboard
summary: Copy an image to your clipboard and paste it straight into TouchDesigner with Alt+V.
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Pasting image files
    anchor: pasting-image-files
platforms:
  - windows
hotkeys:
  - keys: alt.v
    does: 'Paste the clipboard image into the current network, then press 1, 2 or 3 to pick how'
feature_list:
  - name: Paste a clipboard image
    anchor: how-to-use-it
    does: '`Alt+V` pastes the image on the clipboard into the current network, at the mouse, with three ways to paste on the keys `1`, `2` and `3`.'
    platform: Windows only
  - name: Paste as Movie File In
    anchor: how-to-use-it
    does: 'Saves the image in the tool''s Save Folder, clipboard_images by default, and reads it with a Movie File In.'
    platform: Windows only
  - name: Paste as locked Script TOP
    anchor: how-to-use-it
    does: 'Stores the image in a locked Script TOP, which grows the .toe file but avoids external dependencies.'
    platform: Windows only
  - name: Paste as annotation
    anchor: how-to-use-it
    does: 'Pins the image in the network as an annotation the size of the image, kept inside the .toe like the Script TOP.'
    platform: Windows only
  - name: Paste image files
    anchor: pasting-image-files
    does: 'Image files copied in Explorer paste from the original files, several at once, laid out in a row.'
    platform: Windows only
---

## Why use it

A reference image, a screenshot of a bug, a texture from a browser: getting it
into TouchDesigner usually means saving it somewhere, finding the file again,
and dragging it in or browsing to it from a Movie File In.

PasteFromClipboard skips the file juggling. Copy the image, press `Alt+V` in the
network, and pick how it should land. It was implemented by
[DotSimulate](https://www.patreon.com/c/dotsimulate) and
[Lake Heckaman](https://www.patreon.com/cw/water__shed), and integrated by
Function Store.

## How to use it

1. Copy an image: from a browser, a screenshot tool, an image editor, or image
   files selected in Explorer.
2. Point the mouse at the spot in the network editor where the image should go
   and press `Alt+V`.
3. Pick one of three options with its key, or press `Esc` to cancel:
   - `1` pastes it as a **Movie File In**. The image is also saved in the folder
     set by the tool's **Save Folder** parameter (`clipboard_images` by
     default), and the Movie File In reads it from there.
   - `2` pastes it as a **locked Script TOP**, with the pixels stored in the
     `.toe`.
   - `3` pastes it as an **annotation** the size of the image, with a
     transparent background, holding the image the same way as the Script TOP.
     Handy for pinning a reference or a sketch beside the part of the network
     it belongs to.

The new operator lands at the mouse while **Position at Mouse** is on, which it
is out of the box.

Options `2` and `3` produce a locked TOP, which increases your `.toe` file size
but avoids external dependencies. Option `1` keeps the `.toe` small, and the
project then needs the image folder wherever it goes.

To skip the menu, run **Paste image**, **Paste as Script TOP** or **Paste as
annotate** from quick-launch.

PasteFromClipboard is Windows only: it reads the Windows clipboard directly. On
macOS it switches itself off, and its **Status** says why. If you know a native
macOS route that needs no external Python libraries, let us know.

## Pasting image files

Image files copied in Explorer reach the clipboard as files, so PasteFromClipboard
uses the original files themselves, alpha included.

- Several files paste as several operators, laid out in a row.
- With `1`, each file is copied into the Save Folder first, so the Movie File In
  keeps working if the original moves. Switch off **Copy Pasted Files** to read
  the originals where they are.
- With `2` and `3`, a file that cannot be decoded, such as a PSD, a DDS or an
  EXR without its codec, is skipped, and the status bar names it and suggests
  pasting it as a File In.
- Anything in the selection that is not an image file is ignored.
