"""
Build documentation for the clams-vocabulary project.

This script is equivalent to:
    1. pip install -e .[docs]
    2. sphinx-build -b html -a -E documentation <output-dir>
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


def build_docs_local(source_dir: Path, output_dir: Path,
                     local_build: bool = False):
    """
    Builds documentation for the provided source directory.

    :param source_dir: Path to the source directory containing the project.
    :param output_dir: Path to the output directory for built documentation.
    :param local_build: When True, additionally render a ``dev/`` hierarchy
        from the current working tree (handy for previewing unreleased
        archetype changes). CI publish builds leave this off so the
        published site doesn't carry a duplicate of the latest tag.
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
        "-D", f"local_build={'1' if local_build else '0'}",
    ]
    run_command(sphinx_command)

    print(f"\nDocumentation build complete. Output in: {output_dir}")
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Build documentation for the clams-vocabulary project."
    )
    parser.add_argument(
        "--build-ver",
        metavar="<version>",
        default=None,
        help="Accepted for CLI compatibility with other SDK repos. "
             "Ignored by this script (all versions are built in "
             "a single pass)."
    )
    parser.add_argument(
        "--output-dir",
        metavar="<path>",
        default="docs-test",
        help="The directory for documentation output "
             "(default: docs-test)."
    )
    parser.add_argument(
        "--local-build",
        action="store_true",
        help="Also emit a 'dev/' hierarchy rendered from the current "
             "working tree. Intended for local previews of unreleased "
             "archetype changes; off by default so CI publish builds "
             "don't duplicate the latest tag under a misleading URL."
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    build_docs_local(Path.cwd(), output_dir, local_build=args.local_build)


if __name__ == "__main__":
    main()
