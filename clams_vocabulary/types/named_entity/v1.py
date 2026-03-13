"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.span.v5 import Span_v5


class NamedEntity_v1(Span_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/NamedEntity/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "NamedEntity"

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
