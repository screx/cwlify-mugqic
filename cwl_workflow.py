#!/usr/bin/ pythonm

#TODO write docstrings

# trying to develop a tool that allows users to generate workflows
# add something to core_config

# steps are added
# then create_workflow is ran


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
			'class': 'Workflow',
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
			for j in curstep["in"]:
				curparam = curstep["in"][j]
				if isinstance(curparam["value"], dict):
					# chainable types
					pass
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
					pass
				else:
					cwl_steps[tool][param] = source
					source = "{toolname}_{parametername}".format(tool, j)
					
			for param in self.steps[tool]["out"]:
				cwl_steps[toolname]['out'] += [param]
		return cwl_steps

	def build_outputs(self):
		outputs = {"outputs": []}
		steps = self.steps
		# for tool in steps:
		# 	curstep = self.steps["out"]
		# 	for param in curstep:
		# 		outputs["out"] = param



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

	# we know we're building a queue
	# put all steps in an array. if a step previous step is there that can be chained-- then modify the output and input
	# all leftover things in out should be put in outputs.
	# if prevstep in steps:
	# 	
	# what other ways can i do this. Sometimes I don't want to collect all outputs and only up to a certain step....
	# if its chained, I don't want it
	# if it's terminal I /sometimes/ want it. 
	# hmmmmmmmmmmmmm.....
	# not rly sure what to do here.

	# to interact with the pipeline just make an argparse command that switches things to the CWL versions. override [Mugqic] with [MugqicCWl] 
	# 