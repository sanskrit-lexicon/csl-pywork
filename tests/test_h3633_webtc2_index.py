"""Tests for the H3487 G3 / H3633 webtc2 generation-time search index.

G3: v02/makotemplates/pywork/webtc2/build_query_index.py builds
    query_dump.sqlite3 (lines(off,t) + meta dumpsize + user_version 1)
    alongside the flat file, byte-accurate for fseek().
P10: init_query.py no longer crashes with NameError on a zero-record input,
    and no longer writes a junk ` :: \t ` row for such a file.
redo.sh: the webtc2 stage is fail-closed (set -e), builds the index, and
    moves dump + index to web/webtc2/ together so they never go stale-paired.
inventory.txt: the new builder ships to every dictionary.

Runs entirely against synthetic sandbox data - no Cologne production data.
"""
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
V02 = HERE.parent / "v02"
WEBTC2 = V02 / "makotemplates" / "pywork" / "webtc2"
INIT_QUERY = WEBTC2 / "init_query.py"
BUILD_INDEX = WEBTC2 / "build_query_index.py"
REDO_SH = WEBTC2 / "redo.sh"
INVENTORY = V02 / "inventory.txt"


def _run_py(script, *args):
    return subprocess.run(
        [sys.executable, str(script), *args], check=True, capture_output=True, text=True
    )


def _make_xml_line(key, body, lnum):
    return f"<H1>{key}<key1>{key}</key1><body>{body}</body><L>{lnum}</L></H1>\n"


class TestInitQueryP10:
    def test_zero_records_no_nameerror(self, tmp_path):
        """P10: zero <H> records used to raise NameError (keysanskrit unbound)."""
        src = tmp_path / "in.xml"
        out = tmp_path / "query_dump.txt"
        src.write_text("<xml>\n<nothing/>\n</xml>\n", encoding="utf-8")
        r = _run_py(INIT_QUERY, str(src), str(out))
        assert out.exists()
        assert out.read_text(encoding="utf-8") == ""
        assert "0 records read" in r.stdout

    def test_zero_records_no_junk_row(self, tmp_path):
        """A zero-record dump must not carry a junk ` :: \\t ` row."""
        src = tmp_path / "in.xml"
        out = tmp_path / "query_dump.txt"
        src.write_text("garbage line\n", encoding="utf-8")
        _run_py(INIT_QUERY, str(src), str(out))
        for line in out.read_text(encoding="utf-8").splitlines():
            assert "prevkey :: keysanskrit" not in line  # P11 stays dead
            assert line != " :: \t"

    def test_records_format_unchanged(self, tmp_path):
        """With records present the output format is byte-identical to legacy."""
        src = tmp_path / "in.xml"
        out = tmp_path / "query_dump.txt"
        src.write_text(
            _make_xml_line("a", "the first letter <s>A</s>", 1)
            + _make_xml_line("a", "again a", 2)
            + _make_xml_line("i", "indigo <s>indu</s>", 3),
            encoding="utf-8",
        )
        _run_py(INIT_QUERY, str(src), str(out))
        lines = out.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2  # two distinct keys
        assert lines[0].startswith("a :: ")
        assert "\t" in lines[0] and "the first letter" in lines[0]
        assert lines[1].startswith("i :: ")
        assert "indigo" in lines[1]


class TestBuildQueryIndex:
    def _dump_bytes(self):
        line1 = "a :: A\ta word with dia-mond and café\n".encode("utf-8")
        line2 = "i :: I\tindigo\n".encode("utf-8")
        line3 = "z :: Z\twindows line\r\n".encode("utf-8")
        return line1 + line2 + line3

    def test_schema_offsets_and_hyphen_strip(self, tmp_path):
        import sqlite3

        dump = tmp_path / "query_dump.txt"
        idx = tmp_path / "query_dump.sqlite3"
        dump.write_bytes(self._dump_bytes())
        _run_py(BUILD_INDEX, str(dump), str(idx))

        con = sqlite3.connect(idx)
        try:
            assert con.execute("PRAGMA user_version").fetchone()[0] == 1
            dumpsize = con.execute(
                "SELECT v FROM meta WHERE k='dumpsize'"
            ).fetchone()[0]
            assert int(dumpsize) == dump.stat().st_size
            rows = con.execute("SELECT off, t FROM lines ORDER BY off").fetchall()
            assert len(rows) == 3
            # offsets must be byte offsets usable with PHP fseek()
            raw = dump.read_bytes()
            assert raw[rows[0][0] :].startswith(b"a :: A\t")
            assert raw[rows[1][0] :].startswith(b"i :: I\t")
            assert raw[rows[2][0] :].startswith(b"z :: Z\t")
            assert rows[2][0] > rows[1][0] > rows[0][0] == 0
            # '-' removed (querymodel matches hyphen-stripped lines, COLOGNE#75)
            assert "dia-mond" not in rows[0][1]
            assert "diamond" in rows[0][1]
            assert rows[0][1].endswith("café")
        finally:
            con.close()

    def test_rebuild_replaces_existing_index(self, tmp_path):
        import sqlite3

        dump = tmp_path / "query_dump.txt"
        idx = tmp_path / "query_dump.sqlite3"
        dump.write_bytes(self._dump_bytes())
        _run_py(BUILD_INDEX, str(dump), str(idx))
        _run_py(BUILD_INDEX, str(dump), str(idx))  # rebuild over existing file
        con = sqlite3.connect(idx)
        try:
            assert con.execute("SELECT count(*) FROM lines").fetchone()[0] == 3
        finally:
            con.close()


class TestStageWiring:
    def test_redo_sh_builds_and_ships_index_pair(self):
        text = REDO_SH.read_text(encoding="utf-8")
        assert text.splitlines()[0] == "set -e"  # fail-closed (memo P10 note)
        assert "init_query.py" in text
        assert "build_query_index.py query_dump.txt query_dump.sqlite3" in text
        assert "mv query_dump.txt query_dump.sqlite3 ../../web/webtc2/" in text

    def test_inventory_ships_builder_for_all_dicts(self):
        text = INVENTORY.read_text(encoding="utf-8")
        assert "*:pywork/webtc2/build_query_index.py:C" in text
