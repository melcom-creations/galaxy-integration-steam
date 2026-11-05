import platform

if platform.system().lower() == "windows":
    from galaxy.registry_monitor import RegistryMonitor

    HKEY_CURRENT_USER = 0x80000001

    def _get_windows_steam_registry_monitor():
        return RegistryMonitor(HKEY_CURRENT_USER, r"Software\Valve\Steam\Apps")

    get_steam_registry_monitor = _get_windows_steam_registry_monitor

else:

    import os

    class FileRegistryMonitor:

        def __init__(self, filename):
            self._filename = filename
            self._stat = self._get_stat()

        def _get_stat(self):
            try:
                st = os.stat(self._filename)
            except OSError:
                return (0, 0)
            return (st.st_size, st.st_mtime_ns)

        def is_updated(self):
            current_stat = self._get_stat()
            changed = self._stat != current_stat
            self._stat = current_stat
            return changed

        def close(self):
            pass

    class SteamAppStateMonitor:
        """Watch the files Steam actually updates on macOS.

        Steam for macOS does not write per-app state into ``registry.vdf``
        anymore, so watching only that file means local game changes are
        never noticed. Instead, watch the registry, ``libraryfolders.vdf``
        and every ``appmanifest_*.acf`` file: installs, uninstalls and the
        running flag all modify those files.
        """

        def __init__(self):
            self._fingerprint = self._get_fingerprint()

        @staticmethod
        def _steam_folder():
            return os.path.expanduser("~/Library/Application Support/Steam")

        def _tracked_files(self):
            steam_folder = self._steam_folder()
            files = [os.path.join(steam_folder, "registry.vdf")]
            try:
                # Imported lazily: client imports the galaxy API, which is only
                # available once Galaxy has started the plugin.
                from client import get_app_manifests, get_library_folders

                library_folders = get_library_folders()
                files.append(os.path.join(steam_folder, "steamapps", "libraryfolders.vdf"))
                files.extend(get_app_manifests(library_folders))
            except Exception:
                pass
            return files

        def _get_fingerprint(self):
            fingerprint = []
            for path in self._tracked_files():
                try:
                    st = os.stat(path)
                except OSError:
                    continue
                fingerprint.append((path, st.st_size, st.st_mtime_ns))
            return tuple(sorted(fingerprint))

        def is_updated(self):
            current_fingerprint = self._get_fingerprint()
            changed = current_fingerprint != self._fingerprint
            self._fingerprint = current_fingerprint
            return changed

        def close(self):
            pass

    def _get_macos_steam_state_monitor():
        return SteamAppStateMonitor()

    get_steam_registry_monitor = _get_macos_steam_state_monitor
