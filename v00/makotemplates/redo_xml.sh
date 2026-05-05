<%doc>
redo_xml.sh — Mako template. Rendered per-dictionary by generate.py / redo_cologne_2020.sh.
Template variables: ${dictlo} (lowercase code), ${dictup} (uppercase code).

Generated script reads orig/<dict>.txt directly from csl-orig/v00/csl-data/<DICT>Scan/2020/.
Produces <dict>.xml, validates it with xmllint against <dict>.dtd, then:
  - runs sqlite/redo.sh to build <dict>.sqlite
  - runs webtc2/init_query.sh to build the advanced-search query dump

Note: v00 is superseded by v02, which reads orig/ from a local copy and uses
redo_postxml.sh for the post-XML steps.
</%doc>
echo "BEGIN redo_xml.sh"
echo "construct ${dictlo}.xml..."
python make_xml.py ../../../csl-orig/v00/csl-data/${dictup}Scan/2020/orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
echo "xmllint on ${dictlo}.xml..."
xmllint --noout --valid ${dictlo}.xml
echo "${dictlo}.sqlite..."
cd ../web/sqlite
sh redo.sh
echo "query_dump ..."
cd ../webtc2
sh init_query.sh
echo "END redo_xml.sh"
