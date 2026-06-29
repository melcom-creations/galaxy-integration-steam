## Version 2.1.4-64bit

### Overview
Maintenance release. Rebuilt all third-party dependencies as clean 64-bit wheels for Python 3.13 via `melcom's Galaxy Plugin Scout v1.1.15`. Removed unused `cffi` and `mypy_extensions`.

### Changed
- **Dependency rebuild:** All third-party packages in `/modules/` reinstalled as verified 64-bit (`cp313-win_amd64`) wheels with proper `.dist-info` metadata.
- **Removed unused libraries:** `cffi` and `mypy_extensions` identified as unused by static import analysis and removed.

### Packages rebuilt (64-bit)
`aiohappyeyeballs`, `aiohttp`, `aiosignal`, `attrs`, `certifi`, `cryptography`, `dataclasses_json`, `frozenlist`, `galaxy_plugin_api`, `idna`, `marshmallow`, `multidict`, `packaging`, `propcache`, `protobuf`, `pyasn1`, `pycparser`, `rsa`, `typing_extensions`, `typing_inspect`, `vdf`, `websockets`, `yarl`

---

## Version 2.1.3-64bit

### Overview
This maintenance release finalizes the automated dependency maintenance workflow for the Steam plugin. Dependency detection has been refined to avoid installing incorrect alias packages while preserving full compatibility with the GOG Galaxy 2.1+ 64-bit runtime based on Python 3.13.

### Fixed
- **Alias package resolution:** Corrected dependency generation so alias-only import names are no longer written as standalone pip packages.
- **`attrs` handling:** Prevents the unrelated `attr` PyPI package from being installed. The plugin now correctly relies solely on `attrs`, which already provides the required `attr` namespace.
- **Import conflict prevention:** Eliminated the possibility of conflicting `attr.py` and `attr/` implementations being installed together.

### Changed
- **Dependency generation:** Improved library export logic used by the maintenance toolkit to produce a cleaner `plugin-config.txt`.
- **Maintenance workflow:** Fresh dependency alignment now installs only the required packages, resulting in a cleaner `/modules/` directory and eliminating unnecessary artifacts.

### Technical Breakdown

#### Dependency alias handling
The dependency analysis and alignment workflow was refined to distinguish between import aliases and actual pip package names. Alias-only imports are now filtered during library generation while the corresponding canonical package continues to be installed automatically.

---

## Version 2.1.2-64bit

### Overview
This is a major dependency maintenance release. The entire library stack has been analyzed, cleaned, and re-aligned for the **GOG Galaxy 2.1+ (64-bit)** environment. Using **melcom's Clean-Modules v1.4.5** analyzer and **melcom's Galaxy-Aligner-Toolkit v3.1.4**, all third-party modules were purged and reinstalled as native 64-bit binaries targeted specifically for **Python 3.13**.

### Added
- **Modernized Library Stack:** All dependencies have been updated to their latest stable 64-bit versions.
- **Automated Dependency Alignment:** Implementation of a standardized maintenance workflow to ensure binary compatibility across different Windows environments.

### Fixed
- **Binary Architecture Mismatch:** Resolved potential issues where legacy 32-bit or local-Python-versioned libraries could cause import failures.
- **Module Artifact Bloat:** Removed 25+ orphaned `.dist-info` folders and unreferenced legacy module files to reduce plugin footprint and improve load times.
- **CFFI Backend Resolution:** Specifically ensured the inclusion of the `_cffi_backend` 64-bit extension module required by modern security libraries.

### Changed
- **Core Library Upgrades:**
    - `cryptography`: Upgraded from **46.0.3** to **49.0.0** (Native 64-bit Rust/C binaries).
    - `aiohttp`: Upgraded from **3.13.5** to **3.14.1**.
    - `websockets`: Upgraded from **15.0.1** to **16.0**.
    - `certifi`: Updated to **2026.6.17**.
    - `idna`: Updated to **3.18**.
    - `rsa`: Updated to **4.9.1**.
    - `marshmallow`: Updated to **3.26.2**.
- **Python Runtime Target:** All compiled extensions are now strictly aligned with the **CPython 3.13 (win_amd64)** ABI.

### Technical Breakdown

#### 1. Dependency Analysis & Cleanup
**Tools:** `melcom's Clean-Modules v1.4.5`

The plugin ROOT was scanned to establish a transitive closure of all required imports. This allowed for the safe removal of unused Python modules and metadata without breaking the core functionality. Hidden binary dependencies were identified via `METADATA` and `top_level.txt` manifest parsing.

#### 2. 64-bit Library Alignment
**Tools:** `melcom's Galaxy-Aligner-Toolkit v3.1.4`

The `/modules/` directory was completely refreshed. Using `pip` with strict platform-targeting flags (`--python-version 3.13 --platform win_amd64 --only-binary :all:`), the toolkit pulled fresh, verified 64-bit wheels from PyPI. This guarantees that all compiled components (like `multidict`, `yarl`, and `frozenlist`) are perfectly compatible with the GOG Galaxy 2.1+ internal Python runtime.

---

## Version 2.1.1-64bit

### Overview
This maintenance release focuses on defensive stability improvements inside the Steam integration. No major functionality changes were introduced. The update hardens reconnect handling, improves protection against cache inconsistencies, and reduces the risk of unnecessary background activity during authentication recovery scenarios.

### Fixed
- **Authentication recovery hardening:** Improved handling of authentication-loss scenarios to prevent duplicate recovery signaling during reconnect operations.
- **Reconnect stability improvements:** Additional safeguards reduce the likelihood of redundant recovery actions when multiple authentication events occur close together.
- **Cache consistency protection:** Internal cache management paths are more resilient against transient state mismatches.
- **Background stability improvements:** Reduced the risk of avoidable background activity during repeated authentication recovery attempts.

### Changed
- **`modules/steam_network/websocket_client.py` - Authentication recovery logic hardened:** Recovery paths now perform additional validation before signaling authentication loss.
- **Reconnect handling refined:** Internal reconnect logic is more defensive when processing repeated failure conditions.
- **General stability maintenance:** Minor robustness improvements throughout the authentication and session-management flow.

### Technical Breakdown

#### 1. Authentication recovery protection
**Files:** `modules/steam_network/websocket_client.py`

The authentication recovery path was hardened to prevent duplicate signaling and improve consistency when multiple authentication-related failures occur during reconnect operations.

#### 2. Reconnect robustness improvements
**Files:** `modules/steam_network/websocket_client.py`

Additional defensive checks were introduced to ensure repeated recovery attempts do not unnecessarily increase background workload or create inconsistent runtime state.

---

## Version 2.1.0-64bit

### Overview
This release modernizes the Steam integration for the 64-bit GOG Galaxy client and resolves several long-standing issues affecting achievement synchronization, resource management, and background task stability. Achievement imports for newly released DLCs and expansions now synchronize correctly, multiple Windows resource leaks have been eliminated, and a critical background task bug causing unnecessary CPU activity has been fixed.

### Added
- **Improved Achievement Synchronization:** Achievement imports now use Steam's internal API achievement identifiers when communicating with GOG Galaxy. This allows newly added achievements from DLCs, expansions, and post-launch updates to synchronize correctly.
- **Enhanced Resource Management:** File and registry access now use modern context-manager implementations to guarantee proper cleanup and improve long-term stability.
- **64-bit Compatibility Maintenance:** Continued compatibility updates for GOG Galaxy 2.1+ and Python 3.13 environments.

### Fixed
- **Missing DLC and Expansion Achievements:** Newly released achievements were not appearing in GOG Galaxy because the integration relied on display-name matching instead of Steam's internal achievement identifiers. Achievement synchronization now correctly maps and imports new achievements.
- **Background Task Leak (Critical):** A typo in the cache synchronization throttling logic caused the plugin to continuously create redundant background tasks. This bypassed the intended cooldown mechanism, increased CPU usage, and could generate coroutine warnings during shutdown.
- **File Descriptor Leak:** Steam VDF files were opened without a proper context manager, potentially leaving files locked on Windows systems.
- **Windows Registry Handle Leak:** Registry queries could leave open handles behind when exceptions occurred. Registry access now guarantees automatic cleanup.
- **Client Shutdown Stability:** Background cache tasks are now correctly tracked and cancelled during plugin shutdown.

### Changed
- **`backend_steam_network.py` – Achievement Mapping Logic:** Achievement imports now pass Steam API identifiers directly to GOG Galaxy instead of relying on legacy display-name matching.
- **`plugin.py` – Cache Synchronization Throttling:** Corrected task tracking logic to properly respect cooldown timing and prevent uncontrolled task creation.
- **`client.py` – Resource Cleanup Modernization:** File access and Windows registry operations now use safe context-manager implementations.
- **General Stability Improvements:** Improved long-term reliability during synchronization, achievement imports, and client shutdown operations.

### Technical Breakdown

#### 1. Achievement Synchronization Modernization
**Files:** `backend_steam_network.py`

**Problem:**
New achievements introduced through DLCs, expansions, and post-launch content updates frequently failed to appear in GOG Galaxy. The integration relied on display-name matching and supplied `achievement_id=None`, preventing GOG Galaxy from correctly identifying newly added achievements.

**Solution:**
The plugin now passes Steam's internal API achievement identifier directly as `achievement_id`. Because Steam's protobuf payload already contains the unique identifier, GOG Galaxy can correctly map and synchronize newly released achievements.

**Impact:**
New achievements from DLCs and game updates now synchronize correctly and contribute to completion percentages.

#### 2. Background Task Leak Elimination
**Files:** `plugin.py`

**Problem:**
A typo in the cache synchronization logic assigned active tasks to the wrong variable. This prevented the throttle mechanism from functioning and caused the plugin to continuously spawn unnecessary background tasks whenever cache modifications occurred.

**Solution:**
The active cache task is now correctly assigned and tracked. The intended cooldown mechanism functions properly and active tasks are cleanly cancelled during shutdown.

**Impact:**
Lower CPU usage, reduced memory consumption, cleaner shutdown behavior, and improved overall stability.

#### 3. File and Registry Resource Cleanup
**Files:** `client.py`

**Problem:**
Several Windows-specific resource leaks existed within file and registry handling code. Open file descriptors could remain active and registry handles could remain allocated if exceptions occurred during execution.

**Solution:**
File access was migrated to `with open(...)` context managers and registry operations now use native context-managed `winreg.OpenKey(...)` handling.

**Impact:**
Improved stability, reduced risk of locked files, and guaranteed cleanup of Windows resources.

### Known Limitations

> ⚠️ **Achievement metadata depends on GOG Galaxy servers**
>
> The Steam integration can successfully import newly released achievements and synchronize them with the local GOG Galaxy client. However, achievement names, icons, descriptions, and total achievement counts are provided by GOG Galaxy's backend services.
>
> If GOG has not yet updated its central metadata database for a newly released DLC or expansion, the achievement may not immediately appear in the user interface even though it has already been imported successfully.
>
> **Workaround:** Wait for GOG Galaxy's backend metadata to be updated. No further action is usually required.

---

## Version 2.0

- Upgrade to Python 3.13
- Upgrade dependencies

---

## Version 1.3

- Changes to credential encryption method, reduce relogin requests in the future
- Bump version to override manually installed versions

---

## Version 1.1

- Fixes authorization flow after Steam changed their auth flow
- Fixes issues on large game libraries
- Add protobuf download and generation script
- Changes based on https://github.com/FriendsOfGalaxy/galaxy-integration-steam/pull/171

---

## Version 1.0.7

- Fixes issues when SteamGuard is disabled. Made it so 2FA codes would ignore leading or trailing whitespace.
- Code cleanup

---

## Version 1.0.6

- reintroduces password santization so users with long passwords or illegal characters can log in as intended
- Code cleanup

---

## Version 1.0.5

- implemented a temporary fix to make the receive loop only send off a few jobs before stopping to receive a message, instead of doing all the jobs at once.

---

## Version 1.0.4

- refreshed python generated protobuf files
- removed public profiles `backend`. The new auth flow makes it irrelevant.
- implemented new auth flow.

---

## Version 1.0.2

- refreshed python generated protobuf files
- handle eresult 48: `TryWithDifferentCM` on every login attempt
- fix timeout problems when importing bigger libraries (#129 thanks @nbrochu!)
- amend and cleanup authentication process error handling so that it gives immediate feedback
- add some unit tests for achievement parser + refactor
- fix some unit tests for storing plugin version on which user logged in and test for default backend switch

---

## Version 1.0.1

- added browser window for handling external error during checking profile's privacy
- added browser window for case when user has private game details or has no games
- fixed an issue with plugin incorrectly reporting the steam profile as private (or "Incorrect Steam64 ID") if a game with for example ";" in its title is owned

---

## Version 1.0.0

- refactor high-level code to support multi-backend architecture
- add `fallback backend` functionality in case the `initial backend` loses connection
- add PublicProfiles `backend` that rely on publicly visible user data
- add user configuration at `../steam_plugin_config.ini` (default: SteamNetwork as `initial backend` and PublicProfiles as a `fallback backend`) NOTE: plugin reconnection is required to use fallback functionality

---

## Version 0.60

- add html fixes
- add css visual fixes
- handle eresult 48: `TryWithDifferentCM` and similar cases to blacklist a server temporarily

---

## Version 0.59

- fix not showing installed games due to changed Steam libraryfolders.vdf format (#122 thanks @tfredett and all from #121!)

---

## Version 0.58

- handle not established/broken websockets connection during getting obfuscated IP
- fix all achievements import stuck on 0% when having old version achievements unlocked e.g. in Train Simulator (#114 thanks @Tauron93!)
- translate eresult 5 (`EResult.InvalidPassword`) to `InvalidCredentials` instead of `BackendError` on login key authorization (#103 thanks @SparrowBrain!) this change should cause "Connection Lost" in Galaxy instead of plugin going "Offline" disposing of need for further plugin reconnection
- remove old code leftovers from backend.py

---

## Version 0.57

- add helper script for injecting Nethook (for devs)
- improved login auth protobuf message for following attributes: client_package_version, machine_id, client_language, qos_level, machine_name, client_os_type

---

## Version 0.56

- fix handling if libraryfolders.vdf was not found
- connection stability improvement (no longer connects to servers from different regions) (#108 thanks @SparrowBrain!)

---

## Version 0.55

- add obfuscated_private_ip to ClientLogOn message (#104 thanks @SparrowBrain!) this change should fix losing authentication in case of multiple machines in the same network (eresult 32 and eresult 5)

---

## Version 0.54

- fix common problem with not showing achievements (Steam messages > 1MB) (#100 thanks @Neverous!)
- fix typo in EMsg.ClientLoggedOff listener
- rename "subscription" name from `Family Sharing` to `Steam Family Sharing`
- remove old deprecated code for http logging path

---

## Version 0.53

- fix crashes due to pushing big cache multiple times in a row
- fix crashes due to O(n^2) licenses lookup for big libraries
- fix crashes due to apps parsing for big libraries
- workaround issue with improper games cache invalidation for big libraries
- improved how Steam in/out protobuf traffic is logged

---

## Version 0.52

- raise BackendError instead of BackendTimeout when couldn't login with token
- register steam app ticket with CM before logging and save a new ticket after login

---

## Version 0.51.2

- Enhance local game sizes by returning downloading size if game is not fully installed yet
- Drop attaching obfuscated private ip to login params.

---

## Version 0.51.1

- Fixup marking when games cache is ready in situations when part of the cache was already initialized
- Optimize retrieving subscription status
- Fixes for rich presence translations for certain games (dota, stellaris)

---

## Version 0.51

- Use package access token when retrieving package information, should fix some games not appearing

---

## Version 0.50.9

- Refactor games cache for readability and debugging purposses
- Implement getting local game sizes

---

## Version 0.50.8

- Fix crash on potential looping rich presence translation
- Fix possible 0 owned games sent issue occuring if previous retrieval was stopped mid-way

---

## Version 0.50.7

- Use LoginKeyAccepted message post auth
- Retry using servers from a different cellid (update login params to handle cell id)

---

## Version 0.50.6

- Send log off call on plugin shutdown
- More precise login parameters, up protocol version

---

## Version 0.50.5

- Don't get stuck on broken cache in subsequent runs, instead always reimport packages which didn't end up being resolved (Thanks Dugsdghk!)
- Don't crash protobuf on bytes response in initial rich presence parsing (Thanks Dugsdghk!)

---

## Version 0.50.4

- Fix for owned games which are also present in one of family sharings being reported only as family shared. (Thanks for the help Svill and TM-CG!)

---

## Version 0.50.3

- Dont endlessly retry auth to not lock user out

---

## Version 0.50.2

- Fix missing achievement_id crashing protobuf_client (Thanks MartinCa!)
- Extended supported result codes from steam auth
- Increase logging of protobuf responses

---

## Version 0.50.1

- Ignore incompatible cache

---

## Version 0.50

- Handle potential infinite rich presence translation
- Return Family sharing games as a subscriptions
- Dont crash on unknown presence format

---

## Version 0.49

- Better handle parsing rich presence from steam
- Add a cooldown to parsing local files, should fix ssues with large cpu usage during game installation
- Better flow in case of clicking forgot password during auth ( focus should stay on proper window )

---

## Version 0.48

- Cache the results of owned games so the import is possibly immediate in subsequent plugin runs

---

## Version 0.47

- Change the logic of sent friend nicknames to always display the username with optional given nickname instead of one of the two
- Pull steam friends from protobuf communication instead of scrapping website
- Move authentication to protobuf

---

## Version 0.46.5

- Hotfix for some achievements not being properly recognized by Galaxy (Trailing whitespace in names)

---

## Version 0.46

- Potential fixes for key error on achievements retrieval
- Retrieve last_played time from protobuf instead of website scrapping

---

## Version 0.45

- Quickfix for plugin crash while getting achievements
- Restore mechanism to get last_played time if game was launched via Steam

---

## Version 0.44

- Achievements and GameTime are now pulled from protobufs instead of scrapping the website
- Tags are now pulled from protobufs instead of scrapping local files (allows for tags import without installed steam client)