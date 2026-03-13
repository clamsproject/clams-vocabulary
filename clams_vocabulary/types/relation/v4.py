"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar
from pydantic import Field
from clams_vocabulary.types.annotation.v5 import Annotation_v5


class Relation_v4(Annotation_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Relation/v4"
    version: ClassVar[str] = "v4"
    shortname: ClassVar[str] = "Relation"

    description: ClassVar[str] = (
        "Any relationship between two or more annotation types. For texts could be a grammatical relation such as "
        "subject-object, a semantic relation between meanings or roles, or a temporal relation indicating the "
        "simultaneity or ordering in time of events or states. For image regions and video objects this could involve "
        "spatial relations or part-whole relations."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Relation/v4",
    ]
