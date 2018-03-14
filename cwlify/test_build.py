import yaml
import sys

def build(filename):
	base = {
		"cwlVersion": "v1.0",
		"class": "Workflow",
		"requirements": {
			"InlineJavascriptRequirement": {},
			"ShellCommandRequirement": {},
			"MultipleInputFeatureRequirement": {},
			"StepInputExpressionRequirement": {}
			},
	}
	with open(filename, "w") as workflow:
		yaml.dump(base, workflow, default_flow_style=False)

if len(sys.argv) == 2:
	build(sys.argv[1])
