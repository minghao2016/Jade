#!/usr/bin/env python

from argparse import ArgumentParser

parser = ArgumentParser(" This simple script strips ters out of a PDB file and overwrites the input.  PyMol places ters "
                        "when th numbering is not 1-1.  And then Rosetta will F your Shit up.")

parser.add_argument("pdb_files", help = "Path to PDB file we will be stripping.", nargs="*")


options = parser.parse_args()

for pdb_file in options.pdb_files:
    FILE = open(pdb_file, 'r')
    lines = FILE.readlines()
    FILE.close()



    OUTFILE = open(pdb_file, 'w')
    for line in lines:
        if not "TER" == line[0:3]:
            OUTFILE.write(line)
    OUTFILE.close()