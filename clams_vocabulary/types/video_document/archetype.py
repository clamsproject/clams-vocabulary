from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class VideoDocument(Document):
    description: ClassVar[str] = "A video document."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/VideoDocument/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/VideoDocument/",
        "http://mmif.clams.ai/0.4.1/vocabulary/VideoDocument/",
        "http://mmif.clams.ai/0.4.2/vocabulary/VideoDocument/",
    ]
