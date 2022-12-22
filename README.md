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
The `darkdetect.Listener` class exposes the following methods / members:

##### `.__init__(callback: Optional[Callable[[str], None]])`

The constructor simply sets `.callback` to the given callback argument

##### `.callback: Optional[Callable[[str], None]]`

The callback function that the listener uses.
This function will be passed "Dark" or "Light" when the theme is changed.
It is safe to change this during program execution.
It is safe to set this value to `None`, while the listener will still be active,
theme changes will not invoke the callback; though running callbacks will not be interrupted.
This is useful if 'temporarily pausing' the listener is desired.

##### `.listen()`

This starts listening for theme changes, it will invoke
`self.callback(theme_name)` when a change is detected.

After a listener is stopped successfully via `.stop` (the return value must be `True`),
it can be started again via `.listen()`.
New listeners may be constructed, should waiting for `.stop` not be desired.

##### `.stop(timeout: Optional[int]) -> bool`

This function initiates the listener stop sequence and
waits for the listener to stop for at most `timeout` seconds.
This function returns `True` if the listener successfully
stops before the timeout expires; otherwise `False`.
`timeout` may be any non-negative integer or `None`.
After `.stop` returns, regardless of the argument passed to it,
theme changes will no longer invoke the callback
Running callbacks will not be interrupted and may continue executing.

`.stop` may safely be re-invoked any number of times.
Calling `.stop(None)` after `.stop(0)` will work as expected.

In most cases `.stop(0)` should be sufficient as this will successfully
prevent future theme changes from generating callbacks.
The two primary use cases for `stop` with a timeout are:
1. Cleaning up listener resources (be that subprocesses or something else)
2. To restart the existing listener; a listener's `.listen()` function
may only be re-invoked if a call to `.stop` has returned `True`.

##### Wrapper Function

The simplest method of using this API is the `darkdetect.listener` function, which takes a callback function as an argument.
This function is a small wrapper around `Listener(callback).listen()`.
_In this mode, the listener cannot be stopped_; forceful stops may not clean up resources (such as subprocesses if applicable).


### Examples

##### A simple listener:
```python
import threading
import darkdetect

listener = darkdetect.Listener(print)
t = threading.Thread(target=listener.listen, daemon=True)
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
	print("Callbacks / listener are still running after 5 seconds!")
```

##### Possible GUI app shutdown sequence
```python
def shutdown(self):
  self.listener.stop(0)  # Initiate stop, allows callbacks to continue running
  self.other_shutdown_methods() # Stop other processes

  # Wait a bit longer for callbacks to complete and listener to clean up
  try:
    if self.listener.stop(timeout=10) is False:
		# Log that listener is still running but that we are quitting anyway
		self.logger.exception("Failed to shutdown listener within 10 seconds, quitting anyway.")
```

##### Example of wrapper `listener` function:
```python
import threading
import darkdetect

t = threading.Thread(target=darkdetect.listener, args=(print,), daemon=True)
t.start()
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
