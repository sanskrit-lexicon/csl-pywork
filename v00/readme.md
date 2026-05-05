# v00

> **Superseded.** This was the first experimental version. Use [`v02`](../v02/readme.md) for all current work.

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
cd csl-websanlexicon/v00 && git pull origin master && bash redo_cologne_2020.sh && cd ../..
cd csl-pywork/v00       && git pull origin master && bash redo_cologne_2020.sh && cd ../..
cd csl-orig/v00         && git pull origin master && cd ../..
```

### Regenerate one or all dictionaries

```bash
# All dictionaries
cd csl-pywork && bash redo.sh

# Single dictionary (e.g. SKD)
cd csl-pywork && bash redo.sh SKD
```

`redo.sh` updates both `csl-websanlexicon/v00` and `csl-pywork/v00` from GitHub, then for each dictionary runs `redo_hw.sh` (headwords) and `redo_xml.sh` (XML + SQLite) inside the dictionary's `pywork/` directory.

---

## Applying a correction from the correction form

1. Edit `csl-orig/v00/csl-data/XXXScan/orig/xxx.txt` directly (e.g. `PWGScan/orig/pwg.txt`).
2. `git pull origin master` first to pick up any concurrent changes.
3. Stage the file: `git add v00/csl-data/XXXScan/orig/xxx.txt`
4. Commit with a structured message: `git commit -m 'dictcode:lnum:old:new'`  
   e.g. `git commit -m 'skd:29044:SuMllam:Sullam'`
5. `git push origin master`
6. Regenerate the display: `cd csl-pywork && bash redo.sh XXX`

---

## Source files

Each dictionary's source data consists of two files in `csl-orig`:

| File | Path |
|---|---|
| Main digitisation | `csl-orig/v00/csl-data/XXXScan/2020/orig/xxx.txt` |
| Extra headwords | `csl-orig/v00/csl-data/XXXScan/2020/orig/hwextra/xxx_hwextra.txt` |

`XXX` is the uppercase dictionary code; `xxx` is lowercase (e.g. `PWGScan`, `pwg`).
