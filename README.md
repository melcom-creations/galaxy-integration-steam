# 🚂 Steam Integration Plugin for GOG Galaxy 2.1+ (64-bit)

This repository contains the Steam integration plugin for the 64-bit version of GOG Galaxy 2.1+.

The original community integration has been updated to work with the current 64-bit GOG Galaxy client and Python 3.13. In addition to compatibility improvements, this project includes dependency updates, bug fixes, stability improvements and ongoing maintenance.

---

## ✨ Features

* Compatible with GOG Galaxy 2.1+ (64-bit)
* Python 3.13 support
* Updated 64-bit dependencies
* Improved stability and compatibility
* Ongoing maintenance and bug fixes

---

## 📦 Installation

### Standard Installation (Recommended)

1. Close GOG Galaxy completely.
2. Download the latest release from this repository.
3. Open the following folder:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
```

4. Extract the ZIP archive **directly into this folder**.

After extraction, the directory structure **must** look like this:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
└── steam_ca27391f-2675-49b1-92c0-896d43afa4f8\
    ├── manifest.json
    ├── plugin.py
    ├── README.md
    └── ...
```

5. Start GOG Galaxy.

### If the plugin folder is missing

If the ZIP archive does **not** already contain the folder

```text
steam_ca27391f-2675-49b1-92c0-896d43afa4f8
```

create the folder manually inside

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
```

and extract the contents of the ZIP archive into it.

The final directory structure must be:

```text
%localappdata%\GOG.com\Galaxy\plugins\installed\
└── steam_ca27391f-2675-49b1-92c0-896d43afa4f8\
```

---

## 🔄 Resetting the Plugin Database (Recommended)

If the plugin behaves unexpectedly after an update, resetting the local plugin database is recommended.

1. Open:

```text
C:\ProgramData\GOG.com\Galaxy\storage\plugins\
```

2. Locate all files beginning with:

```text
steam_
```

and ending with:

```text
-storage.db
```

3. Rename each database by appending `.old` to its filename.

Example:

```text
steam_xxxxxxxxx-storage.db
```

becomes

```text
steam_xxxxxxxxx-storage.db.old
```

4. Start GOG Galaxy again.
5. Reconnect the Steam integration if necessary.

---

## ⚠️ Important

Do **not** place backup copies of this plugin inside the `plugins\installed` directory.

GOG Galaxy scans every folder inside this directory during startup. Duplicate plugin folders may lead to GUID conflicts or cause Galaxy to load an outdated version of the plugin.

---

## 🙏 Credits

**Original Community Integration**
Friends of Galaxy
https://github.com/FriendsOfGalaxy/galaxy-integration-steam

**Authorization Flow**
ABaumher
https://github.com/gogcom/galaxy-integrations-steam/pull/171

**64-bit Port, Maintenance and Improvements**
melcom

---

## 📚 References

This integration is based on and inspired by several open-source projects and community resources.

* https://github.com/SteamRE/SteamKit
* https://github.com/ValuePython/steam
* https://github.com/prncc/steam-scraper
* https://github.com/rhaarm/steam-scraper
* https://github.com/mulhod/steam_reviews
* https://github.com/summersb92/aeolipile
* https://github.com/rcpoison/steam-scraper
* https://github.com/chmccc/steam-scraper

---

## 🤝 Support & Feedback

This project is maintained by a single individual. Response times may vary, especially during periods when health-related limitations reduce available development time.

**GitHub Issues are intentionally disabled.**

If you would like to report a bug or suggest an improvement, please use the contact form on my website:

📩 https://melcom-creations.github.io/melcom-music/contact.html

Thank you for your patience and support!
