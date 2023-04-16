#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess

def theme():
    try:
        #Using dbus-send command to get the theme of user using the freedesktop standards
        command = ["dbus-send","--session","--print-reply=literal","--dest=org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop", "org.freedesktop.portal.Settings.Read", "string:org.freedesktop.appearance", "string:color-scheme"]
        out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout=str(out.stdout.decode())
        if len(stdout.strip())<1:
            pass
        else:
            finalResult=stdout.replace("uint32","").strip("variant \n")
            #0=Default, 1=prefers-dark, 2=prefers-light
            if finalResult=="1":
                return 'Dark'
            elif (finalResult=="2"):
                return 'Light'
            else:
                #If result Default(0) or invalid, fallback to gtk-theme method
                pass
    except Exception:
        pass
    try:
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

def isDark():
    return theme() == 'Dark'

def isLight():
    return theme() == 'Light'

# def listener(callback: typing.Callable[[str], None]) -> None:
def listener(callback):
    with subprocess.Popen(
        ('gsettings', 'monitor', 'org.gnome.desktop.interface', 'gtk-theme'),
        stdout=subprocess.PIPE,
        universal_newlines=True,
    ) as p:
        for line in p.stdout:
            callback('Dark' if '-dark' in line.strip().removeprefix("gtk-theme: '").removesuffix("'").lower() else 'Light')
