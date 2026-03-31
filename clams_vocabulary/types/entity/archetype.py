from typing import ClassVar

from clams_vocabulary.types.primary.archetype import Primary


class Entity(Primary):
    alsoKnownAs: ClassVar[list[str]] = []
    description: ClassVar[str] = (
        "A real-world entity referenced by annotations. An entity "
        "may be grounded to an external knowledge base via "
        "<code>location</code> (e.g., a Wikidata QID, a PBCore "
        "record, a LoC name authority entry), or may remain "
        "underspecified when grounding is pending or unavailable. "
        "<br><br>"
        "Entities are linked to their evidencing annotations via "
        "<code>origins</code>. For example, a KIE app extracting "
        "structured records from a chyron produces an Entity whose "
        "<code>origins</code> point to the constituent "
        "<code>NamedEntity</code> spans."
    )
