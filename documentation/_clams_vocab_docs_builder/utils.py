import importlib
import inspect
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def clean_json_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean JSON Schema to use required array instead of anyOf with null.

    Also removes title fields as they are redundant metadata.

    Pydantic generates optional fields as anyOf: [{type: X}, {type: null}].
    This converts them to just {type: X} and removes from required array.

    :param schema: Original JSON schema from Pydantic
    :returns: Cleaned JSON schema
    """
    if not schema or 'properties' not in schema:
        return schema

    cleaned = schema.copy()
    cleaned['properties'] = {}
    required_fields = set(schema.get('required', []))

    if 'title' in cleaned:
        del cleaned['title']

    for prop_name, prop_def in schema['properties'].items():
        cleaned_prop = prop_def.copy()

        if 'title' in cleaned_prop:
            del cleaned_prop['title']

        if 'anyOf' in cleaned_prop:
            any_of_list = cleaned_prop['anyOf']
            non_null_types = [
                t for t in any_of_list if t.get('type') != 'null'
            ]

            if len(non_null_types) == 1:
                cleaned_prop = non_null_types[0].copy()

                if 'description' in prop_def:
                    cleaned_prop['description'] = prop_def['description']

                if prop_name in required_fields:
                    required_fields.discard(prop_name)

        cleaned['properties'][prop_name] = cleaned_prop

    cleaned['required'] = sorted(list(required_fields))
    return cleaned


def get_field_origin(field_name: str, cls: type) -> tuple[int, Optional[str]]:
    """
    Find the class that originally defined this field.

    Walks up the inheritance chain to find the first class that defined the field.

    :param field_name: Name of the field to trace
    :param cls: The class to start from
    :returns: Tuple of (depth, origin_class_name) where depth is 0 for native fields
    """
    depth = 0
    origin_class = None
    current = cls

    while True:
        bases = [b for b in current.__bases__
                 if b.__name__ not in ('BaseModel', 'VocabType')]
        if not bases:
            break
        parent = bases[0]
        if hasattr(parent, 'model_fields') and field_name in parent.model_fields:
            depth += 1
            origin_class = parent.__name__
            current = parent
        else:
            break

    return depth, origin_class


def extract_json_type(json_field: Dict[str, Any]) -> str:
    """
    Extract JSON Schema type from a field definition.

    :returns: Human-readable type string (e.g., "string", "array of string")
    """
    if 'type' in json_field:
        base_type = json_field['type']
        if base_type == 'array' and 'items' in json_field:
            item_type = json_field['items'].get('type', 'any')
            return f"array of {item_type}"
        return base_type

    if 'anyOf' in json_field:
        types = []
        for option in json_field['anyOf']:
            if option.get('type') == 'null':
                continue
            if 'type' in option:
                opt_type = option['type']
                if opt_type == 'array' and 'items' in option:
                    item_type = option['items'].get('type', 'any')
                    types.append(f"array of {item_type}")
                else:
                    types.append(opt_type)

        if len(types) == 1:
            return types[0]
        elif len(types) > 1:
            return ' or '.join(types)

    return 'any'


def discover_type_versions(types_dir: Path) -> Dict[str, List[int]]:
    """
    Discover all type versions by scanning for vX.py files.

    :returns: {'time_frame': [1, 2], 'interval': [1, 2], ...}
    """
    type_versions = {}

    for type_dir in types_dir.iterdir():
        if not type_dir.is_dir() or type_dir.name.startswith('_'):
            continue

        versions = []
        for version_file in type_dir.glob('v*.py'):
            match = re.match(r'v(\d+)\.py$', version_file.name)
            if match:
                versions.append(int(match.group(1)))

        if versions:
            type_versions[type_dir.name] = sorted(versions)

    return type_versions


def get_latest_types(types_dir: Path) -> Dict[str, int]:
    """
    Determine which type version is "latest" for each type.

    Reads __init__.py files to find the alias class that inherits from
    the latest versioned class (e.g., class TimeFrame(TimeFrame_v6)).

    :returns: {'time_frame': 2, 'interval': 2, 'span': 1, ...}
    """
    latest_types = {}

    for type_dir in types_dir.iterdir():
        if not type_dir.is_dir() or type_dir.name.startswith('_'):
            continue

        init_file = type_dir / '__init__.py'
        if not init_file.exists():
            continue

        content = init_file.read_text()
        pattern = r'class \w+\(\w+_v(\d+)\):'
        for line in content.split('\n'):
            match = re.search(pattern, line.strip())
            if match:
                latest_types[type_dir.name] = int(match.group(1))
                break

    return latest_types


def extract_type_metadata(type_dir: Path, version: int) -> Dict[str, Any]:
    """
    Extract metadata from a type version class.

    :param type_dir: Path to type directory (e.g., types/time_frame)
    :param version: Version number (e.g., 1)
    :returns: Metadata dictionary with class info, fields, parent, etc.
    """
    type_name = type_dir.name
    module_path = f'clams_vocabulary.types.{type_name}.v{version}'

    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        print(f"WARNING: Could not import {module_path}: {e}")
        return {}

    class_name = None
    type_class = None
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name.endswith(f'_v{version}') and obj.__module__ == module.__name__:
            class_name = name
            type_class = obj
            break

    if not type_class:
        print(f"WARNING: No class found for {module_path}")
        return {}

    metadata = {
        'class_name': class_name,
        'module_path': module_path,
        'uri': getattr(type_class, 'uri', ''),
        'version': getattr(type_class, 'version', ''),
        'shortname': getattr(type_class, 'shortname', ''),
        'description': getattr(type_class, 'description', ''),
        'alsoKnownAs': getattr(type_class, 'alsoKnownAs', []),
        'similarTo': getattr(type_class, 'similarTo', []),
    }

    bases = [b for b in type_class.__bases__
             if b.__name__ not in ('BaseModel', 'VocabType')]
    if bases:
        parent = bases[0]
        metadata['parent_class'] = parent.__name__
        metadata['parent_module'] = parent.__module__
    else:
        metadata['parent_class'] = None
        metadata['parent_module'] = None

    if hasattr(type_class, 'model_json_schema'):
        raw_schema = type_class.model_json_schema()
        metadata['json_schema'] = clean_json_schema(raw_schema)
    else:
        metadata['json_schema'] = {}

    if hasattr(type_class, 'model_fields'):
        # fields will be a list of dicts with field metadata
        # and it's sorted by
        # 1. inheritance: native first, closest parent next
        # 2. required fields first
        # 3. alphabetically by field name
        fields = []
        json_props = metadata['json_schema'].get('properties', {})

        for field_name, field_info in type_class.model_fields.items():

            json_field = json_props.get(field_name, {})
            json_type = extract_json_type(json_field)

            default_value = None
            if 'default' in json_field:
                default_value = json_field['default']

            inheritance_depth, inherited_from = get_field_origin(
                field_name, type_class
            )

            fields.append({
                'name': field_name,
                'type': str(field_info.annotation),
                'json_type': json_type,
                'required': field_info.is_required(),
                'description': field_info.description or '',
                'alias': field_info.alias if field_info.alias else None,
                'default': default_value,
                'inheritance_depth': inheritance_depth,
                'inherited_from': inherited_from,
            })

        fields.sort(key=lambda f: (
            f['inheritance_depth'],
            0 if f['required'] else 1,
            f['name']
        ))
        metadata['fields'] = fields
    else:
        metadata['fields'] = []

    return metadata


def build_type_to_vocab_index(
    repo_dir: Path,
    force_rebuild: bool = False
) -> Dict[str, List[str]]:
    """
    Build reverse index: TypeVersionClass -> [vocab versions].

    Uses git tags to determine which vocab versions (1.x.x only) included
    each type. Caches results to .type_vocab_index.json.

    :param repo_dir: Repository root directory
    :param force_rebuild: Force rebuild of cache even if it exists
    :returns: {'TimeFrame_v1': ['1.0.0', '1.0.1'], ...}
    """
    cache_file = repo_dir / '.type_vocab_index.json'

    if cache_file.exists() and not force_rebuild:
        cache_mtime = cache_file.stat().st_mtime

        result = subprocess.run(
            ['git', 'for-each-ref', '--sort=-creatordate',
             '--format=%(creatordate:unix)', 'refs/tags', '--count=1'],
            capture_output=True, text=True, cwd=repo_dir
        )
        if result.returncode == 0 and result.stdout.strip():
            latest_tag_time = int(result.stdout.strip())
            if cache_mtime > latest_tag_time:
                print("Using cached type-to-vocab index")
                with open(cache_file) as f:
                    return json.load(f)

    print("Building type-to-vocab index from git tags...")

    vocab_versions = get_vocab_versions(repo_dir)

    if not vocab_versions:
        print("WARNING: No vocabulary version tags found")
        return {}

    index = {}

    for version in vocab_versions:
        full_tag = find_tag_for_version(repo_dir, version)
        if not full_tag:
            print(f"WARNING: Could not find tag for version {version}")
            continue

        types_init_files = get_type_init_files_at_tag(repo_dir, full_tag)

        for type_name, init_content in types_init_files.items():
            latest_class = extract_latest_class_from_init(init_content)
            if latest_class:
                if latest_class not in index:
                    index[latest_class] = []
                index[latest_class].append(version)

    with open(cache_file, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"Built index for {len(index)} type versions")
    return index


def get_type_init_files_at_tag(
    repo_dir: Path,
    tag: str
) -> Dict[str, str]:
    """Get all types/__init__.py files at a specific git tag."""
    result = subprocess.run(
        ['git', 'ls-tree', '-r', '--name-only', tag,
         'clams_vocabulary/types'],
        capture_output=True, text=True, cwd=repo_dir
    )

    if result.returncode != 0:
        return {}

    init_files = [f for f in result.stdout.split('\n')
                  if f.endswith('__init__.py') and '__pycache__' not in f]

    contents = {}
    for file_path in init_files:
        type_name = file_path.split('/')[-2]
        if type_name.startswith('_'):
            continue

        result = subprocess.run(
            ['git', 'show', f'{tag}:{file_path}'],
            capture_output=True, text=True, cwd=repo_dir
        )
        if result.returncode == 0:
            contents[type_name] = result.stdout

    return contents


def extract_latest_class_from_init(init_content: str) -> Optional[str]:
    """
    Parse __init__.py to find the aliased class.

    Example: class TimeFrame(TimeFrame_v5): -> 'TimeFrame_v5'
    """
    pattern = r'class \w+\((\w+_v\d+)\):'
    for line in init_content.split('\n'):
        match = re.search(pattern, line.strip())
        if match:
            return match.group(1)
    return None


def get_vocab_versions(repo_dir: Path) -> List[str]:
    """
    Get all vocabulary versions from git tags, sorted by version.

    Returns version strings (e.g., '1.0.0', '1.0.1').
    Filters to 1.x.x range (legacy MMIF vocabulary versions).
    """
    result = subprocess.run(
        ['git', 'tag', '--sort=version:refname'],
        capture_output=True, text=True, cwd=repo_dir
    )
    if result.returncode != 0:
        return []

    versions = []
    version_pattern = re.compile(r'(\d+\.\d+\.\d+)')

    for tag in result.stdout.strip().split('\n'):
        if not tag:
            continue

        match = version_pattern.search(tag)
        if not match:
            continue

        version = match.group(1)
        if version.startswith('1.'):
            versions.append(version)

    return versions


def find_tag_for_version(repo_dir: Path, version: str) -> Optional[str]:
    """
    Find the git tag that corresponds to a version number.

    :param version: Version string (e.g., '1.0.0')
    :returns: Full tag name (e.g., 'v1.0.0' or 'mmif-1.0.0') or None
    """
    result = subprocess.run(
        ['git', 'tag'],
        capture_output=True, text=True, cwd=repo_dir
    )
    if result.returncode != 0:
        return None

    version_pattern = re.compile(re.escape(version))
    for tag in result.stdout.strip().split('\n'):
        if version_pattern.search(tag):
            return tag

    return None


def get_latest_types_at_tag(repo_dir: Path, tag: str) -> Dict[str, int]:
    """
    Get the latest type versions at a specific git tag.

    :param tag: Version string (e.g., '1.0.0')
    :returns: {'time_frame': 5, 'interval': 4, ...} - type_name -> version
    """
    full_tag = find_tag_for_version(repo_dir, tag)
    if not full_tag:
        return {}

    types_init_files = get_type_init_files_at_tag(repo_dir, full_tag)
    latest_types = {}

    for type_name, init_content in types_init_files.items():
        latest_class = extract_latest_class_from_init(init_content)
        if latest_class:
            version_match = re.search(r'_v(\d+)$', latest_class)
            if version_match:
                latest_types[type_name] = int(version_match.group(1))

    return latest_types
