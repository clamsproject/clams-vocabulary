from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.archetype import Span


class NamedEntity(Span):
    description: ClassVar[str] = (
        "A phrase that clearly identifies an individual from others that have similar attributes, such as the name of "
        "a person, organization, location, artifact, etc. as well as temporal expressions."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/NamedEntity/v1",
        "http://vocab.lappsgrid.org/NamedEntity",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/NamedEntity",
    ]
