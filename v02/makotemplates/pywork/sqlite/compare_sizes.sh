#!/bin/bash
BASEDIR="/Users/dhaval/Documents/GithubRepos/sanskrit-lexicon/csl-pywork/v02"
LEXBASE="/Users/dhaval/Documents/GithubRepos/sanskrit-lexicon"
SQLITE3="/opt/homebrew/opt/sqlite/bin/sqlite3"
TMPDIR=$(mktemp -d)

echo "SQLite versions:"
echo "  CLI:     $($SQLITE3 --version | awk '{print $1}')"
echo "  Python:  $(python3 -c 'import sqlite3; print(sqlite3.sqlite_version)')"
echo ""

compare_size() {
    local label="$1" dir="$2" ifile="$3" tbl="$4" sfile="$5"
    cd "$TMPDIR"
    cp "$dir/$ifile" .
    $SQLITE3 "orig_$tbl.sqlite" < "$dir/$sfile" > /dev/null 2>&1
    python3 "$BASEDIR/makotemplates/pywork/sqlite/sqlite_txt.py" "$ifile" "new_$tbl.sqlite" "$tbl" > /dev/null 2>&1
    orig_size=$(stat -f%z "orig_$tbl.sqlite")
    new_size=$(stat -f%z "new_$tbl.sqlite")
    diff=$((orig_size - new_size))
    rows=$($SQLITE3 "orig_$tbl.sqlite" "SELECT count(*) FROM $tbl;")
    avg_row=$((orig_size / rows))
    if [ "$diff" -eq 0 ]; then
        printf "%-20s  rows=%-7s  sqlite3=%-10s  python3=%-10s  diff=0       avg_row=%d\n" "$label" "$rows" "$orig_size" "$new_size" "$avg_row"
    else
        printf "%-20s  rows=%-7s  sqlite3=%-10s  python3=%-10s  diff=%+d   avg_row=%d\n" "$label" "$rows" "$orig_size" "$new_size" "$diff" "$avg_row"
    fi
}

echo "=== Pattern A: abbreviation tables (2 cols) ==="
for tbl in stcab mwab pwab benab apab caeab burab bhsab graab lanab mdab pwgab pwkvnab ap90ab; do
    case "$tbl" in
        stcab)   dir="$BASEDIR/distinctfiles/stc/pywork/stcab" ;;
        mwab)    dir="$BASEDIR/distinctfiles/mw/pywork/mwab" ;;
        pwab)    dir="$BASEDIR/distinctfiles/pw/pywork/pwab" ;;
        benab)   dir="$BASEDIR/distinctfiles/ben/pywork/benab" ;;
        apab)    dir="$BASEDIR/distinctfiles/ap/pywork/apab" ;;
        caeab)   dir="$BASEDIR/distinctfiles/cae/pywork/caeab" ;;
        burab)   dir="$BASEDIR/distinctfiles/bur/pywork/burab" ;;
        bhsab)   dir="$BASEDIR/distinctfiles/bhs/pywork/bhsab" ;;
        graab)   dir="$BASEDIR/distinctfiles/gra/pywork/graab" ;;
        lanab)   dir="$BASEDIR/distinctfiles/lan/pywork/lanab" ;;
        mdab)    dir="$BASEDIR/distinctfiles/md/pywork/mdab" ;;
        pwgab)   dir="$BASEDIR/distinctfiles/pwg/pywork/pwgab" ;;
        pwkvnab) dir="$BASEDIR/distinctfiles/pwkvn/pywork/pwkvnab" ;;
        ap90ab)  dir="$BASEDIR/distinctfiles/ap90/pywork/ap90ab" ;;
    esac
    compare_size "$tbl" "$dir" "${tbl}_input.txt" "$tbl" "${tbl}.sql"
done

echo ""
echo "=== Pattern B: tooltips (2 cols) ==="
compare_size "ap tooltips" "$BASEDIR/distinctfiles/ap/pywork/apauth" tooltip.txt apauthtooltips tooltips.sql
compare_size "sch tooltips" "$BASEDIR/distinctfiles/sch/pywork/schauth" tooltip.txt schauthtooltips tooltips.sql
compare_size "gra tooltips" "$BASEDIR/distinctfiles/gra/pywork/graauth" tooltip.txt graauthtooltips tooltips.sql
compare_size "ben tooltips" "$BASEDIR/distinctfiles/ben/pywork/benauth" tooltip.txt benauthtooltips tooltips.sql
compare_size "bhs tooltips" "$BASEDIR/distinctfiles/bhs/pywork/bhsauth" tooltip.txt bhsauthtooltips tooltips.sql
compare_size "ap90 tooltips" "$BASEDIR/distinctfiles/ap90/pywork/ap90auth" tooltip.txt ap90authtooltips tooltips.sql

echo ""
echo "=== Pattern C: bibliography (4 cols) ==="
compare_size "pw bib" "$BASEDIR/distinctfiles/pw/pywork/pwauth" pwbib_input.txt pwbib pwbib.sql
compare_size "pwg bib" "$BASEDIR/distinctfiles/pwg/pywork/pwgauth" pwgbib_input.txt pwgbib pwgbib.sql
compare_size "pwkvn bib" "$BASEDIR/distinctfiles/pwkvn/pywork/pwkvnauth" pwkvnbib_input.txt pwkvnbib pwkvnbib.sql

echo ""
echo "=== Pattern D: mw tooltips (4 cols) ==="
compare_size "mw tooltips" "$BASEDIR/distinctfiles/mw/pywork/mwauth" tooltip.txt mwauthtooltips mwauthtooltips.sql

echo ""
echo "=== Pattern E: keys (3 cols) ==="
compare_size "mw keys" "$LEXBASE/mw/pywork/mwkeys" extract_keys_b.txt mwkeys mwkeys.sql

echo ""
echo "=== Pattern F: tab links (3 cols) ==="
compare_size "west mw tab" "$LEXBASE/mw/pywork/westmwtab" westmwtab_input.txt westmwtab westmwtab.sql
compare_size "whit mw tab" "$LEXBASE/mw/pywork/whitmwtab" whitmwtab_input.txt whitmwtab whitmwtab.sql

rm -rf "$TMPDIR"
