# Git based workflow

Now the 2020 version is based on github.
There are only three github repositories which can regenerate a full Cologne Sanskrit lexicon website either on remote server or local machine.
They are `csl-orig`, `csl-pywork` and `csl-websanlexicon`. 

1. csl-orig has only two files per dictionary. Their paths are csl-orig/v00/csl-data/XXXScan/2020/orig/xxx.txt and csl-orig/v00/csl-data/XXXScan/2020/orig/hwextra/xxx_hwextra.txt, where XXX stands for the dictionary code in uppercase and xxx stands for the dictionary code in lowercase. These are the least minimum amount of data from which everything else is calculated / derived by scripts.
2. csl-pywork has following two folders, on basis of which the python code for a specific dictionary is generated.
They are (a) distinctscripts and (b) makotemplates. 
(a) distinctscripts currently house two scripts per dictionary (a1) make_xml.py and (a2) xxx.dtd.
These two items are supposed to be too divergent between dictionaries that it was considered too labour-intensive to create a single code for all dictionaries.
(b) makotemplates house two types of scripts (b1) Copied (b2) Templated.
The scripts which have no differences across dictionaries are Copied.
The scripts which have some differences in them are Templated.
The classification of Copied and Templated are marked by 'C' or 'T' in inventory.txt file.
3. csl-websanlexicon is concerned with the generation of scripts for display of various dictionaries.
It also has two types of scripts in makotemplates folder - Copied and Templated.
The description is the same as in csl-pywork.


# v02 
Version v00 of this repository is experimental.
Version v01 is not in this git repository, but is part of the Cologne file
system.  It served the intermediate purpose of refining the makotemplates
and distinctfiles directory

See the readme for [v02](https://github.com/sanskrit-lexicon/csl-pywork/tree/master/v02).


