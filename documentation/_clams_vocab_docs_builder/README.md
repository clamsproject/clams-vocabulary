# CLAMS Vocabulary Documentation Builder

This Sphinx extension automates the generation of reStructuredText (RST) documentation and JSON schemas from CLAMS Vocabulary Pydantic models, producing versioned HTML documentation for publishing.

The extension supports versioned documentation where type definitions are immutable snapshots. Each vocabulary release captures a snapshot of all current type versions, while individual type pages are shared across releases to avoid duplication.

The underscore prefix in the directory name follows Sphinx convention for internal directories (like `_static`, `_templates`).

## Key Principles

1. **Immutable Type Versions**: Once a type version is released, it never changes.
2. **Snapshot-based Vocab Versions**: A vocabulary release is a collection of specific type versions and their inheritance relations (called as "hierarchy") current at that time.
3. **Deduplicated Type Pages**: HTML documentation for a specific type version is generated once and shared across all vocabulary releases that include it.
4. **Versioned Hierarchies**: The type inheritance tree is generated for each vocabulary release to reflect the relationships valid at that time.

## Architecture

The extension hooks into the Sphinx `builder-inited` event to generate artifacts before the HTML build begins.

### Module Organization

- **`__init__.py`**: Extension entry point. Contains Sphinx setup, the `inheritance-tree` directive, and the main orchestration logic that coordinates the generation process.
- **`type_generator.py`**: Generates individual type documentation pages (RST) and JSON schema files.
- **`hierarchy_generator.py`**: Generates vocabulary hierarchy pages showing the type inheritance tree.
- **`index_generator.py`**: Generates the documentation index page.
- **`utils.py`**: Utility functions for type discovery, metadata extraction, git tag analysis, and JSON schema processing.

## Data Model

The generator extracts metadata from Pydantic models:

- **`alsoKnownAs`**: Tracks identity across URI scheme migrations.
- **`similarTo`**: Links to related external types.
- **`included_in`**: Derived property mapping a type version to vocabulary versions that contain it.

## Output Structure

The extension generates RST and JSON files within the `documentation/` directory. These files are ignored by git and regenerated during each build.

### Generated Files

```text
documentation/
├── index.rst                       # Generated landing page
├── X.Y.Z/                          # Vocabulary version hierarchy
│   └── index.rst                   # Hierarchy tree for this version
└── type/                           # Type documentation
    └── <TypeName>/
        └── vN/
            ├── index.rst           # Type documentation
            └── index.json          # JSON Schema
```

### HTML Output

After Sphinx builds, the HTML is published with this structure:

```text
docs/vocabulary/
├── type/                           # Shared type documentation
│   └── <TypeName>/
│       └── vN/
│           └── index.html
├── X.Y.Z/                          # Vocabulary snapshot
│   └── index.html                  # Includes hierarchy tree
└── ...
```

## Navigation

The extension implements context-aware navigation:

1. **Vocab Version Pages**: Navigate between vocabulary releases. Each page includes the type hierarchy tree valid at that snapshot.

2. **Type Version Pages**: Navigate between type versions and display which vocabulary versions include this type. Pages show version indicators when viewing older versions.

### Implementation Details

- Vocabulary snapshot pages serve as entry points containing the hierarchy tree
- Type pages are context-aware with version indicators
- Individual type pages are marked `:orphan:` to exist outside the main toctree while remaining reachable via links

## Generation Process

The extension generates documentation in four stages:

### 1. Type Discovery

Scans the types directory for version files to catalog all available type versions and their history.

### 2. Latest Resolution

Determines the current active version for each type by analyzing alias definitions. This identifies which type versions constitute the current vocabulary snapshot.

### 3. Reverse Indexing

Builds a mapping of type versions to vocabulary versions by querying git tags. Uses non-destructive git operations to trace historical inclusion. Results are cached to optimize build performance.

### 4. RST Generation

Renders Jinja2 templates to produce RST files:
- **Type Pages**: Individual pages with fields, description, and JSON schema
- **Hierarchy Pages**: Type trees for each vocabulary version
- **Index Page**: Landing page discovering all manual RST files
