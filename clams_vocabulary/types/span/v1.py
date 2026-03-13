"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.interval.v1 import Interval_v1


class Span_v1(Interval_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Span/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Span"

    description: ClassVar[str] = (
        "An annotation over a region in primary text data. A Span may be defined by pointing directly into primary "
        "data (by using start and end offsets) or by linking to one or more other Annotations with the targets "
        "property."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Span/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/Span/",
        "http://mmif.clams.ai/0.4.1/vocabulary/Span/",
        "http://mmif.clams.ai/0.4.2/vocabulary/Span/",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Region",
    ]
