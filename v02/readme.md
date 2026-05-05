# v02

The current, production version of the CSL code-generation pipeline.

---

## Prerequisites

- **Python 3** + `mako` (`pip install mako`)
- **bash**, **sqlite3**, **xmllint** (libxml2-utils), **zip**
- **php** (CLI + pdo + sqlite3) — for web display
- **git**
- A web server (apache2 or XAMPP) to serve displays locally

---

## Repository layout

All three sibling repositories must be checked out in the same parent directory:

```
cologne/
  csl-orig/           ← source digitisation text files
  csl-pywork/         ← this repo
  csl-websanlexicon/  ← web display code generation
```

---

## Quick start

```bash
# Generate (or update) a single dictionary
cd csl-pywork/v02
sh generate_dict.sh mw ../../MWScan/2020

# Generate all dictionaries on a Cologne server
sh redo_cologne_all.sh

# Generate all dictionaries on a local XAMPP server
sh redo_xampp_all.sh

# Update only dictionaries changed in csl-orig since last run
sh redo_xampp_selective.sh
```

Dictionary codes (lowercase): `acc ae ap ap90 ben bhs bop bor bur cae ccs gra gst ieg inm krm lan mci md mw mw72 mwe pd pe pgn pui pw pwg pwkvn sch shs skd snp stc vcp vei wil yat` and newer additions `armh lrv abch acph acsj fri`.

---

## What `generate_dict.sh` does

`sh generate_dict.sh <dict> <outdir>` builds a complete, self-contained dictionary installation at `<outdir>`:

```
outdir/
  orig/       ← source text copied from csl-orig
  pywork/     ← scripts for headwords, XML, SQLite
  web/        ← display scripts (from csl-websanlexicon)
  downloads/  ← zip archive generation scripts
```

It runs four stages in sequence:

### Stage 1 — `generate_orig.sh`
Copies `<dict>.txt`, `<dict>_hwextra.txt`, `<dict>header.xml`, and `<dict>-meta2.txt` from `csl-orig/v02/<dict>/` into `outdir/orig/` and `outdir/pywork/`.

### Stage 2 — `generate_pywork.sh`
Runs `generate.py` which reads `inventory.txt` and assembles `outdir/pywork/` by:
- **Copying** (`C`) shared files from `makotemplates/`
- **Rendering** (`T`) Mako templates in `makotemplates/` with the dictionary's parameters from `dictparms.py`
- **Copying distinct** (`CD`) per-dictionary files from `distinctfiles/<dict>/pywork/`
- **Deleting** (`D`) obsolete files that may exist from a previous generation

### Stage 3 — `generate_web.sh` (runs from `csl-websanlexicon/v02`)
Assembles `outdir/web/` using the same C/T/CD/D model from that repo's own `inventory.txt` and `makotemplates/`.

Also runs `generate_ab_bib_ls.sh` to generate `redo.sh` and SQL scripts for abbreviation, tooltip, and bibliography tables into the appropriate `outdir/pywork/<dict>ab/` and `outdir/pywork/<dict>auth/` subdirectories.

### Stage 4 — Execute the generated scripts
Runs the assembled pipeline inside `outdir/pywork/`:

| Script | Output |
|---|---|
| `redo_hw.sh` | `<dict>hw.txt` — headword list extracted from orig text |
| `redo_xml.sh` | `<dict>.xml` — full XML, validated against `<dict>.dtd` via xmllint |
| `redo_postxml.sh` | `web/sqlite/<dict>.sqlite`, abbreviation/tooltip/bib SQLite databases |
| `downloads/redo_all.sh` | zip archives for txt, xml, and web |

---

## XAMPP file system layout (Windows)

```
htdocs/
  cologne/
    csl-orig/
    csl-pywork/
    csl-websanlexicon/
    mw/           ← generated output for MW dictionary
    acc/          ← generated output for ACC dictionary
    ...
```

Local URL for a dictionary (e.g. MW): `http://localhost/cologne/mw/web/`

### Installing sqlite3 and zip on Windows (Git Bash)

**sqlite3**: Download `sqlite-tools-win32` from https://www.sqlite.org/download.html, extract `sqlite3.exe` to `C:\xampp\sqlite3\`, and add that directory to the system `Path`.

**zip**: Install [GoW](https://github.com/bmatzelle/gow/releases/download/v0.8.0/Gow-0.8.0.exe) (Gnu on Windows), then copy `zip.exe` from `C:\Program Files (x86)\Gow\bin\` to your sqlite3 directory.

---

## Ubuntu installation

```bash
sudo apt install python3-pip git apache2 zip sqlite3 php php-cli php-xml php-sqlite3 libxml2-utils
sudo pip3 install mako

cd /var/www/html
sudo mkdir cologne && cd cologne
sudo git clone https://github.com/sanskrit-lexicon/csl-orig.git
sudo git clone https://github.com/sanskrit-lexicon/csl-pywork.git
sudo git clone https://github.com/sanskrit-lexicon/csl-websanlexicon.git

cd csl-pywork/v02
sudo bash redo_xampp_all.sh
```

---

## Selective update (cron / auto-update)

`redo_xampp_selective.sh` is designed to run automatically (e.g. at system boot via cron):

```
@reboot sleep 120 && bash /var/www/html/cologne/csl-pywork/v02/redo_xampp_selective.sh
```

It tracks the last-processed `csl-orig` commit in `csl-orig/v02/.xampp_last_run`. On each run it:

1. Pulls all relevant git repositories (csl-orig, csl-pywork, csl-websanlexicon, hwnorm1, csl-json, cologne-stardict)
2. Finds `.txt` files changed in `csl-orig` since the last run
3. Regenerates only affected dictionaries via `generate_dict.sh`
4. Rebuilds Stardict files and pushes to `cologne-stardict` and `indic-dict/stardict-sanskrit`
5. Rebuilds JSON files and pushes to `csl-json`
6. Updates `csl-orig/.version` and refreshes the `csl-homepage`

Prerequisites for selective update: sibling directories `cologne-stardict`, `csl-json`, `csl-homepage`, `hwnorm1`, and `indic-dict/stardict-sanskrit` must be present and have cached git credentials.
