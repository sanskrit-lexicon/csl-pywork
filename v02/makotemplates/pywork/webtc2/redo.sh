set -e
python3 init_query.py ../${dictlo}.xml query_dump.txt
# H3633 (G3): generation-time search index alongside the flat file.
# querymodel.php consults it when present and falls back to the plain
# query_dump.txt scan when it is absent (or stale).
python3 build_query_index.py query_dump.txt query_dump.sqlite3
# move to webtc2
mv query_dump.txt query_dump.sqlite3 ../../web/webtc2/
