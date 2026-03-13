"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.v5 import Span_v5


class Sentence_v1(Span_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Sentence/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Sentence"

    description: ClassVar[str] = (
        "A sequence of words capable of standing alone to make an assertion, ask a question, or give a command, "
        "usually consisting of a subject and a predicate containing a finite verb."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Sentence/v1",
        "http://vocab.lappsgrid.org/Sentence",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Sentence",
    ]
