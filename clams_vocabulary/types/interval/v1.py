"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, List, Optional
from pydantic import Field
from clams_vocabulary.types.region.v1 import Region_v1


class Interval_v1(Region_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Interval/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Interval"

    description: ClassVar[str] = (
        "An annotation over an interval of linear primary data, either a text, a video or audio stream. An Interval "
        "may be defined by pointing directly into primary data (by using start and end offsets) or by linking to one "
        "or more other Annotations with the targets property. This annotation type is intended to be an abstract type "
        "and typically one of the sub types will be used."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Interval/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/Interval/",
        "http://mmif.clams.ai/0.4.1/vocabulary/Interval/",
        "http://mmif.clams.ai/0.4.2/vocabulary/Interval/",
    ]

    start: Optional[int] = Field(
        None,
        description="The starting offset in the primary data. This point is inclusive. For time intervals, the unit "
                    "is determined by the *timeUnit* metadata key. For text intervals, the unit is Unicode code "
                    "point."
    )
    end: Optional[int] = Field(
        None,
        description="The ending offset in the primary data. This point is exclusive. For time intervals, the unit is "
                    "determined by the *timeUnit* metadata key. For text intervals, the unit is Unicode code point."
    )
    targets: Optional[List[str]] = Field(
        None,
        description="IDs of a sequence of annotations covering the region of primary data referred to by this "
                    "annotation. Used as an alternative to *start* and *end* to point to component annotations (for "
                    "example a token sequence) rather than directly into primary data, or to link two or more "
                    "annotations (for example in a coreference annotation)."
    )
