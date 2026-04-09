"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from importlib.metadata import version
__version__ = version("clams-vocabulary")

from .types.thing import *
from .types.alignment import *
from .types.annotation import *
from .types.bounding_box import *
from .types.chapter import *
from .types.interval import *
from .types.named_entity import *
from .types.noun_chunk import *
from .types.paragraph import *
from .types.polygon import *
from .types.region import *
from .types.relation import *
from .types.sentence import *
from .types.span import *
from .types.time_frame import *
from .types.time_point import *
from .types.token import *
from .types.verb_chunk import *
from .types.video_object import *
from .types.audio_document import *
from .types.document import *
from .types.image_document import *
from .types.text_document import *
from .types.video_document import *


class AnnotationTypes:
    """Namespace for all annotation types."""
    pass

class DocumentTypes:
    """Namespace for all document types."""
    pass

class ThingType:
    """Namespace for the top-level Thing type. (for backwards compatibility)"""
    pass

class Enums:
    """Namespace for all controlled vocabularies."""
    pass

for _cls in [Thing_v1, Thing]:
    setattr(ThingType, _cls.__name__, _cls)

for _cls in [Alignment_v1, Alignment, Annotation_v2, Annotation_v3, Annotation_v4, Annotation_v5, Annotation_v6, Annotation, BoundingBox_v1, BoundingBox_v2, BoundingBox_v3, BoundingBox_v4, BoundingBox_v5, BoundingBox, Chapter_v1, Chapter_v2, Chapter_v3, Chapter_v4, Chapter_v5, Chapter_v6, Chapter, Interval_v1, Interval_v2, Interval_v3, Interval_v4, Interval_v5, Interval, NamedEntity_v1, NamedEntity, NounChunk_v1, NounChunk, Paragraph_v1, Paragraph, Polygon_v1, Polygon_v2, Polygon_v3, Polygon_v4, Polygon_v5, Polygon, Region_v1, Region_v2, Region_v3, Region_v4, Region_v5, Region, Relation_v1, Relation_v2, Relation_v3, Relation_v4, Relation_v5, Relation, Sentence_v1, Sentence, Span_v1, Span_v2, Span_v3, Span_v4, Span_v5, Span, TimeFrame_v1, TimeFrame_v2, TimeFrame_v3, TimeFrame_v4, TimeFrame_v5, TimeFrame_v6, TimeFrame, TimePoint_v1, TimePoint_v2, TimePoint_v3, TimePoint_v4, TimePoint_v5, TimePoint, Token_v1, Token, VerbChunk_v1, VerbChunk, VideoObject_v1, VideoObject_v2, VideoObject_v3, VideoObject_v4, VideoObject_v5, VideoObject]:
    setattr(AnnotationTypes, _cls.__name__, _cls)

for _cls in [AudioDocument_v1, AudioDocument_v2, AudioDocument, Document_v1, Document_v2, Document, ImageDocument_v1, ImageDocument_v2, ImageDocument, TextDocument_v1, TextDocument_v2, TextDocument, VideoDocument_v1, VideoDocument_v2, VideoDocument]:
    setattr(DocumentTypes, _cls.__name__, _cls)

# Aggregate property aliases from type classes
AnnotationTypes._prop_aliases = {}
for _attr in dir(AnnotationTypes):
    if not _attr.startswith("_"):
        _cls = getattr(AnnotationTypes, _attr)
        if hasattr(_cls, "_property_aliases"):
            AnnotationTypes._prop_aliases[_cls.__name__] = _cls._property_aliases

ThingType._typevers = {_t.shortname: _t.version for _t in [Thing]}

AnnotationTypes._typevers = {_t.shortname: _t.version for _t in [Alignment, Annotation, BoundingBox, Chapter, Interval, NamedEntity, NounChunk, Paragraph, Polygon, Region, Relation, Sentence, Span, TimeFrame, TimePoint, Token, VerbChunk, VideoObject]}

DocumentTypes._typevers = {_t.shortname: _t.version for _t in [AudioDocument, Document, ImageDocument, TextDocument, VideoDocument]}

URI_TO_TYPE = {}
for _type in [Thing_v1, Thing, Alignment_v1, Alignment, Annotation_v2, Annotation_v3, Annotation_v4, Annotation_v5, Annotation_v6, Annotation, BoundingBox_v1, BoundingBox_v2, BoundingBox_v3, BoundingBox_v4, BoundingBox_v5, BoundingBox, Chapter_v1, Chapter_v2, Chapter_v3, Chapter_v4, Chapter_v5, Chapter_v6, Chapter, Interval_v1, Interval_v2, Interval_v3, Interval_v4, Interval_v5, Interval, NamedEntity_v1, NamedEntity, NounChunk_v1, NounChunk, Paragraph_v1, Paragraph, Polygon_v1, Polygon_v2, Polygon_v3, Polygon_v4, Polygon_v5, Polygon, Region_v1, Region_v2, Region_v3, Region_v4, Region_v5, Region, Relation_v1, Relation_v2, Relation_v3, Relation_v4, Relation_v5, Relation, Sentence_v1, Sentence, Span_v1, Span_v2, Span_v3, Span_v4, Span_v5, Span, TimeFrame_v1, TimeFrame_v2, TimeFrame_v3, TimeFrame_v4, TimeFrame_v5, TimeFrame_v6, TimeFrame, TimePoint_v1, TimePoint_v2, TimePoint_v3, TimePoint_v4, TimePoint_v5, TimePoint, Token_v1, Token, VerbChunk_v1, VerbChunk, VideoObject_v1, VideoObject_v2, VideoObject_v3, VideoObject_v4, VideoObject_v5, VideoObject, AudioDocument_v1, AudioDocument_v2, AudioDocument, Document_v1, Document_v2, Document, ImageDocument_v1, ImageDocument_v2, ImageDocument, TextDocument_v1, TextDocument_v2, TextDocument, VideoDocument_v1, VideoDocument_v2, VideoDocument]:
    URI_TO_TYPE[_type.uri] = _type
    for aka in _type.alsoKnownAs:
        URI_TO_TYPE[aka] = _type

# Register prefixes
from .base import TypesBase
for _type in URI_TO_TYPE.values():
    if _type.shortname not in TypesBase._prefixes:
        _prefix = TypesBase._create_prefix(_type.shortname, TypesBase._prefixes.values())
        TypesBase._prefixes[_type.shortname] = _prefix
