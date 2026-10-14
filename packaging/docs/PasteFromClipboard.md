---
package: PasteFromClipboard
summary: Copy an image to your clipboard and paste it directly in TD with alt+v shortcut
features:
  - name: Clipboard Image Paste
    anchor: clipboard-image-paste
platforms:
  - windows
feature_list:
  - name: Paste a clipboard image
    anchor: clipboard-image-paste
    does: 'Pastes the clipboard image into the current network, offering three ways to paste on the keys 1, 2 and 3.'
    platform: Windows only
  - name: Paste as Movie File In
    anchor: clipboard-image-paste
    does: 'Creates a Movie File In and saves the image in the tool''s Save Folder, clipboard_images by default.'
    platform: Windows only
  - name: Paste as locked Script TOP
    anchor: clipboard-image-paste
    does: 'Stores the image in a locked Script TOP, which grows the .toe file but avoids external dependencies.'
    platform: Windows only
  - name: Paste as annotation
    anchor: clipboard-image-paste
    does: 'Pastes the image as an annotation; like the Script TOP option, it produces a locked TOP kept inside the .toe.'
    platform: Windows only
---

## Clipboard Image Paste

> Windows only! Implemented by [DotSimulate](https://www.patreon.com/c/dotsimulate) and [Lake Heckaman](https://www.patreon.com/cw/water__shed), integrated by Function Store

Copy an image to your clipboard and paste it directly in TD with `alt+v` shortcut  
   - You will be met with three options (hotkeys **1,2,3**): 🟢 Paste as **Movie File In**, 🔵 Paste as **locked Script TOP**, 🟠 Paste as **Annotate**  
   - When pasting as Movie File, the image also gets saved in the folder specified by the tool's own **Save Folder** parameter (default: `clipboard_images`) 📂  
   - The other two options will produce a locked TOP which increases your `.toe` file size but avoids external dependencies  
   - ❗ **WINDOWS ONLY**. If anyone knows of a native Mac solution (not using external Python libs), let us know!  
