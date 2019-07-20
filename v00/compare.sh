# Usage - sh compare.sh script dictcode
echo "Usage - sh compare.sh hw.py vcp"
diff makotemplates/$1 ../../../Cologne_localcopy/$2/pywork/$1
echo "If you saw nothing, there is no diff."
