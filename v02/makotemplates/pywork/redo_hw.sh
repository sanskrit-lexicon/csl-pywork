echo "BEGIN redo_hw.sh"
echo "construct xxxhw.txt"
%if (dictlo == 'mw') and cologne_flag: # use python3
python3 hw.py ../orig/${dictlo}.txt hwextra/${dictlo}_hwextra.txt ${dictlo}hw.txt
python3 hw2.py ${dictlo}hw.txt ${dictlo}hw2.txt
python3 hw0.py ${dictlo}hw.txt ${dictlo}hw0.txt
%else:
echo "BEGIN hw.py"
python3 hw.py ../orig/${dictlo}.txt hwextra/${dictlo}_hwextra.txt ${dictlo}hw.txt
echo "END hw.py"
echo ""
echo "BEGIN hw2.py"
python3 hw2.py ${dictlo}hw.txt ${dictlo}hw2.txt
echo "END hw2.py"

echo "BEGIN hw0.py"
python3 hw0.py ${dictlo}hw.txt ${dictlo}hw0.txt
echo "END hw0.py"

%endif
# both hw2.txt and hw0.txt are easily constructed from hw.txt
# not clear, therefore, that either hw2.txt or hw0.txt is needed directly
# We would need to change the 'awork/sanhw1.py' program. 
# To avoid this change might be sufficient reason to keep hw2.txt and hw0.txt
#echo "construct xxxhw2.txt"
#echo "construct xxxhw0.txt"
%if dictlo == 'mw':
echo "construct mwkeys.sqlite"
cd mwkeys
sh redo.sh
%endif
echo "END  redo_hw.sh"
