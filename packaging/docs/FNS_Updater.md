---
package: FNS_Updater
summary: Clicking this icon will open this Wiki page.
features:
  - name: Wiki
    anchor: wiki
    icon: Wiki.png
  - name: Self-Update Feature
    anchor: self-update-feature
  - name: Notes after an update
    anchor: notes-after-an-update
feature_list:
  - name: Update indicator on the help icon
    anchor: wiki
    does: 'The toolbar ? icon gets a yellow border when any installed package has an update; clicking it prompts to update, otherwise it opens the wiki.'
  - name: Update only changed packages
    anchor: self-update-feature
    does: 'Fetches only the packages that changed from the store, verifies each download''s hash and replaces just those, leaving uninstalled packages uninstalled.'
  - name: Settings kept across updates
    anchor: self-update-feature
    does: Saves all tool configs to a JSON file before updating and reloads each replaced tool's saved configs afterwards.
  - name: Release notes after an update
    anchor: notes-after-an-update
    does: 'Shows that release''s notes once on the first project open after an update; Show Notes After Update turns it off, and Hub''s Updates tab keeps them.'
---

## Wiki

Clicking this icon will open this Wiki page. If the border of this icon is yellow it means one or more of your installed packages have an update available. Clicking it in that state will prompt you for an update.

## Self-Update Feature

If there is an update available for any package installed in your project, the `?` icon in the toolbar will have a yellow border. Clicking the icon will prompt you for an update, you can say `No` in which case it will take you to the Wiki as usual, otherwise the following is going to happen:
- Save all configs (custom parameters of tools) to a `json` file
- Fetch only the packages that actually changed from the store (verifying each download's hash), and replace just those; a package you never installed stays uninstalled
- Reload each replaced tool's saved configs

This way we can ensure that your settings are retained between updates, alongside the externally retained data, outlined in the next chapter.

## Notes after an update

The first time a project opens after an update landed, a small popup shows that release's notes. It appears once per update, never on a plain project open.

Turn off **Show Notes After Update** on the updater's parameters to skip it. The setting roams with your other toolkit settings, so one click silences the popup in every project on the machine. The notes stay readable at any time on the Hub's Updates tab.
