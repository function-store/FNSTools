---
package: SlideShow
summary: 'A slideshow of a folder of images and movies: timed or stepped with next and previous, in order or random, moving on when a movie ends, with a crossfade between slides and a fitted output resolution.'
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
  - name: Movies
    anchor: movies
  - name: Output
    anchor: output
feature_list:
  - name: Play a folder of images and movies
    anchor: how-to-use-it
    does: 'Point it at a folder and it plays the images and movies in it, each fitted to the output resolution.'
  - name: Timed playback
    anchor: how-to-use-it
    does: Period advances the slides by itself, in seconds per slide.
  - name: Step through slides
    anchor: how-to-use-it
    does: 'With Period at zero, Next and Prev step through the slides, from a button, a key or a MIDI note.'
  - name: Jump to a slide
    anchor: how-to-use-it
    does: Select goes straight to a slide.
  - name: Random order
    anchor: how-to-use-it
    does: Random shuffles the order and draws a new shuffle each time the folder has been played through.
  - name: Crossfade between slides
    anchor: how-to-use-it
    does: Every change crossfades from the old slide to the new one on the out1 TOP.
  - name: Move on when a movie ends
    anchor: movies
    does: 'Auto-Skip on Done goes to the next slide when a movie reaches its end, without waiting for Period.'
---

## Why use it

A folder of images on a loop sounds like the simplest job in TouchDesigner
until you build it: a Folder DAT to list the files, a Movie File In TOP to load
them, a timer to step through, a second Movie File In and a Cross TOP for the
fade, and a Fit TOP so every picture lands at the same size. Movies bring their
own rules on top: start from the beginning, move on when they end.

SlideShow is all of that in one node. Point it at a folder of images and movies
and it plays them, timed or stepped, in order or shuffled, with a crossfade
between slides. It is a quick way to fill a lobby screen, a backdrop between
sets, or the second output while you work on the first.

## How to use it

1. Create it from the **FNS** tab of the OP Create dialog. It starts on
   TouchDesigner's own sample movies, so it shows something the moment it is
   placed.
2. Set **Folder** to your own folder. Every slide is fitted to **Res**, 1920 by
   1080 unless you set it.
3. Choose how it moves on:
   - **Timed:** **Period** is the number of seconds per slide.
   - **Stepped:** set Period to 0 and step with **Next** and **Prev**, from a
     button, a key or a MIDI note. Next and Prev also work while a Period
     runs; they restart the count, so the slide you step to gets its full time.
   - **Straight to a slide:** set **Select**.
4. Switch on **Random** for a shuffled order. A new shuffle is drawn each time
   the folder has played through, and it never starts on the slide just shown.
   Switching Random off carries on in order from the slide on screen.
5. Set the fade with **Crossfade Opacity**: the higher it is, the longer the
   previous slide lingers.

## Movies

A movie plays from its start each time it comes up, and only the slide on
screen plays. With **Auto-Skip on Done** on, the show moves to the next slide
as soon as the movie reaches its end, so a folder of clips plays through at
their own lengths. Period still applies to stills and to movies longer than it.

## Output

- **out1** (TOP): the current slide, crossfading into the next.
