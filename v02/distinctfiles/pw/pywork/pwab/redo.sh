echo "making pwab.sqlite from pwab_input.txt"
sh redo_pwab.sh
echo "moving pwab.sqlite to web/sqlite/"
mv pwab.sqlite ../../web/sqlite/
