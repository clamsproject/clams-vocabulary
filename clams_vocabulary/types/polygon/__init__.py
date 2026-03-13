"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import Polygon_v1
from .v2 import Polygon_v2
from .v3 import Polygon_v3


class Polygon(Polygon_v3):
    """Latest version alias for Polygon_v3."""
    pass

__all__ = ['Polygon_v1', 'Polygon_v2', 'Polygon_v3', 'Polygon']
