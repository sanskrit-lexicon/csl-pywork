
Modify stcab_input.txt manually.
Then redo.sh  (remakes stcab.sqlite, and copies it to web/sqlite)

Jan 20, 2020 stcab_input.txt initialized
 start with copy of csl-orig/v02/stc/abbrev/abbreviationsStchoupak.txt.
 reformat it to have the 'standard form' (based on burab_input.txt).
 remove comment lines (those that start with ';')

change redo.sh, redo_stcab.sh, and stcab.sql to refer to stc.

Changes to pywork/v02/
1. inventory.txt:
  add stc to dictionary list in abbreviations section
2. makotemplates/pywork/redo_postxml.sh
