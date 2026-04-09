from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class ImageDocument(Document):
    description: ClassVar[str] = "An image document."
    alsoKnownAs: ClassVar[list[str]] = []
