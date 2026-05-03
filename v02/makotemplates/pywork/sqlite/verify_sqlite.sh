#!/bin/bash
# verify_sqlite.sh
# Compares sqlite3-generated databases vs sqlite_txt.py-generated databases
# for all tab-separated input tables.
# Checks: content, schema, indexes, binary

set -e

BASEDIR="/Users/dhaval/Documents/GithubRepos/sanskrit-lexicon/csl-pywork/v02"
LEXBASE="/Users/dhaval/Documents/GithubRepos/sanskrit-lexicon"
SQLITE3="/opt/homebrew/opt/sqlite/bin/sqlite3"
TMPDIR=$(mktemp -d)
CONTENT_PASS=0; CONTENT_FAIL=0
SCHEMA_PASS=0; SCHEMA_FAIL=0
INDEX_PASS=0; INDEX_FAIL=0
BINARY_PASS=0; BINARY_FAIL=0

trap "rm -rf $TMPDIR" EXIT

echo "Working in: $TMPDIR"
echo "SQLite versions: CLI=$($SQLITE3 --version | awk '{print $1}'), Python=$(python3 -c 'import sqlite3; print(sqlite3.sqlite_version)')"
echo ""

compare_db() {
    local label="$1"
    local sql_dir="$2"
    local input_file="$3"
    local table="$4"
    local sql_file="$5"

    local orig_db="$TMPDIR/${table}_orig.sqlite"
    local new_db="$TMPDIR/${table}_new.sqlite"

    echo "--- $label ---"

    if [ ! -f "$sql_dir/$input_file" ]; then
        echo "  SKIP (input file not found)"
        return
    fi

    cp "$sql_dir/$input_file" "$TMPDIR/" 2>/dev/null
    (cd "$TMPDIR" && $SQLITE3 "$orig_db" < "$sql_dir/$sql_file" > /dev/null 2>&1)

    python3 "$BASEDIR/makotemplates/pywork/sqlite/sqlite_txt.py" "$TMPDIR/$input_file" "$new_db" "$table" > /dev/null 2>&1

    # 1. Content comparison
    orig_dump=$($SQLITE3 "$orig_db" "SELECT * FROM $table ORDER BY rowid;" 2>/dev/null)
    new_dump=$($SQLITE3 "$new_db" "SELECT * FROM $table ORDER BY rowid;" 2>/dev/null)
    if [ "$orig_dump" = "$new_dump" ]; then
        echo "  content:   PASS"
        CONTENT_PASS=$((CONTENT_PASS + 1))
    else
        echo "  content:   FAIL"
        CONTENT_FAIL=$((CONTENT_FAIL + 1))
    fi

    # 2. Schema comparison
    orig_schema=$($SQLITE3 "$orig_db" ".schema" 2>/dev/null)
    new_schema=$($SQLITE3 "$new_db" ".schema" 2>/dev/null)
    if [ "$orig_schema" = "$new_schema" ]; then
        echo "  schema:    PASS"
        SCHEMA_PASS=$((SCHEMA_PASS + 1))
    else
        echo "  schema:    FAIL"
        SCHEMA_FAIL=$((SCHEMA_FAIL + 1))
    fi

    # 3. Index comparison
    orig_indexes=$($SQLITE3 "$orig_db" ".indexes" 2>/dev/null)
    new_indexes=$($SQLITE3 "$new_db" ".indexes" 2>/dev/null)
    if [ "$orig_indexes" = "$new_indexes" ]; then
        echo "  indexes:   PASS"
        INDEX_PASS=$((INDEX_PASS + 1))
    else
        echo "  indexes:   FAIL"
        INDEX_FAIL=$((INDEX_FAIL + 1))
    fi

    # 4. Binary comparison (MD5)
    orig_md5=$(md5 -q "$orig_db" 2>/dev/null)
    new_md5=$(md5 -q "$new_db" 2>/dev/null)
    if [ "$orig_md5" = "$new_md5" ]; then
        echo "  binary:    PASS"
        BINARY_PASS=$((BINARY_PASS + 1))
    else
        echo "  binary:    DIFF (internal layout differs)"
        BINARY_FAIL=$((BINARY_FAIL + 1))
    fi

    rm -f "$TMPDIR/$input_file" "$orig_db" "$new_db"
}

# Pattern A: abbreviation tables (2 cols: id, data)
for tbl in stcab mwab pwab benab apab caeab burab bhsab graab lanab mdab pwgab pwkvnab ap90ab; do
    dict=$(echo "$tbl" | sed 's/ab$//')
    if [ "$tbl" = "stcab" ]; then
        dir="$BASEDIR/distinctfiles/stc/pywork/stcab"
    elif [ "$tbl" = "mwab" ]; then
        dir="$BASEDIR/distinctfiles/mw/pywork/mwab"
    elif [ "$tbl" = "pwab" ]; then
        dir="$BASEDIR/distinctfiles/pw/pywork/pwab"
    elif [ "$tbl" = "benab" ]; then
        dir="$BASEDIR/distinctfiles/ben/pywork/benab"
    elif [ "$tbl" = "apab" ]; then
        dir="$BASEDIR/distinctfiles/ap/pywork/apab"
    elif [ "$tbl" = "caeab" ]; then
        dir="$BASEDIR/distinctfiles/cae/pywork/caeab"
    elif [ "$tbl" = "burab" ]; then
        dir="$BASEDIR/distinctfiles/bur/pywork/burab"
    elif [ "$tbl" = "bhsab" ]; then
        dir="$BASEDIR/distinctfiles/bhs/pywork/bhsab"
    elif [ "$tbl" = "graab" ]; then
        dir="$BASEDIR/distinctfiles/gra/pywork/graab"
    elif [ "$tbl" = "lanab" ]; then
        dir="$BASEDIR/distinctfiles/lan/pywork/lanab"
    elif [ "$tbl" = "mdab" ]; then
        dir="$BASEDIR/distinctfiles/md/pywork/mdab"
    elif [ "$tbl" = "pwgab" ]; then
        dir="$BASEDIR/distinctfiles/pwg/pywork/pwgab"
    elif [ "$tbl" = "pwkvnab" ]; then
        dir="$BASEDIR/distinctfiles/pwkvn/pywork/pwkvnab"
    elif [ "$tbl" = "ap90ab" ]; then
        dir="$BASEDIR/distinctfiles/ap90/pywork/ap90ab"
    fi
    compare_db "$tbl abbreviation" "$dir" "${tbl}_input.txt" "$tbl" "${tbl}.sql"
done

# Pattern B: tooltip tables (2 cols: key, data)
compare_db "ap tooltips" "$BASEDIR/distinctfiles/ap/pywork/apauth" "tooltip.txt" "apauthtooltips" "tooltips.sql"
compare_db "sch tooltips" "$BASEDIR/distinctfiles/sch/pywork/schauth" "tooltip.txt" "schauthtooltips" "tooltips.sql"
compare_db "gra tooltips" "$BASEDIR/distinctfiles/gra/pywork/graauth" "tooltip.txt" "graauthtooltips" "tooltips.sql"
compare_db "ben tooltips" "$BASEDIR/distinctfiles/ben/pywork/benauth" "tooltip.txt" "benauthtooltips" "tooltips.sql"
compare_db "bhs tooltips" "$BASEDIR/distinctfiles/bhs/pywork/bhsauth" "tooltip.txt" "bhsauthtooltips" "tooltips.sql"
compare_db "ap90 tooltips" "$BASEDIR/distinctfiles/ap90/pywork/ap90auth" "tooltip.txt" "ap90authtooltips" "tooltips.sql"

# Pattern C: bibliography tables (4 cols: id, code, codecap, data)
compare_db "pw bibliography" "$BASEDIR/distinctfiles/pw/pywork/pwauth" "pwbib_input.txt" "pwbib" "pwbib.sql"
compare_db "pwg bibliography" "$BASEDIR/distinctfiles/pwg/pywork/pwgauth" "pwgbib_input.txt" "pwgbib" "pwgbib.sql"
compare_db "pwkvn bibliography" "$BASEDIR/distinctfiles/pwkvn/pywork/pwkvnauth" "pwkvnbib_input.txt" "pwkvnbib" "pwkvnbib.sql"

# Pattern D: mw tooltips (4 cols: cid, key, data, type)
compare_db "mw tooltips" "$BASEDIR/distinctfiles/mw/pywork/mwauth" "tooltip.txt" "mwauthtooltips" "mwauthtooltips.sql"

# Pattern E: keys (3 cols: key, lnum, data)
compare_db "mw keys" "$LEXBASE/mw/pywork/mwkeys" "extract_keys_b.txt" "mwkeys" "mwkeys.sql"

# Pattern F: tab links (3 cols: key, lnum, data)
compare_db "west mw tab" "$LEXBASE/mw/pywork/westmwtab" "westmwtab_input.txt" "westmwtab" "westmwtab.sql"
compare_db "whit mw tab" "$LEXBASE/mw/pywork/whitmwtab" "whitmwtab_input.txt" "whitmwtab" "whitmwtab.sql"

echo ""
echo "================================"
echo "Content: $CONTENT_PASS passed, $CONTENT_FAIL failed"
echo "Schema:  $SCHEMA_PASS passed, $SCHEMA_FAIL failed"
echo "Indexes: $INDEX_PASS passed, $INDEX_FAIL failed"
echo "Binary:  $BINARY_PASS passed, $BINARY_FAIL failed"
echo "================================"

if [ $CONTENT_FAIL -gt 0 ] || [ $SCHEMA_FAIL -gt 0 ] || [ $INDEX_FAIL -gt 0 ]; then
    exit 1
fi
