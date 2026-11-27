from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.time_frame.archetype import TimeFrame


class Chapter(TimeFrame):
    description: ClassVar[str] = (
        "Example case for when we do not want to use Segment with a specific segmentType or if we want to introduce "
        "special properties."
    )
    alsoKnownAs: ClassVar[list[str]] = []

    title: Optional[str] = Field(None, description="Title of the chapter")
