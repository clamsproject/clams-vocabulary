"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import Any, ClassVar, Dict, Optional
from pydantic import Field
from clams_vocabulary.types.document.v1 import Document_v1


class TextDocument_v1(Document_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TextDocument/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "TextDocument"

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
