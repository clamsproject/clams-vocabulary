"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import BoundingBox_v1
from .v2 import BoundingBox_v2
from .v3 import BoundingBox_v3
from .v4 import BoundingBox_v4


class BoundingBox(BoundingBox_v4):
    """Latest version alias for BoundingBox_v4."""
    pass

__all__ = ['BoundingBox_v1', 'BoundingBox_v2', 'BoundingBox_v3', 'BoundingBox_v4', 'BoundingBox']
