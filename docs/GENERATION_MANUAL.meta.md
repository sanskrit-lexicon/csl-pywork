# GENERATION_MANUAL.md — metadoc

_Created: 28-07-2026 · Last updated: 28-07-2026_

## Purpose

Companion record for
[docs/GENERATION_MANUAL.md](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/docs/GENERATION_MANUAL.md) —
the operator manual for the canonical CDSL dictionary-generation pipeline.
The manual's contract: a new operator regenerates one dictionary end-to-end
from the manual alone and knows what to validate.

## Audience

New pipeline operators (primary); maintainers touching `makotemplates/` or
vendoring scripts outward (appendix); agents executing the correction
workflow's regeneration step.

## Provenance

- Authored 28-07-2026 under handoff
  [H1783](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1783-Fable_csl-pywork_dict-generation-operator-manual_28.07.26.md)
  by Fable 5 (`claude-fable-5`); handoff minted by Grok 4.5 (`grok-4.5`) as #2
  of the H1782–H1786 "code-heavy / docs-thin Cologne engines" batch.
- Every stage claim was verified against the scripts at commit `d53d7f2`
  (`generate_dict.sh`, `generate_orig.sh`, `generate_pywork.sh`,
  `generate_ab_bib_ls.sh`, `xmlchk_xampp.sh`, `inventory.txt`, `dictparms.py`,
  `generate.py`, the `redo_*.sh` / `make_xml.py` / `updateByLine.py`
  templates) — not from prior prose.
- Shape follows the org operator-manual skeleton (cheat-sheet · data-flow ·
  step-by-step · env · symptom→cause→cure · glossary · maintainer appendix),
  as in the sibling
  [csl-websanlexicon WEB_FRONTEND_MANUAL](https://github.com/sanskrit-lexicon/csl-websanlexicon/blob/main/docs/WEB_FRONTEND_MANUAL.md)
  (H1782).

## Improvement backlog (ranked)

1. **Worked end-to-end transcript** — append a real `generate_dict.sh` run log
   for one small dictionary (e.g. `ben`) with the healthy output annotated
   line-by-line.
2. **Stardict/JSON downstream** — §10 mentions the selective updater's
   Stardict/csl-json pushes; a short map of those downstream repos and their
   consumers would close the loop.
3. **`generate.py` inventory reference** — the full record grammar (multi-dict
   fields, rename form, `D` semantics on nested paths) deserves a compact
   reference table once someone needs it.
4. **v00 census** — which dictionary repos still vendor the v00
   `updateByLine.py`/`parseheadline.py`, so the migration debt is measurable.
5. **Windows shim recipe** — a copy-paste `python3` shim + PATH block tested on
   a clean Git Bash install.

## Limitations

- Not a correction-workflow manual — that lives in
  [csl-corrections](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md);
  §7 covers only the change-file format.
- Web display internals deferred entirely to the csl-websanlexicon manual.
- The per-dictionary quirks under `distinctfiles/<dict>/` are intentionally
  not enumerated (37+ dictionaries); the manual teaches the mechanism, the
  nearest `readme.*` teaches the quirk.

## Revision history

| Date | Change | Actor |
|---|---|---|
| 28-07-2026 | Initial authoring (H1783) | Fable 5 (`claude-fable-5`) |

_Dr. Mārcis Gasūns_
