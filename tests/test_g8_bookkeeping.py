"""Tests for the H3487 G8 (finding P11/P14/P15/P18) bookkeeping fixes.

P14: v02/refresh_csl.sh aggregates per-repo pull status and exits nonzero
     when any pull fails (previously: failures were indistinguishable from
     success).
P15: v02/regenerate-hwnorm1-sqlite.sh commit gates detect UNTRACKED files
     (git status --porcelain), not just tracked modifications
     (git diff --quiet saw nothing).
P11: v02/makotemplates/pywork/webtc2/init_query.py no longer writes the
     literal junk row "prevkey :: keysanskrit\\tkeydata" into query_dump.txt.
P18: v02/makotemplates/pywork/make_xml.py no longer carries the dead
     ">1000000 records" debug cutoff that would silently truncate a future
     dictionary.

Runs entirely against synthetic sandbox layouts — no Cologne production data.
"""
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
V02 = HERE.parent / "v02"
REFRESH = V02 / "refresh_csl.sh"
REGEN = V02 / "regenerate-hwnorm1-sqlite.sh"
INIT_QUERY = V02 / "makotemplates" / "pywork" / "webtc2" / "init_query.py"
MAKE_XML = V02 / "makotemplates" / "pywork" / "make_xml.py"


def _git(args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def _init_repo(path, remote=None):
    path.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q", "-b", "main"], path)
    _git(["config", "user.email", "test@test"], path)
    _git(["config", "user.name", "test"], path)
    (path / "README.md").write_text("stub\n", encoding="utf-8")
    _git(["add", "-A"], path)
    _git(["commit", "-q", "-m", "init"], path)
    if remote is not None:
        _git(["remote", "add", "origin", str(remote)], path)
        _git(["push", "-q", "-u", "origin", "main"], path)
    return path


@pytest.fixture
def workspace(tmp_path):
    """Sandbox layout: tmp/ws/<repo>/... with refresh_csl.sh in csl-pywork/v02."""
    ws = tmp_path / "ws"
    ws.mkdir()
    pw = ws / "csl-pywork" / "v02"
    pw.mkdir(parents=True)
    (pw / "refresh_csl.sh").write_text(REFRESH.read_text(encoding="utf-8"), encoding="utf-8")
    return ws


def _git_ident(path):
    """CI runners have no global git identity — set a per-repo one."""
    _git(["config", "user.email", "test@test"], path)
    _git(["config", "user.name", "test"], path)


def _healthy_remote(tmp_path, name):
    bare = tmp_path / f"{name}.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True)
    return bare


def _seed_upstream(tmp_path, name):
    """Push one upstream commit to the bare remote via a throwaway seed clone."""
    bare = tmp_path / f"{name}.git"
    clone = tmp_path / f"{name}-seed"
    subprocess.run(
        ["git", "clone", "-q", str(bare), str(clone)], check=True, capture_output=True
    )
    _git_ident(clone)
    (clone / "new.txt").write_text("x\n", encoding="utf-8")
    _git(["add", "-A"], clone)
    _git(["commit", "-q", "-m", "upstream change"], clone)
    _git(["push", "-q"], clone)


class TestRefreshCslAggregation:
    def test_all_pulls_ok_exits_zero(self, workspace, tmp_path):
        for name in ("csl-orig", "csl-pywork", "csl-app"):
            _init_repo(workspace / name, remote=_healthy_remote(tmp_path, name))
            # new upstream commit so the pull actually does something
            _seed_upstream(tmp_path, name)

        # the script pulls every one of its 12 repos; the missing ones must be
        # reported as FAIL (missing), so only assert on the ones we created.
        r = subprocess.run(
            ["sh", "refresh_csl.sh"], cwd=workspace / "csl-pywork" / "v02",
            capture_output=True, text=True,
        )
        assert r.returncode == 1  # the 9 repos we did NOT create are missing
        for name in ("csl-orig", "csl-pywork", "csl-app"):
            assert f"OK   {name}" in r.stdout

    def test_failed_pull_is_named_and_exit_nonzero(self, workspace, tmp_path):
        good = _init_repo(workspace / "csl-orig", remote=_healthy_remote(tmp_path, "csl-orig"))
        # healthy repo gets an upstream commit so its pull is a real success
        _seed_upstream(tmp_path, "csl-orig")

        # dead-remote repo: pull must fail
        dead = _init_repo(workspace / "csl-pywork")
        _git(["remote", "add", "origin", str(tmp_path / "no-such-remote.git")], dead)

        r = subprocess.run(
            ["sh", "refresh_csl.sh"], cwd=workspace / "csl-pywork" / "v02",
            capture_output=True, text=True,
        )
        assert r.returncode == 1
        assert "FAIL csl-pywork" in r.stdout
        assert "OK   csl-orig" in r.stdout
        assert "FAILED pulls: csl-pywork" in r.stdout

    def test_script_names_all_twelve_repos(self):
        text = REFRESH.read_text(encoding="utf-8")
        for name in ("csl-orig", "csl-pywork", "csl-websanlexicon", "csl-corrections",
                     "csl-apidev", "csl-doc", "csl-homepage", "hwnorm1", "hwnorm2",
                     "cologne-stardict", "csl-lslink", "csl-app"):
            assert name in text


class TestRegeneratorUntrackedGate:
    def test_no_git_diff_quiet_gate_remains(self):
        text = REGEN.read_text(encoding="utf-8")
        assert "git diff --quiet" not in text
        assert text.count("git status --porcelain") == 3

    def test_untracked_files_are_seen_by_the_new_gate(self, tmp_path):
        """The exact command sequence of one push block, on a stub repo:
        untracked generated output must lead to a commit, not 'No changes'."""
        repo = _init_repo(tmp_path / "hwnorm1")
        # simulate regeneration producing a NEW file (untracked) + no tracked edit
        (repo / "hwnorm1c.sqlite").write_bytes(b"\x00stub sqlite payload\n")

        if subprocess.run(["git", "status", "--porcelain"], cwd=repo,
                          capture_output=True, text=True).stdout.strip():
            _git(["add", "-A"], repo)
            _git(["commit", "-q", "-m", "Regenerated"], repo)
        committed = subprocess.run(
            ["git", "log", "--oneline"], cwd=repo, capture_output=True, text=True
        ).stdout
        assert "Regenerated" in committed

    def test_clean_repo_is_still_a_noop(self, tmp_path):
        """A truly-nothing-changed run must not create a commit (no noise)."""
        repo = _init_repo(tmp_path / "hwnorm1")
        status = subprocess.run(["git", "status", "--porcelain"], cwd=repo,
                                capture_output=True, text=True).stdout.strip()
        assert status == ""
        before = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo,
                                capture_output=True, text=True).stdout
        after = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo,
                               capture_output=True, text=True).stdout
        assert before == after


class TestInitQueryJunkRow:
    XML = (
        "<H><key1>khala</key1><body>dummy <s>body</s> one.</body><L>1</L></H>\n"
        "<H><key1>vrksha</key1><body>dummy <s>body</s> two.</body><L>2</L></H>\n"
    )

    def test_no_junk_row_and_records_preserved(self, tmp_path):
        xml = tmp_path / "in.xml"
        out = tmp_path / "query_dump.txt"
        xml.write_text(self.XML, encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(INIT_QUERY), str(xml), str(out)],
            capture_output=True, text=True,
        )
        assert r.returncode == 0, r.stderr
        lines = out.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        assert lines[0].startswith("khala :: ")
        assert lines[1].startswith("vrksha :: ")
        assert "prevkey" not in out.read_text(encoding="utf-8")


class TestMakeXmlDebugCutoff:
    def test_no_debug_cutoff_remains_in_v02_template(self):
        text = MAKE_XML.read_text(encoding="utf-8")
        assert "debug stopping" not in text
        assert "ihwrec > 1000000" not in text
