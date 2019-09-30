
> This version v00 was the first development.  
> It is superceded by the v02 version.

# v00 operating instructions
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

