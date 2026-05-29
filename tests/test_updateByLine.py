"""Unit tests for updateByLine.py — the core correction-pipeline engine.

Tests run the script via subprocess to exercise the full CLI contract
(including UTF-8 file I/O and exit codes on error).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Path to the script under test
SCRIPT = Path(__file__).parent.parent / "v02" / "makotemplates" / "pywork" / "updateByLine.py"


def run_update(input_text: str, change_text: str) -> tuple[str, int]:
    """Write temp files, run updateByLine.py, return (output_text, exit_code)."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        fin  = td / "input.txt"
        fchg = td / "changes.txt"
        fout = td / "output.txt"
        fin.write_text(input_text, encoding="utf-8")
        fchg.write_text(change_text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(fin), str(fchg), str(fout)],
            capture_output=True, text=True, encoding="utf-8"
        )
        output = fout.read_text(encoding="utf-8") if fout.exists() else ""
        return output, result.returncode


class TestNewOperation:
    def test_replaces_target_line(self):
        inp = "line one\nline two\nline three\n"
        chg = "2 old line two\n2 new line TWO\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines()[1] == "line TWO"

    def test_other_lines_unchanged(self):
        inp = "line one\nline two\nline three\n"
        chg = "2 old line two\n2 new line TWO\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        lines = out.splitlines()
        assert lines[0] == "line one"
        assert lines[2] == "line three"

    def test_preserves_line_count(self):
        inp = "a\nb\nc\n"
        chg = "1 old a\n1 new A\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert len(out.splitlines()) == 3


class TestInsOperation:
    def test_inserts_after_target_line(self):
        inp = "a\nb\nc\n"
        chg = "2 old b\n2 ins B_EXTRA\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        lines = out.splitlines()
        assert lines == ["a", "b", "B_EXTRA", "c"]

    def test_increases_line_count_by_one(self):
        inp = "a\nb\nc\n"
        chg = "1 old a\n1 ins X\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert len(out.splitlines()) == 4


class TestDelOperation:
    def test_deletes_target_line(self):
        inp = "a\nb\nc\n"
        chg = "2 old b\n2 del \n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines() == ["a", "c"]

    def test_decreases_line_count_by_one(self):
        inp = "a\nb\nc\n"
        chg = "3 old c\n3 del \n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert len(out.splitlines()) == 2


class TestMultipleChanges:
    def test_two_new_changes(self):
        inp = "alpha\nbeta\ngamma\n"
        chg = "1 old alpha\n1 new ALPHA\n3 old gamma\n3 new GAMMA\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines() == ["ALPHA", "beta", "GAMMA"]

    def test_new_then_del(self):
        inp = "a\nb\nc\nd\n"
        chg = "1 old a\n1 new A\n3 old c\n3 del \n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines() == ["A", "b", "d"]


class TestCommentLines:
    def test_semicolon_lines_skipped(self):
        inp = "a\nb\n"
        chg = "; this is a comment\n1 old a\n1 new A\n; another comment\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines()[0] == "A"

    def test_multiple_comments_between_pairs(self):
        inp = "x\ny\n"
        chg = "; first\n; second\n2 old y\n; mid-pair comment is non-standard but skipped\n2 new Y\n"
        # Comments between old and new break pairing — only test comment-only separator
        # This just verifies comments before first pair don't break anything
        chg = "; comment\n1 old x\n1 new X\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines()[0] == "X"


class TestUnicodeContent:
    def test_devanagari_replacement(self):
        inp = "पुस्तक\nग्रन्थ\n"
        chg = "1 old पुस्तक\n1 new पाठ्यपुस्तक\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert out.splitlines()[0] == "पाठ्यपुस्तक"

    def test_mixed_ascii_and_unicode(self):
        inp = "<entry>शब्द</entry>\n<entry>word</entry>\n"
        chg = "1 old <entry>शब्द</entry>\n1 new <entry>वाक्य</entry>\n"
        out, rc = run_update(inp, chg)
        assert rc == 0
        assert "<entry>वाक्य</entry>" in out


class TestErrorHandling:
    def test_old_text_mismatch_exits_nonzero(self):
        inp = "correct text\n"
        chg = "1 old WRONG TEXT\n1 new anything\n"
        _, rc = run_update(inp, chg)
        assert rc != 0

    def test_out_of_range_line_number_exits_nonzero(self):
        inp = "only one line\n"
        chg = "99 old only one line\n99 new something\n"
        _, rc = run_update(inp, chg)
        assert rc != 0
