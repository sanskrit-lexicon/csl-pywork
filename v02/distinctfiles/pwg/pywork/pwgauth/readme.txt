
pwgauth/readme.txt

06-01-2020
To make changes, modify file pwgbib_input.txt.

Note: pwbib_input.txt has 4 tab-delimited fields.
For consistency with the sqlite construction (pwbib.sql), the
first field must be a unique identifier.
check_pwbib.py checks that pwbib_input.txt conforms to these constraints.
python check_pwbib.py pwbib_input.txt

Note 2:  '&#13;&#10;' is used in long tooltips. 
   the tooltip is displayed with line breaks at these points
   This is same as '\r\n' in Python.
Note 1:
There is some confusion regarding pwgbib_input.txt and pwgbib.txt.
pwgbib.txt is NOT used in remaking the pwbib.sqlite
Reason:
- pwgbib.sql references pwgbib_input.txt
- redo_pwgbib.sh uses pwgbib.sql
- redo.sh uses redo_pwgbib.sh

However, pwgbib.txt IS used by make_xml_ls.py  as part of redo_xml.sh.

This is rather confusing. 
When we make an correction to an abbreviation expansion in pwgbib_input.txt,
this correction makes its way into the display abbreviation tooltip by
means of pwgauth.sqlite.

In the rare case where an entirely new abbreviation is introduced by means
of pwgbib_input.txt,  there would be a need to make a corresponding change
in pwgbib.txt.

SUGGESTION:  It might be better to have a program which constructs 
pwgbib_input.txt from pwgbib.txt (or vice-versa).  This would have the
advantage of having only one source of truth.

Note 2:
bibrec.py  
This is used by make_xml_ls.py
