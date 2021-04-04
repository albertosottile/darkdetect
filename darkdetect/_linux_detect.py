#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

from ctypes import util, cdll, c_char_p, byref
import subprocess

def theme():
    # Here we just triage to GTK settings for now
    out = subprocess.Popen(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout, stderr = out.communicate()
    stdout = stdout.lower()
    
    if 'dark' in stdout:
        return 'Dark'
    elif 'highcontrast' in stdout:
        return 'HighContrast'
    else:
        return 'Light'     
    
def isDark():
    return theme() == 'Dark'

def isLight():
    return theme() == 'Light'
