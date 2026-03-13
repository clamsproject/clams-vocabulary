"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.time_frame.v2 import TimeFrame_v2


class Chapter_v2(TimeFrame_v2):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Chapter/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "Chapter"

    description: ClassVar[str] = (
        "Example case for when we do not want to use Segment with a specific segmentType or if we want to introduce "
        "special properties."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Chapter/v2",
    ]

    title: Optional[str] = Field(None, description="Title of the chapter")
