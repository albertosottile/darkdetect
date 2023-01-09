# `darkdetect` API

The centerpiece of the API is the `Listener` class.
Members of this class are:

### The constructor: `.__init__(callback: Optional[Callable[[str], None]])`

The constructor simply sets `.callback` to the given callback argument

### The callback: `.callback: Optional[Callable[[str], None]]`

The callback function that the listener uses.
This function will be passed "Dark" or "Light" when the theme is changed.
It is safe to change this during program execution.
It is safe to set this value to `None`, while the listener will still be active,
theme changes will not invoke the callback; though running callbacks will not be interrupted.
This is useful if 'temporarily pausing' the listener is desired.

### The listen function: `.listen()`

This starts listening for theme changes, it will invoke
`self.callback(theme_name)` when a change is detected.

After a listener is stopped successfully via `.stop` (the return value must be `True`),
it can be started again via `.listen()`.
New listeners may be constructed, should waiting for `.stop` not be desired.

### The stop function: `.stop(timeout: Optional[int]) -> bool`

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

---

## Wrapper Function

The simplest method of using this API is the `darkdetect.listener` function, which takes a callback function as an argument.
This function is a small wrapper around `Listener(callback).listen()`.
_In this mode, the listener cannot be stopped_; forceful stops may not clean up resources (such as subprocesses if applicable).
