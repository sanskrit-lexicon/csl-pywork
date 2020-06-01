
pwauth/readme.txt

06-01-2020
To make changes, modify file pwbib_input.txt.

Note 1:
There is some confusion regarding pwbib_input.txt and pwbib.txt.
pwbib.txt is NOT used in remaking the pwbib.sqlite
Reason:
- pwbib.sql references pwbib_input.txt
- redo_pwbib.sh uses pwbib.sql
- redo.sh uses redo_pwbib.sh

However, pwbib.txt IS used by make_xml_ls.py  as part of redo_xml.sh.

This is rather confusing. 
When we make an correction to an abbreviation expansion in pwbib_input.txt,
this correction makes its way into the display abbreviation tooltip by
means of pwauth.sqlite.

In the rare case where an entirely new abbreviation is introduced by means
of pwbib_input.txt,  there would be a need to make a corresponding change
in pwbib.txt.

SUGGESTION:  It might be better to have a program which constructs 
pwbib_input.txt from pwbib.txt (or vice-versa).  This would have the
advantage of having only one source of truth.

Note 2:
bibrec.py  
This is used by make_xml_ls.py
