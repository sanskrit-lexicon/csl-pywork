dt=$(date '+%Y%m%d%H%M%S');
echo "STEP 1. SELECT THE FILES TO BE HANDLED BASED ON GIT LOG OF CSL-ORIG REPOSITORY."
cd /var/www/html/cologne/csl-pywork/v02
cd ../../csl-orig
touch v02/.xampp_last_run
git pull origin master
git diff --name-only `(cat v02/.xampp_last_run)`..`(git rev-parse HEAD)` | grep -oP '[\/]\K([^\/]*)(?=[.]txt)' > v02/.files_to_handle

echo "STEP 2. GENERATE DICTIONARIES FOR LOCAL DISPLAY."
cd ../csl-pywork/v02
while read dict;
do
	sh generate_dict.sh $dict  ../../$dict
done < ../../csl-orig/v02/.files_to_handle

echo "STEP 3. GENERATE STARDICT FILES."
cd ../../hwnorm1
git pull origin master
cd ../cologne-stardict
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

echo "STEP 5. UPDATE THE .XAMPP_LAST_RUN FILE."
cd ../csl-orig
git rev-parse HEAD > v02/.xampp_last_run

echo "STEP 6. UPDATE COLOGNE HOMEPAGE TO DISPLAY TODAY'S DATE."
cd ../csl-homepage
bash redo_xampp.sh
cd ../csl-pywork/v02

