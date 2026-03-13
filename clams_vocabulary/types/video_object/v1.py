"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, List
from pydantic import Field
from clams_vocabulary.types.region.v1 import Region_v1


class VideoObject_v1(Region_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/VideoObject/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "VideoObject"

    description: ClassVar[str] = (
        "A sequence of Polygons, where each Polygon is associated with a TimePoint. So a VideoObject is in effect a "
        "sequence of image objects at certain time points."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/VideoObject/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/VideoObject/",
        "http://mmif.clams.ai/0.4.1/vocabulary/VideoObject/",
        "http://mmif.clams.ai/0.4.2/vocabulary/VideoObject/",
    ]

    polygons: List[str] = Field(..., description="The Polygons that make up the object.")
