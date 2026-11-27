from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.interval.archetype import Interval


class Span(Interval):
    _property_aliases: ClassVar[dict] = {
        'text': {'text', 'word'},
    }

    description: ClassVar[str] = (
        "An annotation over a region in primary text data. A Span may be defined by pointing directly into primary "
        "data (by using start and end offsets) or by linking to one or more other Annotations with the targets "
        "property."
    )
    alsoKnownAs: ClassVar[list[str]] = []
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Region",
    ]

    text: Optional[str] = Field(None, description="The surface string in the primary data covered by this span.")
