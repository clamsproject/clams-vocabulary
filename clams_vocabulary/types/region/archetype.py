from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.annotation.archetype import Annotation


class Region(Annotation):
    description: ClassVar[str] = (
        "An annotation over a region in primary data where primary data can be a text, an image, an audio stream or a "
        "video streem. Typically one of the sub types of this will be used."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Region/v5",
    ]

    timeUnit: Optional[str] = Field(
        None,
        description="Specifies which unit of time the measurement is based. Can be *seconds* or *milliseconds*, or "
                    "in case of annotations on a VideoDocument, *frames*. If not specified, *milliseconds* (in whole "
                    "numbers) is assumed. <br><br> [note] This property is only relevant for time-based annotations. "
                    "[/note]"
    )
