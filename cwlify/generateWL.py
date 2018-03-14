#!/usr/bin/ python

#TODO write docstrings

# trying to develop a tool that allows users to generate workflows
# add something to core_config
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
		self.cwl = parse_cwl(self)

	def parse_cwl(self):
		# REQUIREMENTS: get_path() has to point at a real cwl file in yml format. 
		with open(self.get_path()) as info:
			info_dict = yaml.load(info)
		self.inputs = info_dict["inputs"]
		self.outputs = infor_dict["outputs"]
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
			if "value" in param:
				valid_inputs[param] = self.inputs[param]
		return valid_inputs

	def get_valid_outputs(self):
		return self.outputs # they are all valid and can be parsed later.

class Workflow:
	def __init__(self):
		self.cwl_version = config.param("cwl", "cwl_version")
		self.steps = {} # basically list of all the tools

	def add_step(self, cl_tool):
		# get_valid_inputs() retrieves a dict with that have values attached
		# get_valid_outputs() retrieves a list of output param names
		# get_path() returns the path stored as part of the object
		steps[cl_tool.toolname]["run"] = cl_tool.get_path()	
		steps[cl_tool.toolname]["in"] = cl_tool.get_valid_inputs()
		steps[cl_tool.toolname]["out"] = cl_tool.get_valid_outputs()
		# what do you do if there are two of the same toolname?
	def create_workflow(self):
		cwl = open(filename + ".cwl", "rw")
		yaml = open(filename + ".yml", "rw")
		workflow = self.build()
		# convert build to a workflow file and yaml file
		# this will use the built in yaml support in python

	def build(self):
		# build(self, filename) takes in a file to write the cwl and yml to the 
		# globally defined output_dir and returns nothing.
		inputs = self.build_inputs()
		outputs = self.build_outputs()
		steps = self.build_steps()
		version = self.cwl_version
		requirements = self.requirements

		workflow = {
			'cwlVersion': cwl_version,
			'class': 'Workflow'
			'inputs': inputs,
			'outputs': outputs,
			'steps': steps,
			'requirements': requirements
		}
		return workflow

	def build_inputs(self):
		# build_inputs(self) formats the inputs from each of the step
		# to be used by a CWL workflow and returns a dict.

		# TODO: put all the inputs from the tools into one dict
		# modify the names to be <toolname>_<parametername>
		# and put the type signature down (should be the same)
		# then write to file.\

		inputs = {}
		for i in self.steps:
			curstep = self.steps[i]
			for j in curstep["in"]
				curparam = curstep["in"][j]
				if isinstance(curparam["value"], dict):
					# chainable types
				else:			
					key = "{toolname}_{parametername}".format(i, j)
					inputs[key]["type"] = curparam["type"]
					if "secondary_files" in curparam:
						inputs[key]["secondary_files"] = curparam["secondary_files"]
		return inputs
		# now convert to inputs to yaml and write to file.
		# also take their values and plop it in a yml file


	def build_step(self, f):
		cwl_steps = {}
		for tool in self.steps:
			toolname = tool.toolname
			cwl_steps[toolname]['run'] = tool.toolname.get_path()
			cwl_steps[toolname]['in'] = {}
			cwl_steps[toolname]['out'] = []
			for param in self.steps[tool]["in"]:
				if isinstance(self.steps[tool]["in"][param]["value"], dict):			
					# chain type i.e. no need for a value in inputs
					source = "{toolname}_{parametername}".format(tool, j)
					cwl_steps[tool][param] = source
				else:
			for param in self.steps[tool]["out"]:
				out += [param]
		return cwl_steps

	def build_outputs(self):
		outputs = {'out': []}
		for tool in self.steps:

		# TODO: add the outputs to the workflow file
		# how do we know what outputs we want?

# class PicardSamToFastq(CommandLineTool):
# 	def __init__(self):
# 		# TODO make an init
# 		# need a base dir for all CWL files
# 		# get _inputs will add all the important values to this class
# 		self.parse_cwl(cwl_dir, "picard_sam_to_fastq.cwl")

# 	inputs["illumina_clip"]["value"] = adapter_file + config.param("trimmomatic","illuminal_clip_settings") + headcrop_length


	# actual descriptions of the tool.	
	# how do i actually want to keep track of and use these tools.

	# What oop programming techniques can i/should i use.


# in my run steps I can have it so that it can just 
# have a .add(workflow) method which adds it to the workflow

# what else do I need?
# need a way to interact with the actual pipeline now
# this might prove to be a bit difficult
# the pipeline has methods/functions to get data from the config and readme files
# also to select inputs based on priority
# need to also hard code some params in.
