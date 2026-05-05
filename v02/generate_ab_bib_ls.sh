#!/bin/bash
# generate_ab_bib_ls.sh
# Generates redo.sh, redo_xxx.sh, and xxx.sql scripts for all abbreviation,
# tooltip (ls), and bibliography tables.
# Usage: sh generate_ab_bib_ls.sh [PYWORK_DIR]
#   PYWORK_DIR: optional target directory for generated scripts.
#     If omitted, generates into distinctfiles/<dict>/pywork/.
#     If provided (e.g. ../../md/pywork), generates into <dict>/{dict}ab/{dict}auth under it.
# Run from csl-pywork/v02 directory.

set -e

BASEDIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASEDIR"

PYWORK_DIR="$1"

########################################################################
# Helper: target directory resolver
########################################################################
resolve_dir() {
    local dict="$1" sub="$2"
    if [ -n "$PYWORK_DIR" ]; then
        echo "${PYWORK_DIR}/${sub}"
    else
        echo "distinctfiles/${dict}/pywork/${sub}"
    fi
}

########################################################################
# Pattern A: abbreviation tables
########################################################################
generate_ab() {
    local dict="$1"
    local dir
    dir="$(resolve_dir "$dict" "${dict}ab")"
    local t="${dict}ab"
    mkdir -p "$dir"

    # redo_XXab.sh - mwab has extra check.py step
    if [ "$dict" = "mw" ]; then
        cat > "$dir/redo_${t}.sh" <<EOF
echo "checking mwab_input.txt..."
python3 check.py 2 mwab_input.txt
echo "remaking ${t}.sqlite"
rm ${t}.sqlite
python3 ../sqlite/sqlite_txt.py ${t}_input.txt ${t}.sqlite ${t}
echo "finished remaking ${t}.sqlite"
chmod 0755 ${t}.sqlite
EOF
    else
        cat > "$dir/redo_${t}.sh" <<EOF
echo "remaking ${t}.sqlite"
rm ${t}.sqlite
python3 ../sqlite/sqlite_txt.py ${t}_input.txt ${t}.sqlite ${t}
echo "finished remaking ${t}.sqlite"
chmod 0755 ${t}.sqlite
EOF
    fi

    # XXab.sql - identical for all dicts (has create index)
    cat > "$dir/${t}.sql" <<EOF
DROP TABLE if exists ${t};
CREATE TABLE ${t} (
 \`id\` VARCHAR(100)  UNIQUE,
 \`data\` TEXT  NOT NULL
);
.separator "\\t"
.import ${t}_input.txt ${t}
create index datum on ${t}(id);
pragma table_info (${t});
select count(*) from ${t};
.exit
EOF

    # redo.sh - varies by dict
    case "$dict" in
        ap|ap90|bur|lan|mw|stc)
            cat > "$dir/redo.sh" <<EOF
sh redo_${t}.sh
mv ${t}.sqlite ../../web/sqlite/
EOF
            ;;
        ben|cae)
            cat > "$dir/redo.sh" <<EOF
sh redo_${t}.sh
echo "moving ${t}.sqlite to web/sqlite"
mv ${t}.sqlite ../../web/sqlite/
EOF
            ;;
        bhs|gra|md|pw|pwkvn)
            cat > "$dir/redo.sh" <<EOF
echo "making ${t}.sqlite from ${t}_input.txt"
sh redo_${t}.sh
echo "moving ${t}.sqlite to web/sqlite/"
mv ${t}.sqlite ../../web/sqlite/
EOF
            ;;
        pwg)
            cat > "$dir/redo.sh" <<EOF
sh redo_${t}.sh
mv ${t}.sqlite ../../web/sqlite/
EOF
            ;;
    esac

    echo "Generated ${dict}ab scripts"
}

########################################################################
# Pattern B: tooltip tables (ap, ap90, ben, bhs, gra, sch, mw)
########################################################################
generate_tooltip() {
    local dict="$1"
    local dir
    dir="$(resolve_dir "$dict" "${dict}auth")"
    local tbl="${dict}authtooltips"
    mkdir -p "$dir"

    # redo.sh - varies by dict
    if [ "$dict" = "ben" ] || [ "$dict" = "bhs" ] || [ "$dict" = "gra" ]; then
        cat > "$dir/redo.sh" <<EOF
echo "${tbl}.sqlite"
rm -f ${tbl}.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt ${tbl}.sqlite ${tbl}
chmod 0755 ${tbl}.sqlite  # needed?
echo "move ${tbl}.sqlite to web/sqlite"
mv ${tbl}.sqlite ../../web/sqlite/
EOF
    elif [ "$dict" = "mw" ]; then
        cat > "$dir/redo.sh" <<EOF
echo "tooltip.txt ..."
#python tooltip.py roman mwauth.txt tooltip.txt
#echo "temp_tooltip.txt ..."
#python temp_tooltip.py roman mwauth.txt temp_tooltip.txt
echo "${tbl}.sqlite"
rm -f ${tbl}.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt ${tbl}.sqlite ${tbl}
chmod 0755 ${tbl}.sqlite  # needed?
echo "copy ${tbl}.sqlite to web/sqlite"
cp ${tbl}.sqlite ../../web/sqlite/
EOF
    else
        cat > "$dir/redo.sh" <<EOF
echo "${tbl}.sqlite"
rm -f ${tbl}.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt ${tbl}.sqlite ${tbl}
chmod 0755 ${tbl}.sqlite  # needed?
echo "copy ${tbl}.sqlite to web/sqlite"
cp ${tbl}.sqlite ../../web/sqlite/
EOF
    fi

    # SQL file
    if [ "$dict" = "mw" ]; then
        cat > "$dir/${tbl}.sql" <<EOF
DROP TABLE if exists ${tbl};
CREATE TABLE ${tbl} (
 \`cid\` VARCHAR(20) NOT NULL,
 \`key\` VARCHAR(20) NOT NULL,
 \`data\` VARCHAR(20000) NOT NULL,
 \`type\` VARCHAR(20) NOT NULL
);
.separator "\\t"
.import tooltip.txt ${tbl}
pragma table_info (${tbl});
select count(*) from ${tbl};
.exit
EOF
        # mwauthtooltips.sql has CRLF line endings
        python3 -c "
import sys
f = sys.argv[1]
text = open(f, 'rb').read().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
open(f, 'wb').write(text)
" "$dir/${tbl}.sql"
    else
        cat > "$dir/tooltips.sql" <<EOF
DROP TABLE if exists ${tbl};
CREATE TABLE ${tbl} (
 \`key\` VARCHAR(20) NOT NULL,
 \`data\` VARCHAR(20000) NOT NULL
);
.separator "\\t"
.import tooltip.txt ${tbl}
pragma table_info (${tbl});
select count(*) from ${tbl};
.exit
EOF
    fi

    echo "Generated ${dict} tooltip scripts"
}

########################################################################
# Pattern C: bibliography tables (pw, pwg, pwkvn)
########################################################################
generate_bib() {
    local dict="$1"
    local dir
    dir="$(resolve_dir "$dict" "${dict}auth")"
    local bib="${dict}bib"
    mkdir -p "$dir"

    # redo_XXbib.sh - identical for all bib dicts
    cat > "$dir/redo_${bib}.sh" <<EOF
echo "remaking ${bib}.sqlite"
rm ${bib}.sqlite
python3 ../sqlite/sqlite_txt.py ${bib}_input.txt ${bib}.sqlite ${bib}
echo "finished remaking ${bib}.sqlite"
chmod 0755 ${bib}.sqlite
EOF

    # redo.sh - varies by dict
    case "$dict" in
        pw)
            cat > "$dir/redo.sh" <<EOF
#python pwbib_input.py pwbib.txt pwbib_input.txt
python3 check_pwbib.py pwbib_input.txt
sh redo_pwbib.sh
mv pwbib.sqlite ../../web/sqlite/
EOF
            ;;
        pwg)
            cat > "$dir/redo.sh" <<EOF
python3 check_pwbib.py pwgbib_input.txt
sh redo_pwgbib.sh
mv pwgbib.sqlite ../../web/sqlite/
EOF
            ;;
        pwkvn)
            cat > "$dir/redo.sh" <<EOF
#python pwkvnbib_input.py pwkvnbib.txt pwkvnbib_input.txt
python3 check_pwbib.py pwkvnbib_input.txt
sh redo_pwkvnbib.sh
mv pwkvnbib.sqlite ../../web/sqlite/
EOF
            ;;
    esac

    # XXbib.sql - has create index line, CRLF for pw
    if [ "$dict" = "pw" ]; then
        cat > "$dir/${bib}.sql" <<EOF
DROP TABLE if exists ${bib};
CREATE TABLE ${bib} (
 \`id\` VARCHAR(100)  UNIQUE,
 \`code\` TEXT,
 \`codecap\` TEXT,
 \`data\` TEXT  NOT NULL
);
.separator "\\t"
.import ${bib}_input.txt ${bib}
create index datum on ${bib}(id);
pragma table_info (${bib});
select count(*) from ${bib};
.exit
EOF
        python3 -c "
import sys
f = sys.argv[1]
text = open(f, 'rb').read().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
open(f, 'wb').write(text)
" "$dir/${bib}.sql"
    else
        cat > "$dir/${bib}.sql" <<EOF
DROP TABLE if exists ${bib};
CREATE TABLE ${bib} (
 \`id\` VARCHAR(100)  UNIQUE,
 \`code\` TEXT,
 \`codecap\` TEXT,
 \`data\` TEXT  NOT NULL
);
.separator "\\t"
.import ${bib}_input.txt ${bib}
create index datum on ${bib}(id);
pragma table_info (${bib});
select count(*) from ${bib};
.exit
EOF
    fi

    echo "Generated ${dict} bib scripts"
}

########################################################################
# Main
########################################################################
if [ -n "$PYWORK_DIR" ]; then
    dict=$(echo "$PYWORK_DIR" | awk -F'/' '{print $(NF-1)}')
    # Determine which generators to run based on dictionary
    # All dicts in the ab list get ab scripts
    case " ap ap90 ben bhs bur cae gra lan md mw pw pwg pwkvn stc " in
        *" $dict "*) generate_ab "$dict" ;;
    esac
    case " ap ap90 ben bhs gra sch mw " in
        *" $dict "*) generate_tooltip "$dict" ;;
    esac
    case " pw pwg pwkvn " in
        *" $dict "*) generate_bib "$dict" ;;
    esac
    echo "Done. Scripts generated for $dict."
else
    echo "=== Generating abbreviation scripts ==="
    for d in ap ap90 ben bhs bur cae gra lan md mw pw pwg pwkvn stc; do
        generate_ab "$d"
    done

    echo ""
    echo "=== Generating tooltip scripts ==="
    for d in ap ap90 ben bhs gra sch mw; do
        generate_tooltip "$d"
    done

    echo ""
    echo "=== Generating bibliography scripts ==="
    for d in pw pwg pwkvn; do
        generate_bib "$d"
    done

    echo ""
    echo "Done. 27 scripts regenerated."
fi
