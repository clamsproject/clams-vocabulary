"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.interval.v4 import Interval_v4


class Span_v4(Interval_v4):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Span/v4"
    version: ClassVar[str] = "v4"
    shortname: ClassVar[str] = "Span"

    description: ClassVar[str] = (
        "An annotation over a region in primary text data. A Span may be defined by pointing directly into primary "
        "data (by using start and end offsets) or by linking to one or more other Annotations with the targets "
        "property."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Span/v4",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Region",
    ]
