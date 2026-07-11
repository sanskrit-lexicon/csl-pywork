# csl-pywork

_Created: 15-05-2026 · Last updated: 11-07-2026_

CDSL **data-store** repository in the Sanskrit Lexicon project — the template for
the per-dictionary `pywork` build tree, and the canonical home of the shared CDSL
dictionary-generation pipeline (`generate_dict.sh`, `make_xml.py`,
`updateByLine.py`, `parseheadline.py`, `digentry.py`). These scripts are
**vendored** (copied, never forked-and-edited) into the individual dictionary
repos across the org, so a fix belongs here first — pull from
[`v02/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02) (and
[`v00/makotemplates/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v00/makotemplates)
for the older `updateByLine.py` / `parseheadline.py`).

<!-- BEGIN MANUAL: overview -->
`csl-pywork` contains the per-dictionary build scripts and templates used to
turn `csl-orig` source text into generated CDSL artifacts: headword lists, XML,
SQLite databases, downloads, and web-display support files.

## Input and output

| Direction | Location | Notes |
|---|---|---|
| Input source | `../csl-orig/v02/<dict>/` | Canonical dictionary text, metadata, and extra headwords. |
| Web templates | `../csl-websanlexicon/` | Used by `generate_web.sh` during `v02` generation. |
| Generated output | `../<dict>/` or server-specific scan directories | Contains `orig/`, `pywork/`, `web/`, and `downloads/`. |
| Documentation | `v02/readme.md` | Current production pipeline notes. |

## Directory map

| Path | Role |
|---|---|
| `v02/` | Current production generation pipeline. |
| `v00/` | Older generation pipeline and historical scripts. |
| `v02/makotemplates/` | Shared template files rendered or copied into dictionary builds. |
| `v02/distinctfiles/` | Per-dictionary files that override or extend shared templates. |
| `issues/` | Issue-specific experiments and fixes. |
| `tests/` | Regression checks where available. |

## Typical build flow

The current single-dictionary flow is documented in `v02/readme.md`:

```sh
cd csl-pywork/v02
sh generate_dict.sh mw ../../MWScan/2020
```

At a high level:

```text
csl-orig source -> generate_orig.sh -> generate_pywork.sh -> generate_web.sh -> generated pywork/web/downloads
```

The root `redo.sh` is an older broad regeneration script that pulls sibling
repositories and rebuilds selected dictionaries in a Cologne/XAMPP-style layout.

## Per-dictionary conventions

Most detailed notes live under `v02/distinctfiles/<dict>/pywork/` or a local
issue directory.  Read the nearest `readme.*` before changing a dictionary's
abbreviation, bibliography, tooltip, or SQLite generation scripts.

## Common failure modes

- Sibling repositories are expected in the same parent directory.
- Several scripts assume bash plus command-line `sqlite3`, `xmllint`, `zip`,
  PHP, and Python/Mako.
- Generated files can be stale; check the source commit and rerun the relevant
  `redo*` script before drawing conclusions.
- Windows/XAMPP and Cologne server paths differ; older notes may need path
  adjustment before rerun.
<!-- END MANUAL: overview -->

## Tech Stack

Per the prerequisites in [`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md):

- **Python 3** + `mako` — templating and the correction/XML pipeline scripts.
- **bash** — the `generate_*.sh` / `redo_*.sh` orchestration scripts.
- **sqlite3**, **xmllint** (libxml2-utils), **zip** — database, XML validation, downloads.
- **PHP** (CLI + pdo + sqlite3) — web display generation.
- A local web server (apache2 / XAMPP) to serve displays.

Repo category `data-store`; broader pipeline in the [csl-observatory tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md).

## Issues Overview

Snapshot 2026-07-11: **3** open, **30** closed. All 3 open issues sit in the
**Developer Experience** milestone:

| # | Title | Type | Severity |
|---:|---|---|---|
| [63](https://github.com/sanskrit-lexicon/csl-pywork/issues/63) | Stuck with master / main conflicts — Read here | documentation | minor |
| [53](https://github.com/sanskrit-lexicon/csl-pywork/issues/53) | Modernise `redo_xampp_selective.sh`: python3, parameterise paths, document prereqs | infrastructure | major |
| [52](https://github.com/sanskrit-lexicon/csl-pywork/issues/52) | Add `.gitattributes` (`text=auto eol=lf`) to normalise line endings | infrastructure | minor |

## GitHub Issue Conventions

Follows the [Cologne tooling-repo taxonomy](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md):

- **17 type labels** across 5 categories
- **4 severity levels**: trivial, minor, major, critical
- **5 milestones**: API Stability, User Experience, Data Quality, Developer Experience, Community
- **Domain labels** scoped to data-store: `domain:schema`, `domain:migration`, `domain:integrity`, `domain:storage`
- **Org Project**: [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9)

---

_Issue-overview and taxonomy sections generated by the Cologne Tooling Runbook (2026-05-29); manual overview and facts refreshed 11-07-2026._

_Dr. Mārcis Gasūns_
