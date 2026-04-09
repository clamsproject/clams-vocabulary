from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class AudioDocument(Document):
    description: ClassVar[str] = "An audio document."
    alsoKnownAs: ClassVar[list[str]] = []
