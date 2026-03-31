from typing import ClassVar, List, Optional

from pydantic import Field

from clams_vocabulary.types.thing.archetype import Thing
from clams_vocabulary.base import PrimaryTypesBase


class Primary(Thing, PrimaryTypesBase):
    alsoKnownAs: ClassVar[list[str]] = []
    description: ClassVar[str] = (
        "Abstract intermediate type for primary objects that exist "
        "independently of annotations. Primary types reference "
        "something outside the MMIF (external files, knowledge base "
        "entries) and carry derivation links back to the annotations "
        "they were derived or inferred from."
    )

    location: Optional[str] = Field(
        None,
        description=(
            "The location of the source material. For documents, "
            "this is typically a file path or URI to the media file. "
            "For entities, this is a URI to a knowledge base entry "
            "(e.g., a Wikidata QID)."
        ),
    )
    origins: Optional[List[str]] = Field(
        None,
        description=(
            "Annotation IDs from which this object was derived or "
            "inferred. Unlike <code>targets</code> on Annotation "
            "types, <code>origins</code> carries no part-whole "
            "semantics and no ordering guarantees."
        ),
    )
    provenance: Optional[str] = Field(
        None,
        description=(
            "The kind of derivation that produced this object from "
            "its <code>origins</code> (e.g., "
            "<code>transcription</code>, <code>extraction</code>)."
        ),
    )
