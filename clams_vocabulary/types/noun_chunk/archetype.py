from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.archetype import Span


class NounChunk(Span):
    description: ClassVar[str] = (
        "The initial portion of a non-recursive noun phrase up to the head, including determiners but not including "
        "postmodifying prepositional phrases or clauses."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/NounChunk/v1",
        "http://vocab.lappsgrid.org/NounChunk",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/NounChunk",
    ]
