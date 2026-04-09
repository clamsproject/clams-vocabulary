"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import Any, ClassVar, Dict, Optional
from pydantic import Field
from clams_vocabulary.types.document.v2 import Document_v2


class TextDocument_v2(Document_v2):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/TextDocument/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "TextDocument"

    description: ClassVar[str] = "A text document."
    alsoKnownAs: ClassVar[list[str]] = []

    text: Optional[Dict[str, Any]] = Field(
        None,
        description="A JSON-LD value object which has a *@value* and a *@language* property."
    )
