#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess


def theme():
    # Here we just triage to GTK settings for now
    out = subprocess.Popen(
        ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = out.communicate()
    theme = stdout.lower().decode().strip()[1:-1]  # remove start and end quote
    if theme.endswith('-dark'):
        return 'Dark'
    else:
        return 'Light'

def isDark():
    return theme() == 'Dark'

def isLight():
    return theme() == 'Light'
