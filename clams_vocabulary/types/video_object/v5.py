"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, List
from pydantic import Field
from clams_vocabulary.types.region.v5 import Region_v5


class VideoObject_v5(Region_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/VideoObject/v5"
    version: ClassVar[str] = "v5"
    shortname: ClassVar[str] = "VideoObject"

    description: ClassVar[str] = (
        "A sequence of Polygons, where each Polygon is associated with a TimePoint. So a VideoObject is in effect a "
        "sequence of image objects at certain time points."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/VideoObject/v5",
    ]

    polygons: List[str] = Field(..., description="The Polygons that make up the object.")
