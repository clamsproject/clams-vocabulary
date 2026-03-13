from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.span.archetype import Span


class VerbChunk(Span):
    description: ClassVar[str] = (
        "Non-recursive verb groups, which include modals, auxiliary verbs, and medial adverbs, and end at the head "
        "verb or predicate adjective."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/VerbChunk/v1",
        "http://vocab.lappsgrid.org/VerbChunk",
    ]
    similarTo: ClassVar[list[str]] = [
        "http://vocab.lappsgrid.org/VerbChunk",
    ]

    tense: Optional[str] = Field(
        None,
        description="Provides tense information for the verb. Example values include BeVBG, BeVBN, FutCon, HaveVBN, "
                    "Pas, PasCon, PasPer, PasPerCon, Per, Pre, PreCon, PrePer, PrePerCon, SimFut, SimPas, SimPre, "
                    "none"
    )
    voice: Optional[str] = Field(
        None,
        description="Indicates if the verb group is active or passive. Possible values include ACTIVE, PASSIVE, or NONE"
    )
    neg: Optional[str] = Field(
        None,
        description="Indicates whether or not the verb is negated. Values include YES, NO."
    )
