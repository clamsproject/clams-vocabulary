import re
from pathlib import Path
from typing import Dict, List, Optional

from jinja2 import Environment

from .utils import extract_type_metadata


def build_tree(latest_types: Dict[str, int], types_dir: Path) -> str:
    """
    Build inheritance tree with box-drawing characters.

    :param latest_types: Dict mapping type names to version numbers
    :param types_dir: Path to types directory
    :returns: Formatted tree string. Each line: "└── TypeName (v1) | props"
    """
    type_info = {}

    for type_name_snake, version in latest_types.items():
        type_dir = types_dir / type_name_snake
        metadata = extract_type_metadata(type_dir, version)

        pascal_name = ''.join(word.capitalize()
                            for word in type_name_snake.split('_'))

        parent_class = metadata.get('parent_class')
        parent_name = None
        if parent_class and parent_class != 'VocabType':
            parent_name = re.sub(r'_v\d+$', '', parent_class)

        own_properties = [
            f['name'] for f in metadata.get('fields', [])
            if not f.get('inherited_from')
        ]

        type_info[type_name_snake] = {
            'pascal': pascal_name,
            'version': version,
            'parent': parent_name,
            'properties': own_properties
        }

    children = {}
    for snake_name, info in type_info.items():
        parent = info['parent']
        if parent:
            parent_snake = re.sub(r'(?<!^)(?=[A-Z])', '_', parent).lower()
            if parent_snake not in children:
                children[parent_snake] = []
            children[parent_snake].append(snake_name)

    root = 'thing'

    def render_node(snake_name: str, prefix: str = '',
                   is_last: bool = True) -> List[str]:
        if snake_name not in type_info:
            return []

        info = type_info[snake_name]
        lines = []

        connector = '└── ' if is_last else '├── '
        node_label = f"{info['pascal']} (v{info['version']})"
        props = ', '.join(info['properties']) if info['properties'] else ''
        lines.append(f"{prefix}{connector}{node_label} | {props}")

        node_children = children.get(snake_name, [])
        node_children.sort()

        for i, child in enumerate(node_children):
            is_child_last = (i == len(node_children) - 1)
            child_prefix = prefix + ('    ' if is_last else '│   ')
            lines.extend(render_node(child, child_prefix, is_child_last))

        return lines

    tree_lines = render_node(root)
    return '\n'.join(tree_lines)


def generate_hierarchy_rst(
    latest_types: Dict[str, int],
    output_dir: Path,
    vocab_version: str,
    template_env: Environment,
    types_dir: Path,
    is_latest: bool = False,
    previous_vocab: Optional[str] = None,
    latest_vocab: Optional[str] = None
):
    """
    Generate hierarchy RST showing type inheritance tree.

    :param latest_types: Dict mapping type names to version numbers
    :param output_dir: Base output directory (creates X.Y.Z/index.rst)
    :param vocab_version: Version string (e.g., '1.0.0')
    :param template_env: Jinja2 environment
    :param types_dir: Path to types directory
    :param is_latest: Whether this is the latest vocabulary version
    :param previous_vocab: Previous vocabulary version for linking
    :param latest_vocab: Latest vocab version for non-latest pages
    """
    tree = build_tree(latest_types, types_dir)

    template = template_env.get_template('hierarchy.rst.j2')
    content = template.render(
        vocab_version=vocab_version,
        tree=tree,
        is_latest=is_latest,
        previous_vocab=previous_vocab,
        latest_vocab=latest_vocab
    )

    vocab_dir = output_dir / vocab_version
    vocab_dir.mkdir(parents=True, exist_ok=True)

    output_file = vocab_dir / 'index.rst'
    output_file.write_text(content)
    print(f"  Generated {vocab_version}/index.rst")
