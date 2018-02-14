import yaml

class CommandLineTool:
	"""A CommandLineTool object is used to interact with CWL tool descriptions
	in order to write workflows. It should be able to collect all the necessary inputs
	and use them to combine command line tools into a workflow."""
	def __init__(self, toolname):
		self.toolname = toolname
		# try:
		# 	self.base_dir = config.param("cwl", "cwl_base")
		# 	self.filename = config.param("cwl", toolname)
		# except Exception e:
		# 	print("{toolname} doesnt exist. Check the config file and try again"\
		# 		.format(toolname))
		self.inputs = {}
		self.outputs = {}
		# self.cwl = parse_cwl(self)

	def parse_cwl(self):
		# REQUIREMENTS: get_path() has to point at a real cwl file in yml format. 
		with open(self.get_path()) as info:
			info_dict = yaml.load(info)
			info.close()
		self.inputs = info_dict["inputs"]
		self.outputs = info_dict["outputs"]
		return info_dict

	def add_input(self, input_name, input_value):
		# REQUIRES: the input has to exist in the cwl file.
		if input_name in self.inputs:
			self.inputs[input_name]["value"] = input_value
		else:
			print "{input_name} not in inputs".format(input_name)

	def get_path(self):
		return self.base_dir + "/" + self.filename

	def get_valid_inputs(self):
		valid_inputs = {}
		for param in self.inputs:
			if "value" in self.inputs[param]:
				valid_inputs[param] = self.inputs[param]
		return valid_inputs

	def get_valid_outputs(self):
		return self.outputs # they are all valid and can be parsed later.
