# CWLIFY:

There are many independently functional groups that perform bioinformatics analysis that interoperability sometimes isn’t a concern. Making sure that a result can be reproduced by another group and that the same process can be repeated for other studies. CWL aims to separate the running of the workflow from its description in an attempt to standardize how workflows are shared and used.

Modifying the GenAP pipeline itself to output CWL would require bad control flow [i.e. if pipeline.cwl -> create_cwl_steps()] to create CWL and input objects instead of shell scripts. Instead we create something that works parallel to the pipeline but mimics most of the functionality and writes out CWL. 


