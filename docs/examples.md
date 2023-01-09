# `darkdetect` Examples

### Listening with the `listener` method
```python
import threading
import darkdetect

t = threading.Thread(target=darkdetect.listener, args=(print,), daemon=True)
t.start()
```

### Listening with the `Listener` class
```python
import threading
import darkdetect

listener = darkdetect.Listener(print)
t = threading.Thread(target=listener.listen, daemon=True)
t.start()
```

### Stop on user input
```python
import threading
import darkdetect

listener = darkdetect.Listener(print)
t = threading.Thread(target=listener.listen, daemon=True)
t.start()

input()  # Wait for user input
listener.stop(0)
```

### User adjustable callback
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

### Possible GUI app shutdown sequence
```python
def shutdown(self):
  self.listener.stop(0)  # Prevent callback from being invoked on theme changes
  # Existing callbacks may still be running!
  
  self.other_shutdown_methods() # Stop other processes

  # Wait a bit longer for callbacks to complete and listener to clean up
  if self.listener.stop(timeout=5) is False:
      # Log that listener is still running but that we are quitting anyway
      self.logger.exception("Failed to shutdown listener / running callbacks within 5 seconds, quitting anyway.")
```
