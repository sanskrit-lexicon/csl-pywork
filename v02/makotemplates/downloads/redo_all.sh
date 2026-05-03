output=$(sh redo_txt.sh 2>&1)
printf "%s\n" "$output" | awk '
/BEGIN: downloads\/redo_txt\.sh$/ { in_txt=1; txt_line=0; print; next }
/END: downloads\/redo_txt\.sh$/ { in_txt=0; print; next }
in_txt {
  txt_line++
  ok=0
  if (txt_line==1 && $0 ~ /^remove old .*txt\.zip$/) ok=1
  if (txt_line==2 && $0 == "copying files from ../pywork to txt/") ok=1
  if (txt_line==3 && $0 ~ /^create new .*txt\.zip$/) ok=1
  if (ok) { print }
  else { printf "\033[31m%s\033[0m\n", $0 }
  next
}
{ print }
'
output=$(sh redo_xml.sh 2>&1)
printf "%s\n" "$output" | awk '
/BEGIN: downloads\/redo_xml\.sh$/ { in_xml=1; xml_line=0; print; next }
/END: downloads\/redo_xml\.sh$/ { in_xml=0; print; next }
in_xml {
  xml_line++
  ok=0
  if (xml_line==1 && $0 ~ /^remove old .*xml\.zip$/) ok=1
  if (xml_line==2 && $0 == "copying files from ../pywork to xml/") ok=1
  if (xml_line==3 && $0 ~ /^create new .*xml\.zip$/) ok=1
  if (ok) { print }
  else { printf "\033[31m%s\033[0m\n", $0 }
  next
}
{ print }
'
output=$(sh redo_web.sh 2>&1)
printf "%s\n" "$output" | awk '
/BEGIN: downloads\/redo_web1\.sh$/ { in_web=1; web_line=0; print; next }
/END: downloads\/redo_web1\.sh$/ { in_web=0; print; next }
in_web {
  web_line++
  ok=0
  if (web_line==1 && $0 ~ /^remove old .*web1\.zip$/) ok=1
  if (ok) { print }
  else { printf "\033[31m%s\033[0m\n", $0 }
  next
}
{ print }
'
