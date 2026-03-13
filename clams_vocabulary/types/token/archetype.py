from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.span.archetype import Span


class Token(Span):
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
