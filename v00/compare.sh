scripts=(hw2.py)
dicts=(BUR INM MWE PWG SKD STC VCP ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
for dict in ${dicts[*]}
do
	echo $dict
	for script in ${scripts[*]}
	do
		diff ../../../Cologne_localcopy/"${dict,,}"/pywork/"$script" ../../"$dict"Scan/2020/pywork/"$script"
	done
done

