#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess
from typing import Callable, Optional

from .base import BaseListener

def theme():
    try:
        #Using the freedesktop specifications for checking dark mode
        out = subprocess.run(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
            capture_output=True)
        stdout = out.stdout.decode()
        #If not found then trying older gtk-theme method
        if len(stdout)<1:
            out = subprocess.run(
                ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
                capture_output=True)
            stdout = out.stdout.decode()
    except Exception:
        return 'Light'
    # we have a string, now remove start and end quote
    theme = stdout.lower().strip()[1:-1]
    if '-dark' in theme.lower():
        return 'Dark'
    else:
        return 'Light'


class GnomeListener(BaseListener):
    """
    A listener for Gnome on Linux
    """

    def __init__(self, callback: Callable[[str], None]):
        self._proc: Optional[subprocess.Popen] = None
        super().__init__(callback)

    def _listen(self):
        self._proc = subprocess.Popen(
            ('gsettings', 'monitor', 'org.gnome.desktop.interface', 'gtk-theme'),
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        with self._proc:
            for line in self._proc.stdout:
                self.callback('Dark' if '-dark' in line.strip().removeprefix("gtk-theme: '").removesuffix("'").lower() else 'Light')

    def _stop(self):
        self._proc.kill()

    def _wait(self):
        self._proc.wait()


__all__ = ("theme", "GnomeListener",)
