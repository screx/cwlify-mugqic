cwlVersion: v1.0
class: Workflow

inputs:
  messages:
    type: string[]

requirements:
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}
steps:
  echo:
    run: scatter-test.cwl
    in:
      message: 
        source: messages
    scatter: message
    out: [echo_out]
  cat:
    run: cat.cwl
    in:
      inp_files: [echo/echo_out]
    out: [cat_out]

outputs: 
  workflow_out:
    type: File
    outputSource: cat/cat_out


