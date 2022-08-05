See ../readme.org - mwab.sqlite for update details (02-23-2017)

mwupdate/mwab/readme.txt on sanskrit1d
ejf Nov 2, 2012
Nov 6, 2017
Modify mwab_input.txt manually.
Then redo.sh  (remakes mwab.sqlite, and copies it to web/sqlite)
Note (08-05-2022).  redo.sh runs check.py.

Nov 6, 2017.
in work directory:
python filter_simple.py ../../../pywork/mw.xml filter_abbrev.txt
python compare.py filter_abbrev.txt ../mwab_input.txt compare.txt > compare_log.txt
cp mwab_input old/mwab_input_20171103.txt
# some manual changes to mwab_input
cp mwab_input.txt old/mwab_input_20171106.txt
# sort case-insensitive
python work/mwab_sort.py old/mwab_input_20171106.txt mwab_input.txt
------------------------------------------------------------------
Nov 4, 2013. Notes are obsolete. See scans/MWScan/2013/readme.org

1. sh create.sh
 creates the 'mwab' table in the mysql ProdDB database
 This should not need to be repeated.
2. sh load.sh
 deletes all records in 'mwab' table; then loads records
 in from file mwab_init.txt.
3. perl mwab_dump.pl
  dumps all records in 'mwab' table into file mwab_dump.txt,
  which has same format as mwab_init.txt

