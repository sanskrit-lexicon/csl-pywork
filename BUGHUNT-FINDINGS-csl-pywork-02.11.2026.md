# Nightly Bug Hunt — csl-pywork — 02.11.2026

_Created: 02-11-2026 · Last updated: 02-11-2026_

Nightly one-repo bug hunt (MG ruling 26-09-2026): Phase 1 read-only static hunt of
`src/tools/scripts/plugins`-equivalent code (`v02/`, `scripts/`, `tests/`, `v00/install.py`,
root shells; Mako `%`-templates excluded from py_compile as expected), Phase 2 this report,
Phase 3 auto-fix lane.

**Elapsed: ~20 min hunt + ~10 min landing. Executor: GLM 5.3 Flash (zai-coding-plan/glm-5.3-flash).**

## Verdict

**0 HIGH · 2 MEDIUM · 3 LOW · 1 refuted lead.** No committed secrets, no races, no crash-class
bugs found. **Auto-fix lane (Phase 3) not triggered — no HIGH code findings.** One strong
static lead (the changelog guard's sha handling) was disproven by a live A/B probe and is
recorded below so a future hunt does not "fix" correct code.

## What verified green

- `python3 -m pytest tests/ -q` — **276 passed in 63.20s** at origin/main `23b3791`.
- `python3 -m compileall` over `v02/*.py`, `scripts/`, `tests/`, `v00/install.py` — clean
  (only `v02/makotemplates/**` fail, which is Mako directive syntax, not Python).
- Secret scan (`api_key|secret|password|token\s*=` over Python + shells) — no hits.
- Live A/B on the changelog guard (below): control path works, refuted-lead path works as designed.

## MEDIUM

### M1. `redo_cologne_all.sh` ignores per-dict failures — partial regeneration exits 0

[scripts and loop](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_cologne_all.sh)
(`v02/redo_cologne_all.sh`, all ~37 invocation lines, e.g. lines 22-56; no `set -e`, no `$?` checks).

`generate_dict.sh` was deliberately hardened fail-closed (P5): on any stage failure it prints a
red `STOP generate_dict.sh:` marker and exits nonzero "so callers never build on a half-assembled
tree". But its own all-dictionaries driver neither checks exit statuses nor sets `set -e`: a failed
dict 3 of 37 does not stop dicts 4-37, the shell exits 0 at the end, and nothing downstream in this
repo consumes the STOP marker. A half-regenerated tree reads as a successful full run.

Live evidence: `tail -30 v02/redo_cologne_all.sh` — plain sequential `sh generate_dict.sh …`
lines, last statement is the final invocation; `bash -n` clean, no status handling anywhere.
Report-only per hunt fence (MEDIUM).

### M2. `xmlchk_xampp.sh` points at a validator path this repo never ships

[xmlchk_xampp.sh](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/xmlchk_xampp.sh)
(lines 15-19) builds `cmd="python3 ../../xmlvalidate.py $xml $dtd"`, but `xmlvalidate.py` lives at
[v02/utilities/xmlvalidate.py](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/utilities/xmlvalidate.py);
nothing in the repo installs a copy two levels above `v02/`.

Live evidence: `ls v02/../../xmlvalidate.py` → `No such file or directory` on a full checkout.
Dead config wiring: the XAMPP validation step only works if an operator hand-placed a copy at
`/var/www/html/xmlvalidate.py`. Also word-splits unquoted `$cmd` (paths with spaces break).
Report-only per hunt fence (MEDIUM).

## LOW

### L1. `generate.py` `makedirs()` swallows every exception

[v02/generate.py line 57-65](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate.py):
`except Exception: pass` under `os.makedirs(dirname)` treats "already exists" and real failures
(permission denied, ENOSPC) identically; a later `copyfile` then fails with a confusing error.
Legacy upstream code; report-only.

### L2. Stray committed files at repo root: `dbg_test.txt`, `redo.sh`

[dbg_test.txt](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/dbg_test.txt)
(content: "a test file to track git") and
[redo.sh](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/redo.sh) — the latter is a v00-era
display-repo script (references `csl-websanlexicon/v00`, starts with `cd ..`) that does not belong
at csl-pywork root; running it from the repo root acts on the parent directory. Hygiene, report-only.

### L3. `regenerate-hwnorm1-sqlite.sh` csl-apidev commit message is a copy-paste of the hwnorm1 one

[regenerate-hwnorm1-sqlite.sh](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/regenerate-hwnorm1-sqlite.sh)
(final push block): commits csl-apidev with `"Regenerated hwnorm1.sqlite as on $TIMESTAMP"` —
misleading provenance in the published history of that repo. Report-only.

## Refuted lead (do not "fix" this)

### R1. `changelog_released_headings.py` sha `.strip('0 \t')` — CORRECT as written

Line 216 of
[changelog_released_headings.py](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/scripts/changelog_released_headings.py)
looks like it mangles `github.event.before` shas with leading/trailing zeros (`.strip('0 \t')`,
and this repo's history contains 37 shas ending in `0` and 38 starting with `0`). A/B probe on the
real script with a real zero-ending sha (`e1ddb1d1…480`) and a deleted released heading: the guard
still fired with exit 1. Reason: the strip is only a **truthiness test** for the all-zero sentinel;
the base actually used (line 223) is `os.environ['CHANGELOG_GUARD_BASE'].strip()` — the full sha.
Static pattern-matching would have produced a wrong fix here; the live A/B is why the finding is
refuted, not fixed.

## Coverage notes

- The two `scripts/changelog_*.py` guards have **no unit tests in this repo** (their behavior is
  exercised in the source repos' CI). A future test-gap wave could pin the all-zero-sentinel and
  fork-point behaviors probed above.
- `v02/redo_xampp_selective.py` (the modernized driver) and `v02/makotemplates/pywork/webtc2/build_query_index.py`
  (H3633 index builder, byte-offset accounting incl. `\r\n` and missing final newline) were read
  end-to-end — no defects found; `tests/test_redo_xampp_selective.py` covers 13 driver scenarios.

---

Executor: GLM 5.3 Flash (zai-coding-plan/glm-5.3-flash) · nightly hunt, MG ruling 26-09-2026 ·
elapsed ~30 min total.

_Dr. Mārcis Gasūns_
