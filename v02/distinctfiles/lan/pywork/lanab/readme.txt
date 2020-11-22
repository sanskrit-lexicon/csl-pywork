
Modify lanab_input.txt manually.
Then redo.sh  (remakes lanab.sqlite, and copies it to web/sqlite)

Jul 2, 2018

lanab_prep.txt prepared from Abbreviations (pages 293-4) of 
Lanman Sanskrit Reader.


# rearrange in format used by mw, pwg, pw for abbreviations.
python reformat.py burab_prep.txt burab_input.txt

Nov 6, 2017.
in work directory:
python filter_simple.py ../../../pywork/bur.xml filter_abbrev.txt
python compare.py filter_abbrev.txt ../burab_input.txt compare.txt > compare_log.txt
cp burab_input old/burab_input_20171103.txt
# some manual changes to burab_input
cp burab_input.txt old/burab_input_20171106.txt
# sort case-insensitive
python work/burab_sort.py old/burab_input_20171106.txt burab_input.txt
------------------------------------------------------------------
Nov 4, 2013. Notes are obsolete. See scans/BURScan/2013/readme.org

1. sh create.sh
 creates the 'burab' table in the mysql ProdDB database
 This should not need to be repeated.
2. sh load.sh
 deletes all records in 'burab' table; then loads records
 in from file burab_init.txt.
3. perl burab_dump.pl
  dumps all records in 'burab' table into file burab_dump.txt,
  which has same format as burab_init.txt

