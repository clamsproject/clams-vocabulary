"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.interval.v5 import Interval_v5


class Span_v5(Interval_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Span/v5"
    version: ClassVar[str] = "v5"
    shortname: ClassVar[str] = "Span"

    _property_aliases: ClassVar[dict] = {
        'text': {'text', 'word'},
    }

    description: ClassVar[str] = (
        "An annotation over a region in primary text data. A Span may be defined by pointing directly into primary "
        "data (by using start and end offsets) or by linking to one or more other Annotations with the targets "
        "property."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Span/v5",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Region",
    ]

    text: Optional[str] = Field(None, description="The surface string in the primary data covered by this span.")
