"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.thing.v1 import Thing_v1
from clams_vocabulary.base import DocumentTypesBase


class Document_v1(Thing_v1, DocumentTypesBase):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Document/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "Document"

    description: ClassVar[str] = (
        "A document of some media type. Annotations directly or indirectly anchor to documents. In CLAMS, a document "
        "typically refers to an external file fia the *location* property, but for text documents the actual content "
        "can be in-line in the document type."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Document/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/Document/",
        "http://mmif.clams.ai/0.4.1/vocabulary/Document/",
        "http://mmif.clams.ai/0.4.2/vocabulary/Document/",
    ]

    location: Optional[str] = Field(None, description="The location of an external file.")
    mime: Optional[str] = Field(
        None,
        description="The MIME type of the document, only used when the *location* property is used."
    )
