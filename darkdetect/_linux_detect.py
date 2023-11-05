#-----------------------------------------------------------------------------
#  Copyright (C) 2023 Alberto Sottile, Eric Larson, Raghav Dhingra
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess

def _check_dbus_support():
    command = ["dbus-send","--session","--print-reply=literal","--dest=org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop", "org.freedesktop.portal.Setttings.Read", "string:org.freedesktop.appearance", "string:color-scheme"]
    out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout = str(out.stdout.decode())
    stderr = str(out.stderr.decode())
    if "error" in stderr.lower():
        return False
    else:
        return True

def theme():
    try:
        #Using dbus-send command to get the theme of user using the freedesktop standards
        command = ["dbus-send","--session","--print-reply=literal","--dest=org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop", "org.freedesktop.portal.Settings.Read", "string:org.freedesktop.appearance", "string:color-scheme"]
        out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout = str(out.stdout.decode())
        if len(stdout.strip())>1:
            finalResult = stdout.replace("uint32","").strip("variant \n")
            #0=Default, 1=prefers-dark, 2=prefers-light
            if finalResult == "1":
                return 'Dark'
            elif finalResult == "2":
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
    if _check_dbus_support():
        _last_msg = ""
        _last_theme = ""
        command = ("dbus-monitor","--session","--monitor","sender=org.freedesktop.portal.Desktop, member=SettingChanged")
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as p:
            for line in p.stdout:
                #Freedesktop check
                if "color-scheme" in _last_msg:
                    if "string" in line.strip():
                        finalResult = line.strip("variant \n string \"")
                        if finalResult == "prefer-dark":
                            if _last_theme != "Dark":
                                callback('Dark')
                            _last_theme = "Dark"
                        elif finalResult == "prefer-light":
                            if _last_theme != "Light":
                                callback('Light')
                            _last_theme = "Light"
                        else:
                            if _last_theme != "Light":
                                _last_theme = ""
                #kde-theme check, required as there also after selecting light
                #theme freedesktop spec is set to default
                elif "colorscheme" in _last_msg:
                    if "string" in line.strip():
                        finalResult = line.strip("variant \n string \"").lower()
                        if 'dark' in finalResult and _last_theme != "Dark":
                            callback('Dark')
                            _last_theme = "Dark"
                        elif _last_theme != "Light":
                            callback('Light')
                            _last_theme = "Light"
                #gtk-theme check
                elif "gtk-theme" in _last_msg:
                    if "string" in line.strip():
                        finalResult = line.strip("variant \n string \"").lower()
                        if '-dark' in finalResult:
                            if _last_theme != "Dark":
                                callback('Dark')
                            _last_theme = "Dark"
                        elif _last_theme != "Light":
                            callback('Light')
                            _last_theme = "Light"
                _last_msg = line.strip().lower()
    else:
        with subprocess.Popen(
            ('gsettings', 'monitor', 'org.gnome.desktop.interface', 'gtk-theme'),
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as p:
            for line in p.stdout:
                callback('Dark' if '-dark' in line.strip().removeprefix("gtk-theme: '").removesuffix("'").lower() else 'Light')
