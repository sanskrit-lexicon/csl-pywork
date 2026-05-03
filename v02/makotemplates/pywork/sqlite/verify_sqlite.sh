#!/bin/bash
# verify_sqlite.sh
# Compares sqlite3-generated databases vs sqlite_txt.py-generated databases
# for all tab-separated input tables.
# Checks: content, schema, indexes, binary

set -e

# Resolve sqlite3 CLI path
# Strategy: env var > homebrew (macOS) > linuxbrew > system PATH
if [ -n "$SQLITE3" ]; then
    SQLITE3_CMD="$SQLITE3"
elif [ -x /opt/homebrew/opt/sqlite/bin/sqlite3 ]; then
    SQLITE3_CMD="/opt/homebrew/opt/sqlite/bin/sqlite3"
elif [ -x /usr/local/opt/sqlite/bin/sqlite3 ]; then
    SQLITE3_CMD="/usr/local/opt/sqlite/bin/sqlite3"
elif [ -x /home/linuxbrew/.linuxbrew/bin/sqlite3 ]; then
    SQLITE3_CMD="/home/linuxbrew/.linuxbrew/bin/sqlite3"
else
    SQLITE3_CMD=$(command -v sqlite3 2>/dev/null)
    if [ -z "$SQLITE3_CMD" ]; then
        echo "ERROR: sqlite3 not found. Install sqlite3 or set SQLITE3 env var."
        exit 1
    fi
fi

BASEDIR="$(cd "$(dirname "$0")/../../.." && pwd)"
LEXBASE="$(dirname "$(dirname "$BASEDIR")")"
TMPDIR=$(mktemp -d)
CONTENT_PASS=0; CONTENT_FAIL=0
SCHEMA_PASS=0; SCHEMA_FAIL=0
INDEX_PASS=0; INDEX_FAIL=0
BINARY_PASS=0; BINARY_FAIL=0

trap 'rm -rf "$TMPDIR"' EXIT

# Portable MD5: works on macOS (md5 -q) and Linux (md5sum)
get_md5() {
    if command -v md5 &>/dev/null; then
        md5 -q "$1" 2>/dev/null
    elif command -v md5sum &>/dev/null; then
        md5sum "$1" 2>/dev/null | awk '{print $1}'
    else
        echo ""
    fi
}

echo "Working in: $TMPDIR"
CLI_VERSION=$($SQLITE3_CMD --version 2>/dev/null | awk '{print $1}')
PYTHON_VERSION=$(python3 -c 'import sqlite3; print(sqlite3.sqlite_version)' 2>/dev/null)
echo "SQLite versions: CLI=$CLI_VERSION, Python=$PYTHON_VERSION"
if [ "$CLI_VERSION" != "$PYTHON_VERSION" ]; then
    echo "WARNING: Version mismatch may cause binary comparison failures."
    echo "         Content/schema/index checks remain valid."
fi
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

    if [ "$sql_dir/$input_file" != "$TMPDIR/$input_file" ]; then
        cp "$sql_dir/$input_file" "$TMPDIR/" 2>/dev/null
    fi
    (cd "$TMPDIR" && $SQLITE3_CMD "$orig_db" < "$sql_dir/$sql_file" > /dev/null 2>&1)

    python3 "$BASEDIR/makotemplates/pywork/sqlite/sqlite_txt.py" "$TMPDIR/$input_file" "$new_db" "$table" > /dev/null 2>&1

    # 1. Content comparison
    orig_dump=$($SQLITE3_CMD "$orig_db" "SELECT * FROM $table ORDER BY rowid;" 2>/dev/null)
    new_dump=$($SQLITE3_CMD "$new_db" "SELECT * FROM $table ORDER BY rowid;" 2>/dev/null)
    if [ "$orig_dump" = "$new_dump" ]; then
        echo "  content:   PASS"
        CONTENT_PASS=$((CONTENT_PASS + 1))
    else
        echo "  content:   FAIL"
        CONTENT_FAIL=$((CONTENT_FAIL + 1))
    fi

    # 2. Schema comparison
    orig_schema=$($SQLITE3_CMD "$orig_db" ".schema" 2>/dev/null)
    new_schema=$($SQLITE3_CMD "$new_db" ".schema" 2>/dev/null)
    if [ "$orig_schema" = "$new_schema" ]; then
        echo "  schema:    PASS"
        SCHEMA_PASS=$((SCHEMA_PASS + 1))
    else
        echo "  schema:    FAIL"
        SCHEMA_FAIL=$((SCHEMA_FAIL + 1))
    fi

    # 3. Index comparison
    orig_indexes=$($SQLITE3_CMD "$orig_db" ".indexes" 2>/dev/null)
    new_indexes=$($SQLITE3_CMD "$new_db" ".indexes" 2>/dev/null)
    if [ "$orig_indexes" = "$new_indexes" ]; then
        echo "  indexes:   PASS"
        INDEX_PASS=$((INDEX_PASS + 1))
    else
        echo "  indexes:   FAIL"
        INDEX_FAIL=$((INDEX_FAIL + 1))
    fi

    # 4. Binary comparison (MD5)
    orig_md5=$(get_md5 "$orig_db")
    new_md5=$(get_md5 "$new_db")
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
# These input files are generated dynamically by PHP, so we create them first
if command -v php &> /dev/null; then
    cp "$BASEDIR/distinctfiles/mw/pywork/westmwtab/dbinit.php" "$TMPDIR/"
    cp "$BASEDIR/distinctfiles/mw/pywork/westmwtab/mwdp.xml" "$TMPDIR/"
    cp "$BASEDIR/distinctfiles/mw/pywork/westmwtab/westmwtab.sql" "$TMPDIR/"
    php "$TMPDIR/dbinit.php" "$TMPDIR/mwdp.xml" "$TMPDIR/westmwtab_input.txt" > /dev/null 2>&1
    compare_db "west mw tab" "$TMPDIR" "westmwtab_input.txt" "westmwtab" "westmwtab.sql"

    cp "$BASEDIR/distinctfiles/mw/pywork/whitmwtab/dbinit.php" "$TMPDIR/"
    cp "$BASEDIR/distinctfiles/mw/pywork/whitmwtab/mwwhitmap.xml" "$TMPDIR/"
    cp "$BASEDIR/distinctfiles/mw/pywork/whitmwtab/whitmwtab.sql" "$TMPDIR/"
    php "$TMPDIR/dbinit.php" "$TMPDIR/mwwhitmap.xml" "$TMPDIR/whitmwtab_input.txt" > /dev/null 2>&1
    compare_db "whit mw tab" "$TMPDIR" "whitmwtab_input.txt" "whitmwtab" "whitmwtab.sql"

    rm -f "$TMPDIR/dbinit.php" "$TMPDIR/mwdp.xml" "$TMPDIR/mwwhitmap.xml" "$TMPDIR/westmwtab_input.txt" "$TMPDIR/whitmwtab_input.txt" "$TMPDIR/westmwtab.sql" "$TMPDIR/whitmwtab.sql"
else
    echo "--- west mw tab ---"
    echo "  SKIP (php not available to generate input file)"
    echo "--- whit mw tab ---"
    echo "  SKIP (php not available to generate input file)"
fi

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
