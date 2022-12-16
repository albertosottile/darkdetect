#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess
from typing import Callable, Optional

from ._base_listener import BaseListener


def theme() -> Optional[str]:
    try:
        #Using the freedesktop specifications for checking dark mode
        stdout = subprocess.check_output(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'])
        #If not found then trying older gtk-theme method
        if len(stdout)<1:
            stdout = subprocess.check_output(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'])
    except subprocess.SubprocessError:
        return "Light"
    # we have a string, now remove start and end quote
    theme_: bytes = stdout.lower().strip()[1:-1]
    return "Dark" if b"-dark" in theme_.lower() else "Light"


class GnomeListener(BaseListener):
    """
    A listener for Gnome on Linux
    """

    def _listen(self) -> None:
        with subprocess.Popen(
            ('gsettings', 'monitor', 'org.gnome.desktop.interface', 'gtk-theme'),
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as self._proc:
            for line in self._proc.stdout:
                self._invoke_callback(
                    'Dark' if '-dark' in line.strip().removeprefix("gtk-theme: '").removesuffix("'").lower()
                    else 'Light'
                )

    def _initiate_shutdown(self) -> None:
        self._proc.kill()

    def _wait_for_shutdown(self, timeout: Optional[int]) -> bool:
        try:
            self._proc.wait(timeout)
            return True
        except subprocess.TimeoutExpired:
            return False


__all__ = ("theme", "GnomeListener",)
