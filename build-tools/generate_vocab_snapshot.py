#!/usr/bin/env python3
"""
Build and maintenance tool for CLAMS Vocabulary.

Usage:
    python build-tools/generate_vocab_snapshot.py build [types...]
    python build-tools/generate_vocab_snapshot.py clean
"""

import argparse
import ast
import re
import shutil
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import git
except ImportError:
    print("GitPython is required. Install it with: pip install GitPython")
    sys.exit(1)

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import inflection

# CONSTANTS
VOCAB_PACKAGE_NAME = "clams_vocabulary"
VOCAB_TYPES_SUBDIR = "types"

AUTOGEN_WARNING = (
    '"""\n'
    'This file is auto-generated.\n'
    'This file should never be manually modified, and must stay FROZEN.\n'
    '"""\n'
)


@dataclass
class PropertyInfo:
    type_name: str
    description: str
    required: bool


@dataclass
class ArchetypeInfo:
    name: str
    shortname: str
    description: str
    parent: Optional[str]
    also_known_as: List[str] = field(default_factory=list)
    properties: Dict[str, PropertyInfo] = field(default_factory=dict)


# CONFIGURATION
@lru_cache(maxsize=1)
def _get_project_root() -> Path:
    """Find the project root by looking for pyproject.toml or .git."""
    current = Path(__file__).parent
    while current != current.parent:
        if ((current / 'pyproject.toml').exists()
                or (current / '.git').exists()):
            return current
        current = current.parent
    raise FileNotFoundError(
        "Could not find project root (no pyproject.toml or .git)"
    )


@lru_cache(maxsize=1)
def _get_git_repo() -> git.Repo:
    """Get the GitPython Repo object."""
    try:
        return git.Repo(_get_project_root(), search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        print("Error: Not a git repository.")
        sys.exit(1)


@lru_cache(maxsize=1)
def _load_pyproject() -> dict:
    """Load pyproject.toml."""
    with open(_get_project_root() / 'pyproject.toml', 'rb') as f:
        return tomllib.load(f)


def get_type_path_component() -> str:
    """
    Extract the path component from type_prefix URL.

    :returns: Path component (e.g., 'type' from 'https://.../type')
    """
    from urllib.parse import urlparse
    try:
        type_prefix_url = _load_pyproject()['project']['urls']['type_prefix']
        path = urlparse(type_prefix_url).path.strip('/')
        # Get the last component of the path
        return path.split('/')[-1] if path else ''
    except KeyError as e:
        raise KeyError(
            f"Missing required configuration in pyproject.toml: "
            f"[project.urls] type_prefix must be set. Missing key: {e}"
        )


def get_full_uri_prefix() -> str:
    """
    Get the full URI prefix for vocabulary types.

    :returns: Type prefix URL from [project.urls] type_prefix
    :raises KeyError: If type_prefix is not configured
    """
    try:
        return _load_pyproject()['project']['urls']['type_prefix']
    except KeyError as e:
        raise KeyError(
            f"Missing required configuration in pyproject.toml: "
            f"[project.urls] type_prefix must be set. Missing key: {e}"
        )


# GIT & CLEAN UTILITIES
class GitUtils:
    @staticmethod
    def is_tracked(path: Path) -> bool:
        repo = _get_git_repo()
        try:
            # ls-files returns empty string if not found when not using error-unmatch
            # using error-unmatch raises exception on missing
            repo.git.ls_files(str(path), error_unmatch=True)
            return True
        except git.GitCommandError:
            return False

    @staticmethod
    def is_modified(path: Path) -> bool:
        repo = _get_git_repo()
        # is_dirty returns True if modified. 
        # We check specifically for the given path.
        return repo.is_dirty(path=str(path))

    @staticmethod
    def checkout(path: Path):
        repo = _get_git_repo()
        repo.git.checkout('HEAD', str(path))

    @staticmethod
    @lru_cache(maxsize=1)
    def latest_tag() -> Optional[str]:
        """Find the latest semver tag in the repo."""
        repo = _get_git_repo()
        try:
            tags = repo.git.tag(
                '--sort=-version:refname', '--list', '[0-9]*'
            ).strip()
            return tags.split('\n')[0] if tags else None
        except git.GitCommandError:
            return None

    @staticmethod
    def file_at_tag(tag: str, path: Path) -> Optional[str]:
        """Get file contents at a specific git tag."""
        repo = _get_git_repo()
        rel = path.relative_to(_get_project_root())
        try:
            return repo.git.show(f'{tag}:{rel}')
        except git.GitCommandError:
            return None


def smart_clean(path: Path, verbose: bool = True) -> bool:
    """Delete if untracked, restore if modified. Return True if action taken."""
    if not path.exists():
        return False

    rel_path = path.relative_to(_get_project_root())
    
    if not GitUtils.is_tracked(path):
        if verbose:
            print(f"  Deleting untracked: {rel_path}")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return True
    
    if GitUtils.is_modified(path):
        if verbose:
            print(f"  Restoring from git: {rel_path}")
        GitUtils.checkout(path)
        return True
        
    return False


def clean_type_classes(type_dir: Path) -> str:
    """Clean generated pydantic models and __init__ files."""
    for vfile in type_dir.glob('v*.py'):
        if vfile.stem[1:].isdigit():
            smart_clean(vfile)
    smart_clean(type_dir / '__init__.py')
    return inflection.camelize(type_dir.name, uppercase_first_letter=True)


def clean_rst_files(rst_dir: Union[Path, str]):
    """Clean generated RST files."""
    repo_root = _get_project_root()
    if isinstance(rst_dir, str):
        docs_root = repo_root / 'documentation'
        prefix = get_type_path_component()
        rst_dir = (docs_root / prefix / rst_dir) if prefix else (docs_root / rst_dir)

    if not rst_dir.exists():
        return

    for v_dir in rst_dir.glob('v*'):
        if v_dir.is_dir() and v_dir.name[1:].isdigit():
            idx_json, idx_rst = v_dir / 'index.json', v_dir / 'index.rst'
            if (idx_json.exists() and idx_rst.exists() and 
                GitUtils.is_tracked(idx_json) and GitUtils.is_tracked(idx_rst)):
                smart_clean(idx_json)
                smart_clean(idx_rst)
            else:
                rel_path = v_dir.relative_to(repo_root)
                print(f"  Deleting incomplete/untracked: {rel_path}/")
                shutil.rmtree(v_dir)

    if rst_dir.exists() and not any(rst_dir.iterdir()):
        print(f"  Deleting empty directory: {rst_dir.relative_to(repo_root)}/")
        rst_dir.rmdir()


# VERSION & ARCHETYPE MANAGEMENT
class VersionManager:
    @staticmethod
    def find_versions(type_dir: Path) -> List[int]:
        """Find all existing version numbers in a type directory."""
        return sorted(
            int(m.group(1)) for f in type_dir.glob("v*.py") 
            if (m := re.match(r'v(\d+)\.py$', f.name))
        )

    @staticmethod
    def get_latest_version(type_dir: Path) -> Optional[int]:
        versions = VersionManager.find_versions(type_dir)
        return versions[-1] if versions else None


class ArchetypeLoader:
    @staticmethod
    @lru_cache(maxsize=None)
    def read_archetype(type_dir: Path) -> Optional[ArchetypeInfo]:
        """Load archetype.py or vX.py and extract its structure."""
        src = type_dir if (type_dir.is_file() and type_dir.name.startswith('v')) else type_dir / "archetype.py"
        if not src.exists():
            return None
        return ArchetypeLoader.parse_source(src.read_text())

    @staticmethod
    def parse_source(source: str) -> Optional[ArchetypeInfo]:
        """Parse Python source and extract class structure."""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if info := ArchetypeLoader._extract_class_info(node):
                    return info
        return None

    @staticmethod
    def _extract_class_info(node: ast.ClassDef) -> Optional[ArchetypeInfo]:
        shortname = None
        description = None
        parent = None
        also_known_as: List[str] = []
        properties: Dict[str, PropertyInfo] = {}

        if node.bases:
            base = node.bases[0]
            if isinstance(base, ast.Name):
                parent = base.id
            elif isinstance(base, ast.Attribute):
                parent = base.attr

        for item in node.body:
            if isinstance(item, ast.Assign) and len(item.targets) == 1:
                target = item.targets[0]
                if isinstance(target, ast.Name) and target.id in ('shortname', 'description'):
                    value = ArchetypeLoader._extract_value(item.value)
                    if target.id == 'shortname':
                        shortname = value
                    else:
                        description = value
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                fid = item.target.id
                if fid in ('shortname', 'description') and item.value is not None:
                    value = ArchetypeLoader._extract_value(item.value)
                    if fid == 'shortname':
                        shortname = value
                    else:
                        description = value
                elif fid == 'alsoKnownAs' and item.value is not None:
                    also_known_as = ArchetypeLoader._extract_list(item.value)
                elif fid not in ('uri', 'version'):
                    if field_info := ArchetypeLoader._extract_field_info(item):
                        properties[fid] = field_info

        shortname = shortname or re.sub(r'_v\d+$', '', node.name)
        if not description:
            return None

        return ArchetypeInfo(
            name=node.name,
            shortname=shortname,
            description=description,
            parent=parent,
            also_known_as=also_known_as,
            properties=properties,
        )

    @staticmethod
    def _extract_list(node: ast.AST) -> List[str]:
        """Extract a list of string literals from an AST node."""
        if isinstance(node, ast.List):
            return [
                elt.value for elt in node.elts
                if isinstance(elt, ast.Constant)
                and isinstance(elt.value, str)
            ]
        return []

    @staticmethod
    def _extract_value(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Tuple):
            parts = [
                ArchetypeLoader._extract_value(v)
                for v in node.elts
                if isinstance(v, ast.Constant)
                and isinstance(v.value, str)
            ]
            return ' '.join(parts)
        if isinstance(node, ast.JoinedStr):
            parts = [
                ArchetypeLoader._extract_value(v)
                for v in node.values
                if isinstance(v, ast.Constant)
                and isinstance(v.value, str)
            ]
            return ''.join(parts)
        return None

    @staticmethod
    def _extract_field_info(node: ast.AnnAssign) -> Optional[PropertyInfo]:
        if not (node.value and isinstance(node.value, ast.Call)):
            return None
        call = node.value
        if not (isinstance(call.func, ast.Name) and call.func.id == 'Field'):
            return None
            
        required = False
        if call.args and isinstance(call.args[0], ast.Constant):
            required = (call.args[0].value is ...)

        desc = next((ArchetypeLoader._extract_value(k.value) for k in call.keywords 
                     if k.arg == 'description'), '')

        return PropertyInfo(
            type_name=ast.unparse(node.annotation),
            description=desc,
            required=required,
        )

    @staticmethod
    def metadata_matches(
        archetype_info: ArchetypeInfo,
        frozen_info: ArchetypeInfo,
    ) -> bool:
        """
        Compare archetype metadata against frozen vX.py metadata.

        :returns: True if semantically equivalent (no new version needed)
        """
        def strip_ver(name):
            return re.sub(r'_v\d+$', '', name) if name else name

        if archetype_info.shortname != frozen_info.shortname:
            return False
        if archetype_info.description != frozen_info.description:
            return False
        if strip_ver(archetype_info.parent) != strip_ver(frozen_info.parent):
            return False
        if sorted(archetype_info.also_known_as) \
                != sorted(frozen_info.also_known_as):
            return False
        if archetype_info.properties != frozen_info.properties:
            return False
        return True


# CODE GENERATION
class VersionedCodeGenerator:
    def generate(self, type_dir: Path, version_num: int) -> str:
        info = ArchetypeLoader.read_archetype(type_dir)
        if not info:
            raise ValueError(f"Could not parse archetype in {type_dir}")

        content = AUTOGEN_WARNING + (type_dir / "archetype.py").read_text()
        content = self._versionstamp_imports(content, info, type_dir)
        content = self._versionstamp_class(content, info, version_num, type_dir)
        return content

    def _versionstamp_imports(self, content: str, info: ArchetypeInfo, type_dir: Path) -> str:
        parent = info.parent
        if parent and parent != 'VocabType':
            p_ver = self._get_parent_version(parent, type_dir)
            p_snake = inflection.underscore(parent)
            pat = rf'from {VOCAB_PACKAGE_NAME}\.{VOCAB_TYPES_SUBDIR}\.{p_snake}\.archetype import {parent}'
            rep = f'from {VOCAB_PACKAGE_NAME}.{VOCAB_TYPES_SUBDIR}.{p_snake}.v{p_ver} import {parent}_v{p_ver}'
            content = re.sub(pat, rep, content)
        return content

    def _versionstamp_class(self, content: str, info: ArchetypeInfo, version_num: int, type_dir: Path) -> str:
        name = info.name
        parent = info.parent or 'ClamsTypesBase'
        uri = f"{get_full_uri_prefix()}/{info.shortname}/v{version_num}"
        
        # Replace class definition
        if parent == 'ClamsTypesBase':
            rep = f'class {name}_v{version_num}(ClamsTypesBase):'
        else:
            p_ver = self._get_parent_version(parent, type_dir)
            rep = rf'class {name}_v{version_num}({parent}_v{p_ver}\1):'
        
        content = re.sub(rf'class {name}\({parent}(, \w+)?\):', rep, content)
        
        # Add ClassVars
        attrs = (f'    uri: ClassVar[str] = "{uri}"\n'
                 f'    version: ClassVar[str] = "v{version_num}"\n'
                 f'    shortname: ClassVar[str] = "{info.shortname}"\n')
        
        return re.sub(rf'(class {name}_v{version_num}.*?:)', lambda m: m.group(1) + '\n' + attrs, content)

    @staticmethod
    def _get_parent_version(parent: str, type_dir: Path) -> int:
        p_dir = type_dir.parent / inflection.underscore(parent)
        return VersionManager.get_latest_version(p_dir) or 1


class InitFileGenerator:
    @staticmethod
    def generate_local_init(type_dir: Path) -> str:
        name = inflection.camelize(type_dir.name, uppercase_first_letter=True)
        versions = sorted(VersionManager.find_versions(type_dir))
        latest = versions[-1]
        
        lines = [f"from .v{v} import {name}_v{v}\n" for v in versions]
        lines.append(f"\n\nclass {name}({name}_v{latest}):\n")
        lines.append(f'    """Latest version alias for {name}_v{latest}."""\n    pass\n')
        lines.append(f"\n__all__ = {[f'{name}_v{v}' for v in versions] + [name]}\n")
        
        return ''.join(lines)

    @staticmethod
    def _classify_types(types_dir: Path):
        info_map = {}
        for d in sorted(types_dir.iterdir()):
            if d.is_dir() and (d / "__init__.py").exists():
                if info := ArchetypeLoader.read_archetype(d):
                    info_map[info.name] = {
                        'dir': d.name,
                        'parent': info.parent,
                    }

        def is_doc(cls_name):
            if cls_name == 'Document':
                return True
            p = info_map.get(cls_name, {}).get('parent')
            return is_doc(p) if p and p != 'VocabType' else False

        things, docs, anns = [], [], []
        for cls, meta in sorted(info_map.items()):
            if cls == 'Thing':
                things.append((cls, meta['dir']))
            elif is_doc(cls):
                docs.append((cls, meta['dir']))
            else:
                anns.append((cls, meta['dir']))
        return things, anns, docs

    @staticmethod
    def generate_top_level_init(types_dir: Path, enums_dir: Path) -> str:
        lines = [AUTOGEN_WARNING]
        lines.append('from importlib.metadata import version\n')
        lines.append('__version__ = version("clams-vocabulary")\n\n')
        thing_types, ann_types, doc_types = \
            InitFileGenerator._classify_types(types_dir)

        # Imports & Names Collection
        all_cls = {
            'ThingType': [], 'AnnotationTypes': [], 'DocumentTypes': [],
        }

        for cat, t_list in [('ThingType', thing_types),
                            ('AnnotationTypes', ann_types),
                            ('DocumentTypes', doc_types)]:
            for cls, dname in t_list:
                lines.append(f"from .types.{dname} import *\n")
                vers = VersionManager.find_versions(types_dir / dname)
                all_cls[cat].extend([f"{cls}_v{v}" for v in vers])
                all_cls[cat].append(cls)

        # Enums
        if enums_dir.exists():
            for ed in sorted(enums_dir.iterdir()):
                if ed.is_dir() and (ed / "__init__.py").exists():
                    if info := ArchetypeLoader.read_archetype(ed):
                        lines.append(f"from .enums.{ed.name} import {info.name}\n")

        lines.append('\n\nclass AnnotationTypes:\n    """Namespace for all annotation types."""\n')
        lines.append('    pass\n\n')

        lines.append('class DocumentTypes:\n    """Namespace for all document types."""\n    pass\n\n')

        lines.append('class ThingType:\n    """Namespace for the top-level Thing type. (for backwards compatibility)"""\n    pass\n\n')

        lines.append('class Enums:\n    """Namespace for all controlled vocabularies."""\n    pass\n\n')

        # Populate Namespaces
        for cat, classes in all_cls.items():
            if classes:
                lines.append(f"for _cls in [{', '.join(classes)}]:\n    setattr({cat}, _cls.__name__, _cls)\n\n")

        # Aggregate property aliases from all types
        lines.append('# Aggregate property aliases from type classes\n')
        lines.append('AnnotationTypes._prop_aliases = {}\n')
        lines.append('for _attr in dir(AnnotationTypes):\n')
        lines.append('    if not _attr.startswith("_"):\n')
        lines.append('        _cls = getattr(AnnotationTypes, _attr)\n')
        lines.append('        if hasattr(_cls, "_property_aliases"):\n')
        lines.append('            AnnotationTypes._prop_aliases[_cls.__name__] = _cls._property_aliases\n\n')

        # Registries
        for cat, t_list in [('ThingType', thing_types),
                            ('AnnotationTypes', ann_types),
                            ('DocumentTypes', doc_types)]:
            t_names = ', '.join(cls for cls, _ in t_list)
            lines.append(f"{cat}._typevers = {{_t.shortname: _t.version for _t in [{t_names}]}}\n\n")

        # URI Registry
        all_types = (all_cls['ThingType']
                     + all_cls['AnnotationTypes']
                     + all_cls['DocumentTypes'])
        if all_types:
            lines.append('URI_TO_TYPE = {}\n')
            lines.append(f"for _type in [{', '.join(all_types)}]:\n")
            lines.append('    URI_TO_TYPE[_type.uri] = _type\n')
            lines.append('    for aka in _type.alsoKnownAs:\n        URI_TO_TYPE[aka] = _type\n\n')
            
            lines.append('# Register prefixes\nfrom .base import TypesBase\n')
            lines.append('for _type in URI_TO_TYPE.values():\n')
            lines.append('    if _type.shortname not in TypesBase._prefixes:\n')
            lines.append('        _prefix = TypesBase._create_prefix(_type.shortname, TypesBase._prefixes.values())\n')
            lines.append('        TypesBase._prefixes[_type.shortname] = _prefix\n')

        return ''.join(lines)


# BUILD ORCHESTRATION
_warning_count = 0


def _get_tagged_info(type_dir: Path) -> Optional[ArchetypeInfo]:
    """Get archetype info at the latest git tag. Returns None if
    no tag exists or the type didn't exist at that tag."""
    tag = GitUtils.latest_tag()
    if not tag:
        return None
    src = GitUtils.file_at_tag(
        tag, type_dir / "archetype.py"
    )
    if not src:
        return None
    return ArchetypeLoader.parse_source(src)


def _get_tagged_latest_version(type_dir: Path) -> Optional[int]:
    """Get the latest type version that existed at the last tag."""
    tag = GitUtils.latest_tag()
    if not tag:
        return None
    init_src = GitUtils.file_at_tag(
        tag, type_dir / "__init__.py"
    )
    if not init_src:
        return None
    versions = [
        int(m.group(1))
        for m in re.finditer(r'from \.v(\d+) import', init_src)
    ]
    return max(versions) if versions else None


def _uri_prefix_changed(type_dir: Path, tagged_ver: int) -> bool:
    """Check if URI prefix in pyproject.toml changed since the
    tagged version."""
    frozen_file = type_dir / f"v{tagged_ver}.py"
    if not frozen_file.exists():
        return False
    frozen_src = frozen_file.read_text()
    m = re.search(r'uri: ClassVar\[str\] = "(.+)"', frozen_src)
    if not m:
        return False
    frozen_uri = m.group(1)
    frozen_info = ArchetypeLoader.read_archetype(frozen_file)
    if not frozen_info:
        return False
    current_prefix = get_full_uri_prefix()
    expected_uri = (
        f"{current_prefix}/{frozen_info.shortname}"
        f"/v{tagged_ver}"
    )
    return frozen_uri != expected_uri


def _parent_version_advanced(
    type_dir: Path, info: ArchetypeInfo, tagged_ver: int
) -> bool:
    """Check if parent type's version advanced since the tagged
    version."""
    parent = info.parent
    if not parent or parent in ('ClamsTypesBase', 'VocabType'):
        return False
    p_dir = type_dir.parent / inflection.underscore(parent)
    current_parent_ver = VersionManager.get_latest_version(p_dir)
    tagged_file = type_dir / f"v{tagged_ver}.py"
    if not (current_parent_ver and tagged_file.exists()):
        return False
    frozen_src = tagged_file.read_text()
    m = re.search(
        rf'from .+\.v(\d+) import {parent}_v\d+', frozen_src
    )
    frozen_parent_ver = int(m.group(1)) if m else None
    return bool(
        frozen_parent_ver
        and frozen_parent_ver < current_parent_ver
    )


def build_type(type_dir: Path) -> bool:
    global _warning_count
    print(f" Building type: {type_dir.name}, from dir: {type_dir}")
    if not (info := ArchetypeLoader.read_archetype(type_dir)):
        print("  ✗ No archetype found")
        return False

    tagged_ver = _get_tagged_latest_version(type_dir)
    ver = None

    if tagged_ver is None:
        # Type not at last tag (or no tags) → new type
        ver = 2 if type_dir.name == 'annotation' else 1
        print(f"  → Generating v{ver} (new)")
    else:
        frozen_file = type_dir / f"v{tagged_ver}.py"
        frozen_info = (
            ArchetypeLoader.read_archetype(frozen_file)
            if frozen_file.exists() else None
        )
        if (frozen_info is None
                or not ArchetypeLoader.metadata_matches(
                    info, frozen_info)):
            ver = tagged_ver + 1
            print(f"  → Generating v{ver} (changes detected)")
        elif _uri_prefix_changed(type_dir, tagged_ver):
            ver = tagged_ver + 1
            print(f"  → Generating v{ver} (URI prefix changed)")
        elif _parent_version_advanced(
                type_dir, info, tagged_ver):
            ver = tagged_ver + 1
            parent = info.parent
            print(f"  → Generating v{ver} "
                  f"(parent {parent} advanced)")
        else:
            print(f"  ✓ No changes (current: v{tagged_ver})")

    # Orphan cleanup: remove vX.py files beyond tagged version
    # that aren't the version being generated
    if tagged_ver:
        for v in VersionManager.find_versions(type_dir):
            if v > tagged_ver and v != ver:
                (type_dir / f"v{v}.py").unlink()
                print(f"  🗑 Removed orphaned v{v}.py")

    # AKA stale warning
    if (ver and tagged_ver and ver > tagged_ver
            and info.also_known_as):
        tagged_info = _get_tagged_info(type_dir)
        if tagged_info:
            tagged_aka = set(tagged_info.also_known_as)
            cur_aka = set(info.also_known_as)
            stale = cur_aka & tagged_aka
            if stale:
                _warning_count += 1
                print(
                    "  ⚠ WARNING: alsoKnownAs overlaps with "
                    "tagged release — these URIs already "
                    "belong to a released version. Clear "
                    "alsoKnownAs in archetype.py:"
                )
                for uri in sorted(stale):
                    print(f"    - {uri}")

    if ver:
        try:
            code = VersionedCodeGenerator().generate(
                type_dir, ver
            )
            (type_dir / f"v{ver}.py").write_text(code)
            print(f"  ✓ Generated v{ver}.py")
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            return False

    if InitFileGenerator.generate_local_init(type_dir):
        (type_dir / "__init__.py").write_text(
            AUTOGEN_WARNING
            + InitFileGenerator.generate_local_init(type_dir)
        )
        print("  ✓ Updated __init__.py")
    return True


def topological_sort(type_dirs: List[Path]) -> List[Path]:
    deps = {}
    by_name = {d.name: d for d in type_dirs}
    
    for d in type_dirs:
        info = ArchetypeLoader.read_archetype(d)
        parent = info.parent if info else None
        deps[d.name] = (
            inflection.underscore(parent)
            if (parent and parent != 'VocabType') else None
        )

    result, visited = [], set()

    def visit(name):
        if name in visited:
            return
        visited.add(name)
        if (parent := deps.get(name)) and parent in deps:
            visit(parent)
        if name in by_name:
            result.append(by_name[name])

    for name in deps:
        visit(name)
    return result


def _run_build(type_names: Optional[List[str]]) -> int:
    types_dir = _get_project_root() / VOCAB_PACKAGE_NAME / VOCAB_TYPES_SUBDIR
    all_dirs = [d for d in sorted(types_dir.iterdir()) 
                if d.is_dir() and (d / "archetype.py").exists()]
    
    target_dirs = all_dirs
    if type_names:
        targets = {inflection.underscore(n) for n in type_names}
        target_dirs = [d for d in all_dirs if d.name in targets]
        if missing := targets - {d.name for d in target_dirs}:
            print(f"Error: Types not found: {', '.join(missing)}")
            return 1

    sorted_dirs = topological_sort(target_dirs)
    print(f"Sorted build order: {[d.name for d in sorted_dirs]}")
    
    results = {d.name: build_type(d) for d in sorted_dirs}
    
    # Generate __init__ files
    vocab_dir = _get_project_root() / VOCAB_PACKAGE_NAME
    (vocab_dir / VOCAB_TYPES_SUBDIR / "__init__.py").write_text(
        AUTOGEN_WARNING + '"""\nCLAMS vocabulary type definitions.\n"""\n'
    )
    (vocab_dir / "__init__.py").write_text(
        InitFileGenerator.generate_top_level_init(vocab_dir / VOCAB_TYPES_SUBDIR, vocab_dir / "enums")
    )
    
    success = sum(results.values())
    errors = len(results) - success
    parts = [f"{success} built", f"{errors} errors"]
    if _warning_count:
        parts.append(f"{_warning_count} warnings")
    print(f"\nResults: {', '.join(parts)}")
    return 0 if all(results.values()) else 1


def _run_clean() -> int:
    print("Cleaning generated vocabulary files...")
    root = _get_project_root() / VOCAB_PACKAGE_NAME
    
    for d in (root / VOCAB_TYPES_SUBDIR).iterdir():
        if d.is_dir() and not d.name.startswith('_'):
            clean_rst_files(clean_type_classes(d))
            
    for f in [root / VOCAB_TYPES_SUBDIR / '__init__.py', root / '__init__.py']:
        smart_clean(f)

    print("\nClean complete!")
    return 0


def main():
    parser = argparse.ArgumentParser(description='CLAMS Vocabulary Builder')
    sub = parser.add_subparsers(dest='command', required=True)
    
    p_build = sub.add_parser('build', help='Build types')
    p_build.add_argument('types', nargs='*', help='Type names (e.g., Annotation)')
    
    sub.add_parser('clean', help='Clean generated files')
    
    args = parser.parse_args()
    if args.command == 'clean':
        return _run_clean()
    return _run_build(args.types)


if __name__ == '__main__':
    sys.exit(main())
