"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import TimePoint_v1
from .v2 import TimePoint_v2
from .v3 import TimePoint_v3


class TimePoint(TimePoint_v3):
    """Latest version alias for TimePoint_v3."""
    pass

__all__ = ['TimePoint_v1', 'TimePoint_v2', 'TimePoint_v3', 'TimePoint']
