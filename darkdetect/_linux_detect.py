#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

from ctypes import util, cdll, c_char_p, byref


def theme():
    # Here we just triage to GTK settings for now
    try:
        gtklib = cdll.LoadLibrary(util.find_library('gtk-3'))
        gtklib.gtk_init(None, None)
        settings = gtklib.gtk_settings_get_default()
        res = c_char_p()
        gtklib.g_object_get(settings, b"gtk-theme-name", byref(res), 0)
        theme = res.value.decode()
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
