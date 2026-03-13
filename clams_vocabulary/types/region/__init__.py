"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .v1 import Region_v1
from .v2 import Region_v2
from .v3 import Region_v3


class Region(Region_v3):
    """Latest version alias for Region_v3."""
    pass

__all__ = ['Region_v1', 'Region_v2', 'Region_v3', 'Region']
