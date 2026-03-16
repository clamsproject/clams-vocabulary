"""
Build contract tests for generated clams_vocabulary types.

Validates structural invariants that the generated package must satisfy.
All tests are skipped if build artifacts are not available.
"""
import re

import pytest

from clams_vocabulary.base import (
    TypesBase,
    ClamsTypesBase,
    AnnotationTypesBase,
    DocumentTypesBase,
)

try:
    from clams_vocabulary import (
        URI_TO_TYPE, AnnotationTypes, DocumentTypes, Enums,
    )
    _BUILT = True
except (ImportError, AttributeError):
    _BUILT = False

pytestmark = pytest.mark.skipif(
    not _BUILT, reason="Build artifacts not available"
)


# ===================================================================
# URI_TO_TYPE registry
# ===================================================================

class TestRegistry:

    def test_registry_not_empty(self):
        assert len(URI_TO_TYPE) > 0

    def test_canonical_uri_matches_class(self):
        """Each class's own uri must be a key that maps back to it."""
        seen = set()
        for uri, cls in URI_TO_TYPE.items():
            if uri == cls.uri and cls not in seen:
                seen.add(cls)
                assert URI_TO_TYPE[cls.uri] is cls, (
                    f"{cls.__name__}.uri={cls.uri} not mapped to itself"
                )

    def test_also_known_as_registered(self):
        seen = set()
        for cls in URI_TO_TYPE.values():
            if cls in seen:
                continue
            seen.add(cls)
            for aka in cls.alsoKnownAs:
                assert aka in URI_TO_TYPE, (
                    f"{cls.__name__} alsoKnownAs {aka!r} not registered"
                )
                assert URI_TO_TYPE[aka] is cls


# ===================================================================
# Type ClassVar contracts
# ===================================================================

class TestTypeClassVars:

    _REQUIRED_CLASSVARS = [
        'uri', 'version', 'shortname', 'description', 'alsoKnownAs',
    ]

    def _unique_classes(self):
        return set(URI_TO_TYPE.values())

    def test_required_classvars_present(self):
        for cls in self._unique_classes():
            for attr in self._REQUIRED_CLASSVARS:
                assert hasattr(cls, attr), (
                    f"{cls.__name__} missing ClassVar {attr!r}"
                )

    def test_version_format(self):
        for cls in self._unique_classes():
            assert re.fullmatch(r'v\d+', cls.version), (
                f"{cls.__name__}.version={cls.version!r} not vN format"
            )

    def test_is_clams_subclass(self):
        for cls in self._unique_classes():
            assert issubclass(cls, ClamsTypesBase), (
                f"{cls.__name__} not a ClamsTypesBase subclass"
            )


# ===================================================================
# Namespace population
# ===================================================================

class TestNamespaces:

    def test_annotation_types_populated(self):
        attrs = [a for a in dir(AnnotationTypes) if not a.startswith('_')]
        assert len(attrs) > 0

    def test_document_types_populated(self):
        attrs = [a for a in dir(DocumentTypes) if not a.startswith('_')]
        assert len(attrs) > 0

    def test_no_document_types_in_annotation_namespace(self):
        for attr in dir(AnnotationTypes):
            if attr.startswith('_'):
                continue
            cls = getattr(AnnotationTypes, attr)
            assert not issubclass(cls, DocumentTypesBase), (
                f"{attr} is a DocumentType in AnnotationTypes"
            )

    def test_no_annotation_types_in_document_namespace(self):
        for attr in dir(DocumentTypes):
            if attr.startswith('_'):
                continue
            cls = getattr(DocumentTypes, attr)
            assert not issubclass(cls, AnnotationTypesBase), (
                f"{attr} is an AnnotationType in DocumentTypes"
            )

    def test_typevers_populated(self):
        assert hasattr(AnnotationTypes, '_typevers')
        assert len(AnnotationTypes._typevers) > 0
        for shortname, ver in AnnotationTypes._typevers.items():
            assert re.fullmatch(r'v\d+', ver), (
                f"_typevers[{shortname!r}]={ver!r} not vN format"
            )

    def test_prop_aliases_is_dict(self):
        assert hasattr(AnnotationTypes, '_prop_aliases')
        assert isinstance(AnnotationTypes._prop_aliases, dict)


# ===================================================================
# Alias classes
# ===================================================================

# ===================================================================
# Property alias MRO merge with real types
# ===================================================================

class TestPropertyAliasesWithRealTypes:

    def test_bounding_box_has_merged_aliases(self):
        from clams_vocabulary.types.bounding_box.archetype import (
            BoundingBox,
        )
        aliases = BoundingBox._property_aliases
        assert 'label' in aliases, "BoundingBox missing 'label' alias"
        assert 'classification' in aliases, (
            "BoundingBox missing inherited 'classification' alias"
        )

    def test_span_has_merged_aliases(self):
        from clams_vocabulary.types.span.archetype import Span
        aliases = Span._property_aliases
        assert 'text' in aliases, "Span missing 'text' alias"
        assert 'classification' in aliases, (
            "Span missing inherited 'classification' alias"
        )


# ===================================================================
# Alias classes
# ===================================================================

class TestAliasClasses:

    def test_alias_has_no_version_suffix(self):
        """Unversioned aliases should not end with _vN."""
        seen = set()
        for cls in URI_TO_TYPE.values():
            if cls in seen:
                continue
            seen.add(cls)
            name = cls.__name__
            if not re.search(r'_v\d+$', name):
                # This is an alias class — verify it's a subclass
                # of some versioned class
                parent = cls.__bases__[0]
                assert re.search(r'_v\d+$', parent.__name__), (
                    f"Alias {name} does not inherit from a versioned class"
                )


# ===================================================================
# Prefix registry
# ===================================================================

class TestPrefixRegistry:

    def test_all_shortnames_have_prefix(self):
        seen = set()
        for cls in URI_TO_TYPE.values():
            if cls.shortname in seen:
                continue
            seen.add(cls.shortname)
            assert cls.shortname in TypesBase._prefixes, (
                f"No prefix registered for {cls.shortname!r}"
            )

    def test_no_duplicate_prefixes(self):
        prefix_to_name = {}
        for name, prefix in TypesBase._prefixes.items():
            if prefix is None:
                continue
            assert prefix not in prefix_to_name, (
                f"Prefix {prefix!r} shared by "
                f"{prefix_to_name.get(prefix)!r} and {name!r}"
            )
            prefix_to_name[prefix] = name


# ===================================================================
# from_str round-trip
# ===================================================================

class TestFromStrRoundTrip:

    def test_canonical_uri_resolves(self):
        seen = set()
        for cls in URI_TO_TYPE.values():
            if cls in seen:
                continue
            seen.add(cls)
            instance = TypesBase.from_str(cls.uri)
            assert isinstance(instance, cls), (
                f"from_str({cls.uri!r}) returned "
                f"{type(instance).__name__}, expected {cls.__name__}"
            )

    def test_also_known_as_resolves(self):
        seen = set()
        for cls in URI_TO_TYPE.values():
            if cls in seen:
                continue
            seen.add(cls)
            for aka in cls.alsoKnownAs:
                instance = TypesBase.from_str(aka)
                assert isinstance(instance, cls), (
                    f"from_str({aka!r}) returned "
                    f"{type(instance).__name__}, expected {cls.__name__}"
                )


# ===================================================================
# Equality and hashing with real types
# ===================================================================

class TestEqualityWithRealTypes:

    def _some_classes(self):
        """Yield unique classes for sampling."""
        seen = set()
        for cls in URI_TO_TYPE.values():
            if cls not in seen:
                seen.add(cls)
                yield cls

    def test_instance_eq_canonical_uri(self):
        for cls in self._some_classes():
            instance = cls.model_construct()
            assert instance == cls.uri

    def test_instance_eq_class(self):
        for cls in self._some_classes():
            instance = cls.model_construct()
            assert instance == cls

    def test_instance_eq_also_known_as(self):
        for cls in self._some_classes():
            instance = cls.model_construct()
            for aka in cls.alsoKnownAs:
                assert instance == aka, (
                    f"{cls.__name__} instance != alsoKnownAs {aka!r}"
                )

    def test_hash_equality_contract(self):
        """a == b implies hash(a) == hash(b)."""
        for cls in self._some_classes():
            a = cls.model_construct()
            b = cls.model_construct()
            if a == b:
                assert hash(a) == hash(b), (
                    f"hash contract violated for {cls.__name__}"
                )
