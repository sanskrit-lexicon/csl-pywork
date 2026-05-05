# csl-pywork

Code generation tools for the [Cologne Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) — a collection of ~45 digitised Sanskrit dictionaries.

This repository does not contain runnable dictionary scripts directly. Instead it **generates** them: given a dictionary code, it assembles a working directory of headword extraction, XML building, SQLite generation, and web display scripts tailored to that dictionary.

---

## How it fits in

Three sibling repositories together produce a complete, functional dictionary installation:

| Repository | Contents |
|---|---|
| **csl-orig** | Source digitisation text files — one `xxx.txt` per dictionary |
| **csl-pywork** | This repo — generates per-dictionary `pywork/` scripts |
| **csl-websanlexicon** | Generates per-dictionary `web/` display scripts |

All three must be checked out as siblings in the same parent directory:

```
cologne/
  csl-orig/
  csl-pywork/
  csl-websanlexicon/
```

---

## Quick start

```bash
# Generate (or update) a single dictionary
cd csl-pywork/v02
sh generate_dict.sh mw ../../MWScan/2020

# Generate all dictionaries on a local XAMPP server
sh redo_xampp_all.sh

# Update only dictionaries that changed in csl-orig since last run
sh redo_xampp_selective.sh
```

See [`v02/readme.md`](v02/readme.md) for full installation instructions covering Cologne server, XAMPP (Windows), and Ubuntu.

---

## How it works

For each dictionary, `generate_dict.sh` assembles three output subdirectories:

```
outdir/
  orig/        ← source text copied from csl-orig
  pywork/      ← generated scripts for headwords, XML, SQLite
  web/         ← generated display scripts (from csl-websanlexicon)
```

The pywork scripts are built from two sources in this repo:

- **`makotemplates/`** — files shared across dictionaries, either copied verbatim (category `C`) or rendered as [Mako](https://www.makotemplates.org/) templates with per-dictionary parameters (category `T`)
- **`distinctfiles/<dict>/`** — files that are too different between dictionaries to template, copied verbatim (category `CD`)

Which files go where is declared in `inventory.txt`. Dictionary parameters (names, codes, version numbers) live in `dictparms.py`.

After assembly, the pipeline runs automatically:

1. **`redo_hw.sh`** — extracts headwords from the source text → `xxxhw.txt`
2. **`redo_xml.sh`** — builds `xxx.xml` and validates it against `xxx.dtd` with xmllint
3. **`redo_postxml.sh`** — creates `xxx.sqlite`, regenerates abbreviation/tooltip/bibliography databases, updates the advanced-search query dump
4. **`downloads/redo_all.sh`** — packages zip archives for txt, xml, and web

---

## Version history

| Version | Status | Notes |
|---|---|---|
| **v00** | Superseded | First experimental version; uses `distinctscripts/` layout with one `make_xml.py` and one `xxx.dtd` per dictionary in separate subdirectories |
| **v01** | Not in this repo | Lived on the Cologne file system; refined the `makotemplates/` and `distinctfiles/` layout that became v02 |
| **v02** | **Current** | Consolidates `make_xml.py` and `xxx.dtd` into Mako templates (`T` category); adds `CD` category for per-dictionary distinct files; full Python 3 support |

---

## Prerequisites

- Python 3 + `mako` (`pip install mako`)
- bash, sqlite3, xmllint, zip
- php (CLI + pdo + sqlite3) for web display
- A web server (apache2 or XAMPP) to serve the displays locally
