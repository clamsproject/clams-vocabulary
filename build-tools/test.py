"""
Run tests for the clams-vocabulary package.

This script is equivalent to `make test` in the Makefile-based repos:
    1. pip install -e ".[test]"
    2. python -m pytest --cov=clams_vocabulary --cov-report=xml
"""
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_command(command, cwd=None, check=True):
    """Helper to run a shell command."""
    print(f"Running: {' '.join(str(c) for c in command)}")
    result = subprocess.run(command, cwd=cwd)
    if check and result.returncode != 0:
        print(
            f"Error: Command failed with exit code "
            f"{result.returncode}"
        )
        sys.exit(result.returncode)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run tests for the clams-vocabulary package."
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip pip install step "
             "(useful if already installed)."
    )
    args = parser.parse_args()

    project_root = SCRIPT_DIR.parent

    # Install package with test dependencies
    if not args.skip_install:
        print("--- Installing package with test dependencies ---")
        run_command(
            [sys.executable, "-m", "pip",
             "install", "-e", ".[test]"],
            cwd=project_root,
        )

    # Run pytest with coverage
    print("\n--- Running pytest ---")
    run_command(
        [sys.executable, "-m", "pytest",
         "--cov=clams_vocabulary", "--cov-report=xml"],
        cwd=project_root,
    )

    print("\nAll tests passed.")


if __name__ == "__main__":
    main()
