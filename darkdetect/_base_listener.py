from typing import Callable, Optional
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
    It is safe to call stop from a different thread than listen() was called in
    provided multiple threads are not racing to call these methods
    """

    def __init__(self, callback: Optional[Callable[[str], None]]):
        """
        :param callback: The callback to use when the listener detects something
        """
        self._state: ListenerState = ListenerState.Dead
        self.callback: Optional[Callable[[str], None]] = callback

    def listen(self):
        """
        Start the listener if it is not already running
        """
        if self._state == ListenerState.Listening:
            raise RuntimeError("Do not run .listen() from multiple threads concurrently")
        if self._state == ListenerState.Stopping:
            raise RuntimeError("Call .stop to wait for the previous listener to finish shutting down")
        self._state = ListenerState.Listening
        try:
            self._listen()
        except NotImplementedError:
            self._state = ListenerState.Dead
            raise
        except Exception as e:
            self.stop()  # Just in case
            raise RuntimeError("Listen failed") from e

    def stop(self, timeout: Optional[int] = None) -> bool:
        """
        Initiate the listener stop sequence, wait at most timeout seconds for it to complete.
        After this function returns, new theme changes will not invoke callbacks.
        Running callbacks will not be interrupted.
        May safely be called as many times as desired.
        Warning: stop(None) may hang until the next theme change, depending on implementation
        :param timeout: How many seconds to wait until the listener stops; None means infinite
        :return: True if the listener completes before the timeout expires, else False
        """
        if timeout is not None and timeout < 0:
            raise ValueError("timeout may not be negative")
        if self._state == ListenerState.Listening:
            self._initiate_shutdown()
            self._state = ListenerState.Stopping
        if self._state == ListenerState.Stopping:
            if self._wait_for_shutdown(timeout):
                self._state = ListenerState.Dead
        return self._state == ListenerState.Dead

    # Non-public helper methods

    def _invoke_callback(self, value: str) -> None:
        """
        Invoke the stored callback if the state is listening
        """
        if self._state == ListenerState.Listening:
            c: Optional[Callable[[str], None]] = self.callback
            if c is not None:
                c(value)

    # Non-public methods

    def _listen(self) -> None:
        """
        Start the listener
        """
        raise NotImplementedError()

    def _initiate_shutdown(self) -> None:
        """
        Tell the listener to initiate shutdown
        """
        raise NotImplementedError()

    def _wait_for_shutdown(self, timeout: Optional[int]) -> bool:
        """
        Wait for the listener to stop at most timeout seconds
        Promised that _initiate_shutdown() will have already run
        :param timeout: How many seconds to wait until the listener stops; None means infinite
        :return: True if the listener completes before the timeout expires, else False
        """
        raise NotImplementedError()


__all__ = ("BaseListener", "ListenerState")
