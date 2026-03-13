"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.polygon.v1 import Polygon_v1


class BoundingBox_v1(Polygon_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/BoundingBox/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "BoundingBox"

    description: ClassVar[str] = (
        "A rectangular object in an image or video. At the moment it does not have features that would not make any "
        "sense on its parent type Polygon so technically we can do without BoundingBox, but it was introduced because "
        "the term is in widespread use."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/BoundingBox/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/BoundingBox/",
        "http://mmif.clams.ai/0.4.1/vocabulary/BoundingBox/",
        "http://mmif.clams.ai/0.4.2/vocabulary/BoundingBox/",
    ]

    boxType: Optional[str] = Field(
        None,
        description="The type of BoundingBox. Mostly used for text boxes where we use the value text."
    )
