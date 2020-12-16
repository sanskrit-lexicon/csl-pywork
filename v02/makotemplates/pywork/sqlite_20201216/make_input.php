<?php
/* Got memory error (09/13/2018):
    PHP Fatal error:  Allowed memory size of 134217728 bytes exhausted (tried to allocate 628 bytes) in /afs/
   Refactor to read lines one at a time
*/
 $filein = $argv[1]; //"X.xml";
 $fileout = $argv[2]; //"input.txt";
 $fpin = fopen($filein,"r") or die("Cannot open $filein\n");
 #$lines = file($filein);  // this is line that failed.
 $fpout = fopen($fileout,"w") or die("Cannot open $fileout\n");
 $lnum=0;
 #echo count($lines) . " lines from $filein\n";
 $nlines = 0;
 while (($line = fgets($fpin)) !== false) {
 //foreach($lines as $line){
  $nlines = $nlines + 1;
  $line = trim($line);
  if (!preg_match('|^<H|',$line)) {
   continue;}
  // construct output
  $lnum = $lnum + 1;
  if(!preg_match('|<key1>(.*?)</key1>.*<L>(.*?)</L>|',$line,$matches)) {
   echo "ERROR: Could not find key1,lnum from line: $line\n";
   exit(1);
  }
  $key1 = $matches[1];
  $lnum = $matches[2];
  $data = $line;
  $out = "$key1\t$lnum\t$data";
  fwrite($fpout,"$out\n");
 }
 fclose($fpout);
 fclose($fpin);
 echo  "$nlines lines from $filein\n";
exit(0);

?>
