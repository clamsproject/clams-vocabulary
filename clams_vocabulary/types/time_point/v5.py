"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.region.v5 import Region_v5


class TimePoint_v5(Region_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TimePoint/v5"
    version: ClassVar[str] = "v5"
    shortname: ClassVar[str] = "TimePoint"

    description: ClassVar[str] = "A time point in an audio or video stream."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimePoint/v5",
    ]

    timePoint: int = Field(..., description="The starting offset in the stream.")
