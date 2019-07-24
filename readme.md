# Git based workflow

Now the 2020 version is based on github.
There are only three github repositories which can regenerate a full Cologne Sanskrit lexicon website either on remote server or local machine.
They are csl-orig, csl-pywork and csl-websanlexicon. 

1. csl-orig has only two files per dictionary. Their paths are csl-orig/v00/csl-data/XXXScan/2020/orig/xxx.txt and csl-orig/v00/csl-data/XXXScan/2020/orig/hwextra/xxx_hwextra.txt, where XXX stands for the dictionary code in uppercase and xxx stands for the dictionary code in lowercase. These are the least minimum amount of data from which everything else is calculated / derived by scripts.
2. csl-pywork has following two folders, on basis of which the python code for a specific dictionary is generated.
They are (a) distinctscripts and (b) makotemplates. 
(a) distinctscripts currently house two scripts per dictionary (a1) make_xml.py and (a2) xxx.dtd.
These two items are supposed to be too divergent between dictionaries that it was considered too labour-intensive to create a single code for all dictionaries.
(b) makotemplates house two types of scripts (b1) Copied (b2) Templated.
The scripts which have no differences across dictionaries are Copied.
The scripts which have some differences in them are Templated.
The classification of Copied and Templated are marked by 'C' or 'T' in inventory.txt file.
3. csl-websanlexicon is concerned with the generation of scripts for display of various dictionaries.
It also has two types of scripts in makotemplates folder - Copied and Templated.
The description is the same as in csl-pywork.

# Prerequisites

1. python2.6.4 or above / python3.4.10 or above
2. php
3. git
4. apache2 - To run the localhost
4. mako - `pip install mako`

# Install for the first time

This may take some time.
If you want to keep it to the minimum for a local installation, you can use `git clone --depth 1` instead of `git clone`.
That would not download unnecessary git history.

```bash
mkdir scans
cd scans
echo "STEP 1. CLONE THE WEB DISPLAY CODE BASE FROM GITHUB."
git clone https://github.com/sanskrit-lexicon/csl-websanlexicon.git
cd csl-websanlexicon/v00
bash redo_cologne_2020.sh
cd ../..
echo "STEP 2. CLONE THE PYWORK CODE BASE FROM GITHUB."
git clone https://github.com/sanskrit-lexicon/csl-pywork.git
cd csl-pywork/v00
bash redo_cologne_2020.sh
cd ../..
echo "STEP 3. CLONE THE DICTIONARY TEXT FILES FROM GITHUB."
git clone https://github.com/sanskrit-lexicon/csl-orig.git
```

# Subsequent updation

It presumes that you are in the parent directory of csl-orig, csl-pywork and csl-websanlexicon.
Because you have already cloned the repositories, all subsequent changes can be captured by simple `git pull origin master` for these three repositories.

```bash
echo "STEP 1. UPDATE THE WEB DISPLAY CODE BASE FROM GITHUB."
cd csl-websanlexicon/v00
git pull origin master
bash redo_cologne_2020.sh
echo "STEP 2. UPDATE THE PYWORK CODE BASE FROM GITHUB."
cd ../../csl-pywork/v00
git pull origin master
bash redo_cologne_2020.sh
echo "STEP 3. UPDATE THE DICTIONARY TEXT FILES FROM GITHUB."
cd ../../csl-orig/v00
git pull origin master
```

# Dictionary updation based on Correction form submission by user.

1. Instead of the earlier changes by updateByLine.py method, the changes now onwards will be made directly to csl-orig/v00/csl-data/XXXScan/orig/xxx.txt file directly e.g. PWGScan/orig/pwg.txt file directly.
2. On local machine, do `cd /path/to/csl-orig` and then `git pull origin master` to fetch any change made on github by any other user.
3. Make necessary changes in local repository.
4. Once a change is made, it would be added via `git add v00/csl-data/XXXScan/orig/xxx.txt` command.
5. `git commit -m 'dictcode:lnum:old:new'` e.g. `git commit -m 'skd:29044:SuMllam:Sullam'`
6. `git push origin master`

# Install the changes for display.

This pulls any changes from the github repositories and updates the dictionaries.
Generates the xml and sqlite files.

1. For regenerating all dictionaries.
```bash
cd csl-pywork
bash redo.sh
```

or 

2. For regenerating for a particular dictionary e.g. SKD in our example
```bash
cd csl-pywork
bash redo.sh SKD
```

# XXX.txt and hwextra/xxx_hwextra.txt

These files are taken from Cologne server (2013/2014 displays depending on the dictionary).
The data is fetched on 23 Jul 2019.
There is only one change pending in the correctionform.txt on this time.
This change will be made in the 2020 version.
```
Case 24441: 07/21/2019 dict=MW, L= 141468, hw=plu, user=
old = or plāvayati
new = or plavayati
status = PENDING
```

