import os
from shutil import copyfile

# this for setup of the initial run directory
# dirname needs to be highest level scope for access everywhere
dirname = "run"
# need to put this in a loop
def create_run_folder():
	i = 0
	while True:
		try:
			os.mkdir(dirname)
			break
		except:
			i += 1
			dirname = "run" + str(i)

os.mkdir(dirname+"/cwl")
# now to pack all the cwl files into this.
# global var for the home dir of cwl

# e.g.
def add_to_run_folder(tool):
	# returns True if it worked, False if it didn't.
	path = cwl_dir + tool
	print path
	try:
		os.stat(path)
		copyfile(path, dirname+"/cwl/"+tool)
	except os.error:
		return False




# build into this directory
# create workflow.cwl... dont need to provide a workflow name
# create a inputs.yml as well
# also copy the config file to this location as well?

# also need to write docs for each and every tool