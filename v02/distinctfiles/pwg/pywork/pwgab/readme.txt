
pwgab.sqlite

# 12-14-2017  pwgab_prelim.txt is a copy of pwab_prelim.txt.
#  Currently, most abbreviations are NOT marked.
python make_pwgab.py pwgab_prelim.txt pwgab_input.txt

# redo.sh does above, creates pwgab.sqlite, and copies to web/sqlite/
sh redo.sh
