# Selective update (`redo_xampp_selective.sh`)

Regenerates only the dictionaries that have changed in `csl-orig` since the last run. Designed to run automatically at system boot via cron:

```
@reboot sleep 120 && bash /var/www/html/cologne/csl-pywork/v02/redo_xampp_selective.sh
```

---

## Prerequisites

The following sibling directories must exist under the same parent as `csl-pywork`:

```
cologne/
  csl-orig/
  csl-pywork/
  csl-websanlexicon/
  csl-homepage/
  hwnorm1/
  csl-json/
  cologne-stardict/

indic-dict/             ← sibling of cologne/
  stardict-sanskrit/
```

Git credentials must be cached so that `git pull` and `git push` run without prompting.

---

## What it does, step by step

### Step 0 — Pull all repositories

Updates `csl-pywork`, `csl-websanlexicon`, `csl-homepage`, `hwnorm1`, `csl-json`, `cologne-stardict`, and `csl-orig` to their latest commits from GitHub.

### Step 1 — Find changed dictionaries

```bash
git diff --name-only <last-run-commit>..<HEAD> | grep ...
```

Compares the current `csl-orig` HEAD against the commit recorded in `csl-orig/v02/.xampp_last_run` (written at the end of the previous run). Extracts dictionary codes from changed `.txt` filenames and intersects them with valid dict codes, writing the result to `csl-orig/v02/.files_to_handle`.

### Step 2 — Regenerate dictionaries

For each dictionary code in `.files_to_handle`:

```bash
sh generate_dict.sh <dict> ../../<dict>
```

Runs the full four-stage pipeline (orig → pywork → web → hw/xml/sqlite/downloads). See [`readme.md`](readme.md) for details.

### Step 3 — Rebuild Stardict files

For each changed dictionary, regenerates two Babylon files in `cologne-stardict`:

- `python2 make_babylon.py <dict> 0` — line-break variant for reading (`output/`)
- `python2 make_babylon.py <dict> 1` — `<BR>` variant for display (`production/`)

Commits and pushes each dictionary update to `cologne-stardict` with a timestamped message (e.g. `mw update 20240501120000`).

### Step 4 — Sync `stardict-sanskrit`

Pulls `indic-dict/stardict-sanskrit`, runs `cologne-stardict/move_to_stardict.sh` to copy the new Babylon files into their correct locations, then commits and pushes. The `stardict-sanskrit` repository has CI/CD that converts the new files to Stardict format and updates the dictionary-updater index.

### Step 5 — Rebuild JSON files

For each changed dictionary, runs `python2 json_from_babylon.py <dict>` in `csl-json`, commits, and pushes. The JSON files are consumed by [ashtadhyayi.com](https://ashtadhyayi.com) for dictionary search.

### Step 6 — Update version tracking

Writes the current `csl-orig` HEAD commit hash to `csl-orig/v02/.xampp_last_run` so the next run only processes commits after this point. Also writes a version string of the form `2.0.<commit-count>` to `csl-orig/.version` (not tracked by git).

### Step 7 — Refresh the homepage

Runs `csl-homepage/redo_xampp.sh`, which reads `csl-orig/.version` and injects the version number and today's date into the homepage.
