#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess
from typing import Callable, Optional

from ._base_listener import BaseListener, DDTimeoutError


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

    def __init__(self, callback: Callable[[str], None]):
        self._proc: subprocess.Popen
        super().__init__(callback)

    def _listen(self):
        with subprocess.Popen(
            ('gsettings', 'monitor', 'org.gnome.desktop.interface', 'gtk-theme'),
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as self._proc:
            for line in self._proc.stdout:
                self.callback('Dark' if '-dark' in line.strip().removeprefix("gtk-theme: '").removesuffix("'").lower() else 'Light')

    def _stop(self):
        self._proc.kill()

    def _wait(self, timeout: Optional[int]):
        try:
            self._proc.wait(timeout)
        except subprocess.TimeoutExpired as e:
            raise DDTimeoutError from e


__all__ = ("theme", "GnomeListener",)
