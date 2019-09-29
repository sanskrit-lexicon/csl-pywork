sh extract_keys.sh
sh extract_keys_a.sh
sh extract_keys_b.sh

#rm extract_keys.txt
#rm extract_keys_a.txt
sh redo_mwkeys.sh
mv mwkeys.sqlite ../../web/sqlite/
