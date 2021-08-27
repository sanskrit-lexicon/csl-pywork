
# Installation of Cologne sanskrit-lexicon from repositories

This describes in some detail how to install the Cologne sanskrit-lexicon from Github repositories.
In addition to the 3-repository installation instructions described below, there are also 'optional'
installations from repositories. 
* csl-homepage   
* csl-doc
* csl-whitroot
* csl-kale
* csl-apidev

 
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


## Software Prerequisites

1. python  (python2.6.4 or above / python3.4.10 or above)
   * Not all parts are python3 compatible as of 9/29/2019.
   *  mako - `pip install mako`
2. php  
   * cli version required in addition to normal web server ver
   * pdo driver
3. git
4. apache2 - To run the localhost.  
5. bash shell
   * git command-line tool
   * sqlite3 command-line tool
   * zip command-line tool

## Initialization/Update of all dictionaries on Cologne server
The script `redo_cologne_all.sh` installs all dictionaries.
Dictionary xxx is installed into subdirectory XXXScan/2020 of scans directory.
The process takes about 30 minutes and adds about 3Gigabytes of storage.

## Initialization/Update of all dictionaries on XAMPP server
The script `redo_xampp_all.sh` installs all dictionaries.

The file system is assumed as:
* htdocs   -- xampp server root directory
  * cologne --  The name can be different; it should be a descendant
    of htdocs, but need not be a child of htdocs.
    * csl-orig  cloned from https://github.com/sanskrit-lexicon/csl-orig
    * csl-pywork  cloned from https://github.com/sanskrit-lexicon/csl-pywork
    * csl-websanlexicon  cloned from https://github.com/sanskrit-lexicon/csl-websanlexicon
    * xxx1  (first dictionary installed), eg. acc
    * xxx2  (second dictionary installed), eg. ae
    * ...

With this configuration, a localhost url for a given dictionary, say mw, is
http://localhost/cologne/mw/web/.

### Git Bash
The installation under XAMPP server has been tested on Windows 10 using
the GitBash terminal.  In addition to python (Python2.7.x with `mako` installed) , sqlite3.exe and
zip.exe had to be installed.  Here is one way to do this:
* **sqlite3** : From https://www.sqlite.org/download.html, download sqlite-tools-win32.
  * extract the zip file, and put 'sqlite3.exe' into "/c/xampp/htdocs/sqlite3".
    [This assumes the directory of your xampp installation is `C:\xampp`.
  * Add "/c/xampp/htdocs/sqlite3" to the system variable 'Path'.
    Here is [a link](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) that shows how to do this.
  * When GitBash is restarted, the 'sqlite3' executable is available
    try 'which sqlite3' in Git Bash terminal. You should see
    `/c/xampp/sqlite3/sqlite3`.
* **zip** 
  * Download the [GoW installer](https://github.com/bmatzelle/gow/releases/download/v0.8.0/Gow-0.8.0.exe). (Gnu on Windows) 
  * run the installer.
  * copy the zip executable to our sqlite3 directory: In Git Bash terminal:
    `cp "/c/Program Files (x86)/Gow/bin/zip.exe" /c/xampp/sqlite3/`
  * restart Git Bash; try `which zip`, you should see `/c/xampp/sqlite3/zip`
  * Note:  zip is only used to generate the '.zip' files in the 'downloads'
    subdirectory of each dictionary.  For a personal Xampp installation, this
    has little utility, and so 'zip' does not have to be installed.

## Initialization/Update of all dictionaries on local Ubuntu machine.

Tested on Bodhi Linux 5, a minimalist ubuntu based distro, on 20 Oct 2019.

### Installing necessary packages on Ubuntu local machine.

```bash
sudo apt update
sudo apt upgrade
sudo apt install python-pip
sudo pip install mako
sudo apt install git
sudo apt install apache2
sudo apt install zip
sudo apt install sqlite3
sudo apt install php
sudo apt install php-cli
sudo apt install php-xml
sudo apt install php-sqlite3
sudo apt install libxml2-utils
sudo apt service apache2 restart
```

### Downloading the necessary repositories.

```bash
cd /var/www/html
sudo mkdir cologne
cd cologne
sudo git clone https://github.com/sanskrit-lexicon/csl-orig.git
sudo git clone https://github.com/sanskrit-lexicon/csl-pywork.git
sudo git clone https://github.com/sanskrit-lexicon/csl-websanlexicon.git
```

### Regenerate all dictionaries for local usage.

```bash
cd csl-pywork/v02/
sudo bash redo_xampp_all.sh
```

### Regenerate only the changed file based on changes in csl-orig repository for local usage.

This is mostly used for a cronjob to update files which are changed in csl-orig repository since the last usage.

```bash
cd csl-pywork/v02/
sudo bash redo_xampp_selective.sh
```


