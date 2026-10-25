---
package: FNS_HydroHomie
summary: This toolbar icon reminds you to drink water every 45 minutes (can be changed)
features:
  - name: Why use it
    anchor: why-use-it
  - name: How to use it
    anchor: how-to-use-it
feature_list:
  - name: Drink water reminder
    anchor: how-to-use-it
    does: 'A small alert icon pulses on the toolbar at each interval, 45 minutes by default; click it away until the next one.'
  - name: Set your own interval
    anchor: how-to-use-it
    does: 'Set the minutes between reminders, from the parameters or from quick-launch.'
  - name: Enable at project start
    anchor: how-to-use-it
    does: 'With On Start Active on, the reminders start as soon as the project opens.'
  - name: Quiet during a show
    anchor: how-to-use-it
    does: While FNSTools Perform Mode is on the reminder neither animates nor pops up.
---

## Why use it

Hours disappear in a TouchDesigner session, and the glass of water next to
the keyboard stays full. HydroHomie puts a small reminder on the toolbar at a
regular interval, so you take a few sips before you carry on.

## How to use it

1. HydroHomie is off when you install it. Right-click its toolbar icon to
   open its parameters and switch on **Enable**.
2. After 45 minutes, or the interval you set, a small alert icon pulses on
   the toolbar. Click it and it goes away until the next reminder; the
   countdown starts again from there.

- **To change how often,** set **Interval minutes**, or run **Set HydroHomie
  interval** from quick-launch.
- **To have it running whenever the project opens,** switch on **On Start
  Active**.
- **To stop the reminders,** switch **Enable** off again in the same place.

While FNSTools
[Perform Mode](/docs/guides/working-in-your-project/#performing-a-show) is
on, the reminder neither animates nor pops up, and one that comes due starts
its interval over.
