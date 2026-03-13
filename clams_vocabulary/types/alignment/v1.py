"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.thing.v1 import Thing_v1


class Alignment_v1(Thing_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Alignment/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Alignment"

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
        description="The type of sources of the alignment. When an alignment starts from more that two source types, "
                    "namely sources can be different types, one should not use this metadata."
    )
    targetType: Optional[str] = Field(
        None,
        description="The type of targets of the alignment. When an alignment goes to more that two target types, "
                    "namely targets can be different types, one should not use this metadata."
    )

    source: str = Field(..., description="The first of the aligned regions or documents.")
    target: str = Field(..., description="The second of the aligned regions or documents.")
