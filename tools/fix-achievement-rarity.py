#!/usr/bin/env python3
"""Fill Steam global achievement rarity into GOG Galaxy's local database.

GOG Galaxy shows "x% of players unlocked this" using the ``Achievements.rarity``
column of its local database. That column is filled by GOG's metadata service,
which has no global stats for many Steam games (it stores ``0.0`` for them), so
the client displays ``0.0%`` even though Valve publishes the real values:

    https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid=<appid>

This script copies those percentages into Galaxy's database. It only updates
rows that already exist for ``steam_<appid>`` releases (never creates or deletes
anything), keeps a timestamped backup of the database, and can be re-run safely.

Caveats:
  * GOG Galaxy must be closed - the database is locked while the client runs.
  * GOG may restore its own values on the next achievement metadata refresh;
    just run the script again.
  * Achievements stored under GOG's legacy key format
    (``<index>¬Achievement¬<name>``) cannot be matched to Steam API names and
    are reported as skipped.

Examples:
    tools/fix-achievement-rarity.py --dry-run
    tools/fix-achievement-rarity.py
    tools/fix-achievement-rarity.py --db /path/to/galaxy-2.0.db --all
"""

import argparse
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

STEAM_RARITY_URL = (
    "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/"
)

# Thresholds used by GOG for rarity labels (derived from its own metadata).
RARITY_SLUGS = (
    (0.5, "legendary"),
    (2.5, "epic"),
    (10.0, "rare"),
    (30.0, "uncommon"),
    (float("inf"), "common"),
)

LEGACY_KEY_SEPARATOR = "¬"


def log(message):
    print(f"[rarity] {message}", flush=True)


def default_db_paths():
    system = platform.system()
    if system == "Darwin":
        return [ "/Users/Shared/GOG.com/Galaxy/Storage/galaxy-2.0.db" ]
    if system == "Windows":
        program_data = os.environ.get("ProgramData", r"C:\ProgramData")
        return [ os.path.join(program_data, "GOG.com", "Galaxy", "storage", "galaxy-2.0.db") ]
    return [ os.path.expanduser("~/.local/share/GOG.com/Galaxy/Storage/galaxy-2.0.db") ]


def galaxy_is_running():
    system = platform.system()
    try:
        if system == "Darwin":
            return bool(subprocess.run(["pgrep", "-f", "MacOS/GOG Galaxy"], capture_output=True).stdout.strip())
        if system == "Windows":
            output = subprocess.run(["tasklist", "/FI", "IMAGENAME eq GalaxyClient.exe"], capture_output=True, text=True)
            return "GalaxyClient.exe" in output.stdout
        return bool(subprocess.run(["pgrep", "-f", "GalaxyClient"], capture_output=True).stdout.strip())
    except (OSError, subprocess.SubprocessError):
        return False


def rarity_slug(percent):
    for limit, slug in RARITY_SLUGS:
        if percent < limit:
            return slug
    return "common"


def fetch_percentages(app_id, retries=3, timeout=30):
    """Return {steam_api_name: percent} for an app, or None when unavailable."""
    query = urllib.parse.urlencode({"gameid": app_id})
    url = f"{STEAM_RARITY_URL}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "galaxy-steam-rarity-fix"})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.load(response)
            achievements = payload.get("achievementpercentages", {}).get("achievements", [])
            result = {}
            for entry in achievements:
                name = entry.get("name")
                try:
                    percent = float(entry.get("percent"))
                except (TypeError, ValueError):
                    continue
                if name:
                    result[name] = percent
            return result
        except urllib.error.HTTPError as error:
            if error.code in (403, 429) and attempt < retries:
                time.sleep(5 * attempt)
                continue
            log(f"app {app_id}: HTTP {error.code}")
            return None
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            if attempt < retries:
                time.sleep(2 * attempt)
                continue
            log(f"app {app_id}: {error}")
            return None
    return None


def steam_games_with_achievements(connection, only_missing):
    condition = "rarity IS NULL OR rarity = 0" if only_missing else "1"
    rows = connection.execute(
        f"""
        SELECT gameReleaseKey, COUNT(*)
        FROM Achievements
        WHERE gameReleaseKey LIKE 'steam\\_%' ESCAPE '\\' AND ({condition})
        GROUP BY gameReleaseKey
        ORDER BY gameReleaseKey
        """
    )
    return [(key, count) for key, count in rows]


def update_game(connection, release_key, percentages, only_missing, dry_run, verbose):
    rows = connection.execute(
        "SELECT apikey, rarity FROM Achievements WHERE gameReleaseKey = ?", (release_key,)
    ).fetchall()

    updates = []
    unmatched = 0
    legacy = 0
    for apikey, current in rows:
        if LEGACY_KEY_SEPARATOR in apikey:
            legacy += 1
            continue
        percent = percentages.get(apikey)
        if percent is None:
            # Valve sometimes returns different casing than the plugin stored.
            lower = apikey.casefold()
            percent = next((value for name, value in percentages.items() if name.casefold() == lower), None)
        if percent is None:
            unmatched += 1
            continue
        if only_missing and current not in (None, 0, 0.0):
            continue
        if current is not None and abs(current - percent) < 0.005:
            continue
        updates.append((round(percent, 2), rarity_slug(percent), release_key, apikey))

    if updates and not dry_run:
        connection.executemany(
            "UPDATE Achievements SET rarity = ?, raritySlug = ? WHERE gameReleaseKey = ? AND apikey = ?",
            updates,
        )
        connection.commit()

    if verbose and updates:
        for percent, slug, _, apikey in updates[:5]:
            log(f"  {apikey}: {percent}% ({slug})")
        if len(updates) > 5:
            log(f"  ... {len(updates) - 5} more")

    return len(updates), unmatched, legacy


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", type=str, help="path to galaxy-2.0.db (auto-detected by default)")
    parser.add_argument("--dry-run", action="store_true", help="report what would change without writing")
    parser.add_argument("--all", action="store_true", help="also refresh achievements that already have rarity")
    parser.add_argument("--limit", type=int, default=0, help="process at most N games")
    parser.add_argument("--delay", type=float, default=0.5, help="pause between Steam API calls, seconds")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--force", action="store_true", help="run even if GOG Galaxy appears to be running")
    args = parser.parse_args()

    db_path = args.db or next((path for path in default_db_paths() if os.path.exists(path)), None)
    if not db_path or not os.path.exists(db_path):
        parser.error("Galaxy database not found, pass --db explicitly")
    if not args.force and galaxy_is_running():
        parser.error("GOG Galaxy is running - quit it first (or use --force at your own risk)")

    if not args.dry_run:
        backup = f"{db_path}.rarity-backup-{int(time.time())}"
        shutil.copy2(db_path, backup)
        log(f"backup: {backup}")

    connection = sqlite3.connect(db_path)
    try:
        games = steam_games_with_achievements(connection, only_missing=not args.all)
        if args.limit:
            games = games[: args.limit]
        log(f"{len(games)} Steam game(s) with achievements to check")

        total_updated = total_unmatched = total_legacy = 0
        failed = []
        for index, (release_key, _count) in enumerate(games, start=1):
            app_id = release_key.split("_", 1)[1]
            percentages = fetch_percentages(app_id)
            if percentages is None:
                failed.append(app_id)
                continue
            updated, unmatched, legacy = update_game(
                connection, release_key, percentages, only_missing=not args.all,
                dry_run=args.dry_run, verbose=args.verbose,
            )
            total_updated += updated
            total_unmatched += unmatched
            total_legacy += legacy
            if updated and not args.verbose:
                log(f"[{index}/{len(games)}] {release_key}: {updated} achievement(s)")
            if args.delay:
                time.sleep(args.delay)

        verb = "would update" if args.dry_run else "updated"
        log(f"{verb} {total_updated} achievement(s) in {len(games) - len(failed)} game(s)")
        if total_unmatched:
            log(f"skipped {total_unmatched} achievement(s) missing from Steam's response")
        if total_legacy:
            log(f"skipped {total_legacy} achievement(s) stored in GOG's legacy key format")
        if failed:
            log(f"Steam API failed for {len(failed)} game(s): {', '.join(failed[:10])}")
    finally:
        connection.close()


if __name__ == "__main__":
    sys.exit(main())
