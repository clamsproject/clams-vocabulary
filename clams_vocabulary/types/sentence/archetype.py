from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.archetype import Span


class Sentence(Span):
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
