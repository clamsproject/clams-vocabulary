from typing import Any, ClassVar, Dict, Optional
from pydantic import Field
from clams_vocabulary.types.document.archetype import Document


class TextDocument(Document):
    description: ClassVar[str] = "A text document."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/TextDocument/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/TextDocument/",
        "http://mmif.clams.ai/0.4.1/vocabulary/TextDocument/",
        "http://mmif.clams.ai/0.4.2/vocabulary/TextDocument/",
    ]

    text: Optional[Dict[str, Any]] = Field(
        None,
        description="A JSON-LD value object which has a *@value* and a *@language* property."
    )
