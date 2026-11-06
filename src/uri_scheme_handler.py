import platform

if platform.system().lower() == "windows":

    import winreg
    import shlex
    import os

    def _is_windows_uri_handler_installed(protocol):
        key = None
        try:
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, rf"{protocol}\shell\open\command")
            executable_template = winreg.QueryValue(key, None)
            splitted_exec = shlex.split(executable_template)
            if not splitted_exec:
                return False
            return os.path.exists(splitted_exec[0])
        except OSError:
            return False
        except ValueError:
            return False
        finally:
            if key:
                winreg.CloseKey(key)

    is_uri_handler_installed = _is_windows_uri_handler_installed

elif platform.system().lower() == "darwin":

    import os

    # GOG Galaxy's bundled Python does not ship pyobjc, so AppKit /
    # CoreServices cannot be imported. Steam registers the steam:// URL
    # scheme when Steam.app is installed, so checking for the bundle is
    # both sufficient and dependency-free.
    _STEAM_APP_PATHS = (
        "/Applications/Steam.app",
        os.path.expanduser("~/Applications/Steam.app"),
    )

    def _is_macos_uri_handler_installed(protocol):
        if protocol != "steam":
            return False
        return any(os.path.isdir(path) for path in _STEAM_APP_PATHS)

    is_uri_handler_installed = _is_macos_uri_handler_installed

else:

    def _is_unsupported_uri_handler_installed(protocol):
        return False

    is_uri_handler_installed = _is_unsupported_uri_handler_installed
