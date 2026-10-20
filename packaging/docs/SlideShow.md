---
package: SlideShow
summary: 'A slideshow of a folder of images and movies: timed or stepped with next and previous, in order or random, moving on when a movie ends, with a crossfade between slides and a fitted output resolution.'
features:
  - name: What it is
    anchor: what-it-is
  - name: Movies
    anchor: movies
  - name: Output
    anchor: output
feature_list:
  - name: Play a folder of images and movies
    anchor: what-it-is
    does: 'Point it at a folder and it plays the images and movies in it, each fitted to the output resolution.'
  - name: Move on when a movie ends
    anchor: movies
    does: 'Auto-Skip on Done goes to the next slide when a movie reaches its end, without waiting for Period.'
  - name: Timed or stepped playback
    anchor: what-it-is
    does: 'A Period advances slides by itself; with Period at zero, Next and Prev step through them.'
  - name: Random order
    anchor: what-it-is
    does: Random shuffles the order and draws a new shuffle each time the folder has been played through.
  - name: Crossfade between slides
    anchor: what-it-is
    does: Every change crossfades from the old slide to the new one on the out1 TOP.
---

## What it is

Point SlideShow at a folder and it plays the images and movies in it. Give it a Period and it moves on by itself; set the Period to zero and step through with Next and Prev. Random shuffles the order and draws a new shuffle each time the folder has been played through. Every change crossfades from the old slide to the new one, and each image is fitted to the output resolution.

It is a member of the FNS operator family: pick it from the **FNS** tab of the OP Create dialog and it lands as one node.

## Movies

A movie plays from its start each time it comes up, and only the slide on screen plays. With **Auto-Skip on Done** on, the show moves to the next slide as soon as the movie reaches its end, so a folder of clips plays through at their own lengths; Period still applies to stills and to movies longer than it. The default folder is TouchDesigner's own sample movies, so the tool shows something the moment it is placed.

## Output

- **out1** (TOP): the current slide, crossfading into the next.
