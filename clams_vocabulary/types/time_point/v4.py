"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.region.v4 import Region_v4


class TimePoint_v4(Region_v4):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TimePoint/v4"
    version: ClassVar[str] = "v4"
    shortname: ClassVar[str] = "TimePoint"

    description: ClassVar[str] = "A time point in an audio or video stream."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimePoint/v4",
    ]

    timePoint: int = Field(..., description="The starting offset in the stream.")
