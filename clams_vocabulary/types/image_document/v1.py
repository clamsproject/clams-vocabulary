"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.document.v1 import Document_v1


class ImageDocument_v1(Document_v1):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/ImageDocument/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "ImageDocument"

    description: ClassVar[str] = "An image document."
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/ImageDocument/v1",
        "http://mmif.clams.ai/0.4.0/vocabulary/ImageDocument/",
        "http://mmif.clams.ai/0.4.1/vocabulary/ImageDocument/",
        "http://mmif.clams.ai/0.4.2/vocabulary/ImageDocument/",
    ]
