"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import TimeFrame_v1
from .v2 import TimeFrame_v2


class TimeFrame(TimeFrame_v2):
    """Latest version alias for TimeFrame_v2."""
    pass

__all__ = ['TimeFrame_v1', 'TimeFrame_v2', 'TimeFrame']
