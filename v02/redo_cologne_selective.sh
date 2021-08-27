echo "Usage: bash redo_cologne_selective.sh"
dt=$(date '+%Y%m%d%H%M%S');
echo "STEP 1. SELECT THE FILES TO BE HANDLED BASED ON GIT LOG OF CSL-ORIG REPOSITORY."
cd /var/www/html/cologne/csl-pywork/v02
cd ../../csl-orig
touch v02/.cologne_last_run
git pull origin master
git diff --name-only `(cat v02/.cologne_last_run)`..`(git rev-parse HEAD)` | grep -oP '[\/]\K([^\/]*)(?=[.]txt)' > v02/.files_to_handle

echo "STEP 2. GENERATE DICTIONARIES FOR COLOGNE DISPLAY."
cd ../csl-pywork/v02
while read dict;
do
	sh generate_dict.sh $dict  ../../${dict^^}Scan/2020/
done < ../../csl-orig/v02/.files_to_handle

echo "STEP 3. UPDATE THE .XAMPP_LAST_RUN FILE."
cd ../../csl-orig
git rev-parse HEAD > v02/.cologne_last_run

echo "STEP 4. UPDATE COLOGNE HOMEPAGE TO DISPLAY TODAY'S DATE."
cd ../csl-homepage
bash redo_cologne.sh
cd ../csl-pywork/v02

