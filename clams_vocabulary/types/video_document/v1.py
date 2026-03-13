"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.v1 import Document_v1


class VideoDocument_v1(Document_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/VideoDocument/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "VideoDocument"

    description: ClassVar[str] = "A video document."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/VideoDocument/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/VideoDocument/",
        "http://mmif.clams.ai/0.4.1/vocabulary/VideoDocument/",
        "http://mmif.clams.ai/0.4.2/vocabulary/VideoDocument/",
    ]
