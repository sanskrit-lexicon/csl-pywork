echo "BEGIN redo_hw.sh"
echo "construct xxxhw.txt"
python hw.py ../orig/${dictlo}.txt hwextra/${dictlo}_hwextra.txt ${dictlo}hw.txt
# both hw2.txt and hw0.txt are easily constructed from hw.txt
# not clear, therefore, that either hw2.txt or hw0.txt is needed directly
# We would need to change the 'awork/sanhw1.pt' program. 
# To avoid this change might be sufficient reason to keep hw2.txt and hw0.txt
echo "construct xxxhw2.txt"
python hw2.py ${dictlo}hw.txt ${dictlo}hw2.txt
echo "construct xxxhw0.txt"
python hw0.py ${dictlo}hw.txt ${dictlo}hw0.txt
%if dictlo == 'mw':
echo "construct mwkeys.sqlite"
cd mwkeys
sh redo.sh
%endif
echo "DONE redo_hw.sh"
