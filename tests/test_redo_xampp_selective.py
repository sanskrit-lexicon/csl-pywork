"""Tests for v02/redo_xampp_selective.py against the acceptance checklist in
csl-observatory/docs/REFRESH_SCRIPT_MODERNIZATION_PLAN.md.

Builds a synthetic sibling-repo layout (csl-orig with dict-code .txt files,
plus stub repos for the others) so the driver's preflight/diff/phase logic
can be exercised without the real Cologne production data.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

DRIVER = Path(__file__).parent.parent / "v02" / "redo_xampp_selective.py"


def _git(args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def _init_repo(path, dicts=()):
    path.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q"], path)
    _git(["config", "user.email", "test@test"], path)
    _git(["config", "user.name", "test"], path)
    if dicts:
        v02 = path / "v02"
        v02.mkdir(exist_ok=True)
        for d in dicts:
            (v02 / d).mkdir(exist_ok=True)
            (v02 / d / f"{d}.txt").write_text("stub entry\n", encoding="utf-8")
        _git(["add", "."], path)
        _git(["commit", "-q", "-m", "seed"], path)
    else:
        (path / ".keep").write_text("", encoding="utf-8")
        _git(["add", "."], path)
        _git(["commit", "-q", "-m", "seed"], path)
    return path


def _head(path):
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, check=True, capture_output=True, text=True
    ).stdout.strip()


@pytest.fixture
def layout(tmp_path):
    """A minimal sibling-repo layout: base/{csl-orig,csl-websanlexicon,
    csl-homepage,hwnorm1,csl-json,cologne-stardict,csl-pywork},
    indic_base/stardict-sanskrit."""
    base = tmp_path / "cologne"
    indic_base = tmp_path / "indic-dict"
    orig = _init_repo(base / "csl-orig", dicts=["mw", "ap90"])
    for name in ["csl-websanlexicon", "csl-homepage", "hwnorm1", "csl-json", "cologne-stardict", "csl-pywork"]:
        _init_repo(base / name)
    # Stub the homepage refresh script — the real one always runs in Phase 7
    # regardless of whether any dictionary changed; tests need it to exist,
    # committed (so REQUIRED_REPOS' --strict-clean check doesn't flag it dirty).
    homepage_dir = base / "csl-homepage"
    (homepage_dir / "redo_xampp.sh").write_text("#!/bin/bash\nexit 0\n", encoding="utf-8")
    _git(["add", "."], homepage_dir)
    _git(["commit", "-q", "-m", "add stub redo_xampp.sh"], homepage_dir)
    # csl-pywork/v02/ must exist as the real prerequisite layout requires,
    # deliberately WITHOUT generate_dict.sh — tests that reach the generate
    # phase expect a clean DriverError there, not a missing-cwd crash.
    (base / "csl-pywork" / "v02").mkdir(parents=True, exist_ok=True)
    # hwnorm1c.txt source + cologne-stardict/input/ destination dir, for the
    # Stardict-phase pre-copy step (deliberately no make_babylon.py — Stardict
    # generation itself needs the real Cologne production babylon data).
    hwnorm1_dir = base / "hwnorm1" / "sanhw1"
    hwnorm1_dir.mkdir(parents=True, exist_ok=True)
    (hwnorm1_dir / "hwnorm1c.txt").write_text("stub normalization data\n", encoding="utf-8")
    _git(["add", "."], base / "hwnorm1")
    _git(["commit", "-q", "-m", "add stub hwnorm1c.txt"], base / "hwnorm1")
    (base / "cologne-stardict" / "input").mkdir(parents=True, exist_ok=True)
    _init_repo(indic_base / "stardict-sanskrit")
    since = _head(orig)  # captured BEFORE any test mutates csl-orig further
    return {"base": base, "indic_base": indic_base, "orig": orig, "since": since}


def run_driver(layout, *extra_args, since=None):
    args = [
        sys.executable, str(DRIVER),
        "--base", str(layout["base"]),
        "--indic-base", str(layout["indic_base"]),
        "--since", since or layout["since"],
        "--skip-pull",
        *extra_args,
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    return result, since or layout["since"]


class TestPreflight:
    def test_missing_required_repo_fails(self, tmp_path):
        base = tmp_path / "cologne"
        indic_base = tmp_path / "indic-dict"
        _init_repo(base / "csl-orig", dicts=["mw"])
        _init_repo(indic_base / "stardict-sanskrit")
        # csl-websanlexicon etc. deliberately missing.
        result = subprocess.run(
            [sys.executable, str(DRIVER), "--base", str(base), "--indic-base", str(indic_base),
             "--since", "HEAD", "--skip-pull", "--stop-after", "preflight"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        manifest = json.loads(result.stdout)
        assert manifest["failures"], "expected a preflight failure"
        assert manifest["failures"][0]["phase"] == "preflight"

    def test_no_state_file_no_since_fails(self, layout):
        result = subprocess.run(
            [sys.executable, str(DRIVER), "--base", str(layout["base"]),
             "--indic-base", str(layout["indic_base"]), "--skip-pull",
             "--stop-after", "preflight"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        manifest = json.loads(result.stdout)
        assert manifest["failures"][0]["phase"] == "preflight"

    def test_dirty_repo_fails_under_strict_clean(self, layout):
        (layout["base"] / "csl-orig" / "v02" / "mw" / "mw.txt").write_text("dirty\n", encoding="utf-8")
        result, _ = run_driver(layout, "--strict-clean", "--stop-after", "preflight")
        assert result.returncode == 1
        manifest = json.loads(result.stdout)
        assert manifest["failures"][0]["phase"] == "preflight"

    def test_dirty_repo_allowed_via_allow_dirty(self, layout):
        (layout["base"] / "csl-orig" / "v02" / "mw" / "mw.txt").write_text("dirty\n", encoding="utf-8")
        result, _ = run_driver(
            layout, "--strict-clean", "--allow-dirty", "csl-orig", "--stop-after", "preflight"
        )
        assert result.returncode == 0


class TestDiffDeterminism:
    def test_skip_pull_since_dict_stop_after_diff_is_deterministic(self, layout):
        orig = layout["orig"]
        (orig / "v02" / "mw" / "mw.txt").write_text("mw changed\n", encoding="utf-8")
        _git(["add", "."], orig)
        _git(["commit", "-q", "-m", "mw update"], orig)

        r1, since = run_driver(layout, "--dict", "mw", "--stop-after", "diff")
        r2, _ = run_driver(layout, "--dict", "mw", "--stop-after", "diff", since=since)
        assert r1.returncode == 0
        m1 = json.loads(r1.stdout)
        m2 = json.loads(r2.stdout)
        assert m1["dictionaries"] == ["mw"] == m2["dictionaries"]

    def test_invalid_dict_code_fails_before_generation(self, layout):
        result, _ = run_driver(layout, "--dict", "nonexistent-code", "--stop-after", "diff")
        assert result.returncode == 1
        manifest = json.loads(result.stdout)
        assert manifest["failures"][0]["phase"] == "diff"

    def test_empty_diff_produces_no_commits_and_does_not_push(self, layout):
        # since == HEAD, nothing changed.
        result, _ = run_driver(layout, "--stop-after", "state_update")
        assert result.returncode == 0
        manifest = json.loads(result.stdout)
        assert manifest["dictionaries"] == []
        assert manifest.get("pushed_repos", []) == []


class TestDryRun:
    def test_dry_run_never_pushes_or_writes_state(self, layout):
        orig = layout["orig"]
        (orig / "v02" / "mw" / "mw.txt").write_text("mw changed\n", encoding="utf-8")
        _git(["add", "."], orig)
        _git(["commit", "-q", "-m", "mw update"], orig)
        state_file = orig / "v02" / ".xampp_last_run"
        assert not state_file.exists()

        result, _ = run_driver(layout, "--dry-run")
        assert result.returncode == 0
        manifest = json.loads(result.stdout)
        assert manifest["no_push"] is True
        assert manifest.get("pushed_repos", []) == []
        # --dry-run must never actually write the state file.
        assert not state_file.exists()


class TestFailurePreventsStateAdvance:
    def test_failed_phase_does_not_update_state_file(self, layout):
        # Force a generate-phase failure: csl-pywork/v02/generate_dict.sh does not exist.
        orig = layout["orig"]
        (orig / "v02" / "mw" / "mw.txt").write_text("mw changed\n", encoding="utf-8")
        _git(["add", "."], orig)
        _git(["commit", "-q", "-m", "mw update"], orig)
        state_file = orig / "v02" / ".xampp_last_run"

        result, since = run_driver(layout)  # no --dry-run: generate phase will hit missing script
        assert result.returncode == 1
        manifest = json.loads(result.stdout)
        assert not manifest["ok"]
        assert not state_file.exists(), "state file must not advance after a failed phase"


class TestStardictHwnorm1Copy:
    """The Stardict phase must refresh cologne-stardict/input/hwnorm1c.txt from
    hwnorm1/sanhw1/hwnorm1c.txt BEFORE running make_babylon.py — matches
    redo_xampp_selective.sh Step 3's `cp ../hwnorm1/sanhw1/hwnorm1c.txt input/hwnorm1c.txt`."""

    def _stub_generate_dict(self, layout):
        script = layout["base"] / "csl-pywork" / "v02" / "generate_dict.sh"
        script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")

    def test_hwnorm1c_copied_before_make_babylon_runs(self, layout):
        self._stub_generate_dict(layout)
        orig = layout["orig"]
        (orig / "v02" / "mw" / "mw.txt").write_text("mw changed\n", encoding="utf-8")
        _git(["add", "."], orig)
        _git(["commit", "-q", "-m", "mw update"], orig)

        dst = layout["base"] / "cologne-stardict" / "input" / "hwnorm1c.txt"
        assert not dst.exists()
        # No make_babylon.py in the fixture, so the stardict phase still fails
        # overall — but the copy must happen first, before that failure.
        result, _ = run_driver(layout, "--stop-after", "stardict")
        assert result.returncode == 1
        assert dst.is_file(), "hwnorm1c.txt must be copied before make_babylon.py runs"
        assert dst.read_text(encoding="utf-8") == (
            layout["base"] / "hwnorm1" / "sanhw1" / "hwnorm1c.txt"
        ).read_text(encoding="utf-8")

    def test_missing_hwnorm1_source_fails_cleanly(self, layout):
        self._stub_generate_dict(layout)
        orig = layout["orig"]
        (orig / "v02" / "mw" / "mw.txt").write_text("mw changed\n", encoding="utf-8")
        _git(["add", "."], orig)
        _git(["commit", "-q", "-m", "mw update"], orig)
        (layout["base"] / "hwnorm1" / "sanhw1" / "hwnorm1c.txt").unlink()

        result, _ = run_driver(layout, "--stop-after", "stardict")
        assert result.returncode == 1
        manifest = json.loads(result.stdout)
        assert manifest["failures"][0]["phase"] == "stardict"


class TestManifest:
    def test_manifest_records_required_fields(self, layout):
        orig = layout["orig"]
        (orig / "v02" / "mw" / "mw.txt").write_text("mw changed\n", encoding="utf-8")
        _git(["add", "."], orig)
        _git(["commit", "-q", "-m", "mw update"], orig)

        result, since = run_driver(layout, "--dry-run")
        assert result.returncode == 0
        manifest = json.loads(result.stdout)
        for field in ("old_commit", "new_commit", "dictionaries", "phases_run", "failures"):
            assert field in manifest, f"manifest missing '{field}'"
        assert manifest["old_commit"] == since
        assert manifest["dictionaries"] == ["mw"]

    def test_manifest_written_to_file(self, layout, tmp_path):
        manifest_path = tmp_path / "manifest.json"
        result, _ = run_driver(layout, "--dry-run", "--manifest", str(manifest_path))
        assert result.returncode == 0
        assert manifest_path.is_file()
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert data["ok"] is True
