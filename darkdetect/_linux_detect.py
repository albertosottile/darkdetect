#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess


def theme():
    # Here we just triage to GTK settings for now
    try:
        proc = subprocess.run(
            ['gsettings', 'get', 'org.gnome.desktop.interface',
             'gtk-theme'], capture_output=True)
        theme = proc.stdout.decode().strip().strip("'")
    except Exception:
        return None
    else:
        if theme.endswith('-dark'):
            return 'Dark'
        else:
            return 'Light'

def isDark():
    got = theme()
    if got is None:
        return None
    else:
        return theme() == 'Dark'

def isLight():
    got = theme()
    if got is None:
        return None
    else:
        return theme() == 'Light'
