from workflow import Workflow
class DNASeq(object):
	self.steps = [
		self.picard_sam_to_fastq,
		self.trimmomatic,
		self.bwa_mem,
		self.picard_sort,
		self.picard_merge,
		self.gatk_indel_realigner,
		self.merge_realigned,
	]
	self.cwl_dir = "../cwl-local"
	def get_inputs(self):
	## Some Testing
	workflow = Workflow("test")
	workflow.add_input("shared", picard={"type": "[string, File]"})
	workflow.add_input("shared", trimmomatic={"type": "[string, File]"})
	def trimmomatic(self):
		# example of what would be in a function
		out = ["forward_paired", "reverse_paired", "forward_unpaired", "reverse_unpaired"]
		workflow.add_input("trimmomatic", paired_end={"type": "boolean"})
		workflow.add_input("trimmomatic", input_forward={"type":"File"})
		workflow.add_input("trimmomatic", input_reverse={"type": "File"})
		workflow.add_input("trimmomatic", illumina_clip={"type": "string"})
		workflow.add_input("trimmomatic", sliding_window={"type":"string"})
		workflow.add_input("trimmomatic", min_len={"type": "len"})
		workflow.add_input("trimmomatic", trimmomatic={"type": "string"})
		# inp is used to connect the inputs for the step to its correct place.
		inp = {
			"trimmomatic": "shared_trimmomatic",
			"paired_end": "trimmomatic_paired_end",
			# "input_forward": "trimmomatic_input_forward",
			# "input_reverse": "trimmomatic_input_reverse",
			"illumina_clip": "trimmomatic_illumina_clip",
			"sliding_window": "trimmomatic_sliding_window",
			"min_len": "trimmomatic_min_len",
		}
		if self.picard_sam_to_fastq in self.steps:
			inp["input_forward"] = "picard_sam_to_fastq/fastq"
			inp["input_reverse"] = "picard_sam_to_fastq/fastq2"
		else:
			inp["input_forward"] = "trimmomatic_input_forward"
			inp["input_reverse"] = "trimmomatic_input_reverse"
		if self.config["trimmomatic"]["quality_offset"] == "64":
			workflow.add_input("trimmomatic", phred64={"type": "boolean"})
			trim_in["phred64"] = "trimmomatic_phred64"
		else:
			workflow.add_input("trimmomatic", phred33={"type":"boolean"})
			trim_in["phred33"] = "trimmomatic_phred33"
		# now to add the outputs we want to keep.
		workflow.add_outputs(trim_reverse_paired = {"output_source": "trimmomatic/reverse_paired"})
		workflow.add_outputs(trim_forward_paired = {"output_source": "trimmomatic/forward_paired"})
		# add the step to the workflow
		run = "{0}/trimmomatic.cwl".format(self.cwl_dir)
		workflow.add_step("trimmomatic", run, inp, out)
	def picard_sam_to_fastq(self):
		out = [fastq, fastq2]

		workflow.add_input("picard_sam2fq", input={"type": "File"})
		workflow.add_input("picard_sam2fq", fastq={"type": "string"})
		workflow.add_input("picard_sam2fq", second_end_fastq={"type": "string"})
		inp = {
			"picard": "shared_picard",
			"fastq": "picard_sam2fq_fastq",
			"second_end_fastq": "picard_sam2fq_second_end_fastq",


		}
		run = "{0}/picard_sam_to_fastq.cwl".format(self.cwl_dir)
		workflow.add_step("picard_sam2fq", "../cwl-local/picard_sam_to_fastq.cwl", inp, out)
		# conditional statements to check for.


	def bwa_mem(self):
		out=[aligned_sam]
		workflow.add_input("bwa_mem", reference={"type": "File"})
		# workflow.add_input("bwa_mem", fastq1={"type": "File"})
		workflow.add_input("bwa_mem", fastq2={"type": "File"})
		inp = {
			"reference": "bwa_mem_reference",
		}
		scattered = {}
		if self.trimmomatic in self.steps:
			scattered["fastq1"] = "trimmomatic/forward_paired"
			scattered["fastq2"] = "trimmomatic/reverse_paired"
		else if self.picard_sam_to_fastq in self.steps:
			inp["fastq1"] = "picard_sam2fq/fastq"
			inp["fastq2"] = "picard_sam2fq/fastq2"
		else:
			# from the readset file if available or from p
		run = "{0}/bwa_mem.cwl".format(self.cwl_dir)
		workflow.add_step("bwa_mem", run, inp, out, scattered)
	def picard_sort(self):

	def picard_merge(self):
		out=[]
		inp = {}
		run =
		workflow.add_step("picard_merge", run, inp, out)
	def gatk_indel_realigner(self):
		out=[]
		inp = {}
		workflow.add_input("")
		workflow.add_input("")
		run =
		workflow.add_step("picard_merge", run, inp, out)
	def merge_realigned(self):	
		out=[]
		workflow.add_input("picard_merge",)
		workflow.add_input("picard_merge",)

		run = "{}/picard_merge_sam_file.cwl".format(self.cwl_dir)
		workflow.add_step("picard_merge", run, inp, out)
	# functions 

	workflow.build()
	workflow.create_cwl_inputs()

