"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import VideoObject_v1
from .v2 import VideoObject_v2
from .v3 import VideoObject_v3
from .v4 import VideoObject_v4


class VideoObject(VideoObject_v4):
    """Latest version alias for VideoObject_v4."""
    pass

__all__ = ['VideoObject_v1', 'VideoObject_v2', 'VideoObject_v3', 'VideoObject_v4', 'VideoObject']
