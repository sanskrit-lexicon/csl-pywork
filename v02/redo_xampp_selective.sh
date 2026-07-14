#!/bin/bash
# redo_xampp_selective.sh
# Compatibility wrapper around the Python 3 driver (csl-pywork#53). Kept as
# the cron entry point so the deployed crontab line never has to change:
#
#   @reboot sleep 120 && bash /var/www/html/cologne/csl-pywork/v02/redo_xampp_selective.sh
#
# For manual runs, dry-runs, or anything beyond the production defaults, call
# the driver directly instead — it has real flags (--dry-run, --no-push,
# --skip-pull, --dict, --stop-after, --manifest, ...). See
# `python3 redo_xampp_selective.py --help` and readme_selective.md.
#
# CSL_BASE / CSL_INDIC_BASE still override the server paths for non-server
# installs, same as before this wrapper existed:
#   CSL_BASE=/home/me/cologne CSL_INDIC_BASE=/home/me/indic-dict \
#     sh redo_xampp_selective.sh

set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/redo_xampp_selective.py" "$@"
