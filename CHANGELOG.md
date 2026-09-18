_Created: 30-06-2026 · Last updated: 05-09-2026_

# Changelog

## [Unreleased]
### Added
- **G3 webtc2 generation-time search index (H3633, H3487 audit):** the
  webtc2 stage now builds `query_dump.sqlite3` alongside `query_dump.txt`
  (new `pywork/webtc2/build_query_index.py`, shipped for every dictionary
  via `inventory.txt`; wired into `webtc2/redo.sh`). The index stores each
  dump line's byte offset (usable with `fseek`) plus the hyphen-stripped
  line text and the dump size it was built from. csl-websanlexicon's
  `querymodel.php` consults it and falls back to the flat file when absent
  or stale, replacing the per-request linear `fgets` scan
  (audit W10, prior audit D4). Full-dump scans on MW/PWG sample queries
  drop ~2.4-6x with identical top-100 results (parity transcript in
  csl-websanlexicon `tests/webtc2_parity/`).

- Added a root `AGENTS.md` agent-entrypoint stub (H4634): names itself the agent entrypoint, links [CLAUDE.md](CLAUDE.md), points at the [Uprava org standard](https://github.com/gasyoun/Uprava/blob/main/AGENTS.md).
### Fixed
- **P10 (H3487 audit, G3/H3633):** `init_query.py` initialized
  `keysanskrit` only inside the first matching branch, so a file with zero
  `<H>` records crashed with `NameError` after opening the output file,
  and `webtc2/redo.sh` (no `set -e`) shipped the empty dump anyway. The
  variable is now initialized up front, the final record is only written
  when at least one record was read (no zero-record junk row), and
  `webtc2/redo.sh` is fail-closed (`set -e`), so a dump and its index are
  never moved into the web tree half-built. 7 sandbox tests in
  `tests/test_h3633_webtc2_index.py`.

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

### Fixed

- **G8 bookkeeping (H3638, H3487 audit):** `refresh_csl.sh` now reports per-repo
  OK/FAIL and exits nonzero naming failed pulls (a dead network on repo 3 was
  indistinguishable from success); `regenerate-hwnorm1-sqlite.sh` commit gates
  use `git status --porcelain` so untracked generated files actually commit
  (hwnorm1/hwnorm2/apidev no longer silently go stale); dead `>1000000` debug
  cutoff removed from the v02 `make_xml` template; literal junk row no longer
  written into every `query_dump.txt`. 8 sandbox tests in
  `tests/test_g8_bookkeeping.py`.

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

_Dr. Mārcis Gasūns_
