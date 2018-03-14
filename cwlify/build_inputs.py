
class GenerateWorkflowInputs(object):
	"""docstring for GenerateWorkflowInputs"""
	def __init__(self, arg):
		super(GenerateWorkflowInputs, self).__init__()
		self.inputs = {}


	def get_inputs(self, workflow):
		# reads inputs of a workflow then allows user to generate
		# input yaml objects
		with open(workflow) as wf:
			data = yaml.load(wf)
			self.inputs = data[inputs]

	def add_value(self, inp, value):
		'''
		adds a value to one of the workflow inputs
		if it is a valid input
		'''
		if inp in self.inputs:
			self.inputs[inp]["value"] = value


	def build_input_file(self, filename):
		'''
		This should only be used after all the values have been added
		inputs is a dict that is structured as followed:
		inputs = {
			...
			input1: 
				in_type: str or []
				value:
		}
		'''
		with open(filename, "rw"):
			inputs = self.inputs
			for i in inputs:
				try:
					value = inputs[i]["value"]
				except:

				i_type = inputs[i]["in_type"]
				if i_type == "File":
					"{i}:\n  class: File\n  path: {val}\n"\
					.format(i, value)
				else:
					"{i}:{val}\n":
					.format(i, value)





