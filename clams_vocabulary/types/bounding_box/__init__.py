"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import BoundingBox_v1
from .v2 import BoundingBox_v2


class BoundingBox(BoundingBox_v2):
    """Latest version alias for BoundingBox_v2."""
    pass

__all__ = ['BoundingBox_v1', 'BoundingBox_v2', 'BoundingBox']
