"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.region.v1 import Region_v1


class TimePoint_v1(Region_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TimePoint/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "TimePoint"

    description: ClassVar[str] = "A time point in an audio or video stream."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimePoint/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/TimePoint/",
        "http://mmif.clams.ai/0.4.1/vocabulary/TimePoint/",
        "http://mmif.clams.ai/0.4.2/vocabulary/TimePoint/",
    ]

    timePoint: int = Field(..., description="The starting offset in the stream.")
