from typing import ClassVar, List
from pydantic import Field
from clams_vocabulary.types.region.archetype import Region


class VideoObject(Region):
    description: ClassVar[str] = (
        "A sequence of Polygons, where each Polygon is associated with a TimePoint. So a VideoObject is in effect a "
        "sequence of image objects at certain time points."
    )
    alsoKnownAs: ClassVar[list[str]] = []

    polygons: List[str] = Field(..., description="The Polygons that make up the object.")
