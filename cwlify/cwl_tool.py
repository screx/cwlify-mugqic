import os
import yaml

class Step(object):
	"""A CommandLineTool object is used to interact with CWL tool descriptions
	in order to write workflows. It should be able to collect all the necessary inputs
	and use them to combine command line tools into a workflow."""
	def __init__(self, name, filepath):
		if os.path.exists(filepath):	
			self.name = name
			self.path = filepath
			self.inputs = {}
			self.outputs = []
			self.values = {}
			self.valid_inputs = []
			# self.cwl = parse_cwl(self)

	def __eq__(self, other):
		if is_instance(other, str):
			return other == self.name
		if is_instance(other, Step):
			return other.name == self.name

	def parse_cwl(self):
		'''
		parses the cwl file from yaml format information about the inputs and outputs
		'''
		# REQUIREMENTS: get_path() has to point at a real cwl file in yml format. 
		with open(self.get_path()) as info:
			info_dict = yaml.load(info)
			info.close()
		for i in info_dict["inputs"]:
			self.inputs[i] = {}
			self.inputs[i]["type"] = info_dict["inputs"][i]["type"]
		for i in info_dict["outputs"]:
			self.outputs += [i],

	def get_path(self):
		return self.path

	def get_valid_inputs(self):
		valid_inputs = {}
		for param in self.inputs:
			if "value" in self.inputs[param]:
				valid_inputs[param] = self.inputs[param]
		return valid_inputs

	def get_valid_outputs(self):
		return self.outputs # they are all valid and can be parsed later.
	
	def add_value(self, inp, val):
		try:
			inp_type = self.inputs[inp]["type"]
			self.values[inp] = {
				"type": inp_type,
				"value": val
			}
			self.valid_inputs += [inp]
			return True
		except KeyError:
			return False
	


