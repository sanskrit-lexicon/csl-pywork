#!/bin/sh
# refresh_csl.sh — pull every Cologne sibling repo; report per-repo status;
# exit nonzero if ANY pull failed (H3487 G8 / finding P14).
#
# Run from the v02/ directory of a csl-pywork checkout whose parent contains
# the sibling repos (csl-orig, hwnorm1, ...). A dead network on repo 3 is now
# distinguishable from success: every repo is reported OK/FAIL and the script
# exits 1 naming the failures.
cd ../.. || exit 1
BASE=$(pwd)
FAILED=""
for repo in csl-orig csl-pywork csl-websanlexicon csl-corrections csl-apidev \
            csl-doc csl-homepage hwnorm1 hwnorm2 cologne-stardict csl-lslink csl-app; do
    echo "Updating $repo"
    if [ ! -d "$BASE/$repo" ]; then
        echo "FAIL $repo (directory missing)"
        FAILED="$FAILED $repo"
        continue
    fi
    if git -C "$BASE/$repo" pull; then
        echo "OK   $repo"
    else
        echo "FAIL $repo"
        FAILED="$FAILED $repo"
    fi
done
if [ -n "$FAILED" ]; then
    echo "refresh_csl: FAILED pulls:$FAILED"
    exit 1
fi
echo "refresh_csl: all repos up to date"
