# Darkdetect

This package allows to detect if the user is using Dark Mode on:

- [macOS 10.14+](https://support.apple.com/en-us/HT208976)
- [Windows 10 1607+](https://blogs.windows.com/windowsexperience/2016/08/08/windows-10-tip-personalize-your-pc-by-enabling-the-dark-theme/)
- Linux with [a dark GTK theme](https://www.gnome-look.org/browse/cat/135/ord/rating/?tag=dark).

The main application of this package is to detect the Dark mode from your GUI Python application (Tkinter/wx/pyqt/qt for python (pyside)/...) and apply the needed adjustments to your interface. Darkdetect is particularly useful if your GUI library **does not** provide a public API for this detection (I am looking at you, Qt). In addition, this package does not depend on other modules or packages that are not already included in standard Python distributions.

## Install

The preferred channel is PyPI:
```bash
pip install darkdetect
```

Alternatively, you are free to vendor directly a copy of Darkdetect in your app. Further information on vendoring can be found [here](https://medium.com/underdog-io-engineering/vendoring-python-dependencies-with-pip-b9eb6078b9c0).

### macOS Listener Support

To enable the macOS listener, additional components are required, these can be installed via:
```bash
pip install darkdetect[macos-listener]
```

## Usage

```python
import darkdetect

>>> darkdetect.theme()
'Dark'

>>> darkdetect.isDark()
True

>>> darkdetect.isLight()
False
```
It's that easy.

### Listener

`darkdetect` exposes a listener API which is far more efficient than busy waiting on `theme()` changes.
This API is exposed primarily via a `Listener` class.
Detailed API documentation can be found [here](docs/api.md).
For a quick overview: the `darkdetect.Listener` class exposes the following methods / members:

##### `.__init__(callback: Optional[Callable[[str], None]])`
The constructor simply sets `.callback` to the given callback argument

##### `.callback: Optional[Callable[[str], None]]`
The settable callback function that the listener uses; it will be passed "Dark" or "Light" when the theme is changed.

##### `.listen()`
This starts listening for theme changes, it will invoke
`self.callback(theme_name)` when a change is detected.

##### `.stop(timeout: Optional[int]) -> bool`

This function attempts to stop the listener,
waiting at most `timeout` seconds (`None` means infinite),
returning `True` on success, `False` on timeout.

Regardless of the result, after `.stop` returns, theme changes 
will no longer trigger `callback`, though running callbacks will
not be interrupted.

`.stop` may safely be re-invoked any number of times.
`.listen()` may not be called until a call to `.stop` succeeds.

##### Wrapper Function

The simplest method of using this API is the `darkdetect.listener` function,
which takes a callback function as an argument.
This function is a small wrapper around `Listener(callback).listen()`.
_In this mode, the listener cannot be stopped_; forceful stops may not clean up resources (such as subprocesses if applicable).

### Examples

Below are 2 examples of basic usage; additional examples can be found [here](docs/examples.md).

##### A simple listener:
```python
import threading
import darkdetect

listener = darkdetect.Listener(print)
t = threading.Thread(target=listener.listen, daemon=True)
# OR: t = threading.Thread(target=darkdetect.listener, args=(print,), daemon=True)
t.start()
```

##### User input controlling listener
```python
import threading
import darkdetect
import time

listener = darkdetect.Listener(print)
t = threading.Thread(target=listener.listen)
t.start()

txt = ""
while txt != "quit":
  txt = input()
  if txt == "print":
    listener.callback = print
  elif txt == "verbose":
    listener.callback = lambda x: print(f"The theme changed to {x} as {time.time()}")
listener.stop(0)

print("Waiting for running callbacks to complete and the listener to terminate")
if not listener.stop(timeout=5):
  print("Callbacks/listener are still running after 5 seconds!")
```

## Known Issues

1. On macOS, detection of the dark menu bar and dock option (available from macOS 10.10) is not supported.
1. On macOS, using the listener API in a bundled app where `sys.executable` is not a python interpreter (such as pyinstaller builds), is not supported.
1. On Windows, the after `Listener.stop(None)` is not supported as it may not die until another theme change is detected.
Future invocations of `callback` will not be made, but the listener itself will persist.

## Notes

- This software is licensed under the terms of the 3-clause BSD License.
- This package can be installed on any operative system, but `theme()`, `isDark()`, and `isLight()` will always return `None` unless executed on a OS that supports Dark Mode, including older versions of macOS and Windows.
- [Details](https://stackoverflow.com/questions/25207077/how-to-detect-if-os-x-is-in-dark-mode) on the detection method used on macOS.
- [Details](https://askubuntu.com/questions/1261366/detecting-dark-mode#comment2132694_1261366) on the experimental detection method used on Linux.
