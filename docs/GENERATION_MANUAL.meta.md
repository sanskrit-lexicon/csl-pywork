# GENERATION_MANUAL.md — metadoc

_Created: 28-07-2026 · Last updated: 28-07-2026_

Companion record for
[docs/GENERATION_MANUAL.md](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/docs/GENERATION_MANUAL.md).

## Purpose

The operator manual for the csl-pywork dictionary-generation pipeline: enable a
new operator to regenerate a dictionary's pywork artifacts end-to-end
(`generate_dict.sh` → headwords → XML → SQLite → downloads) and to validate the
result, from the manual alone, without reading every vendored script copy.

## Audience

New CDSL operators and agent sessions doing regeneration or correction-support
work; secondarily maintainers extending the pipeline to new dictionaries.

## Provenance

- Handoff: H1783 (Uprava, minted 28-07-2026 by Grok 4.5 `grok-4.5` as #2 of the
  code-heavy/docs-thin Cologne-engine batch H1782–H1786).
- Authored 28-07-2026 by Fable 5 (`claude-fable-5`) from direct reads of
  `generate_dict.sh`, `generate_orig.sh`, `generate_pywork.sh`,
  `generate_ab_bib_ls.sh`, `generate.py`, `inventory.txt`, `inventory_orig.txt`,
  `dictparms.py`, the `makotemplates/pywork/` stage templates (`redo_hw.sh`,
  `redo_xml.sh`, `redo_postxml.sh`, `hw.py`, `make_xml.py`, `updateByLine.py`,
  `parseheadline.py`, `hwparse.py`, `digentry.py`), `xmlchk_xampp.sh`,
  `utilities/xmlvalidate.py`, `v02/readme.md`, `v02/readme_selective.md`, and
  the `distinctfiles/mw/` tree as the worked per-dict example.
- Shape follows the org's operator-manual skeleton (cheat-sheet · data-flow ·
  step-by-step · env · symptom→cause→cure · glossary · maintainer appendix),
  prior art: [MWinflect docs/GENERATION_MANUAL.md](https://github.com/sanskrit-lexicon/MWinflect/blob/main/docs/GENERATION_MANUAL.md) (H511).

## Ranked improvement backlog

1. **Link the csl-websanlexicon operator manual once it lands** (queued as a
   sibling handoff, H1782) — §2/§4 stage 4 currently point at the repo, not a
   manual.
2. **Worked end-to-end transcript for one small dictionary** (e.g. `ben`):
   actual command + full expected output annotated line-by-line — the
   strongest possible newcomer test, deferred to keep this pass source-derived.
3. **Per-dict quirk table** — which codes have ab/auth tables, which have
   custom `make_xml` branches (`skd`/`vcp`/`armh` Devanagari handling, `krm`
   div-closing, `vcp` `Unexpected <H>` whitelist) is currently scattered
   across §4/§8; a single matrix would help maintainers.
4. **Verify and document `redo_cologne_all.sh` / `refresh_csl.sh` on the real
   Cologne server** — blocked on server access
   (csl-observatory DECISIONS_NEEDED C2); until then those drivers are
   documented from source only.
5. Clean up the §10 quirks (usage-message typo, `xmlchk_xampp.sh` path
   dependency) and then simplify §5's copy-step instruction.

## Limitations

- Written from source reading, not from a live end-to-end run on this machine
  (no XAMPP/sqlite3/zip toolchain exercised in the authoring session); the
  green-signal lines are taken from the drivers' own awk whitelists, which is
  what they gate on in production.
- The Cologne-server-side paths (`/nfs/…`, `cologne_flag` branches) are
  documented from template source; server behaviour unverified (backlog #4).
- `v00/` is deliberately covered only as history (§7.3), not operationally.

## Related documents

- [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — the correction-side twin.
- [v02/readme.md](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md) — the pipeline's own quick reference this manual supersedes for onboarding (kept: install specifics).
- [v02/readme_selective.md](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme_selective.md) — selective-update driver flags.
- [Cologne tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md) — org-wide context.

## Revision history

| Date | Change | Author |
|---|---|---|
| 28-07-2026 | Initial manual + metadoc (H1783) | Fable 5 (`claude-fable-5`) |

---

_Dr. Mārcis Gasūns_
