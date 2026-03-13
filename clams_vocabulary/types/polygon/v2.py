"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, List, Optional
from pydantic import Field
from clams_vocabulary.types.region.v2 import Region_v2


class Polygon_v2(Region_v2):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Polygon/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "Polygon"

    description: ClassVar[str] = (
        "A polygon in an image or video. This is a two-dimensional object so if this occurs in a video it will be "
        "anchored to a particular frame or time point in the video."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Polygon/v2",
    ]

    coordinates: List[List[int]] = Field(
        ...,
        description="The coordinates of the polygon, taking the top-left of the image as the origin (0,0). Unit used "
                    "to measure the distance is the number of pixels."
    )
    timePoint: Optional[int] = Field(
        None,
        description="If on a video stream, the TimePoint that the BoundingBox occurs in."
    )
