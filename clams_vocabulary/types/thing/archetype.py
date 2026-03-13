from typing import ClassVar
from pydantic import Field
from clams_vocabulary.base import ClamsTypesBase


class Thing(ClamsTypesBase):
    description: ClassVar[str] = "Abstract top type."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Thing/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/Thing/",
        "http://mmif.clams.ai/0.4.1/vocabulary/Thing/",
        "http://mmif.clams.ai/0.4.2/vocabulary/Thing/",
    ]

    id: str = Field(
        ...,
        description="A unique identifier for the annotation or document. Uniqueness is relative to the view the "
                    "annotation is in or the list of documents at the top level of a MMIF file."
    )
