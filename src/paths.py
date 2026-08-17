"""
    Path helpers that work both when running from source and when
    running from a PyInstaller --onefile bundle.

    A PyInstaller one-file executable decompresses itself into a
    temporary directory at startup and runs from there (exposed as
    ``sys._MEIPASS``). That temp directory is deleted as soon as the
    executable exits, so it is only safe to use for *read-only*
    bundled resources (images, sounds, fonts...). Anything that must
    survive between runs (save data, highscores, config) must be
    resolved elsewhere - see ``persistent_path`` below.
"""

import os
import sys


def resource_path(relative_path: str) -> str:
    """
        Resolve the path to a bundled, read-only resource.

        - Running from source: resolved relative to the current
          working directory, same as a plain relative path.
        - Running from a PyInstaller --onefile bundle: resolved
          relative to the bundle's temporary extraction folder,
          which is where --add-data copies resources to.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def persistent_path(relative_path: str) -> str:
    """
        Resolve the path to a writable, persistent file (highscores,
        save data...).

        This must NEVER point inside the PyInstaller temp extraction
        folder used by ``resource_path`` - that folder, and anything
        written into it, is deleted as soon as the bundled executable
        exits, silently wiping any data written there.

        - Running from source: resolved relative to the current
          working directory (unchanged behaviour).
        - Running from a PyInstaller --onefile bundle: resolved next
          to the executable itself, so the file survives between runs.
    """
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
