"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.span.v5 import Span_v5


class VerbChunk_v1(Span_v5):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/VerbChunk/v1"
    version: ClassVar[str] = "v1"
    shortname: ClassVar[str] = "VerbChunk"

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
