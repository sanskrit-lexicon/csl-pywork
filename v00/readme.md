_Created: 23-07-2019 · Last updated: 15-09-2026_

# v00

> **Superseded.** This was the first experimental version. Use [`v02`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md) for all current work.

---

## What was different in v00

v00 used a `distinctscripts/` layout where each dictionary had its own subdirectory containing a hand-written `make_xml.py` and `xxx.dtd` — files that were considered too divergent to share across dictionaries. Shared scripts lived in `makotemplates/` and were either copied verbatim (`C`) or rendered as Mako templates (`T`), as recorded in `inventory.txt`.

v02 replaced `distinctscripts/` with a `distinctfiles/` layout and moved `make_xml.py` and `xxx.dtd` into the template system (`T` category), eliminating most hand-maintained per-dictionary copies.

---

## Installation (historical reference)

### First-time setup

```bash
mkdir scans && cd scans

git clone https://github.com/sanskrit-lexicon/csl-websanlexicon.git
cd csl-websanlexicon/v00 && bash redo_cologne_2020.sh && cd ../..

git clone https://github.com/sanskrit-lexicon/csl-pywork.git
cd csl-pywork/v00 && bash redo_cologne_2020.sh && cd ../..

git clone https://github.com/sanskrit-lexicon/csl-orig.git
```

### Subsequent updates

Run from the parent directory of all three repositories:

```bash
cd csl-websanlexicon/v00 && git pull --ff-only origin main && bash redo_cologne_2020.sh && cd ../..
cd csl-pywork/v00       && git pull --ff-only origin main && bash redo_cologne_2020.sh && cd ../..
cd csl-orig/v00         && git pull --ff-only origin main && cd ../..
```

All three repositories use `main`. csl-websanlexicon and csl-orig have no `master` branch any more, and the `master` left in csl-pywork is stale (June 2026), so `git pull origin master` either fails or merges old code.

### Regenerate one or all dictionaries

```bash
# All dictionaries
cd csl-pywork && bash redo.sh

# Single dictionary (e.g. SKD)
cd csl-pywork && bash redo.sh SKD
```

`redo.sh` updates both `csl-websanlexicon/v00` and `csl-pywork/v00` from GitHub, then for each dictionary runs `redo_hw.sh` (headwords) and `redo_xml.sh` (XML + SQLite) inside the dictionary's `pywork/` directory.

**If `redo.sh` stops early (since 15-09-2026, [#91](https://github.com/sanskrit-lexicon/csl-pywork/pull/91)):** it exits when a sibling folder (`csl-websanlexicon/v00`, `csl-pywork/v00`, `csl-orig/v00`) is missing or its `git pull --ff-only origin main` fails, instead of carrying on and rebuilding from stale code. Fix the folder it names, or pull that repository by hand, then rerun. A dictionary whose `<DICT>Scan/2020/pywork/` folder is missing is skipped with a `WARNING` line; the others still run.

---

## Applying a correction from the correction form

1. Edit `csl-orig/v00/csl-data/XXXScan/orig/xxx.txt` directly (e.g. `PWGScan/orig/pwg.txt`).
2. `git pull --ff-only origin main` first to pick up any concurrent changes.
3. Stage the file: `git add v00/csl-data/XXXScan/orig/xxx.txt`
4. Commit with a structured message: `git commit -m 'dictcode:lnum:old:new'`  
   e.g. `git commit -m 'skd:29044:SuMllam:Sullam'`
5. `git push origin main`
6. Regenerate the display: `cd csl-pywork && bash redo.sh XXX`

---

## Source files

Each dictionary's source data consists of two files in `csl-orig`:

| File | Path |
|---|---|
| Main digitisation | `csl-orig/v00/csl-data/XXXScan/2020/orig/xxx.txt` |
| Extra headwords | `csl-orig/v00/csl-data/XXXScan/2020/orig/hwextra/xxx_hwextra.txt` |

`XXX` is the uppercase dictionary code; `xxx` is lowercase (e.g. `PWGScan`, `pwg`).

_Dr. Mārcis Gasūns_
