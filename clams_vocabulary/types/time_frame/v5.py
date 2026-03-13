"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.interval.v4 import Interval_v4


class TimeFrame_v5(Interval_v4):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TimeFrame/v5"
    version: ClassVar[str] = "v5"
    shortname: ClassVar[str] = "TimeFrame"

    _property_aliases: ClassVar[dict] = {
        'classification': {'classification', 'classifications'},
        'label': {'frameType', 'label'},
    }

    description: ClassVar[str] = (
        "A temporal interval in an audio or video stream. This is similar to the term segment used in audio "
        "processing, but that term has a different meaning in the image and video community."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TimeFrame/v5",
    ]

    frameType: Optional[str] = Field(
        None,
        description="The type of TimeFrame. Possible values include, but are not limited to, bars, tones, "
                    "bars-and-tones, speech, noise, music, slate, chyron, lower-third, credits, and other. <br><br> "
                    "No longer encouraged to use, instead <code>label</code> property should replace this property."
    )
