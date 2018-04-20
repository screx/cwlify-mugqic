# The CWLifying of the MUGQIC/GenAP Pipeline. 


[github repo](https://github.com/screx/cwlify-mugqic) 


[Common Workflow Language](http://commonwl.org)


There are many independently functional groups that perform bioinformatics analysis that interoperability sometimes isn’t a concern. Making sure that a result can be reproduced by another group and that the same process can be repeated for other studies. CWL aims to separate the running of the workflow from its description in an attempt to standardize how workflows are shared and used.


Modifying the GenAP pipeline itself to output CWL would require bad control flow [i.e. if pipeline.cwl -> create_cwl_steps()] to create CWL and input objects instead of shell scripts. Instead we create something that works parallel to the pipeline but mimics most of the functionality and writes out CWL. 


How the pipeline currently works:
* given a readset file, a config file, and a number of steps: create a bash script that can be run by the cluster.
* creates shell commands by using string formatting
* problems with this: hard to modify bash scripts if necessary, not a portable system.
* hard to read & modify


How CWLifying the pipeline will work
* currently given a readset and a config file can create a directory containing all the associated CWL files as well as the workflow and inputs file.
* Some Disadvantages/nuances:
   * need to implement each tool individually 
   * scattering/gathering steps may be a bit clunky
   * CWL file is separate from the actual workflow creation
   * Need to test each cwl file independently first.￼
* Some Advantages:
   * choosing to add or not add values can use simple control flow
   * Can reuse CWL files
   * can share workflows outside of group relatively easily

*** Installation
> Use Python 2.7
> clone the repo:
> $ git clone https://github.com/screx/cwlify-mugqic.git
> create a virtual environment
> $ virtualenv venv
> install the required python packages
> $ pip install -r requirements.txt

  
![alt text](https://github.com/screx/cwlify-mugqic/blob/master/images/image1.png "UML")
UML Diagram of the proof of concept


workflow.py
* Main script for creating the workflow and associated files
* aggregates all the data required to create the workflow and validates that the workflow is functional.


pipeline.py
* can probably change DNASeq Class to be a concrete implementation of a Pipeline class
* each method is a step in the pipeline
* uses the workflow class to actually implement the DNASeq pipeline & creates the workflow
* methods are layed out as followed
![alt text](https://github.com/screx/cwlify-mugqic/images/image2.png "initialize necessary values")  
* specify the toolname and path to the actual CWL file we are trying to add and add it to the run directory using the add_to_run_folder() method
![alt text](https://github.com/screx/cwlify-mugqic/images/image3.png "add values from readset")    
* Here we gather all the values that are needed from the readset/config file
![alt text](https://github.com/screx/cwlify-mugqic/images/image4.png "add outputs as an array")     
* Add the outputs to the tool as an array of strings (from the names of the outputs in the tool description
![alt text](https://github.com/screx/cwlify-mugqic/images/image5.png "add values to the workflow using add_values() method")  
* they are then added as inputs to the workflow using the add_values() method
![alt text](https://github.com/screx/cwlify-mugqic/images/image6.png "dict of all inputs")    
* after all the inputs have been added create a dict where the key is the parameter name (found from the CWL file) and the value is the name of the input as added into cwl. if the value comes from another step it is of the form {toolname}/{parmeter_name}, otherwise it defaults to {toolname}\_{parametername}
![alt text](https://github.com/screx/cwlify-mugqic/images/image7.png "extra control flow") 
* sometimes some extra control flow is needed to specify how to take arguments 
![alt text](https://github.com/screx/cwlify-mugqic/images/image8.png "Adding requirements")  
* Add any requirements to the system as needed
![alt text](https://github.com/screx/cwlify-mugqic/images/image9.png "Use the add_step() method")    
* add the step to the workflow using the add_step() method


cwlify.py
   * For running the pipeline from the command line
   * ‘-c’ to specifiy the config file
   * ‘-readset’ to specify the readset file
   * name of the workflow goes at the end.


readset.py
   * parses and stores data for the readset (from GenAP pipelines but only for illumina readsets)


config.py
   * allows access of the data stored in the config.ini file (from GenAp Pipeline)




Running the command
![alt text](https://github.com/screx/cwlify-mugqic/images/image10.png "The command to run")  
  
Generates an inputs.yml and workflow.cwl file along with copying the relevant CWL tool descs into a new directory.

![alt text](https://github.com/screx/cwlify-mugqic/images/image11.png "Tree structure of the new directory")  


  



Now the workflow can be run when passed through a cwl runner(cwltool, toil, etc.)