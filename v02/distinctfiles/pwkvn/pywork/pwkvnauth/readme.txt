
pwkvnauth/readme.txt

04-16-2022 (adapted from pwauth)
To make changes, modify file pwkvnbib_input.txt.

Note: pwkvnbib_input.txt has 4 tab-delimited fields.
For consistency with the sqlite construction (pwkvnbib.sql), the
first field must be a unique identifier.
check_pwbib.py checks that pwkvnbib_input.txt conforms to these constraints.
python check_pwbib.py pwkvnbib_input.txt

Note 1:
There is some confusion regarding pwkvnbib_input.txt and pwkvnbib.txt.
pwkvnbib.txt is NOT used in remaking the pwkvnbib.sqlite
Reason:
- pwkvnbib.sql references pwkvnbib_input.txt
- redo_pwkvnbib.sh uses pwkvnbib.sql
- redo.sh uses redo_pwkvnbib.sh

However, pwkvnbib.txt IS used by make_xml_ls.py  as part of redo_xml.sh.
Note: 10-26-2021.  I think make_xml_ls.py is NOT now part of redo_xml.sh for pwkvn
      Thus, pwkvnbib.txt and pwkvnbib_input.txt are allowed to be out of sync.
      
This is rather confusing. 
When we make an correction to an abbreviation expansion in pwkvnbib_input.txt,
this correction makes its way into the display abbreviation tooltip by
means of pwkvnauth.sqlite.

In the rare case where an entirely new abbreviation is introduced by means
of pwkvnbib_input.txt,  there would be a need to make a corresponding change
in pwkvnbib.txt.

SUGGESTION:  It might be better to have a program which constructs 
pwkvnbib_input.txt from pwkvnbib.txt (or vice-versa).  This would have the
advantage of having only one source of truth.

Note 2:
bibrec.py  
This is used by make_xml_ls.py
