"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, List, Optional
from pydantic import Field
from clams_vocabulary.types.thing.v1 import Thing_v1
from clams_vocabulary.base import DocumentTypesBase


class Document_v2(Thing_v1, DocumentTypesBase):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Document/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "Document"

    description: ClassVar[str] = (
        "A document of some media type. Annotations directly or "
        "indirectly anchor to documents. In CLAMS, a document "
        "typically refers to an external file via the "
        "<code>location</code> property, but for text documents "
        "the actual content can be in-line in the document type."
    )
    alsoKnownAs: ClassVar[list[str]] = []

    location: Optional[str] = Field(
        None, description="The location of an external file."
    )
    mime: Optional[str] = Field(
        None,
        description=(
            "The MIME type of the document, only used when the "
            "<code>location</code> property is used."
        ),
    )
    origins: Optional[List[str]] = Field(
        None,
        description=(
            "IDs of annotations or documents that this document "
            "was derived or inferred from. For example, a "
            "<code>TextDocument</code> produced by a transcription "
            "app points back to its source "
            "<code>AudioDocument</code> via this property. Supports "
            "multi-source derivation (e.g., OCR over consecutive "
            "video frames producing a single consensus document). "
            "When this property is set, an accompanying "
            "<code>origination</code> should also be provided to "
            "describe the nature of the derivation."
        ),
    )
    origination: Optional[str] = Field(
        None,
        description=(
            "Describes the nature of the derivation relationship "
            "between this document and its <code>origins</code>. "
            "Example values include <code>derived</code>, "
            "<code>transcription</code>, "
            "<code>topologically-identical</code>."
        ),
    )
