from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.primary.archetype import Primary
from clams_vocabulary.base import DocumentTypesBase


class Document(Primary, DocumentTypesBase):
    alsoKnownAs: ClassVar[list[str]] = []
    description: ClassVar[str] = (
        "A document of some media type. Annotations directly or "
        "indirectly anchor to documents. In CLAMS, a document "
        "typically refers to an external file via the "
        "<code>location</code> property, but for text documents "
        "the actual content can be in-line in the document type."
    )

    mime: Optional[str] = Field(
        None,
        description=(
            "The MIME type of the document, only used when the "
            "<code>location</code> property is used."
        ),
    )
