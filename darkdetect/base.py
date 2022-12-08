from typing import Callable
from enum import Enum, auto


class ListenerState(Enum):
    """
    A listener state
    """
    Listening = auto()
    Stopping = auto()
    Dead = auto()


class BaseListener:
    """
    An abstract listener class
    Subclasses promise that it is safe to call stop() then wait()
    from a different thread than listen() was called in; provides two
    threads are not both racing to call these methods
    """

    def __init__(self, callback: Callable[[str], None]):
        """
        :param callback: The callback to use when the listener detects something
        """
        self._state: ListenerState = ListenerState.Dead
        self.callback: Callable[[str], None] = callback

    def listen(self):
        """
        Start the listener if it is not already running
        """
        if self._state == ListenerState.Listening:
            raise RuntimeError("Do not run .listen() from multiple threads concurrently")
        elif self._state == ListenerState.Stopping:
            raise RuntimeError("Call .wait() to wait for the previous listener to finish shutting down")
        self._state = ListenerState.Listening
        try:
            self._listen()
        except Exception as e:
            self.stop()  # Just in case
            raise RuntimeError("Listen failed") from e

    def stop(self):
        """
        Tells the listener to stop; may return before the listener has stopped
        If the listener is not currently listening, this is a no-op
        This function may be called if .listen() errors
        """
        if self._state == ListenerState.Listening:
            self._stop()
            self._state = ListenerState.Stopping

    def wait(self):
        """
        Stop the listener and wait's for it to finish
        If the listener is dead, this is a no-op
        """
        if self._state != ListenerState.Dead:
            self.stop()
            self._wait()
            self._state = ListenerState.Dead

    # Non-public methods

    def _listen(self):
        """
        Start the listener
        """
        raise NotImplementedError()

    def _stop(self):
        """
        Tell the listener, do not bother waiting for it to finish stopping
        """
        raise NotImplementedError()

    def _wait(self):
        """
        Wait for the listener to stop
        Promised that .stop() method will have already been called
        """
        raise NotImplementedError()


__all__ = ("BaseListener", "ListenerState")
