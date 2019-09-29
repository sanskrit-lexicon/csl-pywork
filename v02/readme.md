
The 'distinctfiles' directory was initialized in the v01 subdirectory at
Cologne. Specifically, the init_distinctfiles.sh script did the initialization.


## repository requirements
The generate_dict.sh script requires local copies of 3 repositories:

* csl-pywork  (this repository)
* csl-orig
* csl-websanlexicon.

All three repositories are in sibling directories in the file structure.

## generate_dict.sh usage
sh generate_dict.sh `<dict>` `<outdir>`

* `<dict>` is one of the Cologne dictionary codes. Usually lower case
  * bur inm mwe pwg skd stc vcp acc ae ap90 ben bhs bop bor cae ccs gra gst ieg krm mci md mw72 mw pe pgn pui pw sch shs snp vei wil yat
* `<outdir>`  The directory in which will be constructed subdirectories
  named 'orig', 'pywork', 'web'. Note that the outdir will be created
  if does not already exist in the file system.
* Examples
  * sh generate_dict.sh acc tempdir/acc
  * sh generate_dict.sh mw ../../MWScan/2020

## Functional summary
generate_dict.sh does 4 things:
* `sh generate_orig.sh <dict> <outdir>`
  * creates `<outdir>/orig` which contains digitization `<dict>.txt`
  * uses inventory_orig.txt and dictparms
* `sh generate_pywork.sh <dict> <outdir>`
  * creates `<outdir>/pywork` which contains 
    * programs to construct headword files such as `<dict>hw.txt`
    * programs to construct xml file `<dict>.xml`
    * programs to construct `<dict>.sqlite` database form of digitization
      used by displays
    * programs to construct ancillary information used by displays,
      such as abbreviation expansions.
    * files with information about the dictionary such as
      * `<dict>header.xml` license in TEI format
      * `<dict>.dtd` validation form of `<dict>.xml`
  * creates `<outdir>/downloads` which contains 
     download files (for txt, xml, and web)
  * uses inventory.txt and dictparms.py of this (csl-pywork) repository to determine which files are
    constructed for the given value of dictionary code `<dict>`
    Source files are classifed as one of three types:
    * C : file is copied from 'makotemplates' directory
    * T : file in 'makotemplates' directory is treated as a template, with
          various details depending on the parameter values in 'dictparms.py'
          for the particular dictionary code `<dict>`.
    * CD: The file is copied from the `distinctfiles/<dict>` directory
* `sh generate_web.sh <dict> <outdir>`
  * It creates `<outdir>/web` which contains programs and data for web displays.
  * This script is located in and run from the csl-websanlexicon/v02 directory.
    It uses inventory.txt and dictparms.py of csl-websanlexicon/v02; and
    the associated files within 'makotemplates' and 'distinctfiles' subdirectories.
* Runs various scripts in the constructed `<outdir>/pywork` directory:
  * `sh redo_hw.sh` : remakes headword files 
  * `sh redo_xml.sh` : 
   * remakes `<dict>.xml`
   * checks (using `xmllint`) that `<dict>.xml` validates against `<dict>.dtd`
   * `sh redo_postxml.sh`  Runs additional scripts to update such things
      as the abbreviation databases.  Only a few dictionaries have markup
      required for such display enhancements.
  * `sh redo_all.sh` in `<outdir>/downloads` directory recreates three
     zip files for download (for digitization, xml form, and web directory).
## Summary
`sh generate_dict.sh <dict> <outdir>` creates a functional copy of the
current digitization data and displays for the given dictionary. 
The value of the 'outdir' should be a subdirectory of form 'x/y', such as
given in the examples above.
Then, if `<outdir>` is in the scope of a web server, a user may access the
displays.   Let 'OUTDIR-URL' be the url corresponding to `<outdir>`.
Then 'OUTDIR-URL/web' will bring up a menu of displays.

