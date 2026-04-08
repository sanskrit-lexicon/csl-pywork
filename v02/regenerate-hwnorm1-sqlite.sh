#!/bin/bash

set -e

cd "$(dirname "${BASH_SOURCE[0]}")"
WORKSPACE=$(cd ../.. && pwd)

DO_PUSH=false
if [ "$1" = "push" ]; then
    DO_PUSH=true
fi

echo "=== Ensuring repos are up to date ==="
cd "$WORKSPACE/csl-pywork" && echo "Pulling csl-pywork..." && git pull && cd "$WORKSPACE"
cd "$WORKSPACE/csl-orig" && echo "Pulling csl-orig..." && git pull && cd "$WORKSPACE"
cd "$WORKSPACE/csl-websanlexicon" && echo "Pulling csl-websanlexicon..." && git pull && cd "$WORKSPACE"
cd "$WORKSPACE/hwnorm1" && echo "Pulling hwnorm1..." && git pull && cd "$WORKSPACE"
cd "$WORKSPACE/hwnorm2" && echo "Pulling hwnorm2..." && git pull && cd "$WORKSPACE"
cd "$WORKSPACE/csl-apidev" && echo "Pulling csl-apidev..." && git pull && cd "$WORKSPACE"

echo "=== Installing dependencies ==="
pip install mako lxml indic-transliteration
sudo apt-get update && sudo apt-get install -y libxml2-utils sqlite3 unzip

echo "=== Preparing pd folder structure ==="
mkdir -p "$WORKSPACE/pd/orig"
mkdir -p "$WORKSPACE/pd/pywork/hwextra"

echo "=== Downloading and extracting pdtxt.zip ==="
cd "$WORKSPACE/pd/orig"
curl -L -o pdtxt.zip https://www.sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/downloads/pdtxt.zip
unzip -o pdtxt.zip
rm pdtxt.zip
cd "$WORKSPACE"

echo "=== Creating blank hwextra file ==="
touch "$WORKSPACE/pd/pywork/hwextra/pd_hwextra.txt"

echo "=== Running redo_xampp_all.sh ==="
cd "$WORKSPACE/csl-pywork/v02"
sh redo_xampp_all.sh
cd "$WORKSPACE"

echo "=== Running hwnorm1 sanhw1 redo.sh ==="
cd "$WORKSPACE/hwnorm1/sanhw1"
sh redo.sh
cd "$WORKSPACE"

echo "=== Moving hwnorm1c.sqlite to csl-apidev ==="
mkdir -p "$WORKSPACE/csl-apidev/simple-search/hwnorm1"
mv "$WORKSPACE/hwnorm1/sanhw1/hwnorm1c.sqlite" "$WORKSPACE/csl-apidev/simple-search/hwnorm1/"

if $DO_PUSH; then
    echo "=== Committing and pushing hwnorm1 ==="
    cd "$WORKSPACE/hwnorm1"
    git config user.name "HWNORM1 BOT"
    git config user.email "actions@github.com"
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    if git diff --quiet; then
        echo "No changes to commit in hwnorm1"
    else
        git add -A
        git commit -m "Regenerated hwnorm1.sqlite as on $TIMESTAMP"
        git push
    fi
    cd "$WORKSPACE"
fi

echo "=== Running hwnorm2 redo scripts ==="
cd "$WORKSPACE/hwnorm2/keydoc/distincthws"
sh redo.sh
cd ../..
sh redo.sh xampp
cd "$WORKSPACE"

if $DO_PUSH; then
    echo "=== Committing and pushing hwnorm2 ==="
    cd "$WORKSPACE/hwnorm2"
    git config user.name "HWNORM1 BOT"
    git config user.email "actions@github.com"
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    if git diff --quiet; then
        echo "No changes to commit in hwnorm2"
    else
        git add -A
        git commit -m "Regenerated hwnorm2 repo as on $TIMESTAMP"
        git push
    fi
    cd "$WORKSPACE"
fi

if $DO_PUSH; then
    echo "=== Committing and pushing csl-apidev ==="
    cd "$WORKSPACE/csl-apidev"
    git config user.name "HWNORM1 BOT"
    git config user.email "actions@github.com"
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    if git diff --quiet; then
        echo "No changes to commit in csl-apidev"
    else
        git add -A
        git commit -m "Regenerated hwnorm1.sqlite as on $TIMESTAMP"
        git push
    fi
    cd "$WORKSPACE"
fi

echo "=== Done ==="
