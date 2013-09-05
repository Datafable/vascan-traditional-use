# Requirements

- [Python](http://www.python.org/) (We used 2.7)
- [Bash](http://www.gnu.org/software/bash/manual/bashref.html): We suggest you use a *nix platform.
- python [requests](http://docs.python-requests.org/en/latest/) library

# Scripts

## runall

Filename: `runall.sh`

This is the main file you need for repeating the convertion. It simply contains the different commands that are required to run the next scripts in the right order and puts all the outputfiles in place.

usage: ./scripts/runall.sh /full/path/to/vascan/taxon.txt

## CleanData

Filename: `CleanData.py`

This file performs data cleansing operations that were easy to automate.

usage: ./scripts/CleanData.py infile outfile

## DwCReader

Filename: `DwCReader.py`

This file contains a class to deal with reading the Darwin Core file and using (searching) the data.

usage: This file is not intended to be run as a script. It will be sourced by `MapToVascan.py`

## MapToVascan

Filename: `MapToVascan.py`

This file reads the data with one line per record, parses the scientific name and maps it on the vascan data. It creates a new file, that adds 2 columns to the inputfile: `taxon_id` and `taxon_match_type`.

usage: ./scripts/MapToVascan.py infile vascan_taxon_file outfile

## OneLinePerRecord

Filename: `OneLinePerRecord.py`

This file reads the input as extracted from the initial Word file (so the corresponding tsv file). It aggregates the lines corresponding to one record on one line.

usage: ./scripts/OneLinePerRecord.py infile outfile
