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

    from importlib import import_module

    def _is_macos_uri_handler_installed(protocol):
        launch_services = import_module("CoreServices.LaunchServices")
        app_kit = import_module("AppKit")
        LSCopyDefaultHandlerForURLScheme = launch_services.LSCopyDefaultHandlerForURLScheme
        NSWorkspace = app_kit.NSWorkspace
        bundle_id = LSCopyDefaultHandlerForURLScheme(protocol)
        if not bundle_id:
            return False
        return NSWorkspace.sharedWorkspace().absolutePathForAppBundleWithIdentifier_(bundle_id) is not None

    is_uri_handler_installed = _is_macos_uri_handler_installed

else:

    def _is_unsupported_uri_handler_installed(protocol):
        return False

    is_uri_handler_installed = _is_unsupported_uri_handler_installed
