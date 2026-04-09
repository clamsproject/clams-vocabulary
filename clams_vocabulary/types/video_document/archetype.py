from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class VideoDocument(Document):
    description: ClassVar[str] = "A video document."
    alsoKnownAs: ClassVar[list[str]] = []
