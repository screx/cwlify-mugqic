# CWLIFY:

This tool can be used to develop workflows programmatically and the input files that go with them.

This tool won't be used to make everything correct automatically but simply to assemble.

A `step` will be used to interact with a cwl tool description. It will hold the information about the files location, along with the inputs directly related to that step.

Steps will be added to a `Workflow` object. `inputs` and `outputs` also have to be added to the workflow manually.

Linking. if an object in inputs is linked then the source is just the object, otherwise it has to be accessed by the ID first e.g. ID/input

error checking. linking can only occur if it already exists in another steps output, or in inputs.

for each tool compile the input values that are acquired for them.
