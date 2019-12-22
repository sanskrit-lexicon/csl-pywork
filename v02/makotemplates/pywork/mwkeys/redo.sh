%if (dictlo == 'mw') and cologne_flag: # use python3
echo "extract_keys"
python3 extract_keys.py ../mwhw.txt  extract_keys.txt
echo "extract_keys_a"
python3 extract_keys_a.py  extract_keys.txt  extract_keys_a.txt 
echo "extract_keys_b"
python3 extract_keys_b.py  extract_keys_a.txt  extract_keys_b.txt 
%else: # just python
echo "extract_keys"
python extract_keys.py ../mwhw.txt  extract_keys.txt
echo "extract_keys_a"
python extract_keys_a.py  extract_keys.txt  extract_keys_a.txt 
echo "extract_keys_b"
python extract_keys_b.py  extract_keys_a.txt  extract_keys_b.txt 
%endif
#rm extract_keys.txt
#rm extract_keys_a.txt
sh redo_mwkeys.sh
mv mwkeys.sqlite ../../web/sqlite/
