echo "making graab.sqlite from graab_input.txt"
sh redo_graab.sh
echo "moving graab.sqlite to web/sqlite/"
mv graab.sqlite ../../web/sqlite/
