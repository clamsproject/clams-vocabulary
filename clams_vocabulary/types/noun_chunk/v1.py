"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.v5 import Span_v5


class NounChunk_v1(Span_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/NounChunk/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "NounChunk"

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
