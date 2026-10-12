# Steam Integration Plugin for GOG Galaxy 2.1+ (64-bit)

This plugin imports your Steam library into GOG Galaxy 2.1+ 64-bit. Based on the original community integration, it has been updated for the current GOG Galaxy client and Python 3.13, with improved support for large libraries.

The steps below are for Windows. Dependencies are bundled; no separate Python installation is needed.

[Installation](#-installation) | [First Start](#-first-start-and-initial-sync) | [Troubleshooting](#-troubleshooting) | [Support & Feedback](#-support--feedback)

## ✨ Features

* Imports your owned Steam games into GOG Galaxy
* Links owned DLCs to their parent games
* Syncs base-game and DLC achievements through Steam's current Player service
* Syncs game time
* Detects locally installed Steam games
* Launches, installs, and uninstalls games through Steam
* Processes large Steam license sets in bounded batches

> [!NOTE]
> macOS compatibility may be technically possible, but it is currently untested because I do not have access to a Mac. If you use macOS and would like to help test the integration, feel free to contact me.

## 📦 Installation

### 🔄 Automatic Installation with Plugin Updater (Recommended)

Use the [melcom GOG Galaxy Plugin Updater](https://github.com/melcom-creations/galaxy-integrations-64bit/tree/main/tools/melcom-galaxy_plugin_updater) to install or update the integration.

1. Download and extract the Plugin Updater.
2. Double-click `update-plugins.bat`.
3. Select your preferred language and follow the displayed instructions.

When installing the Steam integration, the updater can also offer optional automatic startup support for [Steam Achievement Notifier](https://github.com/SteamAchievementNotifier/SteamAchievementNotifier).

### 📂 Manual Installation

1. Close GOG Galaxy completely, including the system tray application.
2. Download the [latest release package](https://github.com/melcom-creations/galaxy-integration-steam/releases/latest).
3. Extract the plugin folder from the ZIP archive into:

   ```text
   %localappdata%\GOG.com\Galaxy\plugins\installed\
   ```

Place `manifest.json` directly inside this folder, without an extra nested plugin folder:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\steam_ca27391f-2675-49b1-92c0-896d43afa4f8\
```

> [!IMPORTANT]
> Do not place backup copies of this plugin inside the `plugins\installed` directory. GOG Galaxy scans every folder inside this directory during startup, so duplicate plugin folders can cause GUID conflicts or load an outdated version.

**Next step:** Continue with [First Start and Initial Sync](#-first-start-and-initial-sync).

## 🚀 First Start and Initial Sync

For the first synchronization after installing or updating the plugin:

1. Start Steam and keep it open.
2. Start GOG Galaxy.
3. Connect the Steam integration through **Settings -> Integrations** if necessary.
4. Open the account menu in the top-right corner and select **Sync integrations**.
5. Wait until the synchronization has finished.

Achievement and game-time imports run in the background. Large libraries can take several minutes to finish even after Galaxy accepts the synchronization request. Missing or unsuccessful Steam achievement responses are retried automatically, with up to three attempts per AppID. If those attempts fail, previously confirmed results from the current session are retained; games without confirmed data report an import timeout and can be retried with another synchronization.

## ⚠️ Known Limitations

### 🏆 Achievement Metadata Depends on GOG Galaxy Servers

The Steam integration can import and sync unlocked achievements, but achievement metadata such as names, descriptions, icons, and total counts is provided by GOG Galaxy backend services.

If GOG has not yet updated this metadata for newer DLCs or game updates, achievements may not immediately appear correctly in the Galaxy interface even when the plugin import has completed successfully.

No plugin action is usually required. The display updates after GOG refreshes the achievement metadata on its servers.

## 🛠️ Troubleshooting

Restart Galaxy and the store app and try one synchronization. If the problem remains, collect a fresh log. A database reset is not required for this.

### 🧪 Create a Fresh Diagnostic Log

1. Close GOG Galaxy completely, including the system tray application.
2. Open `%ProgramData%\GOG.com\Galaxy\logs\`. Move the existing `plugin-steam-ca27391f-2675-49b1-92c0-896d43afa4f8.log` to a backup folder outside this directory, if present. Leave other logs in place.
3. Start Steam. Start Galaxy, reproduce the problem once, then close Galaxy completely to finish writing the log.
4. Send the newly created plugin log, not the entire folder. Include the plugin and Galaxy versions, your steps, the expected and actual result, and whether the problem can be reproduced.

See [Support & Feedback](#-support--feedback) for contact options.

### 🔄 Reset Plugin Storage (Last Resort)

Use this only if restarting and synchronizing do not help, or when requested for troubleshooting. Cached library data and local playtime may be lost; signing in again may be required. Keep the backup.

1. Close GOG Galaxy completely, including the system tray application.
2. Open `%ProgramData%\GOG.com\Galaxy\storage\plugins\`.
3. Find the active `steam_...-storage.db` file for your Galaxy account. If unsure which file is correct, stop. Leave other integrations' databases unchanged.
4. Append `.old` to its name. If that backup already exists, use an unused suffix; never overwrite it.
5. Start Steam. Start Galaxy, reconnect if necessary, and select **Sync integrations** once. Wait until it finishes.

To undo: close Galaxy, rename the new database to an unused backup name, then restore the saved database's original name. Never restore it while Galaxy is running.

## 🙏 Credits

**Original Community Integration**  
Friends of Galaxy  
[Friends of Galaxy Steam integration](https://github.com/FriendsOfGalaxy/galaxy-integration-steam)

**Authorization Flow Contributions**  
ABaumher  
[ABaumher on GitHub](https://github.com/ABaumher)

**64-bit Port, Maintenance and Improvements**  
melcom

## 📚 References

This integration is based on and inspired by several open-source projects and community resources.

* [SteamKit](https://github.com/SteamRE/SteamKit)
* [ValuePython/steam](https://github.com/ValuePython/steam)
* [prncc/steam-scraper](https://github.com/prncc/steam-scraper)
* [rhaarm/steam-scraper](https://github.com/rhaarm/steam-scraper)
* [mulhod/steam_reviews](https://github.com/mulhod/steam_reviews)
* [summersb92/aeolipile](https://github.com/summersb92/aeolipile)
* [rcpoison/steam-scraper](https://github.com/rcpoison/steam-scraper)
* [chmccc/steam-scraper](https://github.com/chmccc/steam-scraper)

## ❤️ Special Thanks

I want to take a moment to thank the people who kept me going during this intense development phase:

* A huge thank you to my friend [**Hustlefan**](https://www.gog.com/u/Hustlefan). Over the past few days, you've been much more than just moral support. You gave me the encouragement I needed, patiently put up with all my Discord spam, and helped beta test the plugins. I'm really happy that you're pleased with the results. Thanks so much for all your support, my friend.

* And a big thank you to my girlfriend [**Florence H.** (fl0H0815)](https://www.gog.com/u/Florence_Heart). While she was enjoying the good life at her parents' place - complete with air conditioning and a huge swimming pool - she kept my spirits up by sending me photos of herself, her friends, her parents, and even her parents' dog. She reminded me that there's a wonderful world outside of a code editor every now and then... 🙈

  *Now that's what I call real support.* ❤️

* A special thank you to GOG community member [**nickpeyon**](https://www.gog.com/u/nickpeyon), with whom I had extensive email conversations. Your massive Steam game collection helped inspire the direction for several of the large-library improvements in this project.

Thank you all for having my back!

## 🤝 Support & Feedback

**GitHub Issues are intentionally disabled.** Health-related limitations prevent me from reliably managing separate issue trackers across all of my plugin repositories.

Before contacting me, follow [Troubleshooting](#-troubleshooting) and prepare a fresh Steam plugin log with a detailed description.

* **GOG:** Send me a message or add me as a friend through my [GOG profile](https://www.gog.com/u/melcom).
* **Email:** `melcom @ gmx.net`
* **Discord:** `.melcom` - the leading dot is part of the username. You can send me a message or add me as a friend.

Logs can be attached directly or shared through Dropbox or OneDrive. Response times may vary depending on my health and available development time. Thank you for your understanding.
