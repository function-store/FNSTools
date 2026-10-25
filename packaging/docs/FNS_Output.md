---
package: FNS_Output
summary: Drag and drop an operator to set it as the Window Operator of the /perform Window.
features:
  - name: Why use it
    anchor: why-use-it
    icon: PerformTools.png
  - name: How to use it
    anchor: how-to-use-it
  - name: Streaming the output
    anchor: streaming-the-output
  - name: Driving another window
    anchor: driving-another-window
feature_list:
  - name: Drop to set the Window Operator
    anchor: how-to-use-it
    does: 'Dropping a TOP or a COMP on the toolbar button makes it the Window Operator of the /perform window, without opening the Window COMP''s parameters.'
  - name: Open the perform window
    anchor: how-to-use-it
    does: Left-clicking the button opens the perform window.
  - name: NDI streaming
    anchor: streaming-the-output
    does: 'The right-click popup streams the perform window over NDI to machines on the same network, under NDI Source Name; on by default.'
  - name: Spout and Syphon streaming
    anchor: streaming-the-output
    does: 'The same popup sends the perform window to other applications on the machine over Spout, or Syphon on macOS, under Sender Name; on by default.'
  - name: Toggle streams from quick-launch
    anchor: streaming-the-output
    does: Switch the NDI and Spout/Syphon streams on and off from quick-launch.
  - name: Choose the Window COMP
    anchor: driving-another-window
    does: 'The button''s Perform parameter sets which Window COMP the drop and the click go to, taking effect on the next drop with nothing to re-install.'
---

## Why use it

Putting something on the projector in TouchDesigner means opening the
`/perform` Window COMP, finding its Window Operator parameter and dragging your
output into it, and again every time you want to show something else.
Streaming the same picture to another application or another machine is a
second set of operators to add and wire.

Output puts all of that on one toolbar button. Drop an operator on it to send
it to the perform window, click it to open the window, and switch NDI and
Spout or Syphon streaming of the same picture from its popup.

## How to use it

1. Drag a TOP or a COMP from the network editor onto the toolbar button. It
   becomes the **Window Operator** of the `/perform` window, with no trip into
   the Window COMP's parameters.
2. Left-click the button to open the perform window.
3. Right-click the button for the configuration popup, which holds the
   switches for streaming.

To change what is on screen, drop another operator on the button.

## Streaming the output

The popup streams the picture `/perform` shows to other software, and both
streams ship switched on.

- **Spout** on Windows, **Syphon** on macOS, sends it to other applications on
  the same machine, such as a projection-mapping tool or a video mixer. They
  see it under **Sender Name**; change the name when two TouchDesigner
  instances would otherwise publish the same one.
- **NDI** sends it to machines on the same network, under **NDI Source Name**.
  Give each machine an identifiable name when several of them stream.

**Toggle NDI output** and **Toggle Spout/Syphon output** in quick-launch switch
the same streams.

## Driving another window

The drop and the left-click go to the Window COMP named on the **Perform**
parameter of the button itself (`button_perform` inside the tool, parent
shortcut `Main`), which is `/perform` unless you change it. Pointing it at
another Window COMP takes effect on the next drop, with nothing to re-install.
The NDI and Spout/Syphon streams follow `/perform`.
