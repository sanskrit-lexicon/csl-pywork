# v00 template analysis

> **Historical.** This document records the per-file decisions made during v00 development about which `pywork` scripts needed to be Mako templates (`T`) versus plain copies (`C`). It informed the `inventory.txt` classification used in both v00 and v02.

---

## Decision summary

| File | Category | Reason |
|---|---|---|
| `hw.py` | T | MW requires an extra `e` key; BEN has no equivalent script |
| `hw0.py` | C/T | BEN has a distinct `hw0.py` |
| `hw2.py` | C/T | BEN has a distinct `hw2.py` |
| `hwparse.py` | T | Always embeds `dict = '${dictlo}'`; MW needs an extra `e` key in `hwrec_keys` |
| `parseheadline.py` | C | No per-dictionary differences; BEN does not use it |
| `updateByLine.py` | C | No per-dictionary differences |

---

## Per-file notes

### `hw.py`

Extracts headwords from `orig/xxx.txt` → `xxxhw.txt`. Templated because:

- **BEN** — has no `hw.py` at all; headword handling is done differently.
- **MW** — requires an extra `e` key in the metadata line (the `HX` entry-type identifier), making its `Hwmeta` class structure slightly different from all other dictionaries.

### `hw0.py` and `hw2.py`

Produce headword variant files (`xxxhw0.txt`, `xxxhw2.txt`) from the main `xxxhw.txt`. BEN has distinct versions of both; all other dictionaries share the same code.

### `hwparse.py`

Parses `xxxhw.txt` into `HW` record objects used by `make_xml.py`. Always templated because:

- It embeds the dictionary code literally as `dictcode = '${dictlo}'`, so a template rendering is required for every dictionary regardless of other differences.
- **BEN** — does not use this file.
- **MW** — needs `e` added to `hwrec_keys` (the `HX` entry-type field):

  ```python
  # all other dictionaries
  hwrec_keys = ['L','pc','k1','k2','h'] + ['type','LP','k1P'] + ['ln1','ln2']

  # MW only
  hwrec_keys = ['L','pc','k1','k2','h'] + ['type','LP','k1P'] + ['ln1','ln2'] + ['e']
  ```

### `parseheadline.py`

Parses `<key>val<key1>val1...` encoded lines into key-value dictionaries. No per-dictionary differences; copied verbatim. BEN does not use it.

### `updateByLine.py`

Applies line-based corrections to dictionary text files. No per-dictionary differences; copied verbatim for all dictionaries.
