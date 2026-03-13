"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.time_frame.v1 import TimeFrame_v1


class Chapter_v1(TimeFrame_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Chapter/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Chapter"

    description: ClassVar[str] = (
        "Example case for when we do not want to use Segment with a specific segmentType or if we want to introduce "
        "special properties."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Chapter/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/Chapter/",
        "http://mmif.clams.ai/0.4.1/vocabulary/Chapter/",
        "http://mmif.clams.ai/0.4.2/vocabulary/Chapter/",
    ]

    title: Optional[str] = Field(None, description="Title of the chapter")
