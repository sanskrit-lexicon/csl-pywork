cd ../../csl-orig
git diff --name-only `(cat v02/.xampp_last_run)`..`(git rev-parse HEAD)` | grep -oP '[\/]\K([^\/]*)(?=[.]txt)' > v02/.files_to_handle
cd ../csl-pywork/v02

while read dict;
do
	sh generate_dict.sh $dict  ../../$dict
done < ../../csl-orig/v02/.files_to_handle

cd ../../csl-orig
git rev-parse HEAD > v02/.xampp_last_run
cd ../csl-pywork/v02

