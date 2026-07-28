# csl-pywork Generation Pipeline Manual

_Created: 28-07-2026 · Last updated: 28-07-2026_

The operator manual for csl-pywork: turning a dictionary's canonical source text
in [csl-orig](https://github.com/sanskrit-lexicon/csl-orig) into the full set of
generated CDSL artifacts — headword list, XML, SQLite databases, web display
support, and download archives — through `generate_dict.sh` and the scripts it
assembles. Written so a new operator regenerates a dictionary end-to-end from
this document alone, without reading every vendored copy.

Companion metadoc: [docs/GENERATION_MANUAL.meta.md](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/docs/GENERATION_MANUAL.meta.md).
Sibling manuals: the correction-side workflow is
[csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
(this manual covers only the *generation* pipeline that workflow drives in its
regeneration step); the web-display side belongs to
[csl-websanlexicon](https://github.com/sanskrit-lexicon/csl-websanlexicon)
(its own operator manual is queued as a sibling of this one).

---

## 1. Cheat-sheet — the whole pipeline on one screen

```bash
# Required sibling layout (all three in ONE parent directory):
#   cologne/
#     csl-orig/           <- canonical source text (input)
#     csl-pywork/         <- this repo (the engine)
#     csl-websanlexicon/  <- web display generation (stage 3 runs from there)

# Generate (or fully regenerate) one dictionary, XAMPP-style layout:
cd csl-pywork/v02
sh generate_dict.sh mw ../../mw          # <dict> <outdir>

# Green signals to watch for in the scroll:
#   "N entries found" / "N lines written to mwhw.txt"   (headword stage)
#   "All records parsed by ET"                          (make_xml.py)
#   NO "BEGIN xmllint_err" block                        (DTD validation clean)
#   "N rows written to mw.sqlite"                       (sqlite stage)
# Anything printed in RED was not on the stage's known-good whitelist — read it.

# Re-validate the XML on its own afterwards:
sh xmlchk_xampp.sh mw                    # delegates to xmlvalidate.py (lxml)

# All dictionaries at once (server bulk runs):
sh redo_cologne_all.sh                   # Cologne server layout
sh redo_xampp_all.sh                     # local XAMPP layout

# Only dictionaries changed in csl-orig since the last run:
python3 redo_xampp_selective.py --dry-run
```

Dictionary codes are lowercase (`mw`, `pwg`, `ap90`, …). The authoritative
registry is
[`v02/dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/dictparms.py) —
a code missing there cannot be generated (§7.2 for adding one).

## 2. What this repo is — and the vendor rule

csl-pywork is the **canonical home of the CDSL dictionary-generation pipeline**.
The scripts under
[`v02/makotemplates/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/makotemplates)
(`make_xml.py`, `hw.py`, `updateByLine.py`, `parseheadline.py`, the `redo_*.sh`
drivers, the sqlite loaders) are **vendored**: generation *copies or renders*
them into each dictionary's output tree, and historical copies also sit inside
individual dictionary repos across the org.

**The vendor rule:** a fix belongs HERE first — in the template under
`v02/makotemplates/` or the per-dictionary override under
`v02/distinctfiles/<dict>/` — and reaches the dictionaries by regeneration.
Never edit a copy found in a generated `pywork/` directory or a dictionary repo
as if it were the source of truth: the next `generate_dict.sh` run overwrites
(categories `C`/`T`), and category `D` files are actively *deleted* from output
trees. Editing a rendered `make_xml.py` in an output tree is doubly wrong — it
is not even the template, it is one dictionary's Mako-rendered instance of it.

The same discipline applies to the input: corrections are **never** made
directly to `csl-orig` source files. They are expressed as change files (§6)
and flow through the
[csl-corrections workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).

## 3. Data-flow diagram

```
csl-orig/v02/<dict>/          (canonical input, §4 stage 1)
  <dict>.txt  <dict>_hwextra.txt  <dict>header.xml  <dict>-meta2.txt
│
│  generate_dict.sh <dict> <outdir>        (run from csl-pywork/v02)
│
├─ 1 generate_orig.sh      copies the four input files
│       -> outdir/orig/<dict>.txt   + outdir/pywork/{hwextra,header,meta2}
│
├─ 2 generate_pywork.sh    generate.py + inventory.txt + dictparms.py
│       C  copy from makotemplates/          (verbatim shared file)
│       T  render Mako template with this dict's parameters
│       CD copy from distinctfiles/<dict>/   (per-dict override)
│       D  delete obsolete file from outdir if present
│       -> outdir/pywork/  (assembled, dict-specific scripts)
│
├─ 3 generate_ab_bib_ls.sh  abbreviation / tooltip / bibliography
│       -> redo.sh + *.sql under outdir/pywork/<dict>ab/, <dict>auth/
│
├─ 4 generate_web.sh       runs from ../../csl-websanlexicon/v02
│       same C/T/CD/D model over THAT repo's inventory + templates
│       -> outdir/web/
│
▼  then generate_dict.sh EXECUTES the assembled outdir/pywork/ scripts:
   redo_hw.sh       hw.py (+ parseheadline.py) -> <dict>hw.txt (+ hw2, hw0)
   redo_xml.sh      make_xml.py -> <dict>.xml   "All records parsed by ET"
                    xmllint --noout --valid vs <dict>.dtd
                    redo_postxml.sh:
                      sqlite/redo.sh    -> web/sqlite/<dict>.sqlite
                      webtc2/redo.sh    -> advanced-search query dump
                      <dict>ab/, <dict>auth/ (where applicable, §4 stage 4)
                      mw only: mwkeys, westmwtab, whitmwtab link DBs
   downloads/redo_all.sh -> txt / xml / web zip archives

outdir/
  orig/        source text copy
  pywork/      scripts + <dict>hw.txt + <dict>.xml + <dict>.dtd
  web/         display app + web/sqlite/*.sqlite
  downloads/   zip archives
```

## 4. Step-by-step: `generate_dict.sh <dict> <outdir>`

Run from `csl-pywork/v02`. `<dict>` is the lowercase code; `<outdir>` is the
target directory, created if absent (XAMPP convention: `../../<dict>`, so the
generated tree lands beside the three repos; any path works).

### Stage 1 — `generate_orig.sh`: pull the canonical input

Reads
[`v02/inventory_orig.txt`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/inventory_orig.txt)
and copies from **`../../csl-orig/v02/<dict>/`**:

| File | Role | Lands in |
|---|---|---|
| `<dict>.txt` | the digitised dictionary text (one metaline `<L>…<k1>…` block per entry) | `outdir/orig/` |
| `<dict>_hwextra.txt` | extra/alternate headwords not derivable from the text | `outdir/pywork/hwextra/` |
| `<dict>header.xml` | XML header block for the generated `<dict>.xml` | `outdir/pywork/` |
| `<dict>-meta2.txt` | dictionary metadata | `outdir/pywork/` |

This is the **entire input contract** — if generation misbehaves and these four
files are current, the problem is in this repo, not in csl-orig.

### Stage 2 — `generate_pywork.sh`: assemble `outdir/pywork/`

[`generate.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate.py)
walks
[`inventory.txt`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/inventory.txt)
(colon-separated: `dict-codes : path [new-path] : category`; `*` = all
dictionaries; `;` = comment) and applies the four categories listed in §3.
Template context comes from `dictparms.py` (`dictlo`, `dictup`, `dictname`,
`dictversion` + `microversion`, `dictmmddyyyy`, `cologne_flag`). One special
case: `pywork/make_xml.py` is Mako-rendered through a pre/post-processing pass
because the dictionary text itself contains literal `<%s>`, `</%s>` and `##`
sequences that would otherwise read as Mako syntax.

### Stage 3 — `generate_ab_bib_ls.sh`: abbreviation / tooltip / bibliography scripts

Generates the `redo.sh` + SQL loaders for abbreviation tables (`<dict>ab/`),
literary-source tooltips and bibliography (`<dict>auth/`) into
`outdir/pywork/`. Only the dictionaries listed inside the script get each
table family; the input data files (`<dict>ab_input.txt`, `tooltip.txt`,
`<dict>bib_input.txt`) come from `distinctfiles/<dict>/pywork/` in stage 2.

### Stage 4 — `generate_web.sh`: assemble `outdir/web/`

`generate_dict.sh` does `cd ../../csl-websanlexicon/v02` and runs **that**
repo's `generate_web.sh` against the resolved absolute `outdir` — same
C/T/CD/D model over its own `inventory.txt` and `makotemplates/`. If
csl-websanlexicon is not a sibling checkout, generation dies here.

### Stage 5 — execute the assembled scripts

`generate_dict.sh` then cd's into `outdir/pywork/` and runs, in order:

| Script | Output | Green signal |
|---|---|---|
| `redo_hw.sh` | `<dict>hw.txt` (+ derived `<dict>hw2.txt`, `<dict>hw0.txt`; mw also rebuilds `mwkeys.sqlite`) | `N entries found`, `N lines written to <dict>hw.txt` |
| `redo_xml.sh` | `<dict>.xml`, validated against `<dict>.dtd`; then calls `redo_postxml.sh` | `All records parsed by ET`, and **no** `xmllint_err` block |
| `redo_postxml.sh` | `web/sqlite/<dict>.sqlite`, webtc2 query dump, ab/tooltip/bib SQLite DBs, mw link DBs | `N rows written to <dict>.sqlite` |
| `downloads/redo_all.sh` | `<dict>txt.zip`, `<dict>xml.zip`, `<dict>web1.zip` | `create new …zip` lines |

The driver pipes each stage through an awk whitelist: expected lines print
normally, **anything unexpected prints in red**. Red output is not always
fatal (e.g. `Unexpected <H>:` lines are whitelisted as normal for `vcp` only),
but every red line deserves a read before you call the run good.

## 5. XML validation — what "green" means

Two independent checks run during `redo_xml.sh`:

1. **`All records parsed by ET`** — `make_xml.py` re-parses every generated
   entry with Python's `xml.etree.ElementTree` as it writes. This is the
   well-formedness gate and it needs no external tools, so it works everywhere
   — including a bare Windows box. If this line is missing, the XML is broken
   regardless of what else printed.
2. **`xmllint --noout --valid <dict>.xml`** — DTD validity against the
   rendered `<dict>.dtd`. Silence is success; any output is wrapped in a red
   `BEGIN xmllint_err … END xmllint_err` block. Requires `xmllint`
   (libxml2-utils) on PATH.

Standalone re-validation after the fact:
[`v02/xmlchk_xampp.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/xmlchk_xampp.sh)
`<dict>` assumes the XAMPP layout (`../../<dict>/pywork/<dict>.xml`) and
delegates to `xmlvalidate.py` — an lxml-based DTD validator it expects at
`../../xmlvalidate.py`, i.e. in the *parent* directory above the repos. On a
fresh setup that file is absent: copy it there from
[`v02/utilities/xmlvalidate.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/utilities/xmlvalidate.py)
(needs `pip install lxml`). Prints `ok` on success.

On Windows without `xmllint`: rely on the ET-parse line for well-formedness and
run `python3 ../../xmlvalidate.py <dict>.xml <dict>.dtd` (lxml) for the DTD
check — the two together equal the Linux green state.

## 6. `updateByLine.py` — the change-file format

[`v02/makotemplates/pywork/updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/updateByLine.py)
applies a change file to a dictionary text:

```bash
python3 updateByLine.py <input.txt> <changefile> <output.txt>
```

The change file is a sequence of **line pairs** (plus `;` comment lines),
UTF-8, one transaction per pair:

```
; simple replacement — "new"
123456 old <s>rAma</s> a typo herre
123456 new <s>rAma</s> a typo here

; insertion — "ins" adds a line AFTER input line 2345
2345 old some existing line
2345 ins the brand-new line that follows it

; deletion — "del", text part empty (keep the trailing space)
3456 old the line to remove
3456 del 
```

Rules and traps, all of which abort the run loudly rather than corrupt output:

- **Line numbers always refer to the INPUT file** (1-based), for every
  transaction — insertions and deletions earlier in the file do not shift the
  numbering of later transactions.
- The `old` text must **byte-match** the input line exactly, or the run stops
  with `CHANGE ERROR #2: Old mismatch`. The usual cause: the change file was
  written against an older csl-orig state — re-derive it against current text.
- An **odd number** of non-comment lines is an error (`Expected EVEN number of
  lines`): every transaction is a pair, even `del`.
- **BOM trap:** a change file saved by a Windows editor with a UTF-8 BOM makes
  its first `old` line start with an invisible `﻿` — guaranteed mismatch
  on transaction 1. Save without BOM. (The generation side reads sources with
  `utf-8-sig` since 30-05-2026 precisely because a BOM once broke `hw.py`, but
  `updateByLine.py` compares raw text.)
- **CRLF trap:** the script strips `\r\n` from both files, so line *endings*
  are safe — but a change file that picked up stray `\r` characters
  mid-line (from copy-paste) still mismatches.

The run summary (`N records written`, `N change transactions`, counts per
`new`/`ins`/`del`) is your audit line — quote it when parking a correction in
the csl-corrections queue.

## 7. Operating notes

### 7.1 Environment / prerequisites

From
[`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md):
Python 3 + `mako` (`pip install mako`), bash, `sqlite3`, `xmllint`
(libxml2-utils), `zip`, PHP (CLI + pdo + sqlite3) for web display, and a local
web server (apache2/XAMPP) to actually browse the result
(`http://localhost/cologne/<dict>/web/`).

Windows specifics (Git Bash):

- Every script calls **`python3`**; Windows installs expose `python`. Create a
  `python3` wrapper on PATH once (e.g. a `python3.bat`/shim that forwards to
  `python`) — the org-standard fix.
- `sqlite3.exe` and `zip.exe` install steps are in
  [`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md)
  (sqlite-tools + GoW).
- The `.sh` drivers are Bourne-shell scripts — run them from **Git Bash**,
  never PowerShell.

### 7.2 Adding or changing a dictionary

1. Register the code in `v02/dictparms.py` (`dictup`, `dictlo`, `dictname`,
   `dictversion`) — `generate.py` does `alldictparms[dictcode]`, so an
   unregistered code is an immediate KeyError.
2. Create `v02/distinctfiles/<dict>/pywork/` with any per-dict overrides, and
   add the dict's code to the relevant `inventory.txt` rows (ab/auth rows are
   explicit code lists, not `*`).
3. If the dict needs abbreviation/tooltip/bib tables, add it to the lists in
   `generate_ab_bib_ls.sh` and `redo_postxml.sh`'s template conditionals.
4. Ensure `csl-orig/v02/<dict>/` carries the four input files (§4 stage 1).

### 7.3 `v00/` vs `v02/`

[`v00/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v00) is the
older generation pipeline (per-`XXScan/2020` distinct scripts). It is kept as
history; **operators do not run v00 for normal regeneration**. You still touch
it only when archaeology demands the pre-v02 copy of a script —
`v00/makotemplates/` holds the older `updateByLine.py` / `parseheadline.py`
generation referenced by some dictionary repos' vendored copies. New work goes
to `v02/` exclusively. The root `redo.sh` is likewise an older broad
regeneration wrapper; prefer the `v02/redo_*` drivers.

### 7.4 Bulk and selective regeneration

- `redo_cologne_all.sh` / `redo_xampp_all.sh` — every dictionary, server vs
  local layout.
- `redo_xampp_selective.py` — only dictionaries whose csl-orig `.txt` changed
  since the last run (state in `csl-orig/v02/.xampp_last_run`), then Stardict/
  JSON/homepage downstream pushes. Full flag reference and the
  server-rehearsal caveat:
  [`v02/readme_selective.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme_selective.md).
  `redo_xampp_selective.sh` survives only as the cron-compatible wrapper.
- `cologne_flag`: `generate.py` sets it by detecting whether the repo path
  starts with `/nfs/` (true only on the Cologne server); templates branch on
  it for mw-specific server behaviour.

## 8. Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| `python3: command not found` (Git Bash, Windows) | scripts hardcode `python3`; Windows exposes `python` | add a `python3` shim to PATH (§7.1) |
| `KeyError: '<dict>'` from `generate.py` | code not registered in `dictparms.py` | §7.2 step 1 |
| `generate.py. ERROR CD copyfile. filename1=distinctfiles/<dict>/…` | an `inventory.txt` row promises a per-dict file that `distinctfiles/<dict>/pywork/` doesn't have (or the code was added to a row it shouldn't be on) | create the file or fix the inventory row |
| Stage 1 red output about missing `<dict>_hwextra.txt` etc. | `csl-orig/v02/<dict>/` lacks one of the four input files | fix csl-orig side first — the input contract is those four files (§4 stage 1) |
| `generate_web.sh` stage dies / `No such file or directory: ../../csl-websanlexicon` | sibling checkout missing or misplaced | clone csl-websanlexicon beside csl-pywork (§1 layout) |
| No `All records parsed by ET` line | `make_xml.py` hit malformed entry markup — the XML is broken | read the red lines above it; fix source markup via a change file (§6), regenerate |
| Red `BEGIN xmllint_err` block | generated XML violates the DTD | the cited line numbers are in `<dict>.xml`; trace back to source text or to `make_xml.py`'s per-dict logic |
| `xmllint: command not found` | libxml2-utils not installed | install it, or use the lxml fallback (§5) |
| `xmlchk_xampp.sh` fails: `xmlvalidate.py` not found | it expects `../../xmlvalidate.py` above the repos | copy `v02/utilities/xmlvalidate.py` there; `pip install lxml` |
| `CHANGE ERROR #2: Old mismatch` from `updateByLine.py` | change file written against an older text state, or BOM/`\r` contamination | re-derive against current text; strip BOM (§6) |
| `Expected EVEN number of lines` | a transaction is missing its pair line (`del` still needs its `old`) | fix the change file (§6) |
| An edit made inside a generated `outdir/pywork/` vanished after regeneration | vendor rule: `C`/`T` overwrite, `D` deletes | make the change in `makotemplates/` or `distinctfiles/<dict>/` here (§2) |
| Red lines during `redo_hw.sh` / sqlite stage that look informational | the awk whitelist only knows the standard progress lines; per-dict oddities print red | read them once; if genuinely benign and recurring, extend the whitelist in `generate_dict.sh` / the stage template |
| `Unexpected <H>:` lines (vcp) | known vcp digitisation quirk | whitelisted as normal for vcp only — ignore |
| Generated output looks stale despite a fresh run | you regenerated into a different `<outdir>` than the one the web server serves | check the XAMPP path convention (`../../<dict>`), rerun |

## 9. Glossary

| Term | Meaning |
|---|---|
| dict code | lowercase dictionary identifier (`mw`, `pwg`, `ap90`); registry = `dictparms.py` |
| metaline | the `<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1` key-value line opening every entry in `<dict>.txt`, parsed by `parseheadline.py` |
| L / L-number | stable entry identifier within a dictionary; duplicate L in one text is a hard error |
| k1 / k2 | headword keys (k1 = the lookup key, k2 = a variant/display form), SLP1-encoded |
| pc | page-column reference into the printed scan |
| h | homonym number (`hom` → `h`) |
| hwextra | extra headwords file (`<dict>_hwextra.txt`) merged in by `hw.py` |
| meta2 | `<dict>-meta2.txt`, dictionary-level metadata copied at stage 1 |
| C / T / CD / D | inventory categories: copy shared / render Mako template / copy per-dict distinct / delete obsolete (§3) |
| makotemplates/ | the shared template pool — the canonical source of every vendored script |
| distinctfiles/ | per-dictionary overrides and data inputs, keyed by dict code |
| dictversion + microversion | version stamp rendered into generated headers; `microversion` (in `dictparms.py`) bumps on cross-dictionary template changes |
| cologne_flag | True when running on the Cologne server (`/nfs/…` path); templates branch on it |
| SLP1 | the ASCII transliteration scheme the source texts use for Sanskrit |
| pywork | the per-dictionary working directory of generated scripts + artifacts (this repo's namesake) |
| webtc2 | the advanced-search query-dump builder run in `redo_postxml.sh` |
| ab / auth | abbreviation and literary-source (tooltip/bibliography) SQLite table families |

## 10. Maintainer appendix

- **Invariants.** The four-file csl-orig contract (§4 stage 1) is the entire
  input surface; everything under an `<outdir>` is derived and disposable;
  `makotemplates/` + `distinctfiles/` + `inventory.txt` + `dictparms.py`
  fully determine `outdir/pywork/`; bump `microversion` whenever a
  cross-dictionary template change ships (§9).
- **CI.** [`ci.yml`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/.github/workflows/ci.yml)
  plus a committed-XML parse check
  ([`xml-parse.yml`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/.github/workflows/xml-parse.yml))
  — the latter skips Mako templates and tolerates multi-root fragments by
  design. `readme-guard.yml` protects the regeneration-safe README markers:
  the README's `BEGIN MANUAL: overview` block is hand-maintained; content
  outside it may be tool-refreshed.
- **Quirks observed while writing this manual (28-07-2026),** candidates for
  cleanup, none load-bearing: `generate_pywork.sh`'s usage message says
  `generate_orig.sh`; `xmlchk_xampp.sh` depends on an out-of-repo
  `../../xmlvalidate.py` while the same file ships in-repo at
  `v02/utilities/xmlvalidate.py` (§5 documents the copy step); the root
  `redo.sh` and `dbg_test.txt` are legacy residue.
- **Where correction work goes.** Agents never commit or push directly to
  csl-orig; corrections are validated locally (this manual §5–§6) and shipped
  as one consolidated monthly PR via the csl-corrections queue — see the
  [correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).
- **Issue taxonomy.** Tooling-repo taxonomy per
  [CLAUDE.md](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/CLAUDE.md);
  org-wide pipeline context in the
  [Cologne tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md).

---

_Dr. Mārcis Gasūns_
