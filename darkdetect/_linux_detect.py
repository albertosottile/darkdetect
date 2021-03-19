#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
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
        return 'Light'
    else:
        if theme.endswith('-dark'):
            return 'Dark'
        else:
            return 'Light'

def isDark():
    return theme() == 'Dark'

def isLight():
    return theme() == 'Light'
