# CLAUDE.md

_Created: 06-05-2026 · Last updated: 05-09-2026_

**csl-pywork** is the Cologne **generator**. It turns
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig) digitised text into
per-dictionary XML, headword lists, SQLite, downloads, and the files the
[csl-websanlexicon](https://github.com/sanskrit-lexicon/csl-websanlexicon)
web frontend needs. Production pipeline: [`v02/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02)
([`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md)).
`v00/` is historical.

Sibling checkouts must share a parent directory:

```
cologne/
  csl-orig/
  csl-pywork/          ← this repo
  csl-websanlexicon/   ← required sibling (web templates)
```

## What to run

```sh
cd v02
sh generate_dict.sh mw ../../MWScan/2020
```

`generate_dict.sh <dict> <outdir>` copies orig → renders Mako templates →
runs [`make_xml.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/make_xml.py)
→ builds SQLite / downloads / web support. Batch: `redo_xampp_all.sh` (local)
or `redo_cologne_all.sh` (server). After a generate, DTD-validate with
[`xmlchk_xampp.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/xmlchk_xampp.sh)
`<dict>` (XAMPP layout).

**Windows / no XAMPP:**

- `generate_dict.sh` calls `python3`. If only `python` is on PATH, put a
  wrapper ahead of it: `echo '#!/bin/bash\npython "$@"' > /tmp/pybin/python3`
  and prepend `/tmp/pybin` to `PATH`.
- Install Mako: `pip install mako`.
- `xmllint` is often missing. The validate signal is then
  `make_xml.py` printing **`All records parsed by ET`**.

Corrections that *drive* this generator follow
[csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
— snapshot → apply → regenerate here → validate → audit. Do not invent a
second sequence.

`updateByLine.py` / `parseheadline.py` live here and are **vendored**
(copied, never forked-and-edited) into dictionary repos. A shared-script
fix belongs in this repo first.

## Do not

- Commit or push [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)
  source. Queue via
  [`/cologne-correction-queue`](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-correction-queue.md).
- Edit a vendored copy of `make_xml.py` / `updateByLine.py` inside a
  dictionary repo and leave this tree stale.
- Write a UTF-8 BOM.

## Primer

[SANSKRIT_CONTEXT_PRIMER.md](https://github.com/gasyoun/github-spine/blob/main/SANSKRIT_CONTEXT_PRIMER.md).

Issues use the Cologne taxonomy — see
[`/cologne-issue-runbook`](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-issue-runbook.md).

_Dr. Mārcis Gasūns_
