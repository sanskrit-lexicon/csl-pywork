echo "making mdab.sqlite from mdab_input.txt"
sh redo_mdab.sh
echo "moving mdab.sqlite to web/sqlite/"
mv mdab.sqlite ../../web/sqlite/
