"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.polygon.v4 import Polygon_v4


class BoundingBox_v4(Polygon_v4):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/BoundingBox/v4"
    version: ClassVar[str] = "v4"
    shortname: ClassVar[str] = "BoundingBox"

    _property_aliases: ClassVar[dict] = {
        'classification': {'classification', 'classifications'},
        'label': {'boxType', 'label'},
    }

    description: ClassVar[str] = (
        "A rectangular object in an image or video. At the moment it does not have features that would not make any "
        "sense on its parent type Polygon so technically we can do without BoundingBox, but it was introduced because "
        "the term is in widespread use."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/BoundingBox/v4",
    ]

    boxType: Optional[str] = Field(
        None,
        description="The type of BoundingBox. Mostly used for text boxes where we use the value text. <br><br> No "
                    "longer encouraged to use, and instead <code>label</code> property should replace this property."
    )
