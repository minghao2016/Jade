#!/usr/bin/env python



#Author: Jared Adolf-Bryfogle
#Purpose: Get change in energy for point mutations of a structure after mutation and FastRelax.


#Instructions: Look at the input options.  Set at least --pdb and --region. (python get_mutation_energy.py --pdb mypdbfile.pdb --region 1:10:B)

from rosetta import *
from optparse import OptionParser
import os
import sys
import time

from basic.RestypeDefinitions import *

rosetta.init()

opts = [ 'app' , '-database' , os.path.abspath( os.environ['PYROSETTA_DATABASE'] ) , '-ex1' , '-ex2' , '-constant_seed', \
         '-ignore_unrecognized_res', '-use_input_sc']

# '-relax:constrain_relax_to_start_coords'
args = rosetta.utility.vector1_string()
args.extend( opts ) 
rosetta.core.init( args )


##Setup Options and Script Inputs:

parser = OptionParser()
args = sys.argv

parser.add_option("--pdb", "-s",
            
    help = "Path to PDB file.  Required."
)

parser.add_option("--outpath","-o",
    default = "/RESULTS",
    help = "Full output directory path.  Default is pwd/RESULTS"
)

parser.add_option("--filename", '-n',
    default = "mutation_energies.txt",
    help = "The filename of the results file"
)

parser.add_option("--region", "-r",
    default = None,
    help = "(region designated as start:end:chain) If none is given, will use whole PDB"
)

parser.add_option("--relax_whole_structure", '-m',
    action = "store_true",
    default = False,
    help = "Relax the whole structure?  Default is to only relax chain under question.  If no region is set, will default to true"
)

parser.add_option("--alanine_scan", "-a",
    action = "store_true",
    default = False,
    help = "Trigger the script to do an alanine scan of the mutations instead of a full mutational scan."
)



##Check that options are set.
(options, args) = parser.parse_args(args=args[1:])

if not options.pdb:
    sys.exit("Input PDB Required")
    
if not options.region:
    print "\nNo region selected.  Using whole structure\n"
else:
    regions = options.region.split(":")
    start_position = int(regions[0]);
    end_position = int(regions[1]);
    chain = regions[2]

if not options.region and not options.relax_whole_structure:
    options.relax_whole_structure = True
    
if options.outpath == "/RESULTS":
    options.outpath = os.getcwd()+"/RESULTS"
    
if not os.path.exists(options.outpath):
    os.mkdir(options.outpath)
    
##Begin the script    
OUTFILE = open(options.outpath+"/"+options.filename, 'w')

#Load the PDB
pose = Pose()
pose_from_pdb(pose, options.pdb)

#Create the Scorefunction
scorefxn = create_score_function("talaris2014")
scorefxn.set_weight(chainbreak, 100)
    

#Create the objects we need
rel = FastRelax(scorefxn)
codes = RestypeDefinitions()

if options.alanine_scan:
    single_letter_residues = []
    single_letter_residues.append("A")
else:
    single_letter_residues = codes.get_all_one_letter_codes()

#Set movemap if nessessary
if not options.relax_whole_structure:
    print "\nSetting backbone movement for chain "+chain+" only.\n"
    mm = MoveMap()
    for i in range(1, pose.total_residue()+1):
        if pose.pdb_info().chain(i) == chain:
            mm.set_bb(i, True)
            mm.set_chi(i, True)
        else:
            mm.set_chi(i, True)
    rel.set_movemap(mm)


#Get Rosetta numbering
if options.region:
    rosetta_start = pose.pdb_info().pdb2pose(chain, start_position)
    rosetta_end = pose.pdb_info().pdb2pose(chain, end_position)

else:
    rosetta_start = 1;
    rosetta_end = pose.total_residue();


pose_copy = Pose()
pose_copy.assign(pose)


print "\nObjects setup.  Starting Native relax. \n"

#Get Native energies:
native_energy = scorefxn(pose)
OUTFILE.write("#Native: "+repr(native_energy)+"\n")
t1 = time.clock()
rel.apply(pose)
t2 = time.clock()
native_relaxed_energy = scorefxn(pose)

pose.dump_pdb(options.outpath+"/native_relaxed.pdb")

OUTFILE.write('#NativeRelaxed: '+repr(native_relaxed_energy)+"\n")
OUTFILE.write("location mutation score delta_relaxed_native\n")

#Compute Time.  This is not a fast protocol.

single_relax_time = (t2-t1)/60
full_run_time = ((rosetta_end-rosetta_start+1)*20*single_relax_time)/60
print "\nApproximate runtime: "+ "%.2f"%full_run_time+" Hours\n"
print "\nNative Relax complete.  Starting mutation run. \n"


#Go through all positions and single letter codes.
for i in range(rosetta_start, rosetta_end+1):
    pdb_location = pose.pdb_info().pose2pdb(i)
    for residue in single_letter_residues:
        
        pdbSP = pdb_location.split()
        print "\n Starting mutant "+pdbSP[0]+"_"+pdbSP[1]+"_"+residue+".pdb\n"
        #Start at the same structure.
        pose.assign(pose_copy)
        mutate_residue(pose, i, residue)
        
        
        
        #Run Relax
        rel.apply(pose)
        
        #Output Results
        OUTFILE.write(pdb_location + " "+residue+" "+repr(scorefxn(pose))+" "+repr(scorefxn(pose) -         native_relaxed_energy)+"\n")
        
	OUTFILE.flush()
    pose.dump_pdb(options.outpath+"/mutant_"+pdbSP[0]+"_"+pdbSP[1]+"_"+residue+".pdb")
        
OUTFILE.close()
