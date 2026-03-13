from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.thing.archetype import Thing
from clams_vocabulary.base import DocumentTypesBase


class Document(Thing, DocumentTypesBase):
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
