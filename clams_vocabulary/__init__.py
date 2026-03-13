"""
This file is auto-generated.
This file should never be manually modified, and must stay FROZEN.
"""
from .types.alignment import *
from .types.annotation import *
from .types.bounding_box import *
from .types.chapter import *
from .types.interval import *
from .types.polygon import *
from .types.region import *
from .types.relation import *
from .types.span import *
from .types.thing import *
from .types.time_frame import *
from .types.time_point import *
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

class Enums:
    """Namespace for all controlled vocabularies."""
    pass

for _cls in [Alignment_v1, Alignment, Annotation_v2, Annotation_v3, Annotation_v4, Annotation, BoundingBox_v1, BoundingBox_v2, BoundingBox_v3, BoundingBox, Chapter_v1, Chapter_v2, Chapter_v3, Chapter_v4, Chapter, Interval_v1, Interval_v2, Interval_v3, Interval, Polygon_v1, Polygon_v2, Polygon_v3, Polygon, Region_v1, Region_v2, Region_v3, Region, Relation_v1, Relation_v2, Relation_v3, Relation, Span_v1, Span_v2, Span_v3, Span, Thing_v1, Thing, TimeFrame_v1, TimeFrame_v2, TimeFrame_v3, TimeFrame_v4, TimeFrame, TimePoint_v1, TimePoint_v2, TimePoint_v3, TimePoint, VideoObject_v1, VideoObject_v2, VideoObject_v3, VideoObject]:
    setattr(AnnotationTypes, _cls.__name__, _cls)

for _cls in [AudioDocument_v1, AudioDocument, Document_v1, Document, ImageDocument_v1, ImageDocument, TextDocument_v1, TextDocument, VideoDocument_v1, VideoDocument]:
    setattr(DocumentTypes, _cls.__name__, _cls)

# Aggregate property aliases from type classes
AnnotationTypes._prop_aliases = {}
for _attr in dir(AnnotationTypes):
    if not _attr.startswith("_"):
        _cls = getattr(AnnotationTypes, _attr)
        if hasattr(_cls, "_property_aliases"):
            AnnotationTypes._prop_aliases[_cls.__name__] = _cls._property_aliases

AnnotationTypes._typevers = {_t.shortname: _t.version for _t in [Alignment, Annotation, BoundingBox, Chapter, Interval, Polygon, Region, Relation, Span, Thing, TimeFrame, TimePoint, VideoObject]}

DocumentTypes._typevers = {_t.shortname: _t.version for _t in [AudioDocument, Document, ImageDocument, TextDocument, VideoDocument]}

URI_TO_TYPE = {}
for _type in [Alignment_v1, Alignment, Annotation_v2, Annotation_v3, Annotation_v4, Annotation, BoundingBox_v1, BoundingBox_v2, BoundingBox_v3, BoundingBox, Chapter_v1, Chapter_v2, Chapter_v3, Chapter_v4, Chapter, Interval_v1, Interval_v2, Interval_v3, Interval, Polygon_v1, Polygon_v2, Polygon_v3, Polygon, Region_v1, Region_v2, Region_v3, Region, Relation_v1, Relation_v2, Relation_v3, Relation, Span_v1, Span_v2, Span_v3, Span, Thing_v1, Thing, TimeFrame_v1, TimeFrame_v2, TimeFrame_v3, TimeFrame_v4, TimeFrame, TimePoint_v1, TimePoint_v2, TimePoint_v3, TimePoint, VideoObject_v1, VideoObject_v2, VideoObject_v3, VideoObject, AudioDocument_v1, AudioDocument, Document_v1, Document, ImageDocument_v1, ImageDocument, TextDocument_v1, TextDocument, VideoDocument_v1, VideoDocument]:
    URI_TO_TYPE[_type.uri] = _type
    for aka in _type.alsoKnownAs:
        URI_TO_TYPE[aka] = _type

# Register prefixes
from .base import TypesBase
for _type in URI_TO_TYPE.values():
    if _type.shortname not in TypesBase._prefixes:
        _prefix = TypesBase._create_prefix(_type.shortname, TypesBase._prefixes.values())
        TypesBase._prefixes[_type.shortname] = _prefix
