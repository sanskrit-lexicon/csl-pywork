<%doc>
redo_hw.sh — Mako template. Rendered per-dictionary by generate.py / redo_cologne_2020.sh.
Template variables: ${dictlo} (lowercase code), ${dictup} (uppercase code).

Generated script reads orig/<dict>.txt and hwextra/<dict>_hwextra.txt directly
from csl-orig/v00/csl-data/<DICT>Scan/2020/ (absolute path from csl-orig sibling).
Produces <dict>hw.txt, <dict>hw2.txt, <dict>hw0.txt in the pywork/ directory.

Note: v00 is superseded by v02, which reads orig/ from a local copy instead.
</%doc>
echo "BEGIN redo_hw.sh"
echo "construct ${dictlo}hw.txt"
python hw.py ../../../csl-orig/v00/csl-data/${dictup}Scan/2020/orig/${dictlo}.txt ../../../csl-orig/v00/csl-data/${dictup}Scan/2020/orig/hwextra/${dictlo}_hwextra.txt ${dictlo}hw.txt
# both hw2.txt and hw0.txt are easily constructed from hw.txt
# not clear, therefore, that either hw2.txt or hw0.txt is needed directly
# We would need to change the 'awork/sanhw1.pt' program. 
# To avoid this change might be sufficient reason to keep hw2.txt and hw0.txt
echo "construct ${dictlo}hw2.txt"
python hw2.py ${dictlo}hw.txt ${dictlo}hw2.txt
echo "construct ${dictlo}hw0.txt"
python hw0.py ${dictlo}hw.txt ${dictlo}hw0.txt
echo "DONE redo_hw.sh"
