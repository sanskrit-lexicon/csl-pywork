#!/bin/sh
# refresh_csl.sh
# Pull all Cologne sibling repos; report per-repo status and exit nonzero
# if any pull failed (H3638 P14: previously 12 sequential bare `git pull`s
# with no aggregation - a dead network on repo 3 was indistinguishable
# from success).
# POSIX sh (invoked historically as `sh refresh_csl.sh`): no bash arrays.
# Assumes invocation from csl-pywork/v02 (../.. = the workspace root).
cd ../..
pwd
repos="csl-orig csl-pywork csl-websanlexicon csl-corrections csl-apidev \
csl-doc csl-homepage hwnorm1 hwnorm2 cologne-stardict csl-lslink \
csl-app"
failed=""
for repo in $repos; do
  echo "Updating $repo"
  if [ ! -d "$repo/.git" ]; then
    echo "FAIL $repo (not a git checkout)"
    failed="$failed $repo"
    continue
  fi
  if (cd "$repo" && git pull); then
    echo "OK   $repo"
  else
    echo "FAIL $repo (git pull failed)"
    failed="$failed $repo"
  fi
done
if [ -n "$failed" ]; then
  echo "refresh_csl: FAILED repos:$failed"
  exit 1
fi
echo "refresh_csl: all repos updated"
