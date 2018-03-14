
class Mugqicwl(object):
	def __init__(self, toolname, filepath):
		self.name = toolname
		self.path = filepat

	def trimmomatic(self):
		trim_out = ["forward_paired", "reverse_paired", "forward_unpaired", "reverse_unpaired"]
		self.add_input("trimmomatic", path={"type": "File"})
		self.add_input("trimmomatic", paired_end={"type": "boolean"})
		trim_in = {}
		if "trimmomatic_path" in self.inputs:
			trim_in["path_to_picard"] = "trimmomatic_path"
		elif "trimmomatic_paired_end" in self.inputs:
			trim_in["paired_end"] = "trimmomatic_paired_end"
		self.add_outputs(trim_reverse_paired = {"output_source": "trimmomatic/reverse_paired"})
		self.add_outputs(trim_forward_paired = {"output_source": "trimmomatic/forward_paired"})
		self.add_step("trimmomatic", "trimmomatic.cwl", trim_in, trim_out)

	def picard_sam_to_fastq(self):
	def picard_merge_sam_files(self):
	def bwa_mem(self):
	def picard_sort_sam(self) 