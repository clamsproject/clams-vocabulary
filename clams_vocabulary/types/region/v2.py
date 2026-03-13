"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.annotation.v3 import Annotation_v3


class Region_v2(Annotation_v3):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Region/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "Region"

    description: ClassVar[str] = (
        "An annotation over a region in primary data where primary data can be a text, an image, an audio stream or a "
        "video streem. Typically one of the sub types of this will be used."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Region/v2",
    ]

    timeUnit: Optional[str] = Field(
        None,
        description="Specifies which unit of time the measurement is based. Can be *seconds* or *milliseconds*, or "
                    "in case of annotations on a VideoDocument, *frames*."
    )
