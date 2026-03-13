"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.span.v5 import Span_v5


class Token_v1(Span_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Token/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Token"

    description: ClassVar[str] = (
        "A string of one or more characters that serves as an indivisible unit for the purposes of morpho-syntactic "
        "labeling (part of speech tagging)."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Token/v1",
        "http://vocab.lappsgrid.org/Token",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/Token",
    ]

    pos: Optional[str] = Field(None, description="Part-of-speech tag associated with the token.")
    lemma: Optional[str] = Field(
        None,
        description="The root (base) form associated with the token. URI may point to a lexicon entry."
    )
    orth: Optional[str] = Field(
        None,
        description="Orthographic properties of the token such as LowerCase, UpperCase, UpperInitial, etc. Ideally a "
                    "URI referencing a pre-defined descriptor."
    )
