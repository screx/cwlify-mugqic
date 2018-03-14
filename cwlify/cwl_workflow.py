#!/usr/bin/ python

#TODO write docstrings

# trying to develop a tool that allows users to generate workflows
# add something to core_config

# steps are added
# then create_workflow is ran


class Workflow:
	def __init__(self):
		self.cwl_version = config.param("cwl", "cwl_version")
		self.steps = {} # basically list of all the tools
		self.input_names = []
		self.inputs = {}
		self.output_names = []
		self.outputs = {}

	def __getattr__(self, attr):
		for i in self.steps:
			if i == attr:
				return i

	def add_step(self, cl_tool):
		# get_valid_inputs() retrieves a dict with that have values attached
		# get_valid_outputs() retrieves a list of output param names
		# get_path() returns the path stored as part of the object
		# maybe it can even move all the cwl files into a common directory
		steps[cl_tool.toolname]["run"] = cl_tool.get_path()	
		steps[cl_tool.toolname]["in"] = cl_tool.get_valid_inputs()
		steps[cl_tool.toolname]["out"] = cl_tool.get_valid_outputs()		

	# def create_workflow(self):
	# 	cwl = open(filename + ".cwl", "rw")
	# 	workflow = self.build()
	# 	# convert build to a workflow file and yaml file
	# 	# this will use the built in yaml support in python

	# def build(self):
	# 	# build(self, filename) takes in a file to write the cwl and yml to the 
	# 	# globally defined output_dir and returns nothing.
	# 	inputs = self.build_inputs()
	# 	outputs = self.outputs()
	# 	steps = self.build_steps()
	# 	version = self.cwl_version
	# 	requirements = self.requirements

	# 	workflow = {
	# 		'cwlVersion': cwl_version,
	# 		'class': 'Workflow',
	# 		'inputs': inputs,
	# 		'outputs': outputs,
	# 		'steps': steps,
	# 		'requirements': requirements
	# 	}
		
	# 	return workflow

	# def build_inputs(self):
	# 	# build_inputs(self) formats the inputs from each of the step
	# 	# to be used by a CWL workflow and returns a dict.

	# 	# TODO: put all the inputs from the tools into one dict
	# 	# modify the names to be <toolname>_<parametername>
	# 	# and put the type signature down (should be the same)
	# 	# then write to file.\

	# 	inputs = {}
	# 	for i in self.steps:
	# 		curstep = self.steps[i]
	# 		for j in curstep["in"]:
	# 			curparam = curstep["in"][j]
	# 			if isinstance(curparam["value"], dict):
	# 				# chainable types
	# 				pass
	# 			else:
	# 				key = "{toolname}_{parametername}".format(i, j)
	# 				inputs[key]["type"] = curparam["type"]
	# 				if "secondary_files" in curparam:
	# 					inputs[key]["secondary_files"] = curparam["secondary_files"]
	# 	return inputs
	# 	# now convert to inputs to yaml and write to file.
	# 	# also take their values and plop it in a yml file


	# def build_step(self, f):
	# 	cwl_steps = {}
	# 	for tool in self.steps:
	# 		toolname = tool.toolname
	# 		cwl_steps[toolname]['run'] = tool.toolname.get_path()
	# 		cwl_steps[toolname]['in'] = {}
	# 		cwl_steps[toolname]['out'] = []
	# 		for param in self.steps[tool]["in"]:
	# 			if isinstance(self.steps[tool]["in"][param]["value"], dict):			
	# 				# chain type i.e. no need for a value in inputs
	# 				pass
	# 			else:
	# 				cwl_steps[tool][param] = source
	# 				source = "{toolname}_{parametername}".format(tool, j)
					
	# 		for param in self.steps[tool]["out"]:
	# 			cwl_steps[toolname]['out'] += [param]
	# 	return cwl_steps

	# 	# for tool in steps:
	# 	# 	curstep = self.steps["out"]
	# 	# 	for param in curstep:
	# 	# 		outputs["out"] = param
	# def add_outputs(self, inp, out):
	# 	# this should be done after a step is added
	# 	if inp in self.steps:
	# 		if out in self.steps[inp]["out"]:
	# 			# what about glob patterns and stuff.
	# 			self.outputs[out] = {"type": "File", "outputSource": "{1}/{2}".format(inp, out)} 
				
	# def add_step_values(self, step):
	# 	for i in step.values:
	# 		key = step.name + "_" + i
	# 		if step.values[i]["type"] == "File":
	# 			self.values[key] = {
	# 				"class": "File",
	# 				"path" step.values[i]["value"]
	# 			}
	# 		else:
	# 			self.values[key] = step.values[i]["value"]

	# 		