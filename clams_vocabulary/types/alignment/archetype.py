from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.thing.archetype import Thing


class Alignment(Thing):
    description: ClassVar[str] = (
        "An alignment between two regions, two documents or a region and a document. Typically one of the regions or "
        "documents is a text span or text document and the other an image or audio segment or document. While there is "
        "no enforced directionality we tend to consider the text region or document as the target of the alignment."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Alignment/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/Alignment/",
        "http://mmif.clams.ai/0.4.1/vocabulary/Alignment/",
        "http://mmif.clams.ai/0.4.2/vocabulary/Alignment/",
    ]

    sourceType: Optional[str] = Field(
        None,
        description="The type of the source of the alignment."
    )
    targetType: Optional[str] = Field(
        None,
        description="The type of the target of the alignment."
    )

    source: str = Field(..., description="The first of the aligned regions or documents.")
    target: str = Field(..., description="The second of the aligned regions or documents.")
