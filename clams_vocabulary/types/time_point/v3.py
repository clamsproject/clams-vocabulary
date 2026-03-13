"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.region.v3 import Region_v3


class TimePoint_v3(Region_v3):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TimePoint/v3"
    version: ClassVar[str] = "v3"
    shortname: ClassVar[str] = "TimePoint"

    description: ClassVar[str] = "A time point in an audio or video stream."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimePoint/v3",
    ]

    timePoint: int = Field(..., description="The starting offset in the stream.")
