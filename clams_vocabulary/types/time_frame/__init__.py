"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import TimeFrame_v1
from .v2 import TimeFrame_v2
from .v3 import TimeFrame_v3
from .v4 import TimeFrame_v4


class TimeFrame(TimeFrame_v4):
    """Latest version alias for TimeFrame_v4."""
    pass

__all__ = ['TimeFrame_v1', 'TimeFrame_v2', 'TimeFrame_v3', 'TimeFrame_v4', 'TimeFrame']
