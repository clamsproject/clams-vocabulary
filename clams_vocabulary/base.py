"""
Base classes for CLAMS vocabulary types.
"""
import re
import warnings
from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict
from pydantic import HttpUrl, TypeAdapter, model_serializer


class TypesBaseMeta(type(BaseModel)):
    """
    Metaclass for TypesBase.
    Inherits from Pydantic's metaclass to avoid conflicts.
    Can be extended by ClamsTypesBaseMeta for additional class-level methods.
    """
    pass


class TypesBase(BaseModel, metaclass=TypesBaseMeta):
    """
    Base Pydantic model for vocabulary types.

    Models vocabulary types that follow the naming convention:
    base_uri (HTTP/HTTPS URL) / single-word shortname = full type URI.
    Based on the LAPPS vocabulary naming convention.

    **Type Resolution**: Use `from_str()` to resolve types from URIs:
    - CLAMS URIs: Resolved via static registry in __init__.py (URI_TO_TYPE)
    - Generic URIs: Creates generic TypesBase instance

    **Prefix Generation**: Annotation ID prefixes are generated dynamically
    for all types (CLAMS and generic) to avoid collisions. Prefixes are
    cached in `_prefixes` ClassVar dict.
    """
    model_config = ConfigDict(
        extra="allow",
        validate_assignment=False,
        arbitrary_types_allowed=True
    )

    # Note: base_uri, shortname, and fuzzy_eq are set in __init__
    # as instance attributes (not Pydantic fields, not ClassVars)

    # Prefix registry: Dynamically generated prefixes for annotation IDs
    # Shared across all instances (CLAMS + generic types)
    _prefixes: ClassVar[dict] = {}  # Shortname -> dynamically generated prefix
    # ClassVars for shared state
    _old_lapps_type_shortnames: ClassVar[set] = {
        'Token', 'Sentence', 'Paragraph', 'Markable',
        'NamedEntity', 'NounChunk', 'VerbChunk'
    }
    _old_lapps_type_base_uri: ClassVar[str] = 'http://vocab.lappsgrid.org'

    def __init__(self, type_uri: str, /, **data):
        """
        Initialize a vocabulary type.

        :param type_uri: Full URI (e.g., "http://example.org/MyType") or shortname
        :param data: Direct field initialization (for subclasses)
        """
        # Initialize Pydantic model first
        super().__init__(**data)
        # Store original input URI for round-trip fidelity
        self.initialized_from = type_uri
        self.fuzzy_eq = False
        if '/' in type_uri:
            self.base_uri, self.shortname = type_uri.rsplit('/', 1)
        else:
            self.base_uri = ""
            self.shortname = type_uri
        # some naive validation of the base part
        if self.base_uri:
            adapter = TypeAdapter(HttpUrl)
            adapter.validate_python(self.base_uri)
        if self.__repr__() not in self.__class__._prefixes:
            # prepare auto-inferred prefix for Annotations.[].id field
            prefix = self.__class__._create_prefix(
                self.shortname, self.__class__._prefixes.values()
            )
            self.__class__._prefixes[self.__repr__()] = prefix

    @classmethod
    def _create_prefix(cls, shortname: str, existing_prefixes) -> Optional[str]:

        def extract_chars(string, indices):
            return "".join(string[i].lower()
                           for i in sorted(set(indices)) if i < len(string))

        if not shortname.isalnum():
            return None

        # capital letters
        cap_chars = [i for i, c in enumerate(shortname) if c.isupper()]
        # put the final fencepost
        cap_chars += [len(shortname)]
        if len(cap_chars) > 1:
            max_diff = max(cap_chars[i] - cap_chars[i - 1]
                           for i in range(1, len(cap_chars)))
        else:
            max_diff = len(shortname)

        add_chars = []
        prefix = extract_chars(shortname, cap_chars)

        # handle collisions
        if prefix in existing_prefixes:
            for i in range(1, max_diff):
                for j in cap_chars:
                    add_chars.append(j + i)
                    prefix = extract_chars(shortname, cap_chars + add_chars)
                    if prefix not in existing_prefixes:
                        break
                else:
                    continue
                break

        return prefix

    @staticmethod
    def attype_uri_isdocument(uri: str) -> bool:
        """
        Check if URI represents a Document type.

        :param uri: URI string to check
        :return: True if URI represents a Document type
        """
        return 'Document/' in uri or uri.endswith('Document')

    # alias for backward compatibility
    attype_iri_isdocument = attype_uri_isdocument

    @classmethod
    def from_str(cls, string: str) -> "TypesBase":
        """
        Create TypesBase instance from URI string.

        If the URI has a pre-defined CLAMS type (defined in __init__),
        returns the corresponding type instance (unvalidated).
        Otherwise, returns a generic TypesBase instance for generic URIs.

        :param string: URI string (full URI or bare shortname)
        :return: TypesBase instance (or subclass instance)
        """
        # Import at function level to avoid circular dependency
        try:
            from . import URI_TO_TYPE
        except ImportError:
            # Registry not yet built (during initialization)
            return cls(string)

        # Check if URI is in registry
        if string in URI_TO_TYPE:
            # Return unvalidated instance for known types
            instance = URI_TO_TYPE[string].model_construct()
            # Store original input URI for round-trip fidelity
            instance.initialized_from = string
            return instance
        else:
            # Generic type (non-CLAMS or unrecognized)
            return cls(string)

    @property
    def uri(self) -> str:
        """
        Get the full type URI.
        """
        # Construct from instance attributes
        if hasattr(self, 'base_uri') and self.base_uri:
            return f"{self.base_uri}/{self.shortname}"
        elif hasattr(self, 'shortname'):
            return self.shortname
        raise ValueError("Cannot determine URI: missing components")

    def __hash__(self):
        """Hash based on canonical URI for consistent dictionary lookups."""
        return hash(self.uri)

    def __eq__(self, other):
        if isinstance(other, str):
            other = self.from_str(other)
        # Handle comparison with classes (not just instances)
        if isinstance(other, type) and issubclass(other, TypesBase):
            return self.uri == repr(other)
        return isinstance(other, TypesBase) and self.uri == other.uri

    def __repr__(self):
        """
        Return string representation of the type URI.

        Prefers the original input URI (initialized_from) if available,
        otherwise uses the canonical URI for round-trip fidelity.
        """
        if hasattr(self, 'initialized_from'):
            return self.initialized_from
        return self.uri

    # aliases
    def __str__(self):
        return repr(self)

    @classmethod
    def _serialize(cls):
        """Serialize to URI string (works for both classes and instances)."""
        return repr(cls)

    @model_serializer
    def _model_serializer(self):
        """
        Experimental, custom Pydantic serializer.
        This will eventually replace de-/serialization logic in
        `Annotation` class in mmif-python.

        Returns: {"@type": uri, "properties": {field_data}}
        """
        # Get all Pydantic fields (excludes instance attrs and ClassVars)
        properties = {}
        for field_name in self.model_fields:
            value = getattr(self, field_name, None)
            if value is not None and value != "":  # Only non-empty values
                properties[field_name] = value

        return {
            "@type": self.uri,
            "properties": properties
        }

    @classmethod
    def get_prefix(cls):
        """
        Get annotation ID prefix for this type.

        Looks up prefix from registry using shortname if available,
        otherwise uses full URI.

        :return: Prefix string for generating annotation IDs
        :rtype: str
        """
        # CLAMS types have shortname as ClassVar, use that as key
        if hasattr(cls, 'shortname'):
            key = cls.shortname
        else:
            # Generic types use full URI
            key = repr(cls)
        return cls._prefixes[key]

    def set_prefix(self, prefix):
        """
        Set annotation ID prefix for this type. Ideally, all per-type
        prefixes are generated automatically, this method allows manual
        override if needed.
        """
        self.__class__._prefixes[self.shortname] = prefix


# This looks wrong, but kept for backward compatibility
ThingTypesBase = TypesBase


class ClamsTypesBaseMeta(TypesBaseMeta):
    """
    Metaclass for CLAMS vocabulary types.

    Inherits from TypesBaseMeta to get class-level _serialize() method.
    Provides class-level equality comparison with fuzzy version matching.
    """

    @staticmethod
    def _compare_types(shortname1, version1, shortname2, version2, fuzzy):
        """
        Shared type comparison logic for both class and instance level.

        :param shortname1: First type's shortname
        :param version1: First type's version
        :param shortname2: Second type's shortname
        :param version2: Second type's version
        :param fuzzy: If True, ignore version differences
        :return: True if types match
        """
        if shortname1 != shortname2:
            return False

        if fuzzy:
            if version1 != version2:
                warnings.warn(
                    f'version difference detected: '
                    f'{version1}&{version2}@{shortname1}')
            return True
        else:
            return version1 == version2

    @staticmethod
    def _is_versioned(name):
        """Check if class name indicates a versioned type (e.g., Type_v1)."""
        return bool(re.search(r'_v\d+$', name))

    def __eq__(cls, other):
        """
        Class-level equality comparison with fuzzy version matching.

        Versioned classes (e.g., TypeOne_v1, TypeOne_v2) use strict comparison.
        Aliases or unversioned classes use fuzzy comparison (ignore version).

        :param other: Class or string to compare with
        :return: True if classes represent the same type
        """
        # Check if cls is a proper CLAMS type class
        if not (hasattr(cls, 'shortname') and hasattr(cls, 'version')):
            return type.__eq__(cls, other)

        # If other is a string, convert using from_str()
        if isinstance(other, str):
            other_instance = cls.from_str(other)
            other = other_instance.__class__

        # Check if other is a proper CLAMS type class
        if not isinstance(other, ClamsTypesBaseMeta):
            return type.__eq__(cls, other)
        if not (hasattr(other, 'shortname') and hasattr(other, 'version')):
            return type.__eq__(cls, other)

        # Proceed with fuzzy-able comparison
        cls_versioned = ClamsTypesBaseMeta._is_versioned(cls.__name__)
        other_versioned = ClamsTypesBaseMeta._is_versioned(other.__name__)
        fuzzy = not (cls_versioned and other_versioned)

        return ClamsTypesBaseMeta._compare_types(
            cls.shortname, cls.version,
            other.shortname, other.version,
            fuzzy
        )

    def __str__(cls):
        """Return string representation of the class type URI."""
        return repr(cls)

    def __repr__(cls):
        """Return string representation of the class type URI."""
        return cls.uri

    def __hash__(cls):
        """Hash based on canonical URI for consistent hashing."""
        # Check if cls is a proper CLAMS type class
        if not (hasattr(cls, 'shortname') and hasattr(cls, 'version')):
            # Not a proper CLAMS type - use URI directly
            return hash(cls.uri)

        # if it's a proper CLAMS type, just use shortname for hashing
        return hash(cls.shortname)


class ClamsTypesBase(TypesBase, metaclass=ClamsTypesBaseMeta):
    """
    Base class for CLAMS vocabulary types.
    This class adds handling of versioning specific to MMIF and CLAMS
    types for fuzzy type matching.
    """
    uri: ClassVar[str]
    version: ClassVar[str]
    shortname: ClassVar[str]
    base_uri: ClassVar[str] = ''
    description: ClassVar[str]
    alsoKnownAs: ClassVar[list[str]] = []
    similarTo: ClassVar[list[str]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'uri') and hasattr(cls, 'shortname'):
            # derive base_uri: strip /{shortname}/{version} from uri
            uri = cls.uri
            short = cls.shortname
            idx = uri.find(f'/{short}/')
            if idx >= 0:
                cls.base_uri = uri[:idx]

    model_config = ConfigDict(
        extra="allow",
        validate_assignment=False,
        arbitrary_types_allowed=True,
        # Disable validation for CLAMS types - they have special URI formats
        validate_default=False
    )

    # in __init__, not as Pydantic fields

    def __init__(self, type_uri=None, fuzzymode=None, **data):
        """
        Initialize a CLAMS vocabulary type wrapper.

        :param type_uri: Either full URI/shortname string or Pydantic class
        :param fuzzymode: If True, enables fuzzy equality comparison that
            ignores version differences. If None, auto-detects based on
            class name (versioned classes like Type_v1 default to strict,
            aliases default to fuzzy)
        :param data: Additional field data for Pydantic initialization
        """
        # Initialize Pydantic BaseModel
        BaseModel.__init__(self, **data)

        # Store original input URI for round-trip fidelity
        if type_uri is not None:
            self.initialized_from = type_uri

        if type_uri is None:
            # this should not happen, but just in case
            self.shortname = ""
        elif type_uri[-1].isdigit():
            # individual version: https://mmif.clams.ai/vocabulary/TypeName/vX
            parts = type_uri.rsplit('/', 3)
            self.shortname = parts[2]
        else:
            # legacy versioning: https://mmif.clams.ai/0.4.X/vocabulary/TypeName
            parts = type_uri.rsplit('/', 3)
            self.shortname = parts[3]

        # Auto-detect fuzzy mode based on class name if not explicitly set
        if fuzzymode is None:
            # Versioned classes (e.g., TypeOne_v1) default to strict (False)
            # Aliases/base classes default to fuzzy (True)
            fuzzymode = not ClamsTypesBaseMeta._is_versioned(
                self.__class__.__name__)

        # Set fuzzy equality mode
        self.fuzzy_eq = fuzzymode

        # Prefix generation is handled during registry finalization

    def model_post_init(self, __context):
        """
        Pydantic v2 hook called after model construction.
        Sets fuzzy_eq for instances created via model_construct().
        """
        # Only set if not already set (avoid overwriting explicit values)
        if not hasattr(self, 'fuzzy_eq'):
            # Auto-detect based on class name
            fuzzymode = not ClamsTypesBaseMeta._is_versioned(
                self.__class__.__name__)
            self.fuzzy_eq = fuzzymode

    def __hash__(self):
        """
        Hash is just based on the shortname, ignoring version and URI prefix.
        """
        return hash(self.shortname)

    def _eq_internal(self, other, fuzzy):
        """
        Internal equality comparison with version handling, using fuzzy flag.

        Note that in old mmif.vocabulary implementation, all legacy types were
        separately "registered" as their own Type instances, but in this new
        implementation, each type is represented by an independent class.
        Therefore, instead of generating class definitions for legacy types, we
        pre-compile normalization rules based on "also-known-as" values in old
        transition rules.

        Meaning:
        - we don't need to implement normalization on-the-fly.
        - if an input MMIF has a legacy URIs, in the output, they (URI strings)
          are replaced with the latest "normal" URIs.
        """

        if isinstance(other, ClamsTypesBase):
            # Use shared comparison logic from metaclass
            return ClamsTypesBaseMeta._compare_types(
                self.shortname, self.version,
                other.shortname, other.version,
                fuzzy
            )
        else:
            # Legacy LAPPSgrid types
            if (self.shortname in self._old_lapps_type_shortnames
                    and self.version == 'v1'
                    and str(other) == f'{self._old_lapps_type_base_uri}/{self.shortname}'):
                return True
            return False

    def __eq__(self, other):
        """
        Equality comparison with version handling.

        Fuzzy matching is enabled if EITHER side has fuzzy_eq=True,
        ensuring symmetric equality (a == b implies b == a).
        """
        if isinstance(other, str):
            other = ThingTypesBase.from_str(other)
        # Handle comparison with classes (not just instances)
        elif isinstance(other, type) and issubclass(other, ClamsTypesBase):
            other = other.model_construct()
        return self._eq_internal(other, self.fuzzy_eq or other.fuzzy_eq)


class AnnotationTypesBase(ClamsTypesBase):
    """
    Thin wrapper for "annotation" types as opposed to "document" types.

    Provides automatic ``_property_aliases`` merging across the MRO
    and guards against accidental Pydantic field redefinition in
    subclasses.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        own = cls.__dict__.get('_property_aliases', {})

        # Merge _property_aliases from all ancestors
        merged = {}
        for parent in reversed(cls.__mro__):
            if parent is cls:
                continue
            parent_aliases = parent.__dict__.get(
                '_property_aliases', {}
            )
            for key, val in parent_aliases.items():
                if key in merged and merged[key] != val:
                    raise TypeError(
                        f"conflicting _property_aliases for "
                        f"'{key}' in MRO of {cls.__name__}: "
                        f"{merged[key]} vs {val}"
                    )
                merged[key] = val
        for key, val in own.items():
            if key in merged and merged[key] != val:
                raise TypeError(
                    f"conflicting _property_aliases for "
                    f"'{key}' in {cls.__name__}: "
                    f"parent defines {merged[key]}, "
                    f"subclass redefines as {val}"
                )
            merged[key] = val
        if merged:
            cls._property_aliases = merged

        # Guard against Pydantic field redefinition
        own_annotations = cls.__dict__.get('__annotations__', {})
        for field_name in own_annotations:
            if field_name.startswith('_'):
                continue
            for parent in cls.__mro__[1:]:
                parent_ann = parent.__dict__.get(
                    '__annotations__', {}
                )
                if field_name in parent_ann:
                    # Allow ClassVar redefinitions (description, etc.)
                    ann_str = str(parent_ann[field_name])
                    if 'ClassVar' in ann_str:
                        continue
                    raise TypeError(
                        f"{cls.__name__} redefines field "
                        f"'{field_name}' already defined in "
                        f"{parent.__name__}"
                    )


class DocumentTypesBase(ClamsTypesBase):
    """
    Thin wrapper for "document" types as opposed to "annotation" types.
    """
    ...
