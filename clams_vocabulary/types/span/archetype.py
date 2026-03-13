from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.interval.archetype import Interval


class Span(Interval):
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
