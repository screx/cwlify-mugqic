from workflow import Workflow
from config import *
import argparse
import sys



class DNASeq(object):
	cwl_dir = "../../cwl-local"
	def __init__(self, name):
		self.steps = [
			self.picard_sam_to_fastq,
			self.trimmomatic,
			# self.bwa_mem,
			# self.picard_sort,
			# self.picard_merge,
			# self.gatk_indel_realigner,
			# self.picard_merge_realigned,
		]
		self.workflow = Workflow("test")
		workflow = self.workflow
		# must use absolute pathing # might need to make this obtained from config

		trimmomatic_jar = config.param("executables", "trimmomatic")
		picard_jar = config.param("executables", "picard")
		# workflow.add_input("shared", picard={"type": ["string", "File"]})
		workflow.add_values("shared", trimmomatic={"type": "File", "value": trimmomatic_jar})
		workflow.add_values("shared", picard={"type": "File", "value": picard_jar})
		for step in self.steps:
			step()
		workflow.build()
		workflow.create_cwl_inputs()

	def trimmomatic(self):
		toolname = "trimmomatic"
		# step 2
		workflow = self.workflow
		# from readset but hardcoded for now
		input_forward = "../../pair1.fastq"
		input_reverse = "../../pair2.fastq"
		paired_end = True
		trailing = int(config.param("trimmomatic", "trailing_min_quality"))
		sliding_window = "4:15"
		min_len = int(config.param("trimmomatic", "min_length"))
		illumina_clip = config.param("trimmomatic", "illumina_clip_settings")
		# example of what would be in a function
		out = ["forward_paired", "reverse_paired", "forward_unpaired", "reverse_unpaired"]
		workflow.add_values("trimmomatic", paired_end={"type": "boolean", "value":paired_end})
		workflow.add_values("trimmomatic", illumina_clip={"type": "string", "value": illumina_clip})		
		workflow.add_values("trimmomatic", sliding_window={"type": "string", "value": sliding_window})		
		workflow.add_values("trimmomatic", min_len={"type": "int", "value": min_len})
		workflow.add_values("trimmomatic", trailing={"type": "int", "value": trailing})
		# hard coding the name changes to map them to the actual values.
		inp = {
			"path_to_trimmomatic": "shared_trimmomatic",
			"paired_end": "trimmomatic_paired_end",
			"illumina_clip": "trimmomatic_illumina_clip",
			"sliding_window": "trimmomatic_sliding_window",
			"min_len": "trimmomatic_min_len",
			"trailing": "trimmomatic_trailing"	
		}
		# want to check if the previous step is available and in the steps, prob not the best way.
		if hasattr(self, "picard_sam_to_fastq") and self.picard_sam_to_fastq in self.steps:
			inp["input_forward"] = "sam2fq/output_fastq"
			inp["input_reverse"] = "sam2fq/output_fastq2"
		else:
			workflow.add_values("trimmomatic", input_forward={"type":"File", "value": input_forward})
			workflow.add_values("trimmomatic", input_reverse={"type": "File", "value": input_reverse})
			inp["input_forward"] = "trimmomatic_input_forward"
			inp["input_reverse"] = "trimmomatic_input_reverse"
		# if self.config["trimmomatic"]["quality_offset"] == "64":
		# 	workflow.add_input("trimmomatic", phred64={"type": "boolean"})
		# 	trim_in["phred64"] = "trimmomatic_phred64"
		# else:
		# 	workflow.add_input("trimmomatic", phred33={"type":"boolean"})
		# 	trim_in["phred33"] = "trimmomatic_phred33"
		# now to add the outputs we want to keep.
		workflow.add_outputs(trim_reverse_paired = {"outputSource": "trimmomatic/reverse_paired"})
		workflow.add_outputs(trim_forward_paired = {"outputSource": "trimmomatic/forward_paired"})
		# add the step to the workflow
		src = "{0}/trimmomatic.cwl".format(self.cwl_dir)
		path = workflow.add_to_run_folder(toolname,src)
		workflow.add_step("trimmomatic",path, inp, out)


	def picard_sam_to_fastq(self):
		toolname ="picard_sam_to_fastq"
		# step 1
		workflow = self.workflow
		out = ["output_fastq", "output_fastq2"]
		sam_file = "../../chrom20_low_cov.bam" # from readset
		fq = "1.fq"
		fq2 = "2.fq"
		workflow.add_values("sam2fq", input={"type": "File", "value": sam_file})
		# workflow.add_input("picard_sam2fq", input={"type": "File"})
		workflow.add_values("sam2fq", fastq={"type": "string", "value": fq})
		# workflow.add_input("picard_sam2fq", fastq={"type": "string"})
		workflow.add_values("sam2fq", second_end_fastq={"type": "string", "value": fq2})
		# workflow.add_input("picard_sam2fq", second_end_fastq={"type": "string"})
		inp = {
			"path_to_picard": "shared_picard",
			"fastq": "sam2fq_fastq",
			"second_end_fastq": "sam2fq_second_end_fastq",
			"input": "sam2fq_input"
		}
		src = "{0}/picard_sam_to_fastq.cwl".format(self.cwl_dir)
		path = workflow.add_to_run_folder(toolname,src)
		workflow.add_step("sam2fq", path, inp, out)
		# conditional statements to check for.


# 	def bwa_mem(self):
# 		# step 4a
# 		workflow = self.workflow
# 		out=["aligned_sam"]
# 		workflow.add_input("bwa_mem", reference={"type": "File"})
# 		# workflow.add_input("bwa_mem", fastq1={"type": "File"})
# 		# workflow.add_input("bwa_mem", fastq2={"type": "File"})
# 		inp = {
# 			"reference": "bwa_mem_reference",
# 		}
# 		scattered = {}
# 		if self.trimmomatic in self.steps:
# 			scattered["fastq1"] = "trimmomatic/forward_paired"
# 			scattered["fastq2"] = "trimmomatic/reverse_paired"
# 		elif self.picard_sam_to_fastq in self.steps:
# 			inp["fastq1"] = "picard_sam2fq/fastq"
# 			inp["fastq2"] = "picard_sam2fq/fastq2"
# 		else:
# 			pass
# 			# from the readset file if available or from p
# 		run = "{0}/bwa_mem.cwl".format(self.cwl_dir)
# 		workflow.add_step("bwa_mem", run, inp, out, scattered)
# 	def picard_sort(self):
# 		workflow=self.workflow
# 		# step 4b
# 		out = ["sorted_sam"]
# 		# workflow.add_input()
# 		# need to add scattering
# 		inp ={
# 			"path_to_picard": "shared_picard",
# 			"input_file": "[bwa_mem/aligned_sam]"
# 		}
# 		run = "{0}".format(self.cwl_dir)
# 		workflow.add_step("picard_sort", run, inp, out)
# 	def picard_merge(self):
# 		# step 5
# 		workflow = self.workflow
# 		out=["merged_file"]
# 		workflow.add_input("picard_merge", sort_order={"type": "string"})
# 		workflow.add_input("picard_merge", assume_sorted={"type": "string"})
# 		inp = {
# 			"path_to_picard": "shared_picard",
# 			"sort_order": "picard_merge_sort_order",
# 			"assume_sorted": "picard_merge_assume_sorted",
# 		}
# 		if self.bwa_mem in self.steps:
# 			inp["sam_files"] = "[picard_sort/sorted_sam]"
# 		else: 
# 			# from readset file.
# 			pass
		
# 		run = "{0}/picard_merge_sam_file.cwl".format(self.cwl_dir)
# 		workflow.add_step("picard_merge", run, inp, out)
# 	def picard_merge_realigned(self):
# 		# step 7
# 		workflow = self.workflow
# 		out = ["merged_file"]
# 		workflow.add_input("merge_realigned", sort_order={"type": "string"})
# 		workflow.add_input("merge_realigned", assume_sorted={"type": "string"})
# 		inp = {
# 			"path_to_picard": "shared_picard",
# 			"sort_order": "merge_realigned_sort_order",
# 			"assume_sorted": "merge_realigned_assume_sorted",
# 			"sam_files": "indel_realign/realigned_bam"
# 		}


# 	def gatk_indel_realigner(self):
# 		# step 6
# 		workflow = self.workflow
# 		out=["realigned_bam"]
# 		workflow.add_input("indel_realign", known_indels={"type": ["string", "File"]})
# 		workflow.add_input("indel_realign", target_intervals={"type": ["string", "File"]})
# 		inp = {
# 			"path_to_gatk": "shared_gatk",
# 			"reference": "shared_reference_genome",
# 			"known_indels": "gatk_known_indels",
# 			"target_intervals": "gatk_target_intervals",

# 		}
# 		run = "{0}/gatk_indel_realigner.cwl".format(self.cwl_dir)
# 		workflow.add_step("indel_realign", run, inp, out)

# 	# def bva_groupfixmate(self):
# 	# 	# step 7
# 	# 	workflow = self.workflow
# 	# 	out = ["groupfixmate"]
# 	# 	workflow.add_input("bva_groupfixmate", level={"type": "int"})
# 	# 	workflow.add_input("bva_groupfixmate", level={"type": "int"})
# 	# 	inp = {
# 	# 		"level": "bva_groupfixmate_level"
# 	# 		"bam": "picard_merge/merged_file" # from picard merge
# 	# 	}
# 	# 	run = "{0}/bvatools_groupfixmate.cwl".format(self.cwl_dir)
# 	# def picard_mark_dup(self):
# 	# 	# step 9
# 	# 	out = ["markdup"]
# 	# 	inp = {`
# 	# 		"path_to_picard": "shared_picard"
# 	# 	}
		
# 	# 	run = "{0}/picard_markdup.cwl".format(self.cwl_dir)


# # import argparse
# # parser = argparse.ArgumentParser(description='Create a cwl DNASeq Pipeline')
# # parser.parse_args()
# # parser.add_argument('--o')

parser = argparse.ArgumentParser(description="This is the DNASeq pipeline created using CWL")
# parsing the number of steps
parser.add_argument("-s", action="store", dest="s")
# parsing for the config file
parser.add_argument("-c", action="store", dest="config_file")
args = parser.parse_args(sys.argv[1:])

try:
	config_file = open(args.config_file)
	r = config_file.readline()
	print config.parse_files([config_file])
except:
	if args.config_file:
		print "can't open config_file at: "	+ args.config_file

test = DNASeq("test")


# we can just make global variables to use as the starting point
