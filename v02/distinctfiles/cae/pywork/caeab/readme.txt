
caeab.sqlite

# do once only
# 1) generate caeab_prelim.txt
python abbrev_expanded.py
# 2) generate caeab_input.txt
python make_caeab.py caeab_prelim.txt caeab_input.txt

For ongoing maintenance, modify caeab_input.txt by hand,
then:
sh redo.sh
