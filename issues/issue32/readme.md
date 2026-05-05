# Issue 32 — Replace `<pe>` tag with `<per>`

**Ref:** https://github.com/sanskrit-lexicon/csl-pywork/issues/32

The `<pe>` tag in `gra.txt` and `md.txt` conflicted with the `<pe>` dictionary code element. It was renamed to `<per>` across csl-orig, csl-pywork, and csl-websanlexicon.

---

## Scope of changes

| Repository | What changed |
|---|---|
| **csl-orig** | `gra/gra.txt` — 1809 `<pe>` tags renamed to `<per>`; `md/md.txt` — 314 `<pe>` tags renamed |
| **csl-pywork** | `v02/makotemplates/pywork/one.dtd` — updated DTD to use `<per>` |
| **csl-websanlexicon** | `basicadjust.php` — treat `<per>` like `<ab>` in gra and md displays |
| **csl-apidev** | `basicadjust.php` — same change as websanlexicon |

---

## Steps taken

### 1. Prepare edited source files

```bash
# Working from csl-orig at commit 1dd36646da9f7ba380d49e658c09b7f40a98fd7e
cp /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt temp_gra_0.txt
cp /c/xampp/htdocs/cologne/csl-orig/v02/md/md.txt  temp_md_0.txt

# Manually rename <pe> → <per> in copies
cp temp_gra_0.txt temp_gra_1.txt   # 1809 replacements across 1775 lines
cp temp_md_0.txt  temp_md_1.txt    # 314 replacements across 188 lines
```

### 2. Install and test locally

```bash
cp temp_gra_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt
cp temp_md_1.txt  /c/xampp/htdocs/cologne/csl-orig/v02/md/md.txt

cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh gra ../../gra && sh xmlchk_xampp.sh gra  # ok
sh generate_dict.sh md  ../../md  && sh xmlchk_xampp.sh md   # ok
```

Also regenerated `pe` (which shares display logic) to confirm no regressions.

### 3. Push to GitHub

```bash
# csl-websanlexicon
git add . && git commit -m "gra, md and 'per' tag; Ref: #32" && git push

# csl-pywork
git add . && git commit -m "per tag. #32" && git push

# csl-apidev (copy of basicadjust.php)
git add . && git commit -m "gra, md and 'per' tag; Ref: #32" && git push

# csl-orig
git add . && git commit -m "gra, md and 'per' tag; Ref: #32" && git push
```

### 4. Sync Cologne server and regenerate

Pull updated repositories on the Cologne server, then:

```bash
cd csl-pywork/v02
sh generate_dict.sh gra ../../GRAScan/2020
sh generate_dict.sh md  ../../MDScan/2020
sh generate_dict.sh pe  ../../PEScan/2020
```
