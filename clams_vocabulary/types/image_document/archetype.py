from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class ImageDocument(Document):
    description: ClassVar[str] = "An image document."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/ImageDocument/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/ImageDocument/",
        "http://mmif.clams.ai/0.4.1/vocabulary/ImageDocument/",
        "http://mmif.clams.ai/0.4.2/vocabulary/ImageDocument/",
    ]
