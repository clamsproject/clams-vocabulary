from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.archetype import Span


class Paragraph(Span):
    description: ClassVar[str] = (
        "A division of a piece of writing, usually dealing with a single theme and indicated by a new line, "
        "indentation, and/or numbering."
    )
    alsoKnownAs: ClassVar[list[str]] = []
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Paragraph",
    ]
