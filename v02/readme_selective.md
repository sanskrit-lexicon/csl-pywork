# Selective update (`redo_xampp_selective.py`)

Regenerates only the dictionaries that have changed in `csl-orig` since the last run. As of the
csl-pywork#53 modernization, the canonical implementation is the Python 3 driver
[`redo_xampp_selective.py`](redo_xampp_selective.py); `redo_xampp_selective.sh` is now a thin
compatibility wrapper that calls it with the production server defaults, so cron entry points
never had to change:

```
@reboot sleep 120 && bash /var/www/html/cologne/csl-pywork/v02/redo_xampp_selective.sh
```

For manual runs, call the driver directly — it has real flags the old shell script never did:

```bash
# Preview a run without writing or pushing anything:
python3 v02/redo_xampp_selective.py --dry-run

# Rehearse locally against the current checkout state (no git pull):
python3 v02/redo_xampp_selective.py --skip-pull --since <commit> --dict mw --stop-after diff

# Full flag reference:
python3 v02/redo_xampp_selective.py --help
```

| Flag | Purpose |
|---|---|
| `--base` | Parent directory for the sibling repos (default `/var/www/html/cologne`, or `$CSL_BASE`). |
| `--indic-base` | Parent directory for `stardict-sanskrit` (default `/var/www/html/indic-dict`, or `$CSL_INDIC_BASE`). |
| `--state-file` | Override the `.xampp_last_run` marker path. |
| `--since` | Manual override for the last-processed commit (needed on a first run, no state file yet). |
| `--dict` | Limit the run to specific dictionary codes (repeatable). |
| `--dry-run` | Print phases/commands without writing or pushing anything. |
| `--no-push` | Commit locally where needed but skip pushes. |
| `--skip-pull` | Use the current local checkout state for offline tests. |
| `--strict-clean` | Fail preflight if a participating repo has uncommitted changes. |
| `--allow-dirty REPO` | Permit a known-dirty repo during manual testing (repeatable). |
| `--stop-after PHASE` | Stop after `preflight`, `pull`, `diff`, `generate`, `stardict`, `stardict_sync`, `json`, `homepage`, or `state_update`. |
| `--manifest PATH` | Write the machine-readable run summary (phases run, dictionaries, changed/pushed repos, failures) to a file instead of stdout. |

**Server rehearsal note.** The driver's phase logic (preflight/pull/diff/generate/stardict/
stardict_sync/json/homepage/state_update) is implemented and unit-tested (`tests/
test_redo_xampp_selective.py`) against a synthetic sibling-repo layout, but a live `--dry-run`
and `--no-push` rehearsal against the *real* Cologne server layout still needs Cologne server
access, which is not yet granted (`csl-observatory/docs/DECISIONS_NEEDED.md` C2). Do not enable
push-capable production runs before that rehearsal and explicit maintainer/server confirmation —
see `csl-observatory/docs/REFRESH_SCRIPT_MODERNIZATION_PLAN.md` steps 7-9.

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

- `python3 make_babylon.py <dict> 0` — line-break variant for reading (`output/`)
- `python3 make_babylon.py <dict> 1` — `<BR>` variant for display (`production/`)

Before generation, refreshes `input/hwnorm1c.txt` from `hwnorm1/sanhw1/hwnorm1c.txt`.

Commits and pushes each dictionary update to `cologne-stardict` with a timestamped message (e.g. `mw update 20240501120000`).

### Step 4 — Sync `stardict-sanskrit`

Pulls `indic-dict/stardict-sanskrit`, runs `cologne-stardict/move_to_stardict.sh` to copy the new Babylon files into their correct locations, then commits and pushes. The `stardict-sanskrit` repository has CI/CD that converts the new files to Stardict format and updates the dictionary-updater index.

### Step 5 — Rebuild JSON files

For each changed dictionary, runs `python3 json_from_babylon.py <dict>` in `csl-json`, commits, and pushes. The JSON files are consumed by [ashtadhyayi.com](https://ashtadhyayi.com) for dictionary search.

### Step 6 — Update version tracking

Writes the current `csl-orig` HEAD commit hash to `csl-orig/v02/.xampp_last_run` so the next run only processes commits after this point. Also writes a version string of the form `2.0.<commit-count>` to `csl-orig/.version` (not tracked by git).

### Step 7 — Refresh the homepage

Runs `csl-homepage/redo_xampp.sh`, which reads `csl-orig/.version` and injects the version number and today's date into the homepage.
