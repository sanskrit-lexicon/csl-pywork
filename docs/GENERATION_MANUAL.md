# csl-pywork generation manual — from csl-orig text to a served dictionary

_Created: 28-07-2026 · Last updated: 29-07-2026_

This is the operator manual for the **canonical CDSL dictionary-generation
pipeline** that lives in this repository. It exists so that a new operator can
regenerate one dictionary's artifacts end-to-end — headword list, XML, SQLite
databases, web display, download archives — **without reading every script**.
The acceptance test for this manual: a newcomer runs
[`generate_dict.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_dict.sh)
for one dictionary from this document alone and knows what to validate at the
end.

Scope boundaries — link, don't re-derive:

- **Correcting** dictionary text (snapshot → apply → regenerate → validate →
  audit → commit) is owned by
  [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).
  This manual covers only the *generation* machinery that workflow drives, plus
  the [`updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/updateByLine.py)
  change-file engine it relies on. Agent-side delivery into csl-orig stays
  **queue + monthly batched PR** — never direct commits, never PR noise.
- The **web display** stage is owned by the sibling repo; its operator manual is
  [csl-websanlexicon/docs/WEB_FRONTEND_MANUAL.md](https://github.com/sanskrit-lexicon/csl-websanlexicon/blob/main/docs/WEB_FRONTEND_MANUAL.md).

---

## 1. Cheat-sheet

All commands run from `csl-pywork/v02/` in a bash shell (Git Bash on Windows).

```bash
# Generate (or fully refresh) ONE dictionary into a target directory
sh generate_dict.sh mw ../../MWScan/2020        # Cologne-style scan directory
sh generate_dict.sh acc tempparent/acc          # local throwaway build

# Validate the generated XML against its DTD (XAMPP layout)
sh xmlchk_xampp.sh mw

# Apply a correction change-file to a source text (the correction engine)
python3 makotemplates/pywork/updateByLine.py <in.txt> <changes.txt> <out.txt>

# Regenerate EVERYTHING (server-scale, slow)
sh redo_cologne_all.sh          # Cologne server layout
sh redo_xampp_all.sh            # local XAMPP layout
sh redo_xampp_selective.sh      # only dictionaries changed in csl-orig since last run

# Run the regression tests (from repo root)
python3 -m pytest tests/
```

Dictionary codes (lowercase): `acc ae ap ap90 ben bhs bop bor bur cae ccs gra
gst ieg inm krm lan mci md mw mw72 mwe pd pe pgn pui pw pwg pwkvn sch shs skd
snp stc vcp vei wil yat`, plus newer additions `armh lrv abch acph acsj fri`.
The authoritative registry is
[`v02/dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/dictparms.py).

---

## 2. The big picture — data flow

Three sibling repositories must be checked out in the same parent directory
(called `cologne/` on servers, `htdocs/cologne/` under XAMPP):

```
cologne/
  csl-orig/           ← source digitisation text (canonical input)
  csl-pywork/         ← this repo: build scripts + templates
  csl-websanlexicon/  ← web display code generation (stage 4)
  mw/  acc/  ...      ← generated per-dictionary output trees
```

One `generate_dict.sh <dict> <outdir>` run flows like this:

```
csl-orig/v02/<dict>/                 csl-pywork/v02/
  <dict>.txt          ─┐
  <dict>_hwextra.txt   ├─ Stage 1 generate_orig.sh ──→ <out>/orig/, <out>/pywork/
  <dict>header.xml     │
  <dict>-meta2.txt    ─┘
                          Stage 2 generate_pywork.sh ─→ <out>/pywork/      (inventory.txt: C/T/CD/D)
                          Stage 3 generate_ab_bib_ls.sh → <out>/pywork/<dict>ab/, <dict>auth/
                          Stage 4 generate_web.sh ────→ <out>/web/         (runs in csl-websanlexicon/v02)

                          then EXECUTES the assembled scripts in <out>/pywork/:
                          redo_hw.sh   → <dict>hw.txt (+ hw2, hw0)
                          redo_xml.sh  → <dict>.xml  (xmllint-validated against <dict>.dtd)
                          redo_postxml.sh → web/sqlite/<dict>.sqlite + ab/auth/ls databases
                          downloads/redo_all.sh → txt/xml/web zip archives
```

The finished tree at `<outdir>` is a self-contained dictionary installation:

```
<outdir>/
  orig/       ← source text copied from csl-orig
  pywork/     ← generated build scripts + derived artifacts (hw, xml, dtd, sqlite)
  web/        ← display code (from csl-websanlexicon)
  downloads/  ← zip archive generation scripts + archives
```

Served locally at `http://localhost/cologne/<dict>/web/` under XAMPP.

---

## 3. Environment and prerequisites

From [`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md):

- **Python 3** + `mako` (`pip install mako`) — templating and all pipeline scripts
- **bash** — orchestration (`generate_*.sh`, `redo_*.sh`)
- **sqlite3**, **xmllint** (libxml2-utils), **zip** — databases, XML validation, downloads
- **PHP** (CLI + pdo + sqlite3) — web display generation
- **git**; a web server (apache2 or XAMPP) to serve displays locally
- `lxml` if you want [`utilities/xmlvalidate.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/utilities/xmlvalidate.py)
  DTD validation (see §6)

Ubuntu one-shot install and the XAMPP/Windows specifics (where to put
`sqlite3.exe` and `zip.exe`, GoW) are in
[`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md) —
follow those verbatim rather than improvising.

Windows notes that bite in practice:

- Scripts invoke `python3`. Git Bash on Windows usually ships only `python` —
  either install Python so `python3.exe` exists on `PATH`, or create a shim
  (`python3` → `python`) before running anything.
- Run the `.sh` scripts under **Git Bash** (or WSL/apache-less bash), never
  PowerShell/cmd.
- Line endings: the repo has no `.gitattributes` yet
  ([issue #52](https://github.com/sanskrit-lexicon/csl-pywork/issues/52)) —
  keep generated and change files **LF**, and never introduce a UTF-8 BOM
  (see §7 traps).

---

## 4. The canonical input contract (`csl-orig/v02/<dict>/`)

Generation reads exactly four files per dictionary from the sibling
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig) repository, per
[`v02/inventory_orig.txt`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/inventory_orig.txt):

| File in `csl-orig/v02/<dict>/` | Copied to | Role |
|---|---|---|
| `<dict>.txt` | `<out>/orig/` | The digitised dictionary text — the single source of truth |
| `<dict>_hwextra.txt` | `<out>/pywork/hwextra/` | Extra headwords not derivable from the text |
| `<dict>header.xml` | `<out>/pywork/` | XML header/metadata block, later copied into `web/` |
| `<dict>-meta2.txt` | `<out>/pywork/` | Dictionary metadata |

Two hard rules follow from this contract:

1. **Never edit generated output to fix content.** A content fix belongs in
   `csl-orig` (via the correction workflow, as a change file — §7); regeneration
   overwrites anything you hand-edit downstream.
2. **Never commit or push directly to csl-orig.** Corrections are queued
   locally and shipped as one consolidated PR at most ~monthly (see the
   [correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)).

---

## 5. Step by step: `generate_dict.sh <dict> <outdir>`

Entry point:
[`v02/generate_dict.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_dict.sh).
`<dict>` is the lowercase code; `<outdir>` is created if absent. Everything
below happens in one invocation, in order.

### Stage 1 — `generate_orig.sh` (copy the source)

[`v02/generate_orig.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_orig.sh)
runs [`generate.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate.py)
against `../../csl-orig/v02/<dict>` with
[`inventory_orig.txt`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/inventory_orig.txt),
populating `<out>/orig/` and `<out>/pywork/` with the four input files of §4.

### Stage 2 — `generate_pywork.sh` (assemble the build scripts)

[`v02/generate_pywork.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_pywork.sh)
runs `generate.py <dict> inventory.txt makotemplates distinctfiles/<dict> <outdir>`.
[`inventory.txt`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/inventory.txt)
is the manifest of what lands in `<out>/pywork/`, with one category letter per
file:

| Category | Meaning | Source |
|---|---|---|
| `C` | **Copy** verbatim | [`v02/makotemplates/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/makotemplates) |
| `T` | **Template** — rendered by Mako with the dictionary's parameters | `v02/makotemplates/` + [`dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/dictparms.py) |
| `CD` | **Copy distinct** — per-dictionary override | [`v02/distinctfiles/<dict>/pywork/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/distinctfiles) |
| `D` | **Delete** from the target if present (removes obsolete generated files) | — |

Inventory record syntax: `dicts:path[:new-path]:category`, `;` starts a
comment, `*` in the dicts field means "all dictionaries", and a two-path form
renames on the way out (e.g. `pywork/one.dtd pywork/${dictlo}.dtd:T` — one
shared DTD template becomes each dictionary's `<dict>.dtd`).

The Mako context comes from `dictparms.py`: `dictup`, `dictlo`, `dictname`,
`dictversion`, plus a global `microversion` string appended to `dictversion` in
generated headers, a generation date stamp (`dictmmddyyyy`), and the
server-vs-local `cologne_flag`. A dictionary code missing from `dictparms.py`
fails immediately (`KeyError: '<dict>'` — the registry is the gate). **Maintainers bump `microversion` whenever a
cross-dictionary template change is deployed** — that is how template-level
changes are tracked in generated output without touching each dictionary's
version.

One template gets special treatment:
[`make_xml.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/make_xml.py)
is pre/post-processed (not plain-rendered) because the dictionary text contains
literal `<%s>`/`</%s>` XML tags that Mako would otherwise parse as its own
syntax; inside the template they are escaped as `!!!s!!!` / `!!!/s!!!` / `!!!##!!!`
(see [`utilities/preprocess_mako.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/utilities/preprocess_mako.py)).
Per-dictionary logic inside shared templates is guarded by
`%if dictlo == '...'`/`%endif` blocks.

### Stage 3 — `generate_ab_bib_ls.sh` (abbreviation / tooltip / bibliography)

[`v02/generate_ab_bib_ls.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_ab_bib_ls.sh)
generates the `redo.sh` + SQL scripts for the abbreviation (`ab`), literary
source tooltip (`ls`), and bibliography/authority (`auth`) SQLite tables into
`<out>/pywork/<dict>ab/` and `<out>/pywork/<dict>auth/` — only for the
dictionaries that have those tables (the lists live in the script and in
[`redo_postxml.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/redo_postxml.sh)).

### Stage 4 — `generate_web.sh` (display code, from the sibling repo)

`generate_dict.sh` resolves `<outdir>` to an absolute path, changes into
`../../csl-websanlexicon/v02`, and runs that repo's `generate_web.sh`, which
assembles `<out>/web/` using the **same C/T/CD/D inventory model** from its own
`inventory.txt` and `makotemplates/`. Details, display architecture, and
web-side troubleshooting: the
[web front-end manual](https://github.com/sanskrit-lexicon/csl-websanlexicon/blob/main/docs/WEB_FRONTEND_MANUAL.md).
If `csl-websanlexicon` is not a sibling checkout, this stage fails.

### Stage 5 — execute the assembled pipeline in `<out>/pywork/`

| Script | Runs | Output |
|---|---|---|
| [`redo_hw.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/redo_hw.sh) | [`hw.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/hw.py) (+ `hw2.py`, `hw0.py`) on `../orig/<dict>.txt` + `hwextra/<dict>_hwextra.txt` | `<dict>hw.txt` headword list (+ `<dict>hw2.txt`, `<dict>hw0.txt`; for `mw` also `mwkeys.sqlite`) |
| [`redo_xml.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/redo_xml.sh) | `make_xml.py ../orig/<dict>.txt <dict>hw.txt <dict>.xml`, then `xmllint --noout --valid` | `<dict>.xml`, DTD-validated against `<dict>.dtd` |
| [`redo_postxml.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/redo_postxml.sh) | copies `<dict>header.xml` to `../web/`; `sqlite/redo.sh`; `webtc2/redo.sh`; the `ab`/`auth`/`ls` redos where applicable | `web/sqlite/<dict>.sqlite` (display database), `webtc2` query dump (advanced search), abbreviation/tooltip/bibliography databases |
| `downloads/redo_all.sh` | `redo_txt.sh`, `redo_xml.sh`, `redo_web.sh` | `<dict>txt.zip`, `<dict>xml.zip`, `<dict>web1.zip` download archives |

### Reading the output — the red/plain convention

`generate_dict.sh` filters every stage's output through `awk` whitelists:
**known-good lines print plain; anything unexpected prints in red.** A fully
healthy run is therefore a stream of plain `BEGIN`/`END` markers, counts, and
the green signals below — any red line is worth reading, even when the run
continues.

Green signals to check after a run:

- `N lines read from ../orig/<dict>.txt`, `N entries found`,
  `N lines written to <dict>hw.txt` — headword stage healthy
- `All records parsed by ET` — `make_xml.py` parsed every generated record
  with Python's ElementTree (§6)
- **No** `BEGIN xmllint_err` block — xmllint found the XML valid against the DTD
- `N rows written to <dict>.sqlite` — display database rebuilt
- (`vcp` only) `Unexpected <H>:` lines are whitelisted as expected

---

## 6. XML validation — xmllint, ET, and the Windows fallback

Three validation layers exist; know which one you are looking at:

1. **In-pipeline ET parse.** `make_xml.py` itself parses each record with
   `xml.etree.ElementTree` while writing `<dict>.xml`. Its
   `All records parsed by ET` line is the first green signal — it means every
   entry is well-formed XML. This runs everywhere Python runs, including
   Windows, with no extra tooling.
2. **xmllint DTD validation.** `redo_xml.sh` then runs
   `xmllint --noout --valid <dict>.xml`, validating against `<dict>.dtd`
   (rendered from the shared
   [`one.dtd`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/one.dtd)
   template). Silence is success; errors surface in a red `BEGIN xmllint_err`
   block. On Windows, `xmllint` is often absent — the run still completes, and
   you fall back to layer 1 + layer 3.
3. **Standalone re-validation:**
   [`v02/xmlchk_xampp.sh <dict>`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/xmlchk_xampp.sh)
   validates `../../<dict>/pywork/<dict>.xml` against its DTD using
   [`xmlvalidate.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/utilities/xmlvalidate.py)
   (lxml-based). Note the script expects `xmlvalidate.py` at `../../` relative
   to `v02/` — i.e. in the `cologne/` parent directory. Copy it there once from
   `v02/utilities/` (and `pip install lxml`). Output `ok` is the pass signal.

Rule of thumb: **"All records parsed by ET" plus a clean xmllint (or
`xmlvalidate.py` "ok") is the green light**; ET-parse success alone proves
well-formedness, not DTD validity.

---

## 7. Correcting text: the `updateByLine.py` change-file format

[`updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/updateByLine.py)
is the engine that applies corrections to a dictionary text. It is vendored
into every dictionary repo, but **this copy is the source of truth** (§8). The
end-to-end correction procedure (when to snapshot, where change files live,
how they are audited and shipped) is the
[correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md);
this section covers only the file format and its traps.

```bash
python3 updateByLine.py <input.txt> <changes.txt> <output.txt>
```

The change file is UTF-8, made of **line pairs**. Each pair shares one line
number `nn` (1-based, in the **input** file); the first line is always
`nn old <exact current text>`, the second is one of `new` / `ins` / `del`:

```
; comment lines start with a semicolon and are skipped
; --- replace line 1234 ---
1234 old the line exactly as it appears in input.txt
1234 new the corrected replacement line
; --- insert a line AFTER line 2000 ---
2000 old the line after which to insert
2000 ins the newly inserted line
; --- delete line 3456 (note the space after 'del') ---
3456 old the line to be removed
3456 del 
```

Semantics and traps, in the order they will bite you:

- **`old` must match exactly.** The script compares the `old` text against the
  input line byte-for-byte; a mismatch aborts with
  `CHANGE ERROR #2: Old mismatch`. The usual causes: the input file moved on
  upstream since the change file was written (regenerate against a fresh
  snapshot), an invisible BOM, or trailing-whitespace drift.
- **All line numbers refer to the ORIGINAL input file.** `ins` and `del` do not
  shift the numbering of later changes — the script applies everything against
  the input's line indexing, so you never renumber a change file to compensate
  for earlier insertions/deletions.
- **`ins` inserts AFTER line `nn`.** The `old` line of the pair is the anchor
  line itself.
- **`del` ignores its text part** — leave it blank, and keep the space after
  `del` (`3456 del `).
- **Even line count.** Non-comment lines must pair up; an odd count aborts with
  `Expected EVEN number of lines`.
- **No BOM, LF endings.** The parser reads plain UTF-8; a UTF-8 BOM at the top
  of a change file makes the first `old` comparison fail invisibly. (The
  pipeline's own readers were hardened to `utf-8-sig` for *source* files on
  30-05-2026 precisely because a BOM once broke `hw.py` — do not reintroduce
  the class.) CRLF is tolerated on read (`rstrip('\r\n')`) but keep files LF
  for git hygiene ([issue #52](https://github.com/sanskrit-lexicon/csl-pywork/issues/52)).
- **After applying:** regenerate the dictionary (`generate_dict.sh`) and
  validate (§6) — a change that produces well-formed text can still break XML
  or headword extraction downstream.
- **The run summary is your audit line.** A successful run prints
  `N records written to <output>` plus a count per transaction type
  (`new`/`ins`/`del`) — quote it when parking a correction in the
  csl-corrections queue.

Regression coverage for this engine lives in
[`tests/test_updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/tests/test_updateByLine.py) —
extend it when you touch the script.

---

## 8. The vendor rule — fix here first, copy outward, never fork

The pipeline scripts (`updateByLine.py`, `make_xml.py`, `parseheadline.py`,
`digentry.py`, `hw*.py`, the `redo_*.sh` templates) are **vendored** — copied,
never forked-and-edited — into the individual dictionary repos across the
[sanskrit-lexicon org](https://github.com/sanskrit-lexicon) (pwg, mws, ap90, …).

- A bug fix or improvement lands **in this repo first**
  ([`v02/makotemplates/pywork/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/makotemplates/pywork),
  or [`v00/makotemplates/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v00/makotemplates)
  for repos still on the older copies), then propagates outward by re-copying.
- **Never edit a vendored copy in a dictionary repo as if it were the source
  of truth** — the next regeneration or re-vendor sweep silently reverts it.
- If you find a dictionary repo's copy diverged (it happens), diff it against
  this repo's template: genuinely per-dictionary logic belongs in
  `distinctfiles/<dict>/` or a `%if dictlo == '...'` guard here, not in a
  drifted fork.

---

## 9. `v00` vs `v02`

[`v00/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v00) is the
older generation pipeline; [`v02/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02)
is current production. Operators still touch `v00` in exactly one case: some
dictionary repos vendor the **older** `updateByLine.py` / `parseheadline.py`
from [`v00/makotemplates/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v00/makotemplates) —
when fixing those, fix the `v00` copy (and prefer migrating the consumer to
the `v02` version). Everything else in `v00` is historical reference; new work
never starts there. The root
[`redo.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/redo.sh)
is likewise an older broad-regeneration script kept for reference.

---

## 10. Bulk regeneration and the selective auto-update

- [`redo_cologne_all.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_cologne_all.sh) /
  [`redo_xampp_all.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_xampp_all.sh) —
  regenerate every dictionary for the Cologne-server or local-XAMPP layout.
  Slow; use for full rebuilds only.
- [`redo_xampp_selective.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_xampp_selective.sh)
  (+ [`redo_xampp_selective.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_xampp_selective.py)) —
  the cron/boot auto-updater. It tracks the last-processed csl-orig commit in
  `csl-orig/v02/.xampp_last_run`, regenerates only dictionaries whose `.txt`
  changed, then rebuilds and pushes Stardict (`cologne-stardict`,
  `indic-dict/stardict-sanskrit`) and JSON (`csl-json`) outputs and refreshes
  the homepage. Extra sibling repos + cached git credentials required — see
  [`v02/readme_selective.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme_selective.md)
  and [`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md).
  `python3 redo_xampp_selective.py --dry-run` rehearses a run without touching
  anything. Modernisation of this script is tracked in
  [issue #53](https://github.com/sanskrit-lexicon/csl-pywork/issues/53).

---

## 11. Symptom → cause → cure

| Symptom | Likely cause | Cure |
|---|---|---|
| Red lines in `generate_dict.sh` output | The awk whitelists flag any unexpected line | Read the red text — it is the actual error; plain lines are known-good |
| `usage: sh generate_dict.sh <dict> <parent-dir>` | Missing/empty arguments | Pass lowercase dict code + target dir |
| Stage 4 fails, `<out>/web/` missing or empty | `csl-websanlexicon` is not a sibling checkout | Clone it next to csl-pywork; see §2 layout |
| `KeyError: '<dict>'` from `generate.py` | Code not registered in [`dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/dictparms.py) | Add the registry entry (§13 adding a dictionary) |
| `generate.py. ERROR CD copyfile. filename1=distinctfiles/<dict>/…` | An `inventory.txt` row promises a per-dict file `distinctfiles/<dict>/pywork/` doesn't have | Create the file, or take the dict code off that inventory row |
| Stage 1 red output about a missing input file | `csl-orig/v02/<dict>/` lacks one of the four §4 files | Fix the csl-orig side first — those four files are the whole input contract |
| `ModuleNotFoundError: mako` | Mako not installed | `pip install mako` |
| `python3: command not found` (Windows Git Bash) | Windows Python installs as `python` | Put a `python3` shim on `PATH` |
| `xmllint: command not found` | libxml2-utils absent (typical on Windows) | Rely on the ET parse + `xmlchk_xampp.sh`/`xmlvalidate.py` (§6), or install libxml2 |
| `xmlchk_xampp.sh`: no such file `../../xmlvalidate.py` | The checker expects the script in the `cologne/` parent dir | Copy [`v02/utilities/xmlvalidate.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/utilities/xmlvalidate.py) there; `pip install lxml` |
| `BEGIN xmllint_err` block in redo_xml output | Generated XML violates the DTD | Read the first error; usually a markup defect in the source text or a `make_xml.py` regression — fix in csl-orig (correction workflow) or in the template here, never in `<dict>.xml` |
| `CHANGE ERROR #2: Old mismatch` from `updateByLine.py` | Change file drifted from the input (upstream edit, BOM, whitespace) | Regenerate the change file against the current source; strip BOM |
| `Expected EVEN number of lines` | A change pair lost its partner, or a comment lacks the leading `;` | Fix the change file pairing |
| First line of a source file misbehaves in `hw.py`-era scripts | UTF-8 BOM in the input | Strip the BOM; keep all pipeline files BOM-less |
| `sqlite3`/`zip: command not found` (Windows) | CLI tools not on `PATH` | Install per [`v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md) §XAMPP |
| Output looks stale / fix not visible | Regeneration not rerun, csl-orig checkout behind, or you regenerated into a different `<outdir>` than the one the web server serves | `git -C ../csl-orig pull`, rerun `generate_dict.sh` into the served path (`../../<dict>` under XAMPP); on servers check `.xampp_last_run` |
| Recurring benign red lines for one dictionary | The awk whitelists only know the standard progress lines | Read them once; if genuinely benign and recurring, extend the whitelist in `generate_dict.sh` or the stage template |
| `Unexpected <H>:` lines for `vcp` | Known, whitelisted quirk of that dictionary | Ignore (plain, not red) |
| Edits to a generated `<out>/pywork/` file keep disappearing | You edited generated output; C/T/CD/D reassembly overwrites it | Move the change into `makotemplates/` (shared), `distinctfiles/<dict>/` (per-dict), or csl-orig (content) |

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **dict code** | Lowercase dictionary identifier (`mw`, `pwg`, `skd`, …) keying everything: input dir, dictparms entry, output tree |
| **metaline** | The `<L>16850<pc>292-3<k1>visarga<k2>visarga<h>1` key-value line opening every entry in `<dict>.txt`, parsed by `parseheadline.py`; key order is irrelevant |
| **L / L-number** | Stable entry identifier within a dictionary (the `<L>` field) |
| **k1 / k2** | Headword keys — `k1` the lookup key, `k2` a variant/display form, SLP1-encoded |
| **pc / h** | Page-column reference into the printed scan / homonym number |
| **SLP1** | The ASCII transliteration scheme the source texts use for Sanskrit |
| **orig** | `<out>/orig/` — the copied source digitisation text; also shorthand for csl-orig itself |
| **pywork** | `<out>/pywork/` — the generated per-dictionary build directory (scripts + derived artifacts); the repo is its template |
| **hw / hwextra** | Headword list `<dict>hw.txt` extracted by `hw.py`; `_hwextra.txt` supplies headwords not present in the text |
| **header.xml / meta2** | Per-dictionary XML header and metadata files from csl-orig, carried into pywork/web |
| **C / T / CD / D** | Inventory categories: Copy, Template (Mako), Copy-Distinct (per-dict override), Delete (§5 stage 2) |
| **makotemplates** | Shared file pool rendered/copied into every dictionary's pywork ([`v02/makotemplates/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/makotemplates)) |
| **distinctfiles** | Per-dictionary overrides ([`v02/distinctfiles/<dict>/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/distinctfiles)) |
| **dictparms / microversion** | Central dictionary registry + the suffix bumped on every cross-dictionary template deployment (§5 stage 2) |
| **one.dtd** | The single shared DTD template rendered to each `<dict>.dtd` |
| **cologne_flag** | Template variable: true when generating on the Cologne server (`/nfs/...` path), selects server-vs-local branches |
| **webtc2 / query_dump** | Advanced-search database rebuilt by `redo_postxml.sh` |
| **ab / ls / auth** | Abbreviation, literary-source tooltip, and bibliography/authority SQLite tables (§5 stage 3) |
| **XAMPP layout** | Local Windows serving layout `htdocs/cologne/…` mirroring the Cologne server (§2) |
| **vendoring** | Copying pipeline scripts from this repo into dictionary repos — never fork-editing them there (§8) |
| **change file** | The `old`/`new`/`ins`/`del` line-pair file applied by `updateByLine.py` (§7) |

---

## 13. Maintainer appendix

- **Tests:** `python3 -m pytest tests/` from the repo root —
  [`test_updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/tests/test_updateByLine.py)
  (CLI contract of the correction engine),
  [`test_dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/tests/test_dictparms.py)
  (registry integrity),
  [`test_redo_xampp_selective.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/tests/test_redo_xampp_selective.py).
  CI ([`ci.yml`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/.github/workflows/ci.yml))
  additionally runs a committed-XML well-formedness check via
  [`xml-parse.yml`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/.github/workflows/xml-parse.yml)
  (skips Mako templates, tolerates multi-root fragments by design), and
  [`readme-guard.yml`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/.github/workflows/readme-guard.yml)
  protects the README's regeneration-safe markers — content inside the
  `BEGIN MANUAL: overview` block is hand-maintained; content outside it may be
  tool-refreshed.
- **Adding a dictionary:** register the code in `dictparms.py` first —
  `generate.py` indexes `alldictparms[dictcode]`, so an unregistered code is an
  immediate `KeyError`. Then create `distinctfiles/<dict>/pywork/` with the
  per-dict files, add the code to the explicit (non-`*`) `inventory.txt` rows
  that apply, extend the dict lists in
  [`generate_ab_bib_ls.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_ab_bib_ls.sh)
  and `redo_postxml.sh`'s conditionals if it has ab/ls/auth tables, and confirm
  the four §4 input files exist in csl-orig.
- **Cosmetic quirks** (observed 28-07-2026, none load-bearing):
  `generate_pywork.sh`'s usage message says `generate_orig.sh`;
  `xmlchk_xampp.sh` depends on an out-of-repo `../../xmlvalidate.py` while the
  same file ships in-repo (§6 documents the copy step); the root `redo.sh` and
  `dbg_test.txt` are legacy residue.
- **Template changes:** any edit under `v02/makotemplates/` that affects all
  dictionaries ⇒ bump `microversion` in
  [`dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/dictparms.py)
  in the same commit, then re-vendor to consuming repos (§8). Test-render at
  least one dictionary into `tempparent/` before pushing.
- **Utilities:**
  [`v02/utilities/`](https://github.com/sanskrit-lexicon/csl-pywork/tree/main/v02/utilities) —
  `xmlvalidate.py` (lxml DTD check), `check_xml_tags.py` / `all_tags.py`
  (tag inventories), `preprocess_mako.py` (the `make_xml.py` escaping).
- **Entry-level tooling:**
  [`digentry.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/digentry.py)
  (dig a single entry out of a text) and
  [`parseheadline.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/parseheadline.py)
  (parse the `<L>`-line metadata) are the two most commonly vendored helpers
  after `updateByLine.py`.
- **Known open debt:** [issue #52](https://github.com/sanskrit-lexicon/csl-pywork/issues/52)
  (no `.gitattributes`), [issue #53](https://github.com/sanskrit-lexicon/csl-pywork/issues/53)
  (modernise `redo_xampp_selective.sh`), [issue #63](https://github.com/sanskrit-lexicon/csl-pywork/issues/63)
  (master/main branch confusion — the default branch is `main`).
- **Improvement backlog for this manual:** see
  [`docs/GENERATION_MANUAL.meta.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/docs/GENERATION_MANUAL.meta.md).

_Dr. Mārcis Gasūns_
