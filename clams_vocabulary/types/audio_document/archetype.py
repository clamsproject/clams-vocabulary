from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class AudioDocument(Document):
    description: ClassVar[str] = "An audio document."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/AudioDocument/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/AudioDocument/",
        "http://mmif.clams.ai/0.4.1/vocabulary/AudioDocument/",
        "http://mmif.clams.ai/0.4.2/vocabulary/AudioDocument/",
    ]
