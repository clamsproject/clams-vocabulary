from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.thing.archetype import Thing
from clams_vocabulary.base import AnnotationTypesBase


class Annotation(Thing, AnnotationTypesBase):
    description: ClassVar[str] = (
        "Any kind of information added to a document. If an annotation is specific to a region over the primary data "
        "or a relation over such regions, specific sub-types should be used instead of this high-level type."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Annotation/v2",
        "http://mmif.clams.ai/0.4.2/vocabulary/Annotation/",
    ]

    document: Optional[str] = Field(
        None,
        description="The identifier of the document that the annotation is over. This has to be defined either at "
                    "the metadata level, in which case it has scope over all annotations of the same type in a view, "
                    "or at the instance level, in which it has scope over just the single annotation."
    )

    document: Optional[str] = Field(None, description="The identifier of the document that the annotation is over.")
