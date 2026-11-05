#!/usr/bin/env python3
"""Build a macOS Steam plugin bundle for GOG Galaxy.

Upstream releases only ship a Windows bundle (``*-64bit.zip``): its ``modules``
folder contains Python 3.13 extension modules compiled as ``*.pyd`` (PE/COFF)
files, which macOS cannot load. This script:

1. downloads (or takes) the official release ZIP;
2. replaces the bundled dependencies with macOS wheels for the CPython
   version used by GOG Galaxy (skipped when the bundle already has macOS
   ``.so`` modules, e.g. if a ``macos.zip`` is supplied);
3. overwrites the bundle's sources with the macOS fixes from this repository;
4. optionally installs the result into GOG Galaxy's plugin directory.

Note: ``src/`` tracks this fork's current code, while the ``macos.zip``
published upstream is an older release - mixing them fails at the
verification step, so prefer the ``*-64bit.zip`` of the same version.

Run it on the Mac that will run GOG Galaxy, so the wheels match the
architecture of the Galaxy application. ``uv`` is used when available,
otherwise the script falls back to ``pip``.

Examples:
    tools/macos/build_plugin.py
    tools/macos/build_plugin.py --install
    tools/macos/build_plugin.py --release-zip ~/Downloads/galaxy-steam-plugin-v2.1.12-64bit.zip
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
REQUIREMENTS_FILE = Path(__file__).with_name("requirements-macos.txt")

PLUGIN_DIR_NAME = "steam_ca27391f-2675-49b1-92c0-896d43afa4f8"
RELEASES_API = "https://api.github.com/repos/melcom-creations/galaxy-integration-steam/releases/latest"
DEFAULT_INSTALL_DIR = (
    Path.home() / "Library" / "Application Support" / "GOG.com" / "Galaxy" / "plugins" / "installed"
)
GALAXY_PYTHON = Path(
    "/Applications/GOG Galaxy.app/Contents/Frameworks/Python.framework/Versions/3.13/bin/python3.13"
)


def log(message):
    print(f"[build-macos] {message}")


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "galaxy-steam-macos-builder"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def download_release(destination: Path) -> Path:
    release = fetch_json(RELEASES_API)
    assets = [asset for asset in release.get("assets", []) if asset["name"].endswith("-64bit.zip")]
    if not assets:
        raise RuntimeError("No *-64bit.zip asset found in the latest GitHub release")
    asset = assets[0]
    log(f"downloading {asset['name']} ({asset['size'] // (1024 * 1024)} MiB)")
    request = urllib.request.Request(asset["browser_download_url"], headers={"User-Agent": "galaxy-steam-macos-builder"})
    with urllib.request.urlopen(request, timeout=300) as response, open(destination, "wb") as output:
        shutil.copyfileobj(response, output)
    return destination


def extract_plugin(zip_path: Path, destination: Path) -> Path:
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(destination)
    matches = list(destination.rglob("manifest.json"))
    for manifest_path in matches:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if manifest.get("platform") == "steam":
            return manifest_path.parent
    raise RuntimeError(f"Could not find the Steam plugin folder inside {zip_path}")


def read_requirements() -> list:
    requirements = []
    for line in REQUIREMENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)
    return requirements


def pip_platform_tag() -> str:
    machine = platform.machine().lower()
    if machine in {"arm64", "aarch64"}:
        return "macosx_11_0_arm64"
    return "macosx_10_15_x86_64"


def install_wheels(modules_dir: Path, python_executable: Path):
    requirements = read_requirements()
    uv = shutil.which("uv")
    if uv:
        command = [
            uv, "pip", "install",
            "--python", str(python_executable),
            "--target", str(modules_dir),
            "--only-binary", ":all:",
            "--no-deps",
            *requirements,
        ]
    else:
        command = [
            sys.executable, "-m", "pip", "install",
            "--target", str(modules_dir),
            "--only-binary=:all:",
            "--no-deps",
            "--implementation", "cp",
            "--python-version", "3.13",
            "--abi", "cp313",
            "--platform", pip_platform_tag(),
            *requirements,
        ]
    log("installing macOS wheels")
    subprocess.run(command, check=True)


def clean_windows_artifacts(output_dir: Path) -> bool:
    """Drop Windows binaries. Returns True if the bundle was a Windows build."""
    modules_dir = output_dir / "modules"
    pyd_files = list(modules_dir.rglob("*.pyd")) if modules_dir.exists() else []
    for path in pyd_files:
        path.unlink()
    shutil.rmtree(modules_dir / "bin", ignore_errors=True)
    for cache in output_dir.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)
    return bool(pyd_files)


def copy_macos_sources(output_dir: Path):
    for source in SRC_DIR.glob("*.py"):
        shutil.copy2(source, output_dir / source.name)
    manifest = SRC_DIR / "manifest.json"
    if manifest.exists():
        shutil.copy2(manifest, output_dir / manifest.name)


def verify_plugin(output_dir: Path, python_executable: Path):
    script = (
        "import sys;"
        f"sys.path.insert(0, {str(output_dir / 'modules')!r});"
        f"sys.path.insert(0, {str(output_dir)!r});"
        "import aiohttp, cryptography, google.protobuf, websockets, vdf, certifi, psutil;"
        "import client, registry_monitor, uri_scheme_handler;"
        "import plugin;"
        "print('plugin imports OK, local games:', len(client.local_games_list()))"
    )
    log("verifying imports with GOG Galaxy's Python")
    subprocess.run([str(python_executable), "-c", script], cwd=output_dir, check=True)


def install_plugin(output_dir: Path, install_dir: Path):
    install_dir.mkdir(parents=True, exist_ok=True)
    target = install_dir / PLUGIN_DIR_NAME
    if target.exists():
        # Keep backups outside plugins/installed: Galaxy scans every folder in
        # that directory and duplicate plugin GUIDs cause load conflicts.
        backup = install_dir.parent / f"{target.name}.backup-{int(__import__('time').time())}"
        log(f"moving existing installation to {backup}")
        target.rename(backup)
    log(f"installing into {target}")
    shutil.copytree(output_dir, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--release-zip", type=Path, help="use this release ZIP instead of downloading the latest one")
    parser.add_argument("--release-dir", type=Path, help="use an already extracted release folder instead of a ZIP")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "build" / f"{PLUGIN_DIR_NAME}-macos",
                        help="where to create the macOS plugin folder")
    parser.add_argument("--install", action="store_true", help="copy the result into GOG Galaxy's plugin folder")
    parser.add_argument("--install-dir", type=Path, default=DEFAULT_INSTALL_DIR)
    parser.add_argument("--python", type=Path, default=GALAXY_PYTHON,
                        help="GOG Galaxy's Python 3.13 interpreter")
    parser.add_argument("--skip-verify", action="store_true")
    args = parser.parse_args()

    if platform.system() != "Darwin":
        parser.error("this script builds a macOS bundle; run it on macOS")

    if not args.python.exists():
        parser.error(f"GOG Galaxy Python not found: {args.python} (use --python)")

    temp_dir = None
    try:
        if args.release_dir:
            release_plugin_dir = args.release_dir
        else:
            temp_dir = Path(tempfile.mkdtemp(prefix="galaxy-steam-"))
            zip_path = args.release_zip or download_release(temp_dir / "release.zip")
            release_plugin_dir = extract_plugin(zip_path, temp_dir / "extracted")

        if args.output.exists():
            log(f"removing previous output {args.output}")
            shutil.rmtree(args.output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        log(f"copying release bundle to {args.output}")
        shutil.copytree(release_plugin_dir, args.output)

        was_windows_bundle = clean_windows_artifacts(args.output)
        copy_macos_sources(args.output)
        if was_windows_bundle:
            install_wheels(args.output / "modules", args.python)
        else:
            log("bundle already contains macOS extension modules; keeping them")

        if not args.skip_verify:
            verify_plugin(args.output, args.python)

        if args.install:
            install_plugin(args.output, args.install_dir)

        log(f"done: {args.output}")
        if not args.install:
            log("quit GOG Galaxy, then copy the folder into:")
            log(f"  {args.install_dir}")
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
