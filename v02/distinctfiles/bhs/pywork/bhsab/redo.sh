echo "making bhsab.sqlite from bhsab_input.txt"
sh redo_bhsab.sh
echo "moving bhsab.sqlite to web/sqlite/"
mv bhsab.sqlite ../../web/sqlite/
