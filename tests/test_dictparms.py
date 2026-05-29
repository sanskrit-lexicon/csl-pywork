"""Unit tests for dictparms.py — the central dictionary registry.

Validates structural invariants for all registered dictionaries so that
typos or malformed entries are caught at CI time rather than silently
producing bad generated output.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "v02"))
import dictparms

REQUIRED_FIELDS = ("dictup", "dictlo", "dictname", "dictversion")
ALL_ENTRIES = list(dictparms.alldictparms.items())


@pytest.mark.parametrize("key, entry", ALL_ENTRIES)
class TestDictEntry:
    def test_required_fields_present(self, key, entry):
        for field in REQUIRED_FIELDS:
            assert field in entry, f"{key}: missing field '{field}'"

    def test_dictlo_matches_key(self, key, entry):
        assert entry["dictlo"] == key, (
            f"dictlo '{entry['dictlo']}' does not match registry key '{key}'"
        )

    def test_dictup_is_uppercase_of_key(self, key, entry):
        assert entry["dictup"] == key.upper(), (
            f"dictup '{entry['dictup']}' is not key.upper() for key '{key}'"
        )

    def test_dictname_nonempty_string(self, key, entry):
        assert isinstance(entry["dictname"], str) and entry["dictname"].strip(), (
            f"{key}: dictname is empty or not a string"
        )

    def test_dictversion_nonempty_string(self, key, entry):
        assert isinstance(entry["dictversion"], str) and entry["dictversion"].strip(), (
            f"{key}: dictversion is empty or not a string"
        )


class TestRegistryGlobal:
    def test_minimum_entry_count(self):
        assert len(dictparms.alldictparms) >= 44, (
            f"Expected at least 44 dicts, got {len(dictparms.alldictparms)}"
        )

    def test_no_duplicate_dictup(self):
        seen = {}
        for key, entry in dictparms.alldictparms.items():
            up = entry["dictup"]
            assert up not in seen, (
                f"dictup '{up}' appears in both '{seen[up]}' and '{key}'"
            )
            seen[up] = key

    def test_microversion_format(self):
        mv = dictparms.microversion
        assert isinstance(mv, str) and mv.startswith("."), (
            f"microversion '{mv}' should start with '.'"
        )
