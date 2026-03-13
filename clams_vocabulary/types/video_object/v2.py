"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, List
from pydantic import Field
from clams_vocabulary.types.region.v2 import Region_v2


class VideoObject_v2(Region_v2):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/VideoObject/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "VideoObject"

    description: ClassVar[str] = (
        "A sequence of Polygons, where each Polygon is associated with a TimePoint. So a VideoObject is in effect a "
        "sequence of image objects at certain time points."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/VideoObject/v2",
    ]

    polygons: List[str] = Field(..., description="The Polygons that make up the object.")
