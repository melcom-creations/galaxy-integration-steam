# Steam Integration Plugin for GOG Galaxy 2.1+ (64-bit)

This plugin imports your Steam library into GOG Galaxy 2.1+ 64-bit. Based on the original community integration, it has been updated for the current GOG Galaxy client and Python 3.13, with improved support for large libraries.

---

## ✨ Features

* Imports your owned Steam games into GOG Galaxy
* Syncs achievements and game time
* Detects locally installed Steam games
* Launches, installs, and uninstalls games through Steam
* Includes improved handling for large Steam libraries

---

## 📦 Installation

### Automatic Installation with Plugin Updater (Recommended)

Use the [melcom GOG Galaxy Plugin Updater](https://github.com/melcom-creations/galaxy-integrations-64bit/tree/main/tools/melcom-galaxy_plugin_updater) to install or update the integration automatically.

1. Download and extract the Plugin Updater.
2. Double-click `update-plugins.bat`.
3. Select your preferred language.
4. Follow the displayed instructions.

When installing the Steam integration, the updater can also offer optional automatic startup support for [Steam Achievement Notifier](https://github.com/SteamAchievementNotifier/SteamAchievementNotifier).

### Manual Installation

1. Close GOG Galaxy completely, including the system tray application.
2. Download the latest release package from this repository.
3. Extract the ZIP archive directly into:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
```

The resulting directory structure must look like this:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
└── steam_ca27391f-2675-49b1-92c0-896d43afa4f8\
    ├── manifest.json
    ├── plugin.py
    ├── README.md
    └── ...
```

4. Continue with **First Start and Initial Sync** below.

> [!IMPORTANT]
> Do not place backup copies of this plugin inside the `plugins\installed` directory. GOG Galaxy scans every folder inside this directory during startup, so duplicate plugin folders can cause GUID conflicts or load an outdated version.

---

## 🚀 First Start and Initial Sync

For the first synchronization after installing or updating the plugin:

1. Start Steam and keep it open.
2. Start GOG Galaxy.
3. Connect the Steam integration through **Settings -> Integrations** if necessary.
4. Open the account menu in the top-right corner and select **Sync integrations**.
5. Wait until the synchronization has finished.

---

## ⚠️ Known Limitation

### Achievement Metadata Depends on GOG Galaxy Servers

The Steam integration can import and sync unlocked achievements, but achievement metadata such as names, descriptions, icons, and total counts is provided by GOG Galaxy backend services.

If GOG has not yet updated this metadata for newer DLCs or game updates, achievements may not immediately appear correctly in the Galaxy interface even when the plugin import has completed successfully.

No plugin action is usually required. The display updates after GOG refreshes the achievement metadata on its servers.

---

## 🔄 Resetting the Plugin Database (Troubleshooting)

Reset the local plugin database if synchronization problems continue after restarting both applications.

1. Close GOG Galaxy completely.
2. Open `C:\ProgramData\GOG.com\Galaxy\storage\plugins\`.
3. Find every file starting with `steam_` and ending in `-storage.db`.
4. Rename each matching file by appending `.old`, for example:

   `steam_xxxxxxxxx-storage.db` -> `steam_xxxxxxxxx-storage.db.old`

5. Start Steam and keep it open.
6. Start GOG Galaxy, reconnect the integration if necessary, select **Sync integrations** from the account menu, and wait for synchronization to finish.

---

## 🛠️ What to Do If the Plugin Has Problems

If the database reset above does not resolve the problem, create a clean session with fresh diagnostic files before contacting me. The reset procedure preserves the previous database as a `.old` file; the steps below remove the active database so the issue can be reproduced from a clean state.

1. Close GOG Galaxy completely, including the system tray application.
2. Open the following directory and delete the existing log files:

   ```text
   %ProgramData%\GOG.com\Galaxy\logs
   ```

3. Open the plugin storage directory:

   ```text
   C:\ProgramData\GOG.com\Galaxy\storage\plugins
   ```

   Delete only the active Steam database file starting with `steam_` and ending in `-storage.db`. Do not delete database files belonging to other integrations. If you are unsure which file is correct, do not delete anything from this directory.
4. Start Steam and keep it open. Start GOG Galaxy, reproduce the problem, and then close GOG Galaxy completely so the new log is fully written.
5. Return to the logs directory and locate the newly created Steam plugin log:

   ```text
   plugin-steam-ca27391f-2675-49b1-92c0-896d43afa4f8.log
   ```

Send only this log file, not the entire logs folder. Include the exact steps taken, the expected and actual result, and whether the problem can be reproduced.

Without a fresh plugin log and a detailed description, I cannot reliably determine what is causing the problem. Once everything is ready, continue with [Support & Feedback](#-support--feedback) for contact options.

---

## 🙏 Credits

**Original Community Integration**  
Friends of Galaxy  
[Friends of Galaxy Steam integration](https://github.com/FriendsOfGalaxy/galaxy-integration-steam)

**Authorization Flow Contributions**  
ABaumher  
[ABaumher on GitHub](https://github.com/ABaumher)

**64-bit Port, Maintenance and Improvements**  
melcom

---

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

---

## ❤️ Special Thanks

I want to take a moment to thank the people who kept me going during this intense development phase:

* A huge thank you to my friend [**Hustlefan**](https://www.gog.com/u/Hustlefan). Over the past few days, you've been much more than just moral support. You gave me the encouragement I needed, patiently put up with all my Discord spam, and helped beta test the plugins. I'm really happy that you're pleased with the results. Thanks so much for all your support, my friend.

* And a big thank you to my girlfriend [**Florence H.** (fl0H0815)](https://www.gog.com/u/Florence_Heart). While she was enjoying the good life at her parents' place - complete with air conditioning and a huge swimming pool - she kept my spirits up by sending me photos of herself, her friends, her parents, and even her parents' dog. She reminded me that there's a wonderful world outside of a code editor every now and then... 🙈

  *Now that's what I call real support.* ❤️

* A special thank you to GOG community member [**nickpeyon**](https://www.gog.com/u/nickpeyon), with whom I had extensive email conversations. Your massive Steam game collection helped inspire the direction for several of the large-library improvements in this project.

Thank you all for having my back!

---

## 🤝 Support & Feedback

**GitHub Issues are intentionally disabled.** Health-related limitations prevent me from reliably managing separate issue trackers across all of my plugin repositories.

Before contacting me, follow **What to Do If the Plugin Has Problems** and prepare a fresh Steam plugin log with a detailed description.

* **GOG:** Send me a message or add me as a friend through my [GOG profile](https://www.gog.com/u/melcom).
* **Email:** `melcom @ gmx.net`
* **Discord:** `.melcom` - the leading dot is part of the username. You can send me a message or add me as a friend.

Logs can be attached directly or shared through Dropbox or OneDrive. Response times may vary depending on my health and available development time. Thank you for your understanding.
