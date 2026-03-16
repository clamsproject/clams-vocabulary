import sys
from pathlib import Path

from jinja2 import Environment

from .utils import find_tag_for_version

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def generate_index_rst(
    repo_dir: Path,
    output_dir: Path,
    template_env: Environment,
    latest_vocab_version: str
):
    """
    Generate index.rst from template.

    :param repo_dir: Repository root directory
    :param output_dir: Documentation output directory
    :param template_env: Jinja2 environment
    :param latest_vocab_version: Latest vocabulary version string
    """
    # Read source repository URL from pyproject.toml
    try:
        pyproject_path = repo_dir / 'pyproject.toml'
        with open(pyproject_path, 'rb') as f:
            pyproject = tomllib.load(f)
        repository_url = pyproject['project']['urls']['source']
    except FileNotFoundError:
        raise FileNotFoundError(
            f"pyproject.toml not found at {pyproject_path}"
        )
    except KeyError as e:
        raise KeyError(
            f"Missing required configuration in pyproject.toml: "
            f"[project.urls] source must be set. Missing key: {e}"
        )

    # rst files manually set to show up early in the list
    rst_files = ['overview', 'usage']
    # Find all RST files in documentation root (excluding index.rst)
    for rst_file in output_dir.glob('*.rst'):
        rst_file = rst_file.stem
        if rst_file != 'index' and rst_file not in rst_files:
            rst_files.append(rst_file)

    git_tag = find_tag_for_version(repo_dir, latest_vocab_version)
    changelog_url = (
        f"{repository_url}/blob/{git_tag}/CHANGELOG.md"
        if git_tag
        else f"{repository_url}/blob/main/CHANGELOG.md"
    )

    template = template_env.get_template('index.rst.j2')
    content = template.render(
        latest_vocab_version=latest_vocab_version,
        getting_started_pages=rst_files,
        repository_url=repository_url,
        changelog_url=changelog_url
    )

    index_file = output_dir / 'index.rst'
    index_file.write_text(content)
    print(f"  Generated index.rst with version {latest_vocab_version}")
