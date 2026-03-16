# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import inspect
import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# -- Path setup ----------------------------------------------------------
# Add project root to sys.path so that autodoc can find clams_vocabulary
proj_root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(proj_root_dir.absolute()))
# Add current directory to sys.path so that local extension can be found
sys.path.append(os.path.abspath("."))
import clams_vocabulary  # test if importable after path setup


# -- Project information -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'clams-vocabulary'
author = 'Brandeis LLC'
copyright = f'{datetime.date.today().year}, {author}'

# Read metadata from pyproject.toml [project.urls]
try:
    with open(proj_root_dir / 'pyproject.toml', 'rb') as f:
        pyproject = tomllib.load(f)
    repository_url = pyproject['project']['urls']['source']
except FileNotFoundError:
    raise FileNotFoundError(
        f"pyproject.toml not found at {proj_root_dir / 'pyproject.toml'}"
    )
except KeyError as e:
    raise KeyError(
        f"Missing required configuration in pyproject.toml: "
        f"[project.urls] source must be set. Missing key: {e}"
    )

# Derived URLs
blob_base_url = f'{repository_url}/blob'

# Don't include version in documentation titles
# Set to None so linkcode_resolve knows to use 'main' branch
version = ''
release = ''

# -- General configuration -----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.linkcode',
    'm2r2',
    '_clams_vocab_docs_builder',  # Local extension for RST generation
]

templates_path = ['_templates']
exclude_patterns = ['_*']
source_suffix = ['.rst', '.md']

# -- Options for HTML output ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']  # Ensure _static is picked up
html_css_files = ['css/tables.css']
html_show_sourcelink = True

# Theme options for visual consistency with CLAMS branding
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "source_repository": repository_url,
    "source_branch": "main",
    "source_directory": "documentation/",

    # CLAMS brand colors
    "light_css_variables": {
        "color-brand-primary": "#008AFF",
        "color-brand-content": "#0085A1",
        "color-link": "#008AFF",
        "color-link-hover": "#0085A1",
    },
}


# -- CLAMS Vocabulary Documentation Settings -----------------------------
# Oldest version detection:
# - Type pages: v1 of each type is automatically marked as oldest version
#   (no previous version link shown)
# - Hierarchy pages: First vocabulary version (1.0.0) is marked as oldest
# Logic is implemented in _clams_vocab_docs_builder/generator.py


# -- Options for linkcode extension --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html

def linkcode_resolve(domain, info):
    if domain != 'py' or not info.get('module'):
        return None

    try:
        # Find the Python object
        obj = sys.modules.get(info['module'])
        if obj is None:
            return None
        for part in info['fullname'].split('.'):
            obj = getattr(obj, part)

        # Get the source file and line numbers
        unwrapped_obj = inspect.unwrap(obj)
        filename = inspect.getsourcefile(unwrapped_obj)
        if not filename:
            return None

        lines, start_lineno = inspect.getsourcelines(unwrapped_obj)
        end_lineno = start_lineno + len(lines) - 1

        # Get git ref (tag or branch)
        # GITHUB_REF_NAME is set by GitHub Actions
        git_ref = os.environ.get("GITHUB_REF_NAME") or version
        if not git_ref or 'dev' in git_ref:
            git_ref = 'main'

        # Get file path relative to repository root
        repo_root = Path(__file__).parent.parent
        rel_path = Path(filename).relative_to(repo_root)

        return (
            f"{blob_base_url}/{git_ref}/{rel_path}"
            f"#L{start_lineno}-L{end_lineno}"
        )

    except Exception:
        # Don't fail the entire build if one link fails
        return None
