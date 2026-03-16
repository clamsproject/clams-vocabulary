"""
Build the clams-vocabulary package.

This script is equivalent to `make package` in the Makefile-based repos:
    1. Run codegen (generate versioned type snapshots from archetypes)
    2. python -m build (produces sdist + wheel in dist/)
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
        description="Build the clams-vocabulary package."
    )
    parser.add_argument(
        "--skip-codegen",
        action="store_true",
        help="Skip the codegen step "
             "(useful if snapshots are already up to date)."
    )
    args = parser.parse_args()

    project_root = SCRIPT_DIR.parent

    # Install dev + build dependencies
    print("--- Installing dependencies ---")
    run_command(
        [sys.executable, "-m", "pip",
         "install", "-e", ".[dev]", "build"],
        cwd=project_root,
    )

    # Codegen: archetypes → versioned vN.py snapshots
    if not args.skip_codegen:
        print("\n--- Codegen: generating versioned type snapshots ---")
        run_command(
            [sys.executable,
             str(SCRIPT_DIR / "generate_vocab_snapshot.py"),
             "build"],
            cwd=project_root,
        )

    # Build sdist + wheel
    print("\n--- Building sdist + wheel ---")
    run_command(
        [sys.executable, "-m", "build"],
        cwd=project_root,
    )

    print("\nBuild complete. Output in: dist/")


if __name__ == "__main__":
    main()
