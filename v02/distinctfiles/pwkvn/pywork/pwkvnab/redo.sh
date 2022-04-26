echo "making pwkvnab.sqlite from pwkvnab_input.txt"
sh redo_pwkvnab.sh
echo "moving pwkvnab.sqlite to web/sqlite/"
mv pwkvnab.sqlite ../../web/sqlite/
