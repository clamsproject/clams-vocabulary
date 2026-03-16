"""
Unit tests for clams_vocabulary.base module.

Tests the hand-written runtime logic: URI parsing, prefix generation,
equality/hashing contracts, and static utility methods.

Only tests TypesBase (the generic base). ClamsTypesBase and its
subclasses depend on generated type modules and are covered by
package contract tests that run after build.
"""
from typing import ClassVar, Optional

import pytest
from pydantic import Field, ValidationError

from clams_vocabulary.base import (
    TypesBase,
    ClamsTypesBaseMeta,
    ClamsTypesBase,
    AnnotationTypesBase,
    DocumentTypesBase,
    ThingTypesBase,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def generic_instance():
    """A generic (non-CLAMS) TypesBase instance."""
    return TypesBase('http://example.org/MyType')


# ===================================================================
# TypesBase.__init__ — URI parsing
# ===================================================================

class TestTypesBaseInit:

    def test_full_uri_splits(self):
        t = TypesBase('http://example.org/MyType')
        assert t.base_uri == 'http://example.org'
        assert t.shortname == 'MyType'

    def test_bare_shortname(self):
        t = TypesBase('SomeType')
        assert t.base_uri == ''
        assert t.shortname == 'SomeType'

    def test_initialized_from_stored(self):
        uri = 'http://example.org/MyType'
        t = TypesBase(uri)
        assert t.initialized_from == uri

    def test_invalid_base_uri_rejected(self):
        with pytest.raises((ValidationError, ValueError)):
            TypesBase('not-a-url/MyType')


# ===================================================================
# TypesBase._create_prefix
# ===================================================================

class TestCreatePrefix:

    def test_camelcase(self):
        assert TypesBase._create_prefix('TimeFrame', []) == 'tf'

    def test_double_capital(self):
        assert TypesBase._create_prefix('BoundingBox', []) == 'bb'

    def test_single_word(self):
        assert TypesBase._create_prefix('Span', []) == 's'

    def test_collision_produces_different_prefix(self):
        first = TypesBase._create_prefix('TimeFrame', [])
        second = TypesBase._create_prefix('TimeFlow', [first])
        assert second != first
        assert second.startswith('t')

    def test_non_alphanumeric_returns_none(self):
        assert TypesBase._create_prefix('Type-Name', []) is None

    def test_empty_string(self):
        result = TypesBase._create_prefix('', [])
        assert result is None or result == ''


# ===================================================================
# TypesBase.from_str (generic path only)
# ===================================================================

class TestFromStr:
    """Only tests the generic fallback path.

    Registry-dependent resolution (URI_TO_TYPE lookups) belongs in
    package contract tests that require build artifacts.
    """

    def test_unknown_uri_returns_generic(self):
        instance = TypesBase.from_str('http://unknown.org/Foo')
        assert type(instance) is TypesBase
        assert instance.shortname == 'Foo'

    def test_bare_shortname_returns_generic(self):
        instance = TypesBase.from_str('BareName')
        assert type(instance) is TypesBase
        assert instance.shortname == 'BareName'
        assert instance.base_uri == ''


# ===================================================================
# TypesBase dunder methods
# ===================================================================

class TestTypesBaseDunders:

    def test_repr_prefers_initialized_from(self, generic_instance):
        assert repr(generic_instance) == 'http://example.org/MyType'

    def test_str_equals_repr(self, generic_instance):
        assert str(generic_instance) == repr(generic_instance)

    def test_hash_based_on_uri(self, generic_instance):
        assert hash(generic_instance) == hash(generic_instance.uri)

    def test_eq_with_same_uri(self):
        a = TypesBase('http://example.org/X')
        b = TypesBase('http://example.org/X')
        assert a == b

    def test_eq_with_string(self):
        a = TypesBase('http://example.org/X')
        assert a == 'http://example.org/X'

    def test_neq_different_uri(self):
        a = TypesBase('http://example.org/X')
        b = TypesBase('http://example.org/Y')
        assert a != b

    def test_uri_property(self, generic_instance):
        assert generic_instance.uri == 'http://example.org/MyType'

    def test_uri_bare_shortname(self):
        t = TypesBase('Bare')
        assert t.uri == 'Bare'


# ===================================================================
# ClamsTypesBaseMeta — static methods
# ===================================================================

class TestClamsTypesBaseMeta:

    def test_is_versioned_true(self):
        assert ClamsTypesBaseMeta._is_versioned('Foo_v1') is True
        assert ClamsTypesBaseMeta._is_versioned('Foo_v99') is True

    def test_is_versioned_false(self):
        assert ClamsTypesBaseMeta._is_versioned('Foo') is False
        assert ClamsTypesBaseMeta._is_versioned('Foo_bar') is False

    def test_compare_types_same_version(self):
        assert ClamsTypesBaseMeta._compare_types(
            'X', 'v1', 'X', 'v1', fuzzy=False
        ) is True

    def test_compare_types_strict_mismatch(self):
        assert ClamsTypesBaseMeta._compare_types(
            'X', 'v1', 'X', 'v2', fuzzy=False
        ) is False

    def test_compare_types_fuzzy_match(self):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = ClamsTypesBaseMeta._compare_types(
                'X', 'v1', 'X', 'v2', fuzzy=True
            )
        assert result is True
        assert any('version difference' in str(x.message) for x in w)

    def test_compare_types_different_shortname(self):
        assert ClamsTypesBaseMeta._compare_types(
            'X', 'v1', 'Y', 'v1', fuzzy=True
        ) is False


# ===================================================================
# attype_uri_isdocument
# ===================================================================

class TestAttypeUriIsdocument:

    def test_document_slash(self):
        assert TypesBase.attype_uri_isdocument(
            'http://x/TextDocument/v1'
        ) is True

    def test_ends_with_document(self):
        assert TypesBase.attype_uri_isdocument(
            'http://x/Document'
        ) is True

    def test_non_document(self):
        assert TypesBase.attype_uri_isdocument(
            'http://x/TimeFrame/v1'
        ) is False

    def test_alias_name(self):
        assert TypesBase.attype_iri_isdocument is (
            TypesBase.attype_uri_isdocument
        )


# ===================================================================
# Backward compatibility aliases
# ===================================================================

# ===================================================================
# __init_subclass__ — property alias MRO merge
# ===================================================================

class TestPropertyAliasesMerge:

    def test_child_inherits_parent_aliases(self):
        class Parent(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'x': {'a', 'x'},
            }

        class Child(Parent):
            _property_aliases: ClassVar[dict] = {
                'y': {'b', 'y'},
            }

        assert 'x' in Child._property_aliases
        assert 'y' in Child._property_aliases

    def test_grandchild_inherits_all(self):
        class G1(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'a': {'a1', 'a'},
            }

        class G2(G1):
            _property_aliases: ClassVar[dict] = {
                'b': {'b1', 'b'},
            }

        class G3(G2):
            _property_aliases: ClassVar[dict] = {
                'c': {'c1', 'c'},
            }

        assert set(G3._property_aliases.keys()) == {'a', 'b', 'c'}

    def test_duplicate_equal_aliases_ok(self):
        class P(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'x': {'a', 'x'},
            }

        # Same key, same value — should not raise
        class C(P):
            _property_aliases: ClassVar[dict] = {
                'x': {'a', 'x'},
            }

        assert C._property_aliases['x'] == {'a', 'x'}

    def test_child_without_own_aliases_inherits(self):
        class P(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'x': {'a', 'x'},
            }

        class C(P):
            pass

        assert C._property_aliases == {'x': {'a', 'x'}}


# ===================================================================
# __init_subclass__ — property alias conflict detection
# ===================================================================

class TestPropertyAliasesConflict:

    def test_conflicting_alias_raises(self):
        class P(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'x': {'a', 'x'},
            }

        with pytest.raises(TypeError, match='conflicting'):
            class C(P):
                _property_aliases: ClassVar[dict] = {
                    'x': {'b', 'x'},
                }

    def test_mro_ancestor_conflict_raises(self):
        class A1(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'x': {'a', 'x'},
            }

        class A2(AnnotationTypesBase):
            _property_aliases: ClassVar[dict] = {
                'x': {'b', 'x'},
            }

        with pytest.raises(TypeError, match='conflicting'):
            class C(A1, A2):
                pass


# ===================================================================
# __init_subclass__ — field redefinition guard
# ===================================================================

class TestFieldRedefinitionGuard:

    def test_redefining_parent_field_raises(self):
        class P(AnnotationTypesBase):
            label: Optional[str] = Field(None, description='p')

        with pytest.raises(TypeError, match='redefines field'):
            class C(P):
                label: Optional[str] = Field(None, description='c')

    def test_classvar_redefinition_allowed(self):
        class P(AnnotationTypesBase):
            description: ClassVar[str] = 'parent'

        # ClassVar override should not raise
        class C(P):
            description: ClassVar[str] = 'child'

        assert C.description == 'child'

    def test_new_field_on_child_ok(self):
        class P(AnnotationTypesBase):
            label: Optional[str] = Field(None, description='p')

        class C(P):
            score: Optional[float] = Field(None, description='c')

        assert 'label' in C.model_fields
        assert 'score' in C.model_fields


# ===================================================================
# Backward compatibility aliases
# ===================================================================

class TestBackwardCompat:

    def test_thing_types_base_alias(self):
        assert ThingTypesBase is TypesBase

    def test_annotation_types_base_is_clams_subclass(self):
        assert issubclass(AnnotationTypesBase, ClamsTypesBase)

    def test_document_types_base_is_clams_subclass(self):
        assert issubclass(DocumentTypesBase, ClamsTypesBase)
