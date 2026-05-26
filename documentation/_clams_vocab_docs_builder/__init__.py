import importlib
import inspect
import re
from pathlib import Path
from typing import Set

from docutils import nodes
from docutils.parsers.rst import Directive
from jinja2 import Environment, FileSystemLoader

from . import utils
from .utils import extract_type_metadata
from .type_generator import (
    generate_type_rst, generate_type_json, rst_description, type_link,
    truncate_desc
)
from .hierarchy_generator import generate_hierarchy_rst
from .index_generator import generate_index_rst


class TreeNode(Directive):
    """
    Directive to render an inheritance tree as HTML.

    Usage:
        .. inheritance-tree::

           └── Thing (v1) | id
               ├── Alignment (v1) | source, target
               └── Annotation (v2) | document, label

    Format: Each line contains tree chars, type name (version), pipe,
    comma-separated property names.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        """Parse tree content and generate HTML with links."""
        tree_data = []
        for line in self.content:
            if not line.strip():
                continue

            parts = line.split('|')
            display_part = parts[0].rstrip()
            properties = parts[1].strip() if len(parts) > 1 else ''

            clean_line = display_part.replace('└── ', '').replace(
                '├── ', '').replace('│   ', '    ')
            leading_spaces = len(clean_line) - len(clean_line.lstrip(' '))
            level = leading_spaces // 4

            match = re.match(
                r'^[\s└├│─]*([A-Z][A-Za-z]+)\s+\(v(\d+)\)',
                display_part
            )

            if match:
                tree_data.append({
                    'level': level,
                    'name': match.group(1),
                    'version': match.group(2),
                    'properties': properties
                })

        def build_table(items, start_idx=0, parent_level=-1):
            html_parts = ['<table class="h">']

            i = start_idx
            while i < len(items):
                item = items[i]

                if item['level'] <= parent_level:
                    break

                if item['level'] == parent_level + 1:
                    html_parts.append('<tr>')
                    html_parts.append('<td class="tc" colspan="4">')
                    html_parts.append(
                        f'<a href="../type/{item["name"]}/v{item["version"]}'
                        f'/index.html">{item["name"]} '
                        f'<span class="version">(v{item["version"]})</span>'
                        f'</a>'
                    )
                    if item.get('properties'):
                        html_parts.append(
                            f': <span class="properties">'
                            f'{item["properties"]}</span>'
                        )
                    html_parts.append('</td>')
                    html_parts.append('</tr>')

                    if (i + 1 < len(items)
                            and items[i + 1]['level'] > item['level']):
                        html_parts.append('<tr>')
                        html_parts.append('<td class="space"></td>')
                        html_parts.append('<td class="bar"></td>')
                        html_parts.append('<td class="space"></td>')
                        html_parts.append('<td>')
                        child_html, next_i = build_table(
                            items, i + 1, item['level']
                        )
                        html_parts.append(child_html)
                        html_parts.append('</td>')
                        html_parts.append('</tr>')
                        i = next_i
                        continue

                i += 1

            html_parts.append('</table>')
            return ''.join(html_parts), i

        table_html, _ = build_table(tree_data)
        return [nodes.raw('', table_html, format='html')]


def generate_all_rst(
    repo_dir: Path,
    types_dir: Path,
    output_dir: Path,
    templates_dir: Path,
    rebuild_index: bool = False,
    local_build: bool = False,
):
    """
    Main entry point for RST generation.

    :param repo_dir: Project root directory
    :param types_dir: Directory containing vocabulary types
    :param output_dir: Directory for generated RST files
    :param templates_dir: Directory containing Jinja2 templates
    :param rebuild_index: Force rebuild of type-to-vocab index cache
    :param local_build: When True, additionally render a ``dev/``
        hierarchy from the current working tree and use it as the
        landing page's active version (for local previews of unreleased
        archetype changes). When False (the CI publish default), only
        per-tag hierarchies are rendered and the landing page points at
        the most recent tagged vocab; the ``dev/`` fallback is still
        emitted when no tags exist at all (pre-first-release setup).
    """
    print("Generating RST documentation from Pydantic vocabulary types")
    print("=" * 70)

    output_dir.mkdir(parents=True, exist_ok=True)

    template_env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template_env.filters['rst_description'] = rst_description
    template_env.filters['type_link'] = type_link
    template_env.filters['truncate_desc'] = truncate_desc

    type_versions = utils.discover_type_versions(types_dir)
    latest_types = utils.get_latest_types(types_dir)
    print(f"Found {len(type_versions)} types")

    type_to_vocab = utils.build_type_to_vocab_index(repo_dir, rebuild_index)

    vocab_versions = utils.get_vocab_versions(repo_dir)
    latest_vocab_version = vocab_versions[-1] if vocab_versions else None

    # Discover all importable types for link validation
    available_types: Set[str] = set()
    for type_name, versions in sorted(type_versions.items()):
        for version in versions:
            try:
                module = importlib.import_module(
                    f'clams_vocabulary.types.{type_name}.v{version}'
                )
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (name.endswith(f'_v{version}')
                            and obj.__module__ == module.__name__):
                        available_types.add(name)
                        break
            except ImportError:
                pass

    # Generate type pages
    print("\nGenerating type RST files...")
    generated_count = 0
    skipped_count = 0

    for type_name, versions in sorted(type_versions.items()):
        type_dir = types_dir / type_name

        for version in versions:
            metadata = extract_type_metadata(type_dir, version)
            if not metadata:
                skipped_count += 1
                continue

            prev_version = None
            if version > 1 and (version - 1) in versions:
                prev_class_name = f"{metadata['shortname']}_v{version - 1}"
                if prev_class_name in available_types:
                    prev_version = version - 1

            class_name = None
            try:
                module = importlib.import_module(
                    f'clams_vocabulary.types.{type_name}.v{version}'
                )
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (name.endswith(f'_v{version}')
                            and obj.__module__ == module.__name__):
                        class_name = name
                        break
            except ImportError as e:
                print(f"  WARNING: Could not import {type_name}.v{version}: {e}")
                skipped_count += 1
                continue

            included_in = type_to_vocab.get(class_name, [])
            latest_ver = latest_types.get(type_name)
            is_latest_version = (latest_ver == version)

            try:
                generate_type_rst(
                    type_dir, version, output_dir,
                    template_env, included_in, prev_version,
                    is_latest=is_latest_version,
                    latest_version=latest_ver,
                    latest_vocab_version=latest_vocab_version
                )
                generate_type_json(type_dir, version, output_dir)
                generated_count += 1
            except Exception as e:
                print(f"  ERROR generating {type_name}/v{version}: {e}")
                skipped_count += 1

    # Generate hierarchy pages
    print("\nGenerating hierarchies...")
    if vocab_versions:
        for i, version in enumerate(vocab_versions):
            types_at_version = utils.get_latest_types_at_tag(repo_dir, version)
            if not types_at_version:
                print(f"  Skipping {version} (no types found)")
                continue

            prev_vocab = vocab_versions[i - 1] if i > 0 else None
            is_latest_vocab = (version == latest_vocab_version)

            generate_hierarchy_rst(
                types_at_version, output_dir, version,
                template_env, types_dir,
                is_latest=is_latest_vocab,
                previous_vocab=prev_vocab,
                latest_vocab=latest_vocab_version
            )
            generated_count += 1

    # Optionally render a "dev" hierarchy from the current working tree.
    # Enabled by --local-build for previewing unreleased archetype work,
    # or as a fallback when no tags exist yet (pre-first-release setup so
    # the landing page has something to link at).
    render_dev = local_build or not latest_vocab_version
    dev_dir = output_dir / 'dev'
    if render_dev and latest_types:
        prev_vocab = latest_vocab_version  # None when no tags exist
        generate_hierarchy_rst(
            latest_types, output_dir, 'dev',
            template_env, types_dir,
            is_latest=True,
            previous_vocab=prev_vocab,
            latest_vocab='dev'
        )
        generated_count += 1
        index_target = 'dev'
    else:
        # Sphinx renders any RST it finds in srcdir; remove a stale
        # dev/ left by an earlier --local-build (or pre-fix) run so it
        # doesn't bleed into the output.
        if dev_dir.exists():
            import shutil as _shutil
            _shutil.rmtree(dev_dir)
        index_target = latest_vocab_version

    # Generate index page
    if index_target:
        print("\nGenerating index.rst...")
        generate_index_rst(repo_dir, output_dir, template_env, index_target)

    print("\n" + "=" * 70)
    print("RST generation complete!")
    print(f"  Generated: {generated_count} files")
    if skipped_count > 0:
        print(f"  Skipped: {skipped_count} files")
        print()
        print("NOTE: If types could not be imported, run scripts/build.py")
        print("      to build versioned type files first.")


def _generate_docs_hook(app):
    """Sphinx hook to generate RST documentation before building."""
    try:
        doc_dir = Path(app.srcdir)
        proj_root = doc_dir.parent
        types_dir = proj_root / 'clams_vocabulary' / 'types'
        templates_dir = doc_dir / '_templates'

        generate_all_rst(
            repo_dir=proj_root,
            types_dir=types_dir,
            output_dir=doc_dir,
            templates_dir=templates_dir,
            local_build=bool(int(app.config.local_build)),
        )
    except Exception as e:
        print(f"WARNING: RST generation failed: {e}")
        print("         Documentation will be built without type pages.")


def setup(app):
    """Sphinx extension setup."""
    app.add_directive('inheritance-tree', TreeNode)
    app.add_css_file('css/tree.css')
    # Off by default so CI publish builds don't emit a "dev/" copy of the
    # latest tag. Local previews set this via `docs.py --local-build`,
    # which appends `-D local_build=1` to the sphinx invocation.
    app.add_config_value('local_build', '0', 'env', [str])

    try:
        app.connect('builder-inited', _generate_docs_hook)
    except Exception as e:
        print(f"WARNING: Error setting up dynamic content generation: {e}")
        print("         Continuing with static documentation only.")

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
