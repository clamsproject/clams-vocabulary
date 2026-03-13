"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.v5 import Span_v5


class Paragraph_v1(Span_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Paragraph/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Paragraph"

    description: ClassVar[str] = (
        "A division of a piece of writing, usually dealing with a single theme and indicated by a new line, "
        "indentation, and/or numbering."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Paragraph/v1",
        "http://vocab.lappsgrid.org/Paragraph",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Paragraph",
    ]
