#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------


__version__: str = '0.7.1'


import sys
import platform
from typing import Callable, Type

from .base import BaseListener
Listener: Type[BaseListener]

#
# Import correct the listener for the given OS
#

def macos_supported_version():
    sysver: str = platform.mac_ver()[0]  # typically 10.14.2 or 12.3
    major: int = int(sysver.split('.')[0])
    if major < 10:
        return False
    if major >= 11:
        return True
    return int(sysver.split('.')[1]) >= 14

if sys.platform == "darwin" and macos_supported_version():
    from ._mac_detect import *
    Listener = MacListener
# If running Windows 10 version 10.0.14393 (Anniversary Update) OR HIGHER.
# The getwindowsversion method returns a tuple.
# The third item is the build number that we can use to check if the user has a new enough version of Windows.
elif sys.platform == "win32" and platform.release().isdigit() and int(platform.release()) >= 10 and \
        int(platform.version().split('.')[2]) >= 14393:
    from ._windows_detect import *
    Listener = WindowsListener
elif sys.platform == "linux":
    from ._linux_detect import *
    Listener = GnomeListener
else:
    from ._dummy import *
    Listener = DummyListener

#
# Common shortcut functions
#

def isDark():
    return theme() == "Dark"

def isLight():
    return theme() == "Light"

def listener(callback: Callable[[str], None]) -> None:
    Listener(callback).listen()


del sys, platform, Callable, Type
