<?php
// mwupdate/whitmwtab/dbinit.php
// ejf: Nov 8, 2012
// convert xml file to tab-delimited file.
 $filein=$argv[1];;
 $fileout = $argv[2];

 $fp = fopen($filein,"r");
 if (!$fp) {
  echo "ERROR: Could not open $filein<br/>\n";
  exit;
 }
 $fpout = fopen($fileout,"w");
 if (!$fpout) {
  echo "ERROR: Could not open $fileout<br/>\n";
  exit;
 }
$n=0;
 while (!feof($fp)) {
  $line = fgets($fp);
  $line = trim($line);
  if ($line == ''){continue;}
  if (!preg_match('|<key1>(.*?)</key1><L>(.*?)</L><whitkey>(.*?)</whitkey><whitpage>(.*?)</whitpage>|',$line,$matches)) {
   echo "skipping line: $line\n";
   continue;
  }
  $key = $matches[1];
  $lnum = $matches[2];
  $whitkey = $matches[3];
  $whitpage = $matches[4];
  $data = "$whitkey $whitpage";
  $n++;
  fwrite($fpout,"$key\t$lnum\t$data\n");
}
 fclose($fp);
 fclose($fpout);
 echo "$n records read from $filein written to $fileout<br/>\n";
 exit;
?>
