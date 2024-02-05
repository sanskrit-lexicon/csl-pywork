issue32

Ref: https://github.com/sanskrit-lexicon/csl-pywork/issues/32

Change '<pe>' tag to '<per>' in gra.txt and md.txt in csl-orig

csl-orig at commit 1dd36646da9f7ba380d49e658c09b7f40a98fd7e
------------------------------------------------------------
cp /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt temp_gra_0.txt
cp /c/xampp/htdocs/cologne/csl-orig/v02/md/md.txt temp_md_0.txt

------------------------------------------------------------
1809 matches in 1775 lines for "<pe>" in buffer: temp_gra_0.txt
5 matches in 4 lines for "<pe " in buffer: temp_gra_0.txt

cp temp_gra_0.txt temp_gra_1.txt
Manually change in temp_gra_1.txt

------------------------------------------------------------
314 matches in 188 lines for "<pe>" in buffer: temp_md_0.tx
0 matches in 4 lines for "<pe " in buffer: temp_md_0.txt

cp temp_md_0.txt temp_md_1.txt
Manually change in temp_md_1.txt

------------------------------------------------------------
revise csl-pywork:  one.dtd
revise csl-websanlexicon:  basicadjust.php
  treat per tag like ab tag in gra, md

install gra, md locally 
cp temp_gra_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt
cp temp_md_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/md/md.txt

cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh gra  ../../gra
sh xmlchk_xampp.sh gra
# ok

sh generate_dict.sh md  ../../md
sh xmlchk_xampp.sh md
# ok

----
sync repositories to github
---
cd /c/xampp/htdocs/cologne/csl-websanlexicon
git add .
git commit -m "gra, md  and 'per' tag;
Ref: https://github.com/sanskrit-lexicon/csl-pywork/issues/32"
git push
---
cd /c/xampp/htdocs/cologne/csl-pywork
git add .
git commit -m "per tag. #32"
git push
---
# copy basicadjust.php from csl-websanlexicon to cal-apidev
cd /c/xampp/htdocs/cologne/csl-apidev
git add .
git commit -m "gra, md  and 'per' tag;
Ref: https://github.com/sanskrit-lexicon/csl-pywork/issues/32"
git push
---
cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "gra, md  and 'per' tag;
Ref: https://github.com/sanskrit-lexicon/csl-pywork/issues/32"
git push
--------------------------------------------------------
sync cologne server
csl-orig
csl-websanlexicon
csl-pywork
csl-apidev
-----
regenerate displays for
cd csl-pywork/v02
gra
md
pe

DONE
