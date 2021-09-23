dt=$(date '+%Y%m%d%H%M%S');
echo "Step 0. UPDATE RELEVANT GIT REPOSITORIES."
cd /var/www/html/cologne/csl-pywork/v02
git pull origin master
cd ../../csl-homepage
git pull origin master
cd ../csl-websanlexicon
git pull origin master
cd ../hwnorm1
git pull origin master
cd ../csl-json
git pull
cd ../cologne-stardict
git pull
cd ../csl-orig
git pull origin master
echo "STEP 1. SELECT THE FILES TO BE HANDLED BASED ON GIT LOG OF CSL-ORIG REPOSITORY."
touch v02/.xampp_last_run
git diff --name-only `(cat v02/.xampp_last_run)`..`(git rev-parse HEAD)` | grep -oP '[\/]\K([^\/]*)(?=[.]txt)' > v02/.files_changed
ls -a v02 | cat | grep '^[^.]*$' > v02/.valid_dicts
# See https://unix.stackexchange.com/questions/398142/common-lines-between-two-files
comm -12 <(sort v02/.files_changed) <(sort v02/.valid_dicts) > v02/.files_to_handle
rm v02/.files_changed
rm v02/.valid_dicts

echo "STEP 2. GENERATE DICTIONARIES FOR LOCAL DISPLAY."
cd ../csl-pywork/v02
while read dict;
do
	sh generate_dict.sh $dict  ../../$dict
done < ../../csl-orig/v02/.files_to_handle

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

echo "STEP 4. UPDATE FOR STARDICT-SANSKRIT-DICTIONARY-UPDATER."
cd ../../indic-dict/stardict-sanskrit
git pull origin master
cd ../../cologne/cologne-stardict
bash move_to_stardict.sh
cd ../../indic-dict/stardict-sanskrit
git add .
git commit -m "update $dt"
git push origin master

echo "STEP 5. GENERATE JSON FILES."
cd ../../cologne/csl-json
while read dict;
do
	python2 json_from_babylon.py $dict
	git add ashtadhyayi.com/
	git commit -m "$dict update $dt"
done < ../csl-orig/v02/.files_to_handle
git push

echo "STEP 6. UPDATE THE .XAMPP_LAST_RUN AND .VERSION FILE."
cd ../csl-orig
git rev-parse HEAD > v02/.xampp_last_run
echo "2.0.`git log | grep '^commit' | wc -l`" > .version

echo "STEP 7. UPDATE HOMEPAGE TO DISPLAY TODAY'S DATE."
cd ../csl-homepage
bash redo_xampp.sh
cd ../csl-pywork/v02

