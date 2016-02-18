
A collection of mainly python modules and scripts written over the years for various purposes.

# Setup

Nothing fancy yet.  

1) Add the root path to your PYTHONPATH environment variable in your shell. 

<code>export PYTHONPATH=$PYTHONPATH:/path/to/Jade/src</code>

2) Add the path to Jade/apps to your PATH environment variable to use scripts and programs as executables 

<code>export PATH=$PATH:/path/to/Jade/apps</code>

# Code Organization

<code>Jade/apps</code>
 - Applications, and scripts
  
<code>Jade/database</code>
 - Collection of files used by Jade applications and modules.
 
<code>Jade/src</code>
 - Jade Source Code
 
<code>Jade/testing</code>
 - Testing code and inputs.  Not yet developed fully.





# Jade SRC Code

## _basic_
Useful general classes and collections of functions (Threading, BioPose, PandasDataFrame, path, etc)

## _utility_
Functions and simple classes go in <code>__init__.py</code> 
vector1 is a list indexed at 1

 - Use: <code>from utility import vector1</code>

## _antibody_
A small collection of general antibody scripts and modules from PyIgClassify.  http://dunbrack2.fccc.edu/PyIgClassify/.  The meat of PyIgClassify should be publically released soon.

## _plotting_
Collection of plotting classes and functions for matplotlib, seaborn

## _pymol_jade_
Python PyMol modules and pymol scripts


## _rosetta_jade_
Rosetta (www.rosettacommons.org) modules and flags files for analyzing results, benchmarking, etc.  PyRosetta (www.pyrosetta.org) modules and scripts from various projects


## _sequence_
Modules for dealing with protein sequence


## _structure_
Modules for reading PDBs and storing structure information.  Yes, my own general PDB reader.  Because everyone has one, right?

## _tcl_
TCL modules for molecular dynamic simulations.


# Notable Scripts and Programs

## RunRosettaMPI

Run MPI-built Rosetta locally, or an a cluster using slurm or qsub as the job manager.  Run from your root project directory or set the root dir as an option in the program.  Will cd into the root, or set the job manager script to cd into root before the MPI run.

It uses JSON files to setup the base flags (<code>--json_base</code>) and then specific flags for different rosetta runs (<code>--json_run</code>).  The [default baseline json](https://github.com/SchiefLab/module_c/blob/master/rosetta_jadeeral/jsons/common_flags.json) should be good for most runs.  See [this dir](https://github.com/SchiefLab/module_c/tree/master/rosetta_jadeeral/jsons) for a list of currently implemented jsons.  Feel free to implement your own.  I typically add that json path as an alias to easily run scripts.  The class is easily extendable for benchmarking experiments, [like I have done for antibody design](https://github.com/SchiefLab/module_c/blob/master/bin/BenchmarkRAbD.py).

Use <code>--print_only</code> to print instead of run to double check everything.  Paths can (and should) be relative.  Will setup any directories mentioned.  You can feed additional flags files or options (or overwrite any set in the json files) using :     <code>--extra_options @rel/path/to/flags rosetta_opt=setting another_opt=setting a_boolean_opt</code>

Set the job manager using the option <code>--job_manager</code>. Current options are __slurm__, __qsub__, and __local__.  Set extra options for the job manager in parenthesis, such as the slurm partition option -p, using <code>--job_manager_opts "set of -options -for run"</code>

Be sure to set <code>--np</code> and <code>--nstruct</code> (if not set in flags files or extra_options)

Relational Database support has been added.  See database section.  If using sqlite3, it will automatically combine the databases at the end of the run.  Very useful for running antibody_features reporters.  

If you think a GUI would be useful for this, let me know!
See below for the current full help of the program:



```
usage: This program runs Rosetta MPI locally or on a cluster using slurm or qsub.  Relative paths are accepted.
       [-h] [--job_manager {slurm,qsub,local,local_test}]
       [--job_manager_opts [JOB_MANAGER_OPTS [JOB_MANAGER_OPTS ...]]]
       [--np NP] [--nodes NODES] [--ppn PPN] [--nstruct NSTRUCT]
       [--compiler {gcc,clang}] [--machine_file MACHINE_FILE]
       [--job_name JOB_NAME] [--program PROGRAM] [-s S] [-l L]
       [--outdir OUTDIR] [--json_base JSON_BASE] [--json_run JSON_RUN]
       [--root ROOT] [--extra_options [EXTRA_OPTIONS [EXTRA_OPTIONS ...]]]
       [--one_file_mpi] [--print_only] [--db_mode {sqlite3,mysql,postgres}]
       [--db_name DB_NAME] [--db_batch DB_BATCH] [--db_in] [--db_out]

optional arguments:
  -h, --help            show this help message and exit

Job Setup:
  --job_manager {slurm,qsub,local,local_test}
                        Job Manager to launch job. Default = 'slurm '
  --job_manager_opts [JOB_MANAGER_OPTS [JOB_MANAGER_OPTS ...]]
                        Extra options for the job manager, such as queue or
                        processor requestsRemove double dashes. Exclusive is
                        on by default. Specify like: -p imperial exclusive.
  --np NP               Number of processors to use for MPI. Default = 101
  --nodes NODES         Number of nodes to ask for. Optional.
  --ppn PPN             Processors per node for qsub. NTasks is np for slurm
  --nstruct NSTRUCT
  --compiler {gcc,clang}, -c {gcc,clang}
                        Set the compiler used. Will set clang automatically
                        for macos. Default = 'gcc'
  --machine_file MACHINE_FILE
                        Optional machine file for passing to MPI
  --job_name JOB_NAME   Set the job name used for mpi_tracer_to_file dir and
                        queue. Default = 'rosetta_run'. (Benchmarking:
                        Override any set in json_base.)

Protocol Setup:
  --program PROGRAM     Define the Rosetta program to use if not set in
                        json_run
  -s S                  Path to a pdb file
  -l L                  Path to a list of pdb files
  --outdir OUTDIR, -o OUTDIR
                        Outpath. Default = 'pwd/decoys'
  --json_base JSON_BASE
                        JSON file for setting up base paths/etc. for the
                        cluster.Default = 'file_dir/jsons/common_flags.json'
  --json_run JSON_RUN   JSON file for specific Rosetta run. Not required.
  --root ROOT           Set the root directory. Default = pwd. (Benchmarking:
                        Override any set in json_base.)
  --extra_options [EXTRA_OPTIONS [EXTRA_OPTIONS ...]], -e [EXTRA_OPTIONS [EXTRA_OPTIONS ...]]
                        Extra Rosetta options. Specify like:
                        cdr_instructions=my_file other_option=setting. Note NO
                        - charactor. Booleans do not need an = sign.
  --one_file_mpi        Don't setup mpi_tracer_to_file.
  --print_only          Do not actually run anything. Just print setup for
                        review.

Relational Databases:
  Options for Rosetta Database input and output. Use for features or for
  inputting and output structures as databases

  --db_mode {sqlite3,mysql,postgres}
                        Set the mode for Rosetta to use if using a database.
                        Features will be output to a database. If not sqlite3,
                        must build Rosetta with extras. If any post-processing
                        is required, such as combining sqlite3 dbs, will do
                        this. Default DB mode for features is sqlite3.
  --db_name DB_NAME     In or Out database name
  --db_batch DB_BATCH   Batch of structures.
  --db_in               Use an input database
  --db_out              Use an output database
```

## score_analysis

Analyze Rosetta decoys that were scored with an output json file.  Get top models, score summaries, top_n_by_10, and output pymol sessions.

Use <code>-scorefile_format json</code> during your Rosetta runs.  This is a fork of the scorefile.py script that is located in rosetta source dir.   

I copy the current help text below.

```
usage: This utility parses and extracts data from score files in JSON format
       [-h] [-s [SCORETYPES [SCORETYPES ...]]] [-n TOP_N]
       [--top_n_by_10 TOP_N_BY_10]
       [--top_n_by_10_scoretype TOP_N_BY_10_SCORETYPE]
       [--decoy_names [DECOY_NAMES [DECOY_NAMES ...]]] [-S] [-c]
       [--list_scoretypes] [--make_pdblist] [--pdblist_prefix PDBLIST_PREFIX]
       [--pdblist_outdir PDBLIST_OUTDIR] [--pymol_session]
       [--session_prefix SESSION_PREFIX] [--session_outdir SESSION_OUTDIR]
       [--native NATIVE] [--top_dir TOP_DIR] [--ab_structure] [--super SUPER]
       [scorefiles [scorefiles ...]]

positional arguments:
  scorefiles            A list of scorefiles

optional arguments:
  -h, --help            show this help message and exit
  -s [SCORETYPES [SCORETYPES ...]], --scoretypes [SCORETYPES [SCORETYPES ...]]
                        List of score terms to extract
  -n TOP_N, --top_n TOP_N
                        Only list Top N when doing top scoring decoys or
                        making pymol sessionsDefault is to print all of them.
  --top_n_by_10 TOP_N_BY_10
                        Top N by 10 percent total score to print out.
  --top_n_by_10_scoretype TOP_N_BY_10_SCORETYPE
                        Scoretype to use for any top N by 10 printing. If
                        scoretype not present, won't do anything.
  --decoy_names [DECOY_NAMES [DECOY_NAMES ...]]
                        Decoy names to use
  -S, --summary         Compute stats summarizing data
  -c, --csv             Output selected columns, top, and decoys as CSV.
  --list_scoretypes     List score term names

PDBLISTs:
  Options for pdblist output

  --make_pdblist        Output PDBlist file(s)
  --pdblist_prefix PDBLIST_PREFIX
                        Prefix to use for PDBLIST outputs
  --pdblist_outdir PDBLIST_OUTDIR
                        Output dir for pdblist files

PyMol:
  Options for pymol session output

  --pymol_session       Make pymol session(s) of the scoretypes specified
  --session_prefix SESSION_PREFIX
                        Prefix used for output pymol session
  --session_outdir SESSION_OUTDIR
                        Output dir for pymol sessions.
  --native NATIVE       Native structure to use for pymol sessions.
  --top_dir TOP_DIR     Top directory for PDBs if different than the directory
                        of the scorefile
  --ab_structure        Specify if the module is a renumbered antibody
                        structure. Will run pymol script for ab-specific
                        selection
  --super SUPER         Super this selection instead of align all to.
  
```

### Current Limitations

Works on individual scorefiles, with no -best-of-all- or combined output.


## RAbD_Jade

GUI for antibody design analysis.  Inputs are Antibody Features Reporter databases.  I will probably change the name soon. Each design strategy should have its own database.  Example: <code>PyRAbD_Compare.py path/to/directory/of/sqlite3/databases</code>

### Current Limitations

Note that it currently only supports sqlite3 databases and each decoy used in the comparison must have a unique name.  


