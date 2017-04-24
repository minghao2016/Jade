#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser

from rosetta import *
from pyrosetta import *

init("-include_sugars -ignore_unrecognized_res -ignore_zero_occupancy false")


parser = ArgumentParser("Simple app to scan a PDB file and print PDB info and Rosetta understood chains and resnums.")

parser.add_argument("pdb_file", help = "The PDB file to scan.")

parser.add_argument("--chain", '-c', help = "Specify only a single chain to scan.")

parser.add_argument("--echo_input", "-e", help = "Echo the input structure as output.  "
                                                 "This is to check how Rosettta worked reading it.",
                    default = False,
                    action = "store_true")

options = parser.parse_args()


pose = pose_from_pdb(options.pdb_file)

print "#resnum chain_num pdb_num chain "
for i in range(1, pose.total_residue() +1 ):
    if options.chain and pose.pdb_info().pose2pdb(i).split()[1] != options.chain:
        continue

    print repr(i)+" "+repr(pose.chain(i))+" "+pose.pdb_info().pose2pdb(i)+" "+pose.residue(i).name()

if options.echo_input:
    pose.dump_pdb("echo_"+os.path.basename(options.pdb_file))