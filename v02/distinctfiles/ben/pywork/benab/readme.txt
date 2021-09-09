
benab.sqlite

For ongoing maintenance, modify benab_input.txt by hand,
then:
sh redo.sh

###  Initial reformatting
The initial format of abbreviation file was:
abbrev = tooltip

Say this was in file temp_old.txt
python format.py temp_old.txt benab_input.txt
changes format of lines to
abbrev\t<id>abbrev</id> <disp>tooltip</disp>

This format is consistent with benab.sql,
and is understood by the php basicadjust.php program of displays
