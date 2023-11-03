#-----------------------------------------------------------------------------
#  Copyright (C) 2023 Alberto Sottile, Eric Larson, Michael Harvey
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess

def _run(args):
    out = subprocess.run(args, capture_output=True)
    return out.stdout.decode()


def _desktop():
    """
    Get simplified desktop identifier. There are several variations of the gnome
    desktop string. If desktop is not recognized, return empty string.

    :return: GNOME, MATE, KDE, XFCE, Unity, LXDE
    """
    import os
    desktop = ''
    if 'XDG_CURRENT_DESKTOP' in os.environ:
        desktop = os.environ['XDG_CURRENT_DESKTOP']

    # https://askubuntu.com/questions/72549/how-to-determine-which-window-manager-and-desktop-environment-is-running/227669#227669
    if 'GNOME' in desktop:
        desktop = 'GNOME'
    elif 'Cinnamon' in desktop:
        desktop = 'GNOME'

    return desktop


def theme():
    """
    :return: 'Dark' or 'Light', or 'Unknown' if the theme cannot be unambiguously identified.
    """
    theme_name = ''
    try:
        desktop = _desktop()

        if desktop == 'GNOME':
            #Using the freedesktop specifications for checking dark mode
            stdout = _run(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'])
            #If not found then trying older gtk-theme method
            if len(stdout)<1:
                stdout = _run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'])
            # we have a string, now remove start and end quote added by gsettings
            theme_name = stdout.lower().strip()[1:-1]
        elif desktop == 'XFCE':
            theme_name = _run(['xfconf-query', '-c', 'xsettings', '-p', '/Net/ThemeName'])
    except Exception:
        return 'Unknown'

    if '-dark' in theme_name.lower():
        return 'Dark'
    elif theme_name:
        return 'Light'
    else:
        return 'Unknown'


def isDark():
    return theme() == 'Dark'


def isLight():
    return theme() == 'Light'


# def listener(callback: typing.Callable[[str], None]) -> None:
def listener(callback):
    desktop = _desktop()

    if desktop == 'GNOME':
        with subprocess.Popen(
            ('gsettings', 'monitor', 'org.gnome.desktop.interface', 'gtk-theme'),
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as p:
            for line in p.stdout:
                callback('Dark' if '-dark' in line.strip().removeprefix("gtk-theme: '").removesuffix("'").lower() else 'Light')
    elif desktop == 'XFCE':
        with subprocess.Popen(
                ('xfconf-query', '-m', '-c', 'xsettings', '-p-', '/Net/ThemeName'),
                stdout=subprocess.PIPE,
                universal_newlines=True,
        ):
            callback(theme())

