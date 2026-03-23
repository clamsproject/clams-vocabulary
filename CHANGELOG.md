
## releasing 1.1.1 (2026-03-16)
### Overview

First release as an independent Python package on PyPI. The vocabulary was previously part of the MMIF specification (versions 1.0.0–1.1.0); as of 1.1.1 it is a standalone Pydantic-based package with its own versioning.

### Changes

- Merged "metadata" and "properties" distinction — all type attributes are now regular Pydantic fields (https://github.com/clamsproject/mmif/issues/230)
- Pydantic-based type definitions enable actual property validation, which was not possible with the YAML-based vocabulary and mmif-python SDK (https://github.com/clamsproject/mmif-python/issues/309)
- `CONTRIBUTING.md` includes release process and URI prefix change workflow



## releasing 1.1.0 (2026-03-13)
- Source: [MMIF 1.1.0 vocabulary](https://github.com/clamsproject/mmif/blob/1.1.0/vocabulary/clams.vocabulary.yaml)


### Overview
Added some of old LAPPS types under `Span`, see https://github.com/clamsproject/mmif/issues/202

### Additions

- Token, Sentence, Paragraph, NamedEntity, NounChunk, VerbChunk (all v1)

### Changes
- `Span`.`text` (String): new property, moved up from `Token`.`word`
- `Token`.`word`: removed (inherited from `Span` as `text`)
- `Region`.`timeUnit` (String): now optional, defaults to "milliseconds"
- All `Region` subtypes incremented accordingly


## releasing 1.0.4 (2026-03-13)
- Source: [MMIF 1.0.4 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.4/vocabulary/clams.vocabulary.yaml)

### Overview

- `Annotation`.`classifications` (Map\<String, Number\>): added back as backward compat alias for `classification`
- All `Annotation` subtypes incremented accordingly 


## releasing 1.0.3 (2026-03-13)
- Source: [MMIF 1.0.3 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.3/vocabulary/clams.vocabulary.yaml)

### Overview

- `Annotation`.`classifications` renamed to `Annotation`.`classification`
- All `Annotation` subtypes incremented accordingly


## releasing 1.0.2 (2026-03-13)
- Source: [MMIF 1.0.2 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.2/vocabulary/clams.vocabulary.yaml)

### Overview

- `Annotation`.`label` (String): added
- `Annotation`.`labelset` (List\<String\>): added (metadata)
- `Annotation`.`labelsetUri` (String): added (metadata)
- `Annotation`.`classifications` (Map\<String, Number\>): added
- `TimeFrame`.`frameType`: now aliased by `label`
- `BoundingBox`.`boxType`: now aliased by `label`
- All `Annotation` subtypes incremented accordingly


## releasing 1.0.4 (2026-03-13)
- Source: [MMIF 1.0.4 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.4/vocabulary/clams.vocabulary.yaml)

### Overview

- `Annotation`.`classifications` (Map\<String, Number\>): added again as backward compat alias
- All `Annotation` subtypes incremented accordingly



## releasing 1.0.3 (2026-03-13)
- Source: [MMIF 1.0.3 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.3/vocabulary/clams.vocabulary.yaml)

### Overview

- `Annotation`.`classifications` renamed to `Annotation`.`classification`
- All `Annotation` subtypes incremented accordingly


## releasing 1.0.2 (2026-03-13)
- Source: [MMIF 1.0.2 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.2/vocabulary/clams.vocabulary.yaml)

### Overview

- `Annotation`.`labelset` (List\<String\>): added (metadata)
- `Annotation`.`labelsetUri` (String): added (metadata)
- `Annotation`.`label` (String): added
- `Annotation`.`classifications` (Map\<String, Number\>): added
- All `Annotation` subtypes incremented accordingly


## releasing 1.0.1 (2026-03-13)
- Source: [MMIF 1.0.1 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.1/vocabulary/clams.vocabulary.yaml)

### Overview

- `TimeFrame`.`frameType`: added property values
- `Chapter` incremented accordingly


## releasing 1.0.0 (2026-03-13)
### Overview

- Before 0.5.0 (0.4.x and earlier)
  - All types shared same version (no individual versioning)
  - `Annotation` underwent significant changes at 0.4.2 (see [issue #134](https://github.com/clamsproject/mmif/issues/134))
    - Re-purposed as general dumping spot for document-level annotations
    - Retroactively considered v2 for when individual versioning began
- 0.5.0 (First Experimental Versioned Release)
  - First introduction of individual type versioning
  - `Annotation` released as v2 (reflecting 0.4.2 changes)
  - All other types at v1
  - No subsequent 0.5.x releases
- 1.0.0 (Stability Declaration)
  - Re-release of 0.5.0 with identical type versions
  - Marked versioned types as stable for production use
  - Starting point for ongoing evolution
  - Source: [MMIF 1.0.0 vocabulary](https://github.com/clamsproject/mmif/blob/1.0.0/vocabulary/clams.vocabulary.yaml)

### Additions
- Alignment v1
- Annotation v2
- AudioDocument v1
- BoundingBox v1
- Chapter v1
- Document v1
- ImageDocument v1
- Interval v1
- Polygon v1
- Region v1
- Relation v1
- Span v1
- TextDocument v1
- Thing v1
- TimeFrame v1
- TimePoint v1
- VideoDocument v1
- VideoObject v1
