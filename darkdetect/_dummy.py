#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

from .base import BaseListener


def theme():
    return None


class DummyListener(BaseListener):
    """
    A dummy listener class that implements nothing the abstract class does not
    """


__all__ = ("theme", "DummyListener")
