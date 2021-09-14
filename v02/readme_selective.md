# Usage

Put the following in the crontab of your computer.
Whenever you reboot your computer, everything should be auto-updated.
`@reboot sleep 120 && bash /var/www/html/cologne/csl-pywork/v02/redo_xampp_selective.sh`


# Prerequisites

1. Folder structure - cologne/csl-orig, cologne/csl-pywork, cologne/csl-websanlexicon, cologne/csl-devanagari, cologne/csl-json, cologne/csl-homepage, cologne/hwnorm1, cologne/cologne-stardict, indic-dict/stardict-sanskrit
2. cologne and indic-dict are siblings.
3. Credentials for github are cached or stored in the system, and allow you to pull or push to the above repositories without prompting for passwords.


# Explanation.

## Step 0.  UPDATE RELEVANT GIT REPOSITORIES.

```bash
echo "Step 0. UPDATE RELEVANT GIT REPOSITORIES."
cd /var/www/html/cologne/csl-pywork/v02
git pull origin master
cd ../../csl-homepage
git pull origin master
cd ../csl-websanlexicon
git pull origin master
cd ../hwnorm1
git pull origin master
cd ../csl-orig
git pull origin master
```

Updates the csl-pywork, csl-homepage, csl-websanlexicon, hwnorm1 and csl-orig repositories to their latest versions.

## Step 1. Find out files which are changed from last run of the program.

```bash
echo "STEP 1. SELECT THE FILES TO BE HANDLED BASED ON GIT LOG OF CSL-ORIG REPOSITORY."
touch v02/.xampp_last_run
git diff --name-only `(cat v02/.xampp_last_run)`..`(git rev-parse HEAD)` | grep -oP '[\/]\K([^\/]*)(?=[.]txt)' > v02/.files_to_handle
```

`touch v02/.xampp_last_run` creates the blank file if it does not exist.
`git diff` line finds out the .txt files which are changed since the commit number stored in `csl-orig/v02/.xampp_last_run` file (i.e. the last time the code was run) and the HEAD (i.e. the latest commit in csl-orig repository.)


## Step 2. GENERATE DICTIONARIES FOR LOCAL DISPLAY.

```bash
echo "STEP 2. GENERATE DICTIONARIES FOR LOCAL DISPLAY."
cd ../csl-pywork/v02
while read dict;
do
	sh generate_dict.sh $dict  ../../$dict
done < ../../csl-orig/v02/.files_to_handle
```

For every file to be handled between the last handled commit and present commit, the dictionaries are regenerated via `generate_dict.sh` script.


## STEP 3. GENERATE STARDICT FILES.

```bash
echo "STEP 3. GENERATE STARDICT FILES."
cd ../../cologne-stardict
cp ../hwnorm1/sanhw1/hwnorm1c.txt input/hwnorm1c.txt
while read dict;
do
	python2 make_babylon.py $dict 0
	python2 make_babylon.py $dict 1
	git add output/
	git add production/
	git commit -m "$dict update $dt"
done < ../csl-orig/v02/.files_to_handle
git push
```


For every file which is changed, babylon files are generated.
e.g. `python2 make_babylon.py wil 0` will regenerate Wilson dictionary babylon file for reading purpose, with `\n` as line break marker, and stored in output folder.
`python2 make_babylon.py wil 1` will regenerate Wilson dictionary babylon file for display purpose, with `<BR>` as line break marker and stored in production folder.
Both output and production folders are added in git.
The commit message has name of dictionary changed and datetime, making it a unique message which explains which change happenned when.
After updating for all such dictionaries as may be updated, the changes are pushed to github.

## STEP 4. UPDATE FOR STARDICT-SANSKRIT-DICTIONARY-UPDATER.

```bash
echo "STEP 4. UPDATE FOR STARDICT-SANSKRIT-DICTIONARY-UPDATER."
cd ../../indic-dict/stardict-sanskrit
git pull origin master
cd ../../cologne/cologne-stardict
bash move_to_stardict.sh
cd ../../indic-dict/stardict-sanskrit
git add .
git commit -m "update $dt"
git push origin master
```

Update the indic-dict/stardict-sanskrit repository.
Go to the cologne/cologne-stardict repository and move the concerned babylon files to their respective places in indic-dict/stardict-sanskrit repository.
Add the changed files, commit and push in the indic-dict/stardict-sanskrit repository.
indic-dict/stardict-sanskrit repository has CI/CD in place which creates stardict files from new babylon files and pushes them to gh branch of the repository and also updates the index shown on their stardict-dictionary-updater application.

## STEP 5. GENERATE JSON FILES.

```bash
echo "STEP 5. GENERATE JSON FILES."
cd ../../cologne/csl-json
while read dict;
do
	python2 json_from_babylon.py $dict
	git add ashtadhyayi.com/
	git commit -m "$dict update $dt"
done < ../csl-orig/v02/.files_to_handle
git push
```

Regenerate the JSON files for changed files.
Add, commit and then push to the cologne/csl-json repository.
www.ashtadhyayi.com uses this data for their dictionary search facility, which has a nice UI and user experience.

## STEP 6. UPDATE THE .XAMPP_LAST_RUN AND .VERSION FILE.

```bash
echo "STEP 6. UPDATE THE .XAMPP_LAST_RUN AND .VERSION FILE."
cd ../csl-orig
git rev-parse HEAD > v02/.xampp_last_run
echo "2.0.`git log | grep '^commit' | wc -l`" > .version
```

`git rev-parse HEAD` shows the latest commit i.e. HEAD. It is stored in `csl-orig/v02/.xampp_last_run` file. 
Whenever this selective code is run again, only the commits after this commit would be processed.
This would reduce the unnecessary regeneration of files, if there is no change since the last run.
`git log | grep '^commit' | wc -l` would give the number of commits in csl-orig repository.
If the number of commits are 596, the version would be 2.0.596. 
`2.0.596` is stored in csl-orig/.version file.
This csl-orig/.version file is not tracked via git.
This file is used by the next step to show the version number in the homepage.

## STEP 7. UPDATE HOMEPAGE TO DISPLAY TODAY'S DATE.

```bash
echo "STEP 7. UPDATE HOMEPAGE TO DISPLAY TODAY'S DATE."
cd ../csl-homepage
bash redo_xampp.sh
cd ../csl-pywork/v02
```

`redo_xampp.sh` code calls `index_xampp.py` which uses `csl-orig/.version` file to show version number at two places in the homepage, one at the heading and the second at the bibliographic reference section.

