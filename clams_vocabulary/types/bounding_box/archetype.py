from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.polygon.archetype import Polygon


class BoundingBox(Polygon):
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
