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
	# need to put this in a loop
	def create_run_folder(self):
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
		# returns True if it worked, False if it didn't.
		try:
			new_path = os.path.abspath(self.dirname)+"/cwl/"+name+".cwl"
			os.stat(path)
			copyfile(path, new_path)
			return new_path
		except os.error:
			return False

	

	def add_step(self, toolname, cwl_file, inputs, outputs, scatter=None, reqs=None):
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
		for simplicities sake the gmail.cominputs will be added to the dict will be
		in the form toolname_inputname. This can be changed later.
		'''
		new_key = "{toolname}_{key}".format(toolname=toolname, key=input_name)
		self.input_names += [new_key]
		self.inputs[new_key] = {
			"type": input_type
		}

	def add_outputs(self, **kwargs):
		# add the outputs to a dict
		for key, value in kwargs.items():
			value["type"] = "File"
			self.outputs[key] = value
			self.output_names += [key]

	def build(self, wd):
		try:
			self.validate()
		finally:
			self.build_cwl(wd)
			self.create_cwl_inputs()

	def build_cwl(self, wd):
		# build will actually create the workflow file.
		steps = {"steps": self.steps}
		inputs = {"inputs": self.inputs}
		outputs = {"outputs": self.outputs}
		with open(wd, "w") as wf:
			yaml.dump(self.base, wf, default_flow_style=False)
			yaml.dump(inputs, wf, default_flow_style=False) 
			yaml.dump(outputs, wf, default_flow_style=False) 
			yaml.dump(steps, wf, default_flow_style=False) 
		return wf

	def add_values(self, toolname, **kwargs):
		'''
		e.g.
		inputname: {
			type: #sometype
			value: #the value associated
		}
		'''
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
			return True
			# return True if successfully added, false otherwise.



	def create_cwl_inputs(self):
		'''
		to be used only after build has been successfully ran
		'''
		inputs = {}
		with open(self.dirname+"/"+"inputs.yml", "w") as inp:
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