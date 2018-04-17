cwlVersion: v1.0
class: CommandLineTool
baseCommand: echo

requirements:
  ResourceRequirement:
    ramMin: 2G
inputs:
  message:
    type: string
    inputBinding:
      position: 1

outputs: []
