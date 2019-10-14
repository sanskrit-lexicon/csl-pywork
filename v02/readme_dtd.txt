
Currently, each xxx.xml validates against its own separate xxx.dtd.
The object here is to get one dtd that applies to ALL dictionaries.
This must be a template, since the xml root of xxx.xml is xxx.
However, with this exception, we want the rest of the template to
require no dictionary-specific parts, if possible.
Currently, xxx.dtd is in v02/distinctfiles/xxx/pywork/xxx.dtd.



; -------------------------------------------------------------

cp ../distinctfiles/acc/pywork/acc.dtd one_v0.dtd
# Manually, change root from 'acc' to ${dictlo} in one_v0.dtd
#
# remove comments from one_v0.dtd, resulting in one.dtd
# (For our purposes, the xml comments  (multiline '<!-- ... -->')
#  are irrelevant in the comparison.)
python no_xml_comment.py one_v0.dtd one.dtd

; --------------------------------------------------------------
strip comments and white space from the distinctfiles/pywork/xxx.dtd
Save results in the local temp_distinctfiles/xxx.dtd
; --------------------------------------------------------------
Note: Currently, the file name for the dtd for xxx is xxx.dtd.  
The current generation code 'T' would generate a file named 'one.dtd' 
We need a new generation code to generate file named 'xxx.dtd' from
template one.dtd, or else we need the filename to imply result xxx.dtd.
; --------------------------------------------------------------
sh check_dict.sh <dict>
  Generates generated/<dict>.dtd
  Checks if it validates ../../../${dictlo}/pywork/${dictlo}.xml
  diff temp_distinctfiles/${dictlo}.dtd generated/${dictlo}.dtd > temp.diff

; 
python check_xml_tags.py ../../../xxx/pywork/xxx.xml temptags.txt
sh check_tags.sh xxx
; -------------------------------------------------------------
changes made to one.dtd (in the order made)
acc: none  (it was used to initialize one.dtd)
ae:  Attribute value 'lb' for n, with element div
ap: <div n="">  CDATA  One value in ap is '?', and this can't be in
    an enumeration.
      Added value 'Q':  <div n="Q">. 
      Changed make_xml.py for AP to use "Q" instead of "?"
    <div name=""> CDATA
    <root/>  new empty element, in body_elts
    add s to elements within 'b'
    add element hom
ap90 add 'lb' to body_elts, and to children of 'b'
    add 'P' to body_elts
ben add 'lang','pic','sup' to child of 'body'
    <lang n="greek"
    <pic name=".."
bhs : no additional changes needed
bop : change children of 'i','b','F' to (#PCDATA  | %body_elts;)*
bor : add elt 'ls'
      add attribute values  1 | I | xe | xs   to attribute 'n' of 'div'
bur : add 'ab' tag.
      add optional 'n' attribute to 'ab'
      add 'lbinfo' tag, with 'n' attribute
      add 's1' tag with 'slp1' attribute
cae : add 'lex' tag
      add (empty) 'vlex' tag with type="root" attribute
      add attribute value 'p' to attribute 'n' of 'div'
ccs : no additional changes needed
gra : add attribute values  H | P1   to attribute 'n' of 'div'
gst : no additional changes needed
ieg : no additional changes needed
inm : add empty tag 'C' with attribute n with values 1 ... 6
      add attribute value 'HI' to attribute 'n' of 'div'
krm : add attribute values  H | P1   to attribute 'n' of 'div'
      add element 'Poem'
      add empty element 'note' with attribute n='1'
      sup element can have 's' element as child (5 lines)
mci : no additional changes needed
md  : no additional changes needed
mw72 : add element 'nsi'
      for 'lang' elt, attribute 'n' add values 'arabic', 'meter', 'slavic',
mwe : no additional changes needed
pd  : no additional changes needed
pe  : no additional changes needed
pgn : no additional changes needed
pui : no additional changes needed
pw  : add element 'is' with attribute n='1'
      add empty element 'sic'
      add element 'bot'
      add value 'russian' to attribute 'n' of 'lang'
      for 'div' element, attribute 'n' add values m | o | 4
      for 'ls' element, attribute 'n'
pwg : add element 'VN'
      for 'F', change form to (#PCDATA | %body_elts;)
      for lang, attribute 'n', add values Russian|Greek|oldhebrew|Old-Church-Slavonic
      for 'div', attribute 'n', add value 'v'
sch : add element 'type'
      add element 'info' with attributes seq, n, part
      for 'hom', attribute n="pwk"
      add 'hom' to children of 'body'
      div does not have attributes.  Change "#REQUIRED" to "#IMPLIED"
         for the attributes of div.
shs : for elt. 'div', attribute 'n', add values E | Poem 
skd : add element 'mark' with attribute 'n'
      for 'C', attribute 'n', add values 7 | 8 | 9 | 10 | 11
snp : Change 'bot' to (#PCDATA  | %body_elts;)*
pui : no additional changes needed
stc : no additional changes needed
vcp : add empty element 'edit' with attribute type="hw"
      for 'C', attribute 'n', add value 12
      for 'div', attribute 'n', add value 'Picture'
vei : no additional changes needed
wil : for 'div', attribute 'n', add value 'lex'
yat : add element 'g'
mw : add children of root (mw) | H2 | H3 | H4 | H1A | H2A | H3A | H4A |
       H1B | H2B | H3B | H4B | H1C | H2C | H3C | H4C | H1E | H2E | H3E | H4E
       Note:  we could include all these for any dictionary.
     add elt. 'bio'
     for 'div' n=: add values to|vp
     add elt. 'etym'
     for elt. 'info', add attributes and, lex, lexcat, or, orsl,
                      phwchild, phwparent, verb, westergaard, whitneyroots
     for elt. 'lang', attr. 'n' add values Arabic|Hindustani|Persian|Turkish
     for elt. 'lang', add attr. script with value Arabic
     for elt. 'lang', change to (#PCDATA | %body_elts; )*
     for elt. 'lex', add attr. type with values 
         hw | hwalt | hwifc | hwinfo | nhw | part | phw 
     add empty elt. 'ns'
     add elt. pb with attr. n
     add empty elt. 'shortlong'
     add empty elt. 'srs'
     add 'info' elt. to children of 'body'
     change attr. 'seq' of elt. 'info' to '#IMPLIED' from '#REQUIRED'
     change attr. 'n' of elt. 'info' to '#IMPLIED' from '#REQUIRED'
     add attr. 'cp' of elt. 'info'
     add attr. 'parse' of elt. 'info'
     add 'srs' to children of 's'
     add 'shortlong' to children of 's'
     add '%body_elts;' to children of 'lex'
     add attr. 'slp1' for elt. 'ab'
; -------------------------------------------------------------
inventory.txt no longer uses the distinctfiles/xxx/pywork/xxx.dtd files.
Rather it uses
*:pywork/one.dtd pywork/${dictlo}.dtd:T

This means that file 'one.dtd' is used as a template for the dtd of all
dictionaries.
Note that 2nd parameter ('pywork/one.dtd pywork/${dictlo}.dtd') specifies
  the input file for all dictionaries is 'pywork/one.dtd', and the corresponding
  output file is 'pywork/${dictlo}.dtd'.
  This use of a space in the 2nd parameter to separate input/output files
  is currently only used here.
  A minor change in generate.py was made to parse this space syntax.
