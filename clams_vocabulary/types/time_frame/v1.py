"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.interval.v1 import Interval_v1


class TimeFrame_v1(Interval_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TimeFrame/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "TimeFrame"

    description: ClassVar[str] = (
        "A temporal interval in an audio or video stream. This is similar to the term segment used in audio "
        "processing, but that term has a different meaning in the image and video community."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimeFrame/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/TimeFrame/",
        "http://mmif.clams.ai/0.4.1/vocabulary/TimeFrame/",
        "http://mmif.clams.ai/0.4.2/vocabulary/TimeFrame/",
    ]

    frameType: Optional[str] = Field(
        None,
        description="The type of TimeFrame. Could be bars-and-tones, speech, noise, music, other."
    )
