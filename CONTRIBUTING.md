# Contributing to CLAMS Vocabulary

This guide provides detailed instructions for contributors to the CLAMS vocabulary repository.

## Background: Vocabulary Migration

Prior to 1.1.1 (until version 1.1.0), the CLAMS vocabulary was part of the [MMIF specification](https://mmif.clams.ai), shared the same version numbers, and was defined in a single YAML file (`clams.vocabulary.yaml` in the [mmif](https://github.com/clamsproject/mmif) repo). In that format, each type had separate "metadata" and "properties" sections.

As of 1.1.1, the vocabulary is an independent Python package with its own versioning. Type definitions are now Pydantic models, and the old metadata/properties distinction is removed — all attributes are unified as regular fields on each type class. This is also a semantic decoupling: the vocabulary now defines type structure and semantics without reference to MMIF serialization details. How fields are distributed between `view.metadata.contains` and `annotation.properties` at serialization time is an MMIF spec and/or serialization SDK concern, not a vocabulary concern.

See [mmif#230](https://github.com/clamsproject/mmif/issues/230) for the underlying discussion.

## Before Submitting a Pull Request

Ensure the following checks pass:

0. Make your changes to type archetypes (`archetype.py` files) ([details](#develop-anchor))
1. Commit all archetype changes and new `vX.py` files
2. `python build-tools/generate_vocab_snapshot.py build` completes without errors ([detail](#build-anchor))
3. `python build-tools/docs.py` completes without errors, manual inspection of generated HTML
4. `python -m pytest tests/` shows no failures
5. Submit a pull request with your changes

## Coding Conventions

### Naming Conventions

For detailed naming conventions (type names, field names, directory names, enums), see [documentation/naming_conventions.rst](documentation/naming_conventions.rst).

### Shortname Auto-Inference

The `shortname` ClassVar is inferred automatically from the class name by the metaclass.
The metaclass strips version suffixes (e.g., `TimeFrame_v6` → `TimeFrame`). Do not hardcode `shortname` in archetype files.

### Class Documentation

**Do not** use Python docstrings in type classes. The `description` ClassVar serves as the single source of documentation to prevent duplication and ensure consistency with JSON schema generation.

```python
# CORRECT - No docstring
class TimeFrame_v5(Interval_v5):
    uri: ClassVar[str] = "http://mmif.clams.ai/vocabulary/TimeFrame/v5"
    version: ClassVar[str] = "v5"
    description: ClassVar[str] = "A timeframe in a video, such as a shot or a scene."

# INCORRECT - Don't add docstrings
class TimeFrame_v5(Interval_v5):
    """A timeframe in a video."""  # DON'T DO THIS!
    description: ClassVar[str] = "A timeframe in a video, such as a shot or a scene."
```

### Writing Formatted Descriptions

The `description` ClassVar and `Field(description=...)` values support a mini-HTML markup that gets converted to RST during documentation builds. Use this markup to add structure and emphasis to your descriptions.

#### Supported Markup

| Markup | Purpose | Rendered As |
|--------|---------|-------------|
| `<code>X</code>` | Inline code reference | `X` (monospace) |
| `<i>X</i>` | Italic/emphasis | *X* |
| `<br><br>` | Paragraph break | New paragraph |
| `[note]...[/note]` | Informational callout | RST note admonition |

#### Admonition Types

The documentation builder recognizes all standard RST admonition types. Use `[type]...[/type]` format:

| Type | Use Case |
|------|----------|
| `note` | General informational callout |
| `warning` | Potential issues or breaking changes |
| `tip` | Helpful suggestions |
| `important` | Critical information |

Other supported types: `hint`, `caution`, `attention`, `danger`, `error`

See the [Furo admonitions reference](https://pradyunsg.me/furo/reference/admonitions/) for how each type renders visually.

> [!WARNING]
> RST is very indentation-sensitive. When writing multi-line description strings in Python, be careful that implicit string concatenation does not introduce unintended leading whitespace. RST directives (like admonitions) require exact indentation to be parsed correctly. Use parenthesized string literals with no leading spaces in continuation lines.

#### Example

```python
# CORRECT — In archetype.py
class MyType(Annotation):
    description: ClassVar[str] = (
        "A map from label values to their scores. "
        "<br><br> "
        "[note] Values are normalized between 0 and 1. [/note]"
    )

    label: Optional[str] = Field(
        None,
        description="The <code>label</code> assigned by the classifier."
    )

# INCORRECT — triple-quoted string adds leading whitespace
class MyType(Annotation):
    description: ClassVar[str] = """A map from label values to their scores.

        [note] This note will be broken by leading spaces. [/note]"""
```

#### Implementation Details

The `rst_description` Jinja2 filter in `documentation/_clams_vocab_docs_builder/type_generator.py` performs the markup conversion at Sphinx build time:

1. `<code>X</code>` → ``` ``X`` ``` (RST inline code)
2. `<i>X</i>` → `*X*` (RST emphasis)
3. `<br>` → newline
4. `[type]...[/type]` → `.. type::` (RST admonition block)

#### Legacy YAML Markup Translation

The original CLAMS Vocabulary was defined in YAML files that used similar markup. 
During migration to Python archetypes, we preserved the original formatting as much as possible, but some adjustments were necessary to fit the new conventions and RST requirements.

| YAML Input | Python Output | Rationale |
|------------|---------------|-----------|
| `[Note]` | `[note]` | Lowercase to match RST admonition name |
| `[Optional]` | `<i>Optional</i>` | Not a callout; render as italic text |
| `[note]...` | `[note]...[/note]` | Explicit closing tag for boundary detection |

**Errata:** Known typos in the upstream YAML (which cannot be fixed in git history) are corrected during extraction. Currently, the only known erratum is an unclosed `<code>` tag in Annotation v6: `<code>TimeFrame<code>` → `<code>TimeFrame</code>`.

### ClassVar Requirements for Archetypes

> [!IMPORTANT]
> When creating new `archetype.py` files, you **must** use `ClassVar` type hints for class-level metadata fields. This is a Pydantic v2 requirement to distinguish class metadata from instance fields.

```python
# CORRECT - archetype.py with ClassVar
from typing import ClassVar, Optional
from pydantic import Field
from clams_vocabulary.types.region.archetype import Region

class Interval(Region):
    description: ClassVar[str] = (
        "An annotation over an interval of linear primary data, either a text, "
        "a video or audio stream."
    )

    start: Optional[int] = Field(None, description="The starting offset...")  # start is not class-level metadata, but instance variable, hence no ClassVar

# INCORRECT - Missing ClassVar
class Interval(Region):
    description = "An annotation over an interval..."  # ❌ Missing ClassVar annotation
```

**Why ClassVar is required:**
- Without `ClassVar`, Pydantic treats variables as instance fields
- This causes validation errors and incorrect serialization behavior
- `ClassVar` explicitly marks these as class-level metadata that Pydantic should ignore for instance validation

> [!NOTE]
> The build script automatically adds `uri`, `version` and `shortname` ClassVars when generating versioned files from archetypes. So you don't need to manually define those.

### __init__.py Auto-Generation

All `__init__.py` files in `type` directory and its subdirectories for each type definition are **AUTO-GENERATED** at build time:

- Do not manually edit these files in the source tree
- The build script will generate them by scanning version files

### Type Dependency (Imports in Archetypes)

When editing `archetype.py`, contributors must choose how to use dependencies (parent classes or enums). This choice determines how the build system handles version updates.

#### "Follow Latest" (Recommended)

Import the **Archetype** of the dependency.

```python
from clams_vocabulary.enums.time_unit.archetype import TimeUnit
```

- The build system interprets this as "I want to use the latest version of this dependency."
- If `TimeUnit` is updated (generating `v2`), the build system will automatically generate a new version of your type (e.g., `TimeFrame_v7`) that imports `TimeUnit_v2`.
- Recommended for most standard types that should evolve with the ecosystem.

#### "Pin Version" (Advanced)

Import a **Specific Version** of the dependency.

```python
from clams_vocabulary.enums.time_unit.v2 import TimeUnit_v2 as TimeUnit
```

- The build system interprets this as "I strictly require Version 2 of this dependency."
- If `TimeUnit` is updated to `v3`, the build system will **not** update your type. Your type will continue to use `v2`.
- Useful for legacy types or types with strict semantic constraints that are incompatible with newer vocabulary versions.

This means when you choose to "Pin Version,", you first need to ensure that the specific version you are importing exists, not as the archetype. Technically, this means you need to git-commit and build the dependency type first (doesn't need to release a new vocab version at this point), before you can pin to it in your type.

<a id="develop-anchor"></a>
## Developing Types

### Adding a New Type

1. **Create the archetype**: Pick the closest existing type's `archetype.py` as a starting point, copy it into a new directory under `clams_vocabulary/types/`, and modify it:
   ```bash
   mkdir clams_vocabulary/types/my_new_type
   cp clams_vocabulary/types/time_frame/archetype.py clams_vocabulary/types/my_new_type/
   ```
   Then edit `clams_vocabulary/types/my_new_type/archetype.py`:
   - Update the parent class import and class inheritance
   - Set the `description` ClassVar (do not set `shortname`, `uri`, or `version` — these are auto-generated)
   - Define property fields with Pydantic `Field` definitions

2. **Verify the archetype** before building:
   ```bash
   python build-tools/verify_archetypes.py -v my_new_type
   ```

3. **Build to generate v1**:
   ```bash
   python build-tools/generate_vocab_snapshot.py build my_new_type
   ```
   The build script will:
   - Generate the initial version file (`v1.py`)
   - Update all `__init__.py` files (both the type's own and the top-level package `__init__.py` which populates `AnnotationTypes`/`DocumentTypes` namespaces and `URI_TO_TYPE` mappings)

### Updating an Existing Type

1. **Edit the archetype**: Modify `clams_vocabulary/types/type_name/archetype.py` with your desired changes

2. **Build with automatic change detection**:
   ```bash
   python build-tools/generate_vocab_snapshot.py build type_name
   ```
   The build system uses git to detect uncommitted changes. If changes are found, it automatically generates a new version (e.g., v6 → v7).

3. **Verify**: Old versions remain frozen and unchanged. Only the new version reflects your changes.

**Note**: If the archetype has no uncommitted changes in git, the build will skip version generation.

### Updating Property Names

Property names can be updated by modifying the archetype and rebuilding the vocabulary.

- Adding a property: add the new field to the `archetype.py` and run the build script. 
   - Should trigger a minor version bump at the repository level.
- Removing a property: remove the field from the `archetype.py` and run the build script. 
   - Should trigger a major version bump at the repository level (since it's a breaking change).
- Renaming a property:
    1. Rename the field in `archetype.py`.
    2. Add the old property name to the alias set for that type in `clams_vocabulary/prop_aliases.py`.
    - Should trigger a minor version bump at the repository level, as long as the old name is still supported as an alias. If you remove the old name from the alias set in a future version, that would be a major version bump.

Example entry in `prop_aliases.py`:
```python
'Span': {'text': {'word', 'text'}}  # 'word' is an alias for the canonical 'text'
```

<a id="build-anchor"></a>
## Building

### Standard Build Tasks

1. `python build-tools/generate_vocab_snapshot.py build [TypeName ...]` — generates Python artifacts (`vX.py`, `__init__.py`) into `clams_vocabulary/`
2. `python build-tools/docs.py [--output-dir <path>]` — generates RST/JSON into `documentation/` and builds HTML into `docs-test/` (or specified output dir)

### Documentation Artifacts

The documentation build process automatically generates reStructuredText (RST) files and JSON schemas for all vocabulary types.
These files are **not version controlled** and are ignored by git via `documentation/.gitignore`.

- RST files: `documentation/<TypeName>/v<Version>/index.rst`
- JSON schemas: `documentation/<TypeName>/v<Version>/index.json`
- Hierarchy diagrams: `documentation/hierarchy*.rst`

> [!WARNING]
> **Do not** force add these files to git. They should only exist as transient build artifacts.
> If the documentation generation process is updated in the future to produce additional file types or locations, ensure `documentation/.gitignore` is updated accordingly to keep the repository clean.


### HTML Artifacts

HTML documentation is built by Sphinx, configured in `documentation/conf.py`. You can invoke Sphinx directly (using `sphinx-xxx` commands), but it's recommended to use the `build-tools/docs.py` wrapper for convenience and consistency.

> [!NOTE]
> Per [clamsproject.github.io#11](https://github.com/clamsproject/clamsproject.github.io/issues/11), running `docs.py` and publishing to the project website will be automated via CI in the near future.

## Testing Your Changes

### Running Tests

Always use `python -m pytest` to run tests (not bare `pytest`), to ensure the correct Python environment and `sys.path`:

```bash
python -m pytest tests/
```

### Test Suite Organization

- `test_base.py` - Unit tests for `clams_vocabulary.base` module (URI parsing, prefix generation, equality, hashing, static utilities). Runs without build artifacts.
- `test_types.py` - Build contract tests validating generated type modules (registry consistency, ClassVar presence, namespace population, round-trip resolution). Automatically skipped if build artifacts are not available.

## Release and Maintenance

> [!WARNING]
> General contributors should not create git tags or perform releases. Only maintainers should do this, following the process outlined below.

### Git Tagging Convention

This repository follows the CLAMS project tagging convention:

- Version Pattern: Use Semantic Versioning (`x.y.z`) for all releases
  - Major version (x): Breaking changes (deletion and change)
  - Minor version (y): New features, backward compatible (addition)
  - Patch version (z): Bug fixes, backward compatible (fixes)
- Tag Format: Use plain version numbers **without prefix**
  - Correct: `1.2.0`, `1.3.0`, `2.0.0`
  - Incorrect: `v1.2.0`, `vocab-1.2.0`
- This convention is consistent with other CLAMS project infrastructure codebases

> [!NOTE]
> Legacy vocabulary versions (1.0.0 through 1.1.0, migrated from YAML-era) use `mmif-x.y.z` tags (e.g., `mmif-1.0.0`). These tags exist in git history for historical documentation generation but were never published to PyPI. New releases must use plain version numbers.
>
> The documentation builder (`_clams_vocab_docs_builder/utils.py:find_tag_for_version`) resolves version numbers to git tags by regex-searching all tags for the version string. This means it transparently handles both legacy `mmif-x.y.z` tags and plain `x.y.z` tags — no special-casing is needed when adding new releases.

### Release Process (Vocab 1.X)

> [!IMPORTANT]
> All `build-tools/` scripts must be run from the project root directory. Commands like `python -m build`, `pip install`, and `pytest` also expect the project root as CWD.

1. Build package: `python build-tools/build.py` (runs codegen + sdist)
2. Run tests: `python build-tools/test.py`
3. Verify documentation locally (optional): `python build-tools/docs.py --output-dir docs-test`
4. Commit, tag the release, and push: `git tag 1.3.0 && git push origin main && git push origin 1.3.0`
5. Tag push triggers the `publish.yml` workflow which uploads to PyPI, generates CHANGELOG, and publishes docs

### URI Prefix Change Workflow

The vocabulary URIs are configured in `pyproject.toml` under `[project.urls]`:
- `type_prefix`: Full URL prefix for type URIs (e.g., `https://clams.ai/vocabulary/type`)
- `enum_prefix`: (currently not used) Full URL prefix for enum URIs (e.g., `https://clams.ai/vocabulary/enum`)

These are used by `generate_vocab_snapshot.py` to construct the `uri` ClassVar in generated `vX.py` files (e.g., `type_prefix + "/Annotation/v2"`). The Sphinx documentation builder then reads `uri` from the generated classes at runtime to display on type pages. The `alsoKnownAs` ClassVar in archetypes lists old URIs for backward compatibility, so that URI-based lookups via `URI_TO_TYPE` still resolve after a prefix change.

Old versions (`vX.py`) are **not** regenerated when the prefix changes. Only the latest version is republished with the new URI. This will make sure the `aKa` values are not pointing to then-nonexistent new URIs for old versions. Also, once `vX.py` file is in a git commit, it's completely frozen and it should never be modified again anyway.

#### Changing Type Prefix URL

A URI prefix change is needed when the vocabulary moves to a different domain or path (e.g., the original vocabulary was hosted under `http://mmif.clams.ai/vocabulary/` and later moved to `http://clams.ai/vocabulary/type/`). This is an infrequent infrastructure-level decision, not a routine development task.

When changing the type prefix URL (e.g., `https://vocab.clams.ai/type` → `https://v.clams.ai/type`):

1. Update Archetypes: Manually add the *old* URI to the `alsoKnownAs` list in the `archetype.py` of affected types
   ```python
   class Annotation(Thing):
       shortname: ClassVar[str] = "Annotation"
       alsoKnownAs: ClassVar[List[str]] = [
           "http://mmif.clams.ai/vocabulary/Annotation/v2"  # old URI
       ]
       description: ClassVar[str] = "..."
   ```

2. Update Config: Change `type_prefix` in `pyproject.toml`
   ```toml
   [project.urls]
   type_prefix = "https://v.clams.ai/type"  # new prefix URL
   ```

3. Regenerate Affected Types: Run the build script with `--reuse-version-number` flag:
   ```bash
   python build-tools/generate_vocab_snapshot.py build <TypeName> --reuse-version-number
   ```
   Example: `python build-tools/generate_vocab_snapshot.py build Annotation --reuse-version-number`

   If changing affects all types, regenerate all:
   ```bash
   # For each type, regenerate with new URI
   for type in Annotation Thing Document Region ...; do
       python build-tools/generate_vocab_snapshot.py build $type --reuse-version-number
   done
   ```

4. Rebuild Docs: Regenerate HTML documentation and verify that the new URIs are displayed correctly on type pages:
   ```bash
   python build-tools/docs.py --output-dir docs-test
   ```

> [!WARNING]
> Changing `type_prefix` is a major operation that affects all types. Plan carefully and consider batch processing.

## Questions?

If you have questions about contributing, please open an issue on GitHub or contact the CLAMS team.
