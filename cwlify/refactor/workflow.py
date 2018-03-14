import yaml
class Workflow:
	def __init__(self, name):
		self.cwl_version = "v1.0"
		self.name = name
		self.steps = {} # basically list of all the tools
		self.input_names = []
		self.inputs = {}
		self.output_names = []
		self.outputs = {}
		self.values = {}
		self.build_base()

	def __getattr__(self, attr):
		for i in self.steps:
			if i == attr:
				return i

	def build_base(self):
		self.base = {
		"cwlVersion": self.cwl_version,
		"class": "Workflow",
		"requirements": {
			"InlineJavascriptRequirement": {},
			"ShellCommandRequirement": {},
			"MultipleInputFeatureRequirement": {},
			"StepInputExpressionRequirement": {}
			},
		}


	def add_step(self, toolname, cwl_file, inputs, outputs, scatter=None):
		''' 
		 toolname is a string
		 cwl_file is a string
		 inputs is a dict of the following form
		 inputs = {
		 	'inputname': 'source'
		 }
		 outputs is an array of strings
		'''
		 
		self.steps[toolname] = {
			"run": cwl_file,
			"in": inputs,
			"out": outputs,
		}
		if scatter:
			steps[toolname]["requirements"]  += "ScatterFeatureRequirement"
			for i in scatter:
				steps[toolname]["scatter"] = []
				steps[toolname]["scatter"] += [i]
		return self.steps[toolname]

	def add_input(self, toolname, **kwargs):
		'''
		for simplicities sake the gmail.cominputs will be added to the dict will be
		in the form toolname_inputname. This can be changed later.
		'''
		for key, value in kwargs.items():
			new_key = "{toolname}_{key}".format(toolname=toolname, key=key)
			self.input_names += [new_key]
			self.inputs[new_key] = value

	def add_outputs(self, **kwargs):
		for key, value in kwargs.items():
			self.outputs[key] = value
			self.output_names += [key]

	def build(self):
		fname = "{}.cwl".format(self.name)
		steps = {"steps": self.steps}
		inputs = {"inputs": self.inputs}
		outputs = {"outputs": self.outputs}
		with open(fname, "w") as wf:
			yaml.dump(self.base, wf, default_flow_style=False)
			yaml.dump(inputs, wf, default_flow_style=False) 
			yaml.dump(outputs, wf, default_flow_style=False) 
			yaml.dump(steps, wf, default_flow_style=False) 

	def add_values(self, type, inputname, value, secondary_files=None):
		if inputname in self.input_names:
			set_value = None
			if type == "File":
				set_value = {
					"class": "File",
					"path": value
				}
				if secondary_files:
					set_value["secondaryFiles"] = secondary_file
			else:
				set_value = value
			self.values[inputname] = set_value
			return True
		else:
			return False


	def create_cwl_inputs(self):
		'''
		to be used only after build has been successfully ran
		'''
		inputs = {}
		with open(self.name+"-inputs.yml", "w") as inp:
			for i in self.input_names:
				if i in self.values:
					inputs[i] = self.values[i]
				else:
					if self.inputs[i]["type"] == "File":
						inputs[i] = {
							"class": "File",
							"path": "#PLACEHOLDER"
							}
					else:
						inputs[i] = "#PLACEHOLDER"
			yaml.dump(inputs, inp, default_flow_style=False)