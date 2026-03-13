"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from typing import ClassVar, Dict, List, Optional
from pydantic import Field
from clams_vocabulary.types.thing.v1 import Thing_v1
from clams_vocabulary.base import AnnotationTypesBase


class Annotation_v6(Thing_v1, AnnotationTypesBase):
    uri: ClassVar[str] = "http://clams.ai/vocabulary/type/Annotation/v6"
    version: ClassVar[str] = "v6"
    shortname: ClassVar[str] = "Annotation"

    _property_aliases: ClassVar[dict] = {
        'classification': {'classification', 'classifications'},
    }

    description: ClassVar[str] = (
        "Any kind of information added to a document. If an annotation is specific to a region over the primary data "
        "or a relation over such regions, specific sub-types should be used instead of this high-level type."
    )
    alsoKnownAs: ClassVar[list[str]] = [
        "http://mmif.clams.ai/vocabulary/Annotation/v6",
    ]

    document: Optional[str] = Field(
        None,
        description="The identifier of the document that the annotation is over. This has to be defined either at "
                    "the metadata level, in which case it has scope over all annotations of the same type in a view, "
                    "or at the instance level, in which it has scope over just the single annotation."
    )
    labelset: Optional[List[str]] = Field(
        None,
        description="When an annotation object contains results of a classification task, this metadata is used to "
                    "specify the label values used in classification. Individual annotations then must have "
                    "<code>label</code> property that is one of the values in this list. <br><br> [note] Annotations "
                    "from a classifier app must have this metadata or <code> labelsetUri </code> metadata. "
                    "[/note]<br><br> [note] Not all of labels specified in the <code>labelset</code> must occur in "
                    "the output annotations. For example, a <code>labelset</code> can contain a <i>catch-all</i> "
                    "negative label, but if the negative label can be not interesting enough to keep in the output "
                    "annotation. [/note]"
    )
    labelsetUri: Optional[str] = Field(
        None,
        description="A URI to an externally defined labelset. Since the <code>labelset</code> metadata is a list of "
                    "simple strings, this URI can be used to point to a more detailed definition of the labelset. "
                    "This can be a JSON-LD document or a SKOS concept scheme, for example. <br><br> [note] "
                    "Annotations from a classifier app must have this metadata or <code> labelset </code> metadata. "
                    "[/note]"
    )

    document: Optional[str] = Field(None, description="The identifier of the document that the annotation is over.")
    label: Optional[str] = Field(
        None,
        description="A label given to this object by classification. The value must be a simple string value of the "
                    "label and must be one of the values defined in the <code>labelset</code> or "
                    "<code>labelsetUri</code> annotation metadata. <br><br> For example, for the "
                    "<code>Sentence</code> subtype, this could be used to indicate the type of sentence, such as "
                    "\"declarative\", \"interrogative\", \"exclamatory\", etc. For <code>NamedEntity</code> subtype, this "
                    "could be used to indicate the type of named entity, such as \"PER\", \"ORG\", \"LOC\", \"MISC\" "
                    "(following the CoNLL-2003 labels). <br><br> For non-linguistic annotations, for example for "
                    "<code>TimeFrame</code>, this could be used to indicate the type of the time frame, such as "
                    "\"speech\", \"music\", \"noise\", \"bars-and-tones\", etc, for acoustic classification. Or \"slate\", "
                    "\"lower-third\", \"credits\" for visual classification of video frames. <br><br> [note] Annotations "
                    "from a type of classifier model must have this property. [/note]"
    )
    classifications: Optional[Dict[str, float]] = Field(
        None,
        description="Alias for the <code>classification</code> metadata. Here for historical reasons."
    )
    classification: Optional[Dict[str, float]] = Field(
        None,
        description="A map from label values to their \"score\" numbers provided by a classifier. The score can be "
                    "probability, similarity, confidence, or any other real number that was used to determine the "
                    "label value. <br><br> <i>Optional</i> on top of the <code>label</code> property. However when "
                    "this property is used, the <code>label</code> property must be one of the keys and the keys must "
                    "match to the values defined in the <code>labelset</code> or <code>labelsetUri</code> annotation "
                    "metadata."
    )
