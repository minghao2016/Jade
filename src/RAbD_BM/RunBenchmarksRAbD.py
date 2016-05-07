#!/usr/bin/env python

import sys
from rosetta_jade.RunRosettaBenchmarks import RunRosettaBenchmarks
from rosetta_jade.RunRosetta import RunRosetta

from overrides import overrides


class RunBenchmarksRAbD( RunRosettaBenchmarks ):
    """
    Benchmark class specifically for RAbD


    Details:

        ALL INPUT PDBs should go into

            project_root/datasets

        Typically, you will have multiple directories - native, relaxed, etc.

          This is specified as a benchmark using 'input_pdb_type' in your json file.

        ALL PDBLISTs for benchmarking should go into

            project_root/datasets/pdblists



    """
    def __init__(self):
        RunRosettaBenchmarks.__init__(self, program = "antibody_designer")

        self._current_settings["CDR"] = "ALL"

        self.dataset_root_dir = "datasets"
        self.pdblist_dir = self.dataset_root_dir+"/pdblists"
        self.instructions_dir = "instructions"

        if self.options.l or self.options.s:
            sys.exit("PDBLIST should be created in datasets/pdblists.  See antibody_design repo for an example.")


    @overrides
    def run_benchmark(self, benchmark_names, benchmark_options):
        """
        Run a single benchmark with options.

        :param benchmark_names: List of benchmark names
        :param benchmark_options: List of benchmark options
        :return:
        """

        cdr_setting = False
        cdr_setting_index = 0

        for index, bm_name in enumerate(benchmark_names):
            self._current_settings[bm_name] = benchmark_options[index]

            if bm_name == 'pdb':
                self.options.s = benchmark_options[bm_name]

        separate_cdrs = benchmark_options[benchmark_names.index("separate_cdrs")]

        if separate_cdrs:
            for cdr in self._get_designable_cdrs():
                self._current_settings["CDR"] = cdr
                RunRosetta.run(self)
        else:
            self._current_settings["CDR"] = "ALL"
            RunRosetta.run(self)


    @overrides
    def _get_output_string(self):

        if not self.options.separate_pdb_per_job():
            self.options.l = self._get_pdb_list_fname()

        s = RunRosettaBenchmarks._get_output_string(self)

        #Decoys
        s.append(" -in:path "+self.dataset_root_dir+"/"+self._current_settings["dataset"])

        #Instructions
        s = s + " -cdr_instructions " + self._create_instructions(self.instructions_dir+"/"+self._get_out_prefix+".instruct")
        return s

    @overrides
    def _get_pdb_list_fname(self):
        return ".".join([self.pdblist_dir+"/"+self._current_settings["dataset"],
                        self._current_settings["input_pdb_type"],
                        self._current_settings["l_chain"]+".PDBLIST.txt"])

    ### Helper Functions ###


    def _create_instructions(self, output_path):
        extra_lines=[]
        extra_lines.append(self.extra_options.json_dict["base_cdr_instruction_lines"])


        extra_lines.append("ALL MinProtocol MinType "+self._current_settings["mintype"])
        extra_lines.append("ALL FIX")


        if self._current_settings["CDR"] != "ALL":
            extra_lines.append(self._current_settings["CDR"]+" GraftDesign Allow")
        else:
            for cdr in self.extra_options.json_dict["graft_design_cdrs"]:
                extra_lines.append(cdr+" GraftDesign Allow")

        if self._current_settings["CDR"] != "ALL" and not self.extra_options.json_dict["separate_cdrs"]["all_given_seq_design"]:
            extra_lines.append(self._current_settings["CDR"]+" SeqDesign Allow")
        else:
            for cdr in self.extra_options.json_dict["seq_design_cdrs"]:
                extra_lines.append(cdr+" SeqDesign Allow")

        FILE = open(output_path, "w")
        FILE.write("\n".join(extra_lines))
        FILE.close()
        return output_path

    def _get_designable_cdrs(self):

        designable_cdrs = []
        seq_design_cdrs = self.extra_options.get_benchmarks_of_key("seq_design_cdrs")
        graft_design_cdrs = self.extra_options.get_benchmarks_of_key("graft_design_cdrs")

        for cdr in ["L1","L2","L3","H1","H2","H3"]:
            if cdr in seq_design_cdrs or cdr in graft_design_cdrs:
                designable_cdrs.append(cdr)

        return designable_cdrs