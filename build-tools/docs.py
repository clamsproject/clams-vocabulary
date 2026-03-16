"""
Build documentation for the clams-vocabulary project.

This script is equivalent to:
    1. pip install -e .[docs]
    2. sphinx-build -b html -a -E documentation <output-dir>

TODO: when adding a "What's New" section, fetch release
notes from the merged release PR body via `gh pr list`
instead of parsing CHANGELOG.md. See
mmif-python/documentation/conf.py::generate_whatsnew_rst
for implementation reference.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None, check=True):
    """Helper to run a shell command."""
    print(f"Running: {' '.join(str(c) for c in command)}")
    result = subprocess.run(command, cwd=cwd)
    if check and result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result


def build_docs_local(source_dir: Path, output_dir: Path):
    """
    Builds documentation for the provided source directory.

    :param source_dir: Path to the source directory containing the project.
    :param output_dir: Path to the output directory for built documentation.
    """
    print("--- Building clams-vocabulary documentation ---")

    # 1. Install package with docs dependencies in editable mode.
    print("\n--- Step 1: Installing package with docs dependencies ---")
    try:
        run_command([sys.executable, "-m", "pip", "install", "-e", ".[docs]"], cwd=source_dir)
    except SystemExit:
        print("Warning: 'pip install -e .[docs]' failed. This might be due to an externally managed environment.")
        print("Attempting to proceed with documentation build assuming dependencies are met...")

    # 2. Build the documentation using Sphinx.
    print("\n--- Step 2: Building Sphinx documentation ---")
    docs_source_dir = source_dir / "documentation"

    if not docs_source_dir.exists():
        print(f"Error: Documentation source directory not found at {docs_source_dir}")
        sys.exit(1)

    sphinx_command = [
        sys.executable, "-m", "sphinx.cmd.build",
        str(docs_source_dir),
        str(output_dir),
        "-b", "html",  # build html
        "-a",          # write all files (rebuild everything)
        "-E",          # don't use a saved environment, reread all files
    ]
    run_command(sphinx_command)

    print(f"\nDocumentation build complete. Output in: {output_dir}")
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Build documentation for the clams-vocabulary project."
    )
    parser.add_argument(
        "--output-dir",
        metavar="<path>",
        default="docs-test",
        help="The directory for documentation output (default: docs-test)."
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    build_docs_local(Path.cwd(), output_dir)


if __name__ == "__main__":
    main()
