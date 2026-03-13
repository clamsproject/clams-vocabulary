from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.region.archetype import Region


class TimePoint(Region):
    description: ClassVar[str] = "A time point in an audio or video stream."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimePoint/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/TimePoint/",
        "http://mmif.clams.ai/0.4.1/vocabulary/TimePoint/",
        "http://mmif.clams.ai/0.4.2/vocabulary/TimePoint/",
    ]

    timePoint: int = Field(..., description="The starting offset in the stream.")
