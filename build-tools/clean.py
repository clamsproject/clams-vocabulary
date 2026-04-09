"""
Clean build artifacts, caches, and generated codegen files.

Removes standard Python build outputs (dist, egg-info, pycache) and
generated vocabulary files (vX.py, __init__.py) under clams_vocabulary/.
For codegen files, untracked files are deleted and tracked-but-modified
files are restored to their git state.
"""
import argparse
import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
VOCAB_PKG = PROJECT_ROOT / "clams_vocabulary"

# Standard build artifact directories
CLEAN_DIRS = [
    "build", "dist", "*.egg-info",
    ".pytest_cache", ".pytype",
    "docs-test",
]

# Standard build artifact files
CLEAN_FILES = [
    "coverage.xml", ".coverage",
    ".type_vocab_index.json",
]

# Recursive glob patterns
CLEAN_GLOBS = [
    "**/__pycache__",
]


def _is_git_tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path)],
        capture_output=True, cwd=PROJECT_ROOT,
    )
    return result.returncode == 0


def _is_git_modified(path: Path) -> bool:
    result = subprocess.run(
        ["git", "diff", "--name-only", str(path)],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    return bool(result.stdout.strip())


def _git_restore(path: Path):
    subprocess.run(
        ["git", "checkout", "--", str(path)],
        cwd=PROJECT_ROOT,
    )


def _smart_clean(path: Path) -> bool:
    """Delete if untracked, restore from git if modified."""
    if not path.exists():
        return False
    if not _is_git_tracked(path):
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return True
    if _is_git_modified(path):
        _git_restore(path)
        return True
    return False


def clean_build_artifacts():
    """Remove standard Python build artifacts."""
    removed = []

    for pattern in CLEAN_DIRS:
        for p in PROJECT_ROOT.glob(pattern):
            if p.is_dir():
                shutil.rmtree(p)
                removed.append(p.relative_to(PROJECT_ROOT))

    for name in CLEAN_FILES:
        p = PROJECT_ROOT / name
        if p.exists():
            p.unlink()
            removed.append(p.relative_to(PROJECT_ROOT))

    for pattern in CLEAN_GLOBS:
        for p in PROJECT_ROOT.glob(pattern):
            if p.is_dir():
                shutil.rmtree(p)
                removed.append(p.relative_to(PROJECT_ROOT))

    return removed


def clean_codegen():
    """Clean generated vX.py and __init__.py files under types/."""
    removed = []
    types_dir = VOCAB_PKG / "types"

    for type_dir in sorted(types_dir.iterdir()):
        if not type_dir.is_dir() or type_dir.name.startswith("_"):
            continue
        for vfile in type_dir.glob("v*.py"):
            if vfile.stem[1:].isdigit() and _smart_clean(vfile):
                removed.append(vfile.relative_to(PROJECT_ROOT))
        init = type_dir / "__init__.py"
        if _smart_clean(init):
            removed.append(init.relative_to(PROJECT_ROOT))

    # Top-level generated inits
    for init in [types_dir / "__init__.py", VOCAB_PKG / "__init__.py"]:
        if _smart_clean(init):
            removed.append(init.relative_to(PROJECT_ROOT))

    # Generated documentation index
    doc_index = PROJECT_ROOT / "documentation" / "index.rst"
    if _smart_clean(doc_index):
        removed.append(doc_index.relative_to(PROJECT_ROOT))

    return removed


def main():
    parser = argparse.ArgumentParser(
        description="Clean build artifacts and generated codegen files.",
    )
    parser.add_argument(
        "--codegen-only", action="store_true",
        help="Only clean generated vX.py and __init__.py files",
    )
    args = parser.parse_args()

    if args.codegen_only:
        removed = clean_codegen()
    else:
        removed = clean_build_artifacts() + clean_codegen()

    if removed:
        print(f"Cleaned {len(removed)} items:")
        for item in sorted(removed):
            print(f"  {item}")
    else:
        print("Nothing to clean.")


if __name__ == "__main__":
    main()
