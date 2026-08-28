# Changelog

## [Unreleased]
### Fixed
- **G1 fail-closed validation (H3631):** `xmlvalidate.py` now exits nonzero on
  DTD-validation failure (P2). `make_xml.py` exits nonzero when malformed
  records are detected instead of shipping them with exit 0 (P3), and writes
  output via temp-file + atomic rename so a mid-loop crash no longer truncates
  the previous good `<dict>.xml` (P4). `redo_xml.sh` gates `redo_postxml.sh`
  on the make_xml + xmllint exit status instead of printing red and proceeding
  (P1). `generate_dict.sh` checks every stage's exit status and every `cd`,
  printing a red STOP line and exiting nonzero instead of falling through on a
  half-assembled tree (P5, O2).

### Changed
- **CI (H3631):** `xml-parse.yml` dict build is now a 6-dict matrix (mci,
  abch, gst, ae, cae, acc) and gates on the pipeline exit status, which the
  fail-closed `generate_dict.sh` now makes meaningful.

## [0.2.2] - 2026-07-31
### Fixed
- **H1783 residual salvage:** fix .gitattributes claim, sync CITATION.cff to v0.2.1 (#75).

### Changed
- **Session journal:** H1783 completion recorded in .ai_state.md (#76).


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-07-29

### Added
- `docs/GENERATION_MANUAL.md`: grafted the verified deltas from the parallel
  H1783 pass (PR #71) — metaline/L/k1-k2/SLP1 glossary, `KeyError` and
  `ERROR CD copyfile` symptom rows, CI workflow specifics, `updateByLine.py`
  audit-summary line, selective `--dry-run`, cosmetic-quirks list.

### Fixed
- Dropped the re-introduced `changelog.md` case-duplicate (re-applying #65);
  `CHANGELOG.md` is the single changelog. (PR #72)

## [0.2.0] - 2026-07-28

### Added
- `docs/GENERATION_MANUAL.md` — operator manual for the dictionary-generation
  pipeline (stage-by-stage `generate_dict.sh`, validation layers, the
  `updateByLine.py` change-file format, vendor rule, symptom→cause→cure), with
  `docs/GENERATION_MANUAL.meta.md` companion and a README docs link. (H1783)

## [0.1.0] - 2026-06-30

### Added
- Initial release of csl-pywork
- Added this changelog so repository-level changes have a stable home.
- Recorded the current repository purpose: CDSL data-store repository in the Sanskrit Lexicon project.

### Changed

### Deprecated

### Removed

### Fixed

### Security

### Recent Git History
- 2026-06-12 docs: add regeneration-safe README overview
- 2026-06-02 ci: fix committed-XML check — skip Mako templates, tolerate multi-root fragments
- 2026-06-02 infra: parameterise refresh-script base path (M1/D2); add full make_xml XML-parse CI (D3)
- 2026-06-01 PD distinct files
- 2026-05-30 fix: read sources with utf-8-sig so a leading BOM can't break hw.py
