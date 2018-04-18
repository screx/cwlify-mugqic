import yaml
import os
from shutil import copyfile
from cwltool.load_tool import validate_document, fetch_document
import tempfile
from schema_salad.validate import ValidationException

dirname = "run"
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
		self.create_run_folder()

	def __getattr__(self, attr):
		for i in self.steps:
			if i == attr:
				return i

	def build_base(self):
		"""
		build_base() adds some of the necessary fields required by CWL
		and returns it as a dict

		build_base:
			return: None
		"""
		return {
		"cwlVersion": self.cwl_version,
		"class": "Workflow",
		"requirements": {
			"InlineJavascriptRequirement": {},
			"ShellCommandRequirement": {},
			"MultipleInputFeatureRequirement": {},
			"StepInputExpressionRequirement": {}
			},
		}

	def create_run_folder(self):
		"""
		create_run_folder() creates a folder in the current directory named self.name
		if a folder already exists, append a number to the dirname.
		"""
		base_dir = self.name
		self.dirname = base_dir
		i = 0
		while True:
			try:
				os.mkdir(self.dirname)
				break
			except:
				i += 1
				self.dirname = base_dir  + str(i)
		os.mkdir(self.dirname+"/cwl")

	def add_to_run_folder(self, name, path):
		"""
		add_to_run_folder(name, path): copies the file located path to the run folder and 
		modifies the file to be {name}.cwl

		add_to_run_folder():
			name: str
			path: str
			return None
		"""
		try:
			new_path = os.path.abspath(self.dirname)+"/cwl/"+name+".cwl"
			os.stat(path)
			copyfile(path, new_path)
			return new_path
		except os.error:
			print "WARNING No File found at {}".format(path)

	

	def add_step(self, toolname, cwl_file, inputs, outputs, scatter=None, reqs=None):
		''' 
		 toolname is a string
		 cwl_file is a string
		 inputs is a dict of the following form
		 inputs = {
			'inputname': 'source'
		 }
		 outputs is an array of strings

		 add_step:
		 	toolname: str
		 	cwl_file: str
		 	inputs: dict
		 	outputs: array[str]
		 	scatter: boolean
		 	reqs: dict

		 	return: None
		'''
		 
		self.steps[toolname] = {
			"run": cwl_file,
			"in": inputs,
			"out": outputs,
		}
		steps = self.steps
		if reqs:
			steps[toolname]["requirements"] = [reqs]

		if scatter:
			if "requirements" in steps[toolname] and "ScatterFeatureRequirement" not in steps[toolname]["requirements"]:
				steps[toolname]["requirements"]  += ["ScatterFeatureRequirement"]
			elif "requirements" not in steps[toolname]:
				steps[toolname]["requirements"] = ["ScatterFeatureRequirement"]
			else:
				pass
			for i in scatter:
				steps[toolname]["scatter"] = []
				steps[toolname]["scatter"] += [i]
		return self.steps[toolname]

	def add_input(self, toolname, input_name, input_type):
		'''
		add_input(toolname, input_name, input_type): adds the input and input_type to the
		list of all inputs to the workflow. It formats the input as {toolname}_{input_name} for the
		possibility of duplicate input_name's

		add_input:
			toolname: str
			input_name: str
			input_type: str

			return: None
		'''
		new_key = "{toolname}_{key}".format(toolname=toolname, key=input_name)
		self.input_names += [new_key]
		self.inputs[new_key] = {
			"type": input_type
		}

	def add_outputs(self, **kwargs):
		"""
		add_outputs(**kwargs): takes a dict containing various output_names as keys and their sources as values
		and adds it to a dict containing all outputs to the workflow

		add_outputs
			key: str
			value: str
		"""
		for key, value in kwargs.items():
			value["type"] = "File"
			self.outputs[key] = value
			self.output_names += [key]

	def build(self, wd):
		"""
		build(wd): validates the workflow using the validate() method, if it passes
		creates a workflow and inputs file in the directory wd.

		build:
			wd: str
			return: None
		"""
		try:
			self.validate()
		finally:
			self.build_cwl(wd)
			self.create_cwl_inputs(wd)

	def build_cwl(self, wd):
		"""
		build_cwl(wd): creates the workflow file in the folder wd

		build:
			wd: str
			return: None
		"""
		# build will actually create the workflow file.
		steps = {"steps": self.steps}
		inputs = {"inputs": self.inputs}
		outputs = {"outputs": self.outputs}
		with open(wd + "/workflow.cwl", "w") as wf:
			yaml.dump(self.base(), wf, default_flow_style=False)
			yaml.dump(inputs, wf, default_flow_style=False) 
			yaml.dump(outputs, wf, default_flow_style=False) 
			yaml.dump(steps, wf, default_flow_style=False) 
		return wf

	def add_values(self, toolname, **kwargs):
		"""
		add_values(toolname, **kwargs): adds an all associated values to an input
		to the workflow. 
		
		add_values:
			toolname: str
			return: None

		e.g.
		inputname: {
			type: #sometype (required)
			value: #the value associated (required)
			secondary_file: # associated files  (optional)
		}
		"""
		for i in kwargs:
			value = kwargs[i] 
			key = i
			input_type = value["type"]
			input_name = key
			self.add_input(toolname, input_name, input_type)
			set_value = None
			if input_type == "File":
				set_value = {
					"class": "File",
					"path": value["value"]
				}
				if "secondary_files" in value:
					set_value["secondaryFiles"] = value["secondary_file"]
			else:
				set_value = value["value"] # works for string, boolean, int.
			self.values[toolname +"_"+input_name] = set_value





	def create_cwl_inputs(self, wd):
		'''
		create_cwl_inputs(): creates a file containing all input values in the folder wd

		create_cwl_inputs:
			wd: str
			return: None
		'''
		inputs = {}
		with open(wd+"/inputs.yml", "w") as inp:
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

	def load_cwl(self, fname):
		"""Load and validate CWL file using cwltool
		"""
		# Fetching, preprocessing and validating cwl
		(document_loader, workflowobj, uri) = fetch_document(fname)
		(document_loader, _, processobj, metadata, uri) = \
			validate_document(document_loader, workflowobj, uri)

		return document_loader, processobj, metadata, uri

	def validate(self):
		"""Validate workflow object.
		This method currently validates the workflow object with the use of
		cwltool. It writes the workflow to a tmp CWL file, reads it, validates
		it and removes the tmp file again. By default, the workflow is written
		to file using absolute paths to the steps. Optionally, the steps can be
		saved inline.
		"""

		# define tmpfile
		(fd, tmpfile) = tempfile.mkstemp()
		os.close(fd)
		try:
			# save workflow object to tmpfile,
			# do not recursively call validate function
			self.build_cwl(tmpfile)
			# load workflow from tmpfile
			document_loader, processobj, metadata, uri = self.load_cwl(tmpfile)
		# except ValidationException:
		# 	print "WARNING! CWL may fail"
		finally:
			# cleanup tmpfile
			os.remove(tmpfile)