import json
import re
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment

from .utils import extract_type_metadata


RST_ADMONITIONS = (
    'attention', 'caution', 'danger', 'error', 'hint',
    'important', 'note', 'tip', 'warning',
)


def rst_description(text: str) -> str:
    """
    Jinja2 filter: convert an HTML-flavored description string to RST.

    Translations applied (in order):

    1. ``<code>X</code>`` → ````X````
    2. ``<i>X</i>`` → ``*X*``
    3. ``<br>`` → newline (``<br><br>`` becomes a paragraph break)
    4. ``[type]…[/type]`` → ``.. type::`` admonition (for RST admonition types)
    """
    if not text:
        return ''
    # HTML inline tags → RST inline markup
    text = re.sub(r'<code>\s*(.*?)\s*</code>', r'``\1``', text)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text)
    # Line breaks → newlines
    text = text.replace('<br>', '\n')

    paragraphs = re.split(r'\n{2,}', text)
    parts = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Check for any RST admonition type
        admon_type = None
        for atype in RST_ADMONITIONS:
            if para.startswith(f'[{atype}]'):
                admon_type = atype
                break

        if admon_type:
            content = para[len(f'[{admon_type}]'):].strip()
            # Strip closing tag if present
            close_tag = f'[/{admon_type}]'
            if content.endswith(close_tag):
                content = content[:-len(close_tag)].strip()
            indented = '\n'.join(
                '   ' + line for line in content.split('\n')
            )
            parts.append(f'.. {admon_type}::\n\n{indented}')
        else:
            # Strip any stray closing tags
            for atype in RST_ADMONITIONS:
                para = para.replace(f'[/{atype}]', '')
            parts.append(para.strip())

    return '\n\n'.join(parts)


def truncate_desc(text: str, length: int = 100) -> str:
    """
    Jinja2 filter: truncate description to a max length.

    :param text: Description text (may contain RST markup)
    :param length: Maximum character length
    :returns: Truncated text with ellipsis if needed
    """
    if not text:
        return ''
    # Strip any RST/HTML markup for the synopsis
    clean = re.sub(r'</?(?:code|i|br)/?>', '', text)
    clean = clean.replace('``', '').replace('*', '')
    if len(clean) <= length:
        return clean
    return clean[:length].rsplit(' ', 1)[0] + ' ...'


def type_link(class_name: str) -> str:
    """
    Jinja2 filter: generate doc link from versioned class name.

    :param class_name: Class name like 'TimeFrame_v5'
    :returns: Link like '../../TimeFrame/v5/index'
    """
    if not class_name:
        return ''
    match = re.search(r'^(.+)_v(\d+)$', class_name)
    if match:
        name, version = match.groups()
        return f'`{name} (v{version}) <../../{name}/v{version}/index>`'
    return class_name


def generate_type_rst(
    type_dir: Path,
    version: int,
    output_dir: Path,
    template_env: Environment,
    included_in: List[str],
    previous_version: Optional[int] = None,
    is_latest: bool = False,
    latest_version: Optional[int] = None,
    latest_vocab_version: Optional[str] = None
):
    """
    Generate RST file for a single type version.

    :param type_dir: Path to type directory (e.g., types/time_frame)
    :param version: Version number (e.g., 1)
    :param output_dir: Base output directory
    :param template_env: Jinja2 environment
    :param included_in: List of vocab versions that include this type
    :param previous_version: Previous version number for linking
    :param is_latest: Whether this is the latest version of this type
    :param latest_version: Latest version number for this type
    :param latest_vocab_version: Latest vocabulary version string
    """
    metadata = extract_type_metadata(type_dir, version)
    if not metadata:
        return

    if previous_version and previous_version < version:
        metadata['previous_version'] = previous_version
    else:
        metadata['previous_version'] = None

    metadata['included_in'] = included_in
    metadata['display_name'] = (
        f"{metadata['shortname']} ({metadata['version']})"
    )

    if previous_version:
        metadata['previous_link'] = f"../v{previous_version}/index"
    else:
        metadata['previous_link'] = None

    if metadata['json_schema']:
        metadata['json_schema_str'] = json.dumps(
            metadata['json_schema'], indent=2
        )
    else:
        metadata['json_schema_str'] = '{}'

    metadata['is_latest'] = is_latest
    metadata['latest_version'] = latest_version
    metadata['latest_vocab_version'] = latest_vocab_version

    template = template_env.get_template('type.rst.j2')
    content = template.render(**metadata)

    type_version_dir = (
        output_dir / 'type' / metadata['shortname'] / metadata['version']
    )
    type_version_dir.mkdir(parents=True, exist_ok=True)

    output_file = type_version_dir / 'index.rst'
    output_file.write_text(content)
    print(f"  Generated type/{metadata['shortname']}/{metadata['version']}/"
          "index.rst")


def generate_type_json(type_dir: Path, version: int, output_dir: Path):
    """
    Generate index.json with JSON Schema for machine-readable consumption.

    :param type_dir: Path to type directory (e.g., types/annotation)
    :param version: Version number (e.g., 2)
    :param output_dir: Base output directory
    """
    metadata = extract_type_metadata(type_dir, version)
    if not metadata:
        return

    type_version_dir = (
        output_dir / 'type' / metadata['shortname'] / metadata['version']
    )
    type_version_dir.mkdir(parents=True, exist_ok=True)

    json_file = type_version_dir / 'index.json'
    with open(json_file, 'w') as f:
        json.dump(metadata['json_schema'], f, indent=2)

    print(f"  Generated type/{metadata['shortname']}/{metadata['version']}/"
          "index.json")
