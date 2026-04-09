"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.v2 import Document_v2


class AudioDocument_v2(Document_v2):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/AudioDocument/v2"
    version: ClassVar[str] = "v2"
    shortname: ClassVar[str] = "AudioDocument"

    description: ClassVar[str] = "An audio document."
    alsoKnownAs: ClassVar[list[str]] = []
