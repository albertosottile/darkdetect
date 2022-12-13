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

##### `.__init__(callback: Callable[[str], None])`

The construct simply sets `.callback` to the given callback argument

##### `.callback: Callable[[str], None]` 

The callback function that the listener uses.
The function will be called with string "Dark" or "Light" when the OS 
It is safe to change this during program execution.

##### `.listen()`

This starts listening for theme changes, it will invoke `self.callback(theme_name)` when a change is detected.

##### `.stop()`

This initiates the listener stop procedure; it will return immediately and will not wait for the listener or running callbacks to complete; it simply informs the listener that it may stop listening.
Internally, listening may be done via a subprocess, so this can be thought of as a `subprocess.kill`.
If the listener is not actively listening, this function is a no-op.

##### `.wait(timeout: Optional[int] = None)`

This will stop (as needed) the listener and wait for it / running callbacks to complete execution.
It is not necessary to invoke `.stop()` before this function, as `.wait()` will invoke `.stop()` automatically.
If a timeout is specified, `.wait` will wait at most `timeout` seconds before exiting.
If this method times out, it will raise a `darkdetect.DDTimeoutError`.

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
listener.stop()

print("Waiting for running callbacks to complete")
listener.wait()
```

##### Possible GUI app shutdown sequence
```python
def shutdown(self):
  self.listener.stop() # Initiate stop, allows callbacks to continue running
  self.other_shutdown_methods() # Stop other processes

  # Wait a bit longer for callbacks to complete and listener to clean up
  try:
    self.listener.wait(timeout = 10)  # This app has long callbacks, shutdown should be fast though!
  except darkdetect.DDTimeoutError as e:
    # Log that callbacks are still running but that we are quitting anyway
    self.logger.exception(e)
```

##### Super simple example of wrapper `listener` function:
```python
import threading
import darkdetect

t = threading.Thread(target=darkdetect.listener, args=(print,), daemon=True)
t.start()
```

## Notes

- This software is licensed under the terms of the 3-clause BSD License.
- This package can be installed on any operative system, but `theme()`, `isDark()`, and `isLight()` will always return `None` unless executed on a OS that supports Dark Mode, including older versions of macOS and Windows.
- On macOS, detection of the dark menu bar and dock option (available from macOS 10.10) is not supported.
- On Windows, the after `Listener.stop()` is invoked and running callbacks complete, future callbacks should not be made, but the listener itself will not die until another theme change; that is `.wait()` will hang until another theme change. _PRs fixing this are welcome._
- [Details](https://stackoverflow.com/questions/25207077/how-to-detect-if-os-x-is-in-dark-mode) on the detection method used on macOS.
- [Details](https://askubuntu.com/questions/1261366/detecting-dark-mode#comment2132694_1261366) on the experimental detection method used on Linux.
